import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://fastapi-backend-fghrfmdeegdydydd.canadacentral-01.azurewebsites.net/api',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true
});

// Interceptor para manejar errores
axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // El servidor respondió con un código de estado fuera del rango 2xx
            console.error('Error de respuesta:', error.response.data);
        } else if (error.request) {
            // La petición fue hecha pero no se recibió respuesta
            console.error('Error de petición:', error.request);
        } else {
            // Algo sucedió al configurar la petición
            console.error('Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export default axiosInstance; 