import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 60000, // 60s crucial for the workflow endpoint
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.error ||
      error.message ||
      'An unexpected error occurred.';
    console.error('[API Error]', message, error.response?.data);
    return Promise.reject({ ...error, userMessage: message });
  }
);
