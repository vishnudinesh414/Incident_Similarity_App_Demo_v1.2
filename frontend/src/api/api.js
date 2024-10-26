import axios from 'axios';

// Create an Axios instance with a base URL
const api = axios.create({
    baseURL: "http://localhost:5000", // Adjust this if your backend runs on a different port or domain
});

// Optional: Add interceptors for request/response handling
api.interceptors.request.use(
    (config) => {
        // You can modify the request config here if needed
        return config;
    },
    (error) => {
        // Handle request error
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => {
        // You can modify the response data here if needed
        return response;
    },
    (error) => {
        // Handle response error
        return Promise.reject(error);
    }
);

export default api;