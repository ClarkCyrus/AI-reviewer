from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import LargeBinary

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Reviewer(db.Model):
    __tablename__ = 'reviewer'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False) 
    photo_data = db.Column(LargeBinary, nullable=False)
    questions = db.relationship('Question', backref='reviewer', lazy=True)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class File(db.Model):
    __tablename__ = 'file' 
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filedata = db.Column(db.LargeBinary, nullable=False)

class FileModelView(ModelView):
    column_display_pk = True  
    form_columns = ['filename', 'filedata']
    column_list = ['id', 'filename']

class UserModelView(ModelView):
    column_display_pk = True
    form_columns = ['email']
    column_list = ['id', 'email']

class ReviewerModelView(ModelView):
    column_display_pk = True
    form_columns = ['title', 'description']
    column_list = ['id', 'title', 'description']

class QuestionModelView(ModelView):
    column_display_pk = True
    form_columns = ['text', 'reviewer_id', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    column_list = ['id', 'text', 'reviewer_id', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

