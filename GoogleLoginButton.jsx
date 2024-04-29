// GoogleLoginButton.js

import React from 'react';
import axios from 'axios';

const GoogleLoginButton = () => {
    const handleGoogleLogin = async () => {
        try {
            const response = await axios.get('http://localhost:8000/google/auth/');

            window.location.href = response.data.url;
        } catch (error) {
            console.error('Google authentication error:', error);
        }
    };

    return (
        <button onClick={handleGoogleLogin}>
            Login with Google
        </button>
    );
};

export default GoogleLoginButton;
