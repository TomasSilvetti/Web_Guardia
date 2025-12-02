/**
 * Constantes de la aplicación
 */

// Niveles de emergencia con sus colores según protocolo de triaje
export const NIVELES_EMERGENCIA = {
  CRITICA: {
    valor: 'CRITICA',
    nombre: 'Crítica',
    color: '#d32f2f', // Rojo
    nivel: 0,
    tiempoMaximo: 5,
    descripcion: 'Inmediato (5 minutos)'
  },
  EMERGENCIA: {
    valor: 'EMERGENCIA',
    nombre: 'Emergencia',
    color: '#f57c00', // Naranja
    nivel: 1,
    tiempoMaximo: 30,
    descripcion: '10 - 30 minutos'
  },
  URGENCIA: {
    valor: 'URGENCIA',
    nombre: 'Urgencia',
    color: '#fbc02d', // Amarillo
    nivel: 2,
    tiempoMaximo: 60,
    descripcion: '60 minutos'
  },
  URGENCIA_MENOR: {
    valor: 'URGENCIA_MENOR',
    nombre: 'Urgencia Menor',
    color: '#388e3c', // Verde
    nivel: 3,
    tiempoMaximo: 120,
    descripcion: '2 horas'
  },
  SIN_URGENCIA: {
    valor: 'SIN_URGENCIA',
    nombre: 'Sin Urgencia',
    color: '#1976d2', // Azul
    nivel: 4,
    tiempoMaximo: 240,
    descripcion: '4 horas'
  }
} as const;

// Estados de ingreso
export const ESTADOS_INGRESO = {
  PENDIENTE: 'PENDIENTE',
  EN_PROCESO: 'EN_PROCESO',
  FINALIZADO: 'FINALIZADO'
} as const;

// Roles de usuario
export const ROLES = {
  ENFERMERA: 'ENFERMERA',
  DOCTOR: 'MEDICO',
  ADMIN: 'ADMIN'
} as const;

// Configuración de la API
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  TIMEOUT: 10000,
  TOKEN_KEY: 'auth_token',
  USER_KEY: 'user_info'
} as const;

// Mensajes de validación
export const MENSAJES_VALIDACION = {
  CAMPO_REQUERIDO: 'Este campo es obligatorio',
  CUIL_INVALIDO: 'El CUIL debe tener 11 dígitos',
  VALOR_NEGATIVO: 'El valor no puede ser negativo',
  TEMPERATURA_INVALIDA: 'La temperatura debe estar entre 30 y 45 °C',
  EMAIL_INVALIDO: 'El email no es válido',
  PASSWORD_MIN: 'La contraseña debe tener al menos 6 caracteres',
  MATRICULA_REQUERIDA: 'La matrícula es obligatoria para enfermeras'
} as const;

// Rangos normales de signos vitales (para referencia visual)
export const RANGOS_SIGNOS_VITALES = {
  temperatura: { min: 36, max: 37.5, unidad: '°C' },
  frecuenciaCardiaca: { min: 60, max: 100, unidad: 'lpm' },
  frecuenciaRespiratoria: { min: 12, max: 20, unidad: 'rpm' },
  tensionSistolica: { min: 90, max: 120, unidad: 'mmHg' },
  tensionDiastolica: { min: 60, max: 80, unidad: 'mmHg' }
} as const;



