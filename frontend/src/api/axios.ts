import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
});

// inject JWT
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('test')
    if (token) {
        config.headers = config.headers || {}
        config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
});

export default api;