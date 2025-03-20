import React, {useState} from 'react';
import { GoogleLogin } from '@react-oauth/google';
import './GoogleLoginButton.css'

const GoogleLoginButton = () => {

  const [user, setUser] = useState(null);

  const responseGoogle = async (response) => {
    console.log(response);
    // Send the token to the backend for verification
    try {
      const res = await fetch('http://localhost:5000/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: response.credential }),
      });
      const data = await res.json();
      console.log(data);  // Log the response from the backend
      setUser(data);
    } catch (error) {
      console.error('Error verifying token:', error);
    }
  };

  const handleLogout = () => { 
    setUser(null);
     google.accounts.id.disableAutoSelect(); 
  };

  return (
    <> 
        {user ? (
          <button className="feedback-btn" onClick={handleLogout}> 
            Log out
          </button>
        ) : (
          <GoogleLogin
            onSuccess={responseGoogle}
            onError={responseGoogle}
            type='standard'
            theme='filled_black'
            text='continue_with'
            shape='pill'
            className='google-login-button'
          />
        )} 
    </>
  );
};

export default GoogleLoginButton;