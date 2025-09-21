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

export default api;