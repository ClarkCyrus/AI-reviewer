// ReviewerDetails.jsx
import React, { useEffect, useState } from 'react';
import GoogleLoginButton from './GoogleLoginButton';
import { useParams } from 'react-router-dom';
import './Reviewer.css'

const ReviewerDetails = () => {
    const { reviewerId } = useParams();
    const [reviewer, setReviewer] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [showAnswers, setShowAnswers] = useState([])
    const [selectedAnswers, setSelectedAnswers] = useState(Array(questions.length).fill(null));

    useEffect(() => {
        if (reviewerId) {
            fetch(`http://localhost:5000/reviewer/${reviewerId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                    } else {
                        setReviewer(data.reviewer);
                        setQuestions(data.questions || []);
                        setShowAnswers(Array(data.questions.length).fill(false));
                    }
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
    }, [reviewerId]);

    const toggleAnswer = index => { 
        setShowAnswers(prevState => { 
            const newState = [...prevState];
            newState[index] = !newState[index]; 
            return newState; 
        }); 
    };

    const handleAnswerSelection = (questionIndex, option) => { 
        const newSelectedAnswers = [...selectedAnswers]; 
        newSelectedAnswers[questionIndex] = option; 
        setSelectedAnswers(newSelectedAnswers); 
    };

    return (
        <body>
            <nav className="navbar navbar-expand-lg navbar-light fixed-top shadow-sm" id="mainNav">
                <div className="container px-5">
                    <a className="navbar-brand fw-bold" href="/">Dashboard</a>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarResponsive">
                        <ul className="navbar-nav ms-auto me-0 my-3 my-lg-0">
                            <li className="nav-item"><a className="nav-link me-lg-3" href="#features">About</a></li>
                            <li className="nav-item"><a className="nav-link me-lg-3" href="#">Reviewers</a></li>
                        </ul>
                        <GoogleLoginButton />
                    </div>
                </div>
            </nav>
            <div className="container py-5" id="mainTop">
            <div className="row mb-5">
                <div className="col-lg-12 text-center">
                    <h1 className="display-3 lh-1 mb-3 fw-bold">Quiz Reviewer</h1>
                    {reviewer && <h2 className="display-6 text-primary">{reviewer.title}</h2>}
                </div>
            </div>
            <div className="row gx-4 gy-4">
                {questions.map((question, index) => (
                    <div className="col-md-6" key={question.id}>
                        <div className="card h-100">
                            <div className="card-body">
                                <h5 className="card-title">{question.text}</h5>
                                <ul className="list-group list-group-flush mb-3">
                                <li 
                                    className={`list-group-item ${selectedAnswers[index] === 'A' ? 'selected-answer' : ''}`} 
                                    onClick={() => handleAnswerSelection(index, 'A')}
                                >
                                    A: {question.option_a.replace(/\*\*/g, '')}
                                </li>
                                <li 
                                    className={`list-group-item ${selectedAnswers[index] === 'B' ? 'selected-answer' : ''}`} 
                                    onClick={() => handleAnswerSelection(index, 'B')}
                                >
                                    B: {question.option_b.replace(/\*\*/g, '')}
                                </li>
                                <li 
                                    className={`list-group-item ${selectedAnswers[index] === 'C' ? 'selected-answer' : ''}`} 
                                    onClick={() => handleAnswerSelection(index, 'C')}
                                >
                                    C: {question.option_c.replace(/\*\*/g, '')}
                                </li>
                                <li 
                                    className={`list-group-item ${selectedAnswers[index] === 'D' ? 'selected-answer' : ''}`} 
                                    onClick={() => handleAnswerSelection(index, 'D')}
                                >
                                    D: {question.option_d.replace(/\*\*/g, '')}
                                </li>

                                </ul>
                                <button className="btn toggle-answer mb-2" onClick={() => toggleAnswer(index)}>
                                    {showAnswers[index] ? "Hide Answer" : "Show Answer"}
                                </button>
                                {showAnswers[index] && ( 
                                <p className="correct-answer"> {selectedAnswers[index] === question.correct_answer.replace(/\*\*/g, '') 
                                ? 'Correct! 🎉' : `Wrong! The correct answer is: ${question.correct_answer.replace(/\*\*/g, '')}`} </p> )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>

            <section className="bg-gradient-primary-to-secondary" id="download">
                <div className="container px-5">
                    <h2 className="text-center text-white font-alt mb-4">Start Reviewing Now!</h2>
                    <div className="d-flex flex-column flex-lg-row align-items-center justify-content-center">
                        <a className="me-lg-3 mb-4 mb-lg-0" href="#!">
                            <img className="app-badge" src="src/assets/app-store-badge.svg" alt="..." /></a><a href="#!">
                        </a>
                    </div>
                </div>
            </section>

            <footer className="bg-black text-center py-5">
                <div className="container px-5">
                    <div className="text-white-50 small">
                        <div className="mb-2">&copy; AI Reviewer. All Rights Reserved.</div>
                        <a href="#!">Privacy</a>
                        <span className="mx-1">&middot;</span>
                        <a href="#!">Terms</a>
                        <span className="mx-1">&middot;</span>
                        <a href="#!">FAQ</a>
                    </div>
                </div>
            </footer>

    </body>
    );
};

export default ReviewerDetails;
