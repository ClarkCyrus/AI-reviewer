// ReviewerList.jsx
import React, { useEffect, useState } from 'react';
import GoogleLoginButton from './GoogleLoginButton';
import { Link } from 'react-router-dom';
import './ReviewerList.css'


const ReviewerList = () => {
    const [reviewers, setReviewers] = useState([]);
    const [selectedReviewerId, setSelectedReviewerId] = useState(null);

    useEffect(() => {
        fetch('http://localhost:5000/reviewers')
        .then(response => response.json())
        .then(data => {
            setReviewers(data.reviewers);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, []);

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
                            <li className="nav-item"><a className="nav-link me-lg-3" href="/reviewers">Reviewers</a></li>
                        </ul>
                        <GoogleLoginButton />
                    </div>
                </div>
            </nav>

            <div className="container px-5" id="mainTop">
                <div className="row gx-5 align-items-center">
                    <div className="col-lg-12 mb-3 search"> 
                        <input type="text" className="form-control" placeholder="Search Reviewers..." />
                    </div>
                    <div className="col-lg-12 d-flex flex-wrap justify-content-center">
                        {reviewers.map(reviewer => (
                            <div className="card reviewer-card mb-3" key={reviewer.id} onClick={() => setSelectedReviewerId(reviewer.id)}>
                                <img src={`http://localhost:5000/reviewer/photo/${reviewer.id}`} className="card-img-top reviewer-img"alt="Reviewer Avatar" />
                                <div className="card-body">
                                    <h5 className="card-title">{reviewer.title}</h5>
                                    <p className="card-text">{reviewer.description}</p>
                                    <p className="card-text">
                                        <small className="text-muted">Last updated 3 mins ago</small>
                                    </p>
                                    <Link to={`/reviewer/${reviewer.id}`} className="btn btn-primary">Open Reviewer</Link>
                                </div>
                            </div>
                        ))}
                    </div>
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

export default ReviewerList;
