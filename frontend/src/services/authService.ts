/**
 * Servicio de autenticación
 */
import api, { getErrorMessage } from '../utils/api';
import { API_CONFIG } from '../utils/constants';

// Tipos
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  rol: string;
  matricula: string;
}

export interface UserInfo {
  email: string;
  rol: string;
  matricula: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_info: UserInfo;
}

/**
 * Login de usuario
 */
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await api.post<AuthResponse>('/api/auth/login', credentials);
    
    // Guardar token y user info en localStorage
    localStorage.setItem(API_CONFIG.TOKEN_KEY, response.data.access_token);
    localStorage.setItem(API_CONFIG.USER_KEY, JSON.stringify(response.data.user_info));
    
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Registro de nuevo usuario
 */
export const register = async (data: RegisterData): Promise<{ message: string }> => {
  try {
    const response = await api.post('/api/auth/register', data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Logout
 */
export const logout = (): void => {
  localStorage.removeItem(API_CONFIG.TOKEN_KEY);
  localStorage.removeItem(API_CONFIG.USER_KEY);
};

/**
 * Verificar si el usuario está autenticado
 */
export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem(API_CONFIG.TOKEN_KEY);
};

/**
 * Obtener información del usuario actual
 */
export const getCurrentUser = (): UserInfo | null => {
  const userStr = localStorage.getItem(API_CONFIG.USER_KEY);
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr) as UserInfo;
  } catch {
    return null;
  }
};

/**
 * Verificar si el usuario es enfermera
 */
export const isEnfermera = (): boolean => {
  const user = getCurrentUser();
  return user?.rol === 'ENFERMERA';
};



