import './App.css';
import UploadForm from './components/FileUpload.jsx'
import ReviewerList from './components/ReviewerList.jsx';
import ReviewerDetails from './components/Reviewer.jsx';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div>
      <GoogleOAuthProvider clientId={process.env.GOOGLE_CLIENT_ID}>
        <Router>
          <Routes>
            <Route path="/" element={<UploadForm />} />
            <Route path="/reviewers" element={<ReviewerList />} />
            <Route path="/reviewer/:reviewerId" element={<ReviewerDetails />} />
          </Routes>
        </Router>
      </GoogleOAuthProvider>
    </div>
  );
}

export default App;
