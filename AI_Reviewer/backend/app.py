from flask import Flask, request, session, send_file, jsonify
from flask_admin import Admin
from flask_cors import CORS
from flask_session import Session
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import requests
import os
import google.generativeai as genai
from models import db, File, FileModelView, UserModelView, User, ReviewerModelView, Reviewer, QuestionModelView, Question
import PyPDF2
import io

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Configure file uploads
ALLOWED_EXTENSIONS = {'pdf'}

# Configure Main database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db

# Initialize SQLAlchemy
db.init_app(app)

with app.app_context(): 
    db.create_all()

admin = Admin(app, name='File Admin', template_mode='bootstrap3', endpoint='fileadmin') 
admin.add_view(FileModelView(File, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(ReviewerModelView(Reviewer, db.session))
admin.add_view(QuestionModelView(Question, db.session))


# Initialize Admin and Session
Session(app)

# Example for database
""""
# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Add User model to Flask-Admin to view in /admin route
admin.add_view(ModelView(User, db.session))
""" 

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set the API_KEY environment variable.")
genai.configure(api_key=api_key)

# OAuth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    authorize_redirect_uri='http://localhost:5000/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'}
)

def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    user_id = session.get('user_id')
    return f'If you see this, Flask is running {user_id}'

@app.route('/auth', methods=['POST'])
def auth():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Missing token'}), 400

        # Verify the token with Google
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        user_info = response.json()
        print(user_info)

        if 'error' in user_info:
            return jsonify({'error': 'Invalid token'}), 400
        
        name = user_info.get('name', 'No name found')
        email = user_info.get('email', 'No email found')
        imageUrl = user_info.get('picture', 'No picture found')

        user = User.query.filter_by(email=email).first() 
        if user is None: 
            user = User(email=email) 
            db.session.add(user) 
            db.session.commit()
        
        session['user_id'] = user.id
        session.permanent = True
        session.modified = True

        # Process the user information as needed
        return jsonify({
            'name': name,
            'email': email,
            'imageUrl': imageUrl
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files or 'photo' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        photo = request.files['photo']
        reviewer_name = request.form['reviewerName'] 
        desc = request.form['description']
        num_questions = int(request.form['numQuestions'])

        print(f"Received file: {file.filename}")
        print(f"Received photo: {photo}")
        print(f"Reviewer Name: {reviewer_name}")
        print(f"Description: {desc}") 
        print(f"Number of Questions: {num_questions}")

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            # Secure the file name
            filename = secure_filename(file.filename)
            # Read the file data
            filedata = file.read()
            photodata = photo.read()

            # Extract text using pypdf
            text_content = extract_text_with_pypdf(filedata)
            if not text_content:
                return jsonify({'error': 'Failed to extract text'}), 500
            
            # Generate Q&A using GenAI
            questions_and_answers = generate_questions_and_answers_with_genai(text_content, num_questions)

            #Create Reviewer Instance
            reviewer = Reviewer(
                title=reviewer_name, 
                description=desc, 
                photo_data=photodata
            )
            db.session.add(reviewer)
            db.session.commit()

            if not reviewer:
                return jsonify({'error': 'Reviewer not found'}), 404
            
            # Save the questions to the database
            for qa in questions_and_answers:
                question = Question(
                    text=qa['question'],
                    option_a=qa['options']['A'],
                    option_b=qa['options']['B'],
                    option_c=qa['options']['C'],
                    option_d=qa['options']['D'],
                    correct_answer=qa['correct_answer'],
                    reviewer_id=reviewer.id
                )
                db.session.add(question)
            
            db.session.commit()

            return questions_and_answers 
        
        else: 
            return jsonify({'error': 'Unsupported file type'}), 415 
    except Exception as e:
        print(f"Error: {e}") 
        return jsonify({'error': 'Internal Server Error'}), 500

def extract_text_with_pypdf(filedata):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(filedata))
    
    # Extract text from each page
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def generate_questions_and_answers_with_genai(text, num_questions):
    # Use the Gemini API to generate Q&A from the text
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Based on the provided text, {text}, create {num_questions} multiple-choice questions. The questions and answers should be based only on the given content. Each question should have 4 answer options (A, B, C, and D). Ensure that one of the options is the correct answer, and the other three are plausible but incorrect. Highlight the correct answer.Use the following format for the questions and answers:\n\n" "- Questions should start with \"Q:\"\n" "- Options should start with \"A:\", \"B:\", \"C:\", and \"D:\"\n" "- Correct answers should be indicated with \"Correct Answer:\"\n\n" f"{text}"
    )

    response = model.generate_content(prompt)
    
    # Extract the text content
    generated_content = response.text
    
    # Parse the generated content into questions and answers
    # This is a simplified parsing and needs to be adjusted based on actual API response format
    questions_and_answers = parse_generated_content(generated_content)
    
    return questions_and_answers

def parse_generated_content(content):
    lines = content.split('\n')
    questions_and_answers = []
    question = None
    options = {}

    for line in lines:
        if line.startswith('Q:'):
            if question:
                question['options'] = options
                questions_and_answers.append(question)
            question = {'question': line.replace('Q:', '').strip(), 'options': {}, 'correct_answer': ''}
            options = {}
        elif any(line.startswith(option) for option in ['A:', 'B:', 'C:', 'D:']):
            option_key, option_value = line.split(':', 1)
            options[option_key.strip()] = option_value.strip()
        elif line.startswith('Correct Answer:'):
            if question:
                correct_answer = line.replace('Correct Answer:', '').strip()
                question['correct_answer'] = correct_answer
                if correct_answer in options:
                    options[correct_answer] = f"**{options[correct_answer]}**"
        elif question and not question['correct_answer']:
            question['correct_answer'] = line.strip()

    if question:
        question['options'] = options
        questions_and_answers.append(question)

    return questions_and_answers

@app.route('/reviewers')
def reviewers():
    try:
        reviewers = Reviewer.query.all()
        reviewers_list = [{'id': r.id, 'title': r.title, 'description': r.description,} for r in reviewers]

        return jsonify({'reviewers': reviewers_list})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/reviewer/<int:reviewer_id>')
def reviewer_details(reviewer_id):
    try:
        reviewer = Reviewer.query.get(reviewer_id)
        if not reviewer:
            return jsonify({'error': 'Reviewer not found'}), 404

        questions = Question.query.filter_by(reviewer_id=reviewer_id).all()
        questions_list = [{
            'id': q.id,
            'text': q.text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'correct_answer': q.correct_answer
        } for q in questions]

        return jsonify({'reviewer': {'id': reviewer.id, 'title': reviewer.title}, 'questions': questions_list})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/reviewer/photo/<int:reviewer_id>')
def get_reviewer_photo(reviewer_id):
    reviewer = Reviewer.query.get_or_404(reviewer_id)
    photo_data = reviewer.photo_data

    photo_io = io.BytesIO(photo_data)
    photo_io.seek(0)  

    return send_file(photo_io, mimetype='image/jpeg') 

    

if __name__ == '__main__':
    app.run(debug=True)

