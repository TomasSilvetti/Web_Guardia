/**
 * Servicio de pacientes
 * Preparado para IS2025-002
 */
import api, { getErrorMessage } from '../utils/api';

// Tipos
export interface Paciente {
  cuil: string;
  nombre: string;
  apellido: string;
  obra_social?: string;
}

/**
 * Buscar paciente por CUIL
 * TODO: Implementar cuando esté disponible el endpoint en el backend
 */
export const buscarPacientePorCuil = async (cuil: string): Promise<Paciente | null> => {
  try {
    // Por ahora retornamos null ya que el endpoint no existe aún
    // Cuando se implemente IS2025-002, descomentar:
    // const response = await api.get<Paciente>(`/api/pacientes/${cuil}`);
    // return response.data;
    return null;
  } catch (error) {
    // Si el paciente no existe, retornar null en lugar de error
    if (getErrorMessage(error).includes('404')) {
      return null;
    }
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Validar formato de CUIL
 */
export const validarCuil = (cuil: string): boolean => {
  // Remover guiones y espacios
  const cuilLimpio = cuil.replace(/[-\s]/g, '');
  
  // Debe tener exactamente 11 dígitos
  if (!/^\d{11}$/.test(cuilLimpio)) {
    return false;
  }
  
  return true;
};

/**
 * Formatear CUIL con guiones (XX-XXXXXXXX-X)
 */
export const formatearCuil = (cuil: string): string => {
  const cuilLimpio = cuil.replace(/[-\s]/g, '');
  if (cuilLimpio.length !== 11) return cuil;
  
  return `${cuilLimpio.slice(0, 2)}-${cuilLimpio.slice(2, 10)}-${cuilLimpio.slice(10)}`;
};






