import axios, { AxiosError } from 'axios';
import { API_CONFIG } from './constants';

/**
 * Instancia de axios configurada con la base URL y timeout
 */
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Interceptor para agregar el token JWT a todas las peticiones
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(API_CONFIG.TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Interceptor para manejar respuestas y errores globalmente
 */
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Si el error es 401 (no autorizado), limpiar el token
    if (error.response?.status === 401) {
      localStorage.removeItem(API_CONFIG.TOKEN_KEY);
      localStorage.removeItem(API_CONFIG.USER_KEY);
      // Redirigir al login si no estamos ya ahí
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

/**
 * Función helper para extraer mensajes de error de las respuestas
 */
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    // Error de respuesta del servidor
    if (error.response?.data?.detail) {
      return typeof error.response.data.detail === 'string'
        ? error.response.data.detail
        : JSON.stringify(error.response.data.detail);
    }
    
    // Error de red
    if (error.message === 'Network Error') {
      return 'Error de conexión. Verifica que el backend esté corriendo.';
    }
    
    // Timeout
    if (error.code === 'ECONNABORTED') {
      return 'La petición tardó demasiado tiempo. Intenta nuevamente.';
    }
    
    // Otros errores de axios
    return error.message;
  }
  
  // Error genérico
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'Ocurrió un error inesperado';
};

export default api;
