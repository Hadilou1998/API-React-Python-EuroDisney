import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// inject JWT
api.interceptors.request.use(
    (config) => {
        console.log('Axios Request:', config.method?.toUpperCase(), config.url);
        console.log('Axios Headers:', config.headers);

        // inject JWT token
        const token = localStorage.getItem('test');
        if (token) {
            config.headers = config.headers || {};
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        console.error('Axios Request Error:', error.message);
        return Promise.reject(error);
    }
);

// interceptor response
api.interceptors.response.use(
    (response) => {
        console.log('Axios Response Success:', response.status, response.config.url);
        return response;
    },
    (error) => {
        console.error('Axios Response Error:', error.message);

        if (error.code === 'ERR_NETWORK') {
            console.error('Erreur reseau - Veuillez vérifier que le serveur FastAPI démarre bien sur le port 8000');
        }

        if (error.response) {
            console.error('Error Response Data:', error.response.data)
            console.error('Error Response Status:', error.response.status)
            console.error('Error Response Headers:', error.response.headers)
        }

        return Promise.reject(error);
    }

);

export default api;