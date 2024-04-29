// GitHubLoginButton.js

import React from 'react';
import axios from 'axios';

const GitHubLoginButton = () => {
    const handleGitHubLogin = async () => {
        try {
            const response = await axios.get('http://localhost:8000/github/auth/');

            window.location.href = response.data.url;
        } catch (error) {
            console.error('GitHub authentication error:', error);
        }
    };

    return (
        <button onClick={handleGitHubLogin}>
            Login with GitHub
        </button>
    );
};

export default GitHubLoginButton;
