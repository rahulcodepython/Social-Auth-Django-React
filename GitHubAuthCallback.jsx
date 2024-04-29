// GitHubAuthCallback.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const GitHubAuthCallback = () => {
    const [loading, setLoading] = useState(true)
    const [authenticated, setAuthenticated] = useState(false)

    const navigator = useNavigate();

    useEffect(() => {
        const handler = async () => {
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get('code');

            if (code) {
                await axios.get(`http://localhost:8000/github/authenticate/?code=${code}`).then(response => {
                    console.log(response.data);
                    setAuthenticated(true);
                    return navigator.push('/profile');
                }).catch(error => {
                    setAuthenticated(false);
                    console.log(error);
                    return navigator.push('/');
                }).finally(() => {
                    setLoading(false);
                });
            }
        }
        handler();
    }, []);

    return loading ? <div>Loading...</div> : null;
};

export default GitHubAuthCallback;
