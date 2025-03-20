import React from 'react';

const QaComponent = ({ questionsAndAnswers }) => {
    return (
        <div>
            <h2>Questions and Answers</h2>
            <ul>
                {questionsAndAnswers.map((item, index) => (
                    <li key={index}>
                        <strong>{item.question}</strong>: {item.answer}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default QaComponent;
