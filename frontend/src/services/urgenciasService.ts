/**
 * Servicio de urgencias
 */
import api, { getErrorMessage } from '../utils/api';

// Tipos
export interface DomicilioRequest {
  calle: string;
  numero: number;
  localidad: string;
  ciudad: string;
  provincia: string;
  pais: string;
}

export interface IngresoUrgenciaRequest {
  cuil: string;
  informe: string;
  nivel_emergencia: string;
  temperatura: number;
  frecuencia_cardiaca: number;
  frecuencia_respiratoria: number;
  frecuencia_sistolica: number;
  frecuencia_diastolica: number;
  nombre?: string;
  apellido?: string;
  obra_social?: string;
  domicilio?: DomicilioRequest;
}

export interface IngresoResponse {
  id: string;
  cuil_paciente: string;
  nivel_emergencia: string;
  estado: string;
  fecha_ingreso: string;
  mensaje_advertencia?: string;
}

export interface IngresoListItem {
  id: string;
  cuil_paciente: string;
  nombre_paciente: string;
  apellido_paciente: string;
  nivel_emergencia: string;
  nivel_emergencia_nombre: string;
  estado: string;
  fecha_ingreso: string;
  temperatura: number;
  frecuencia_cardiaca: number;
  frecuencia_respiratoria: number;
  frecuencia_sistolica: number;
  frecuencia_diastolica: number;
}

export interface NivelEmergenciaItem {
  valor: string;
  nombre: string;
  nivel: number;
  duracion_max_espera_minutos: number;
}

/**
 * Registrar un nuevo ingreso de urgencia
 */
export const registrarIngreso = async (data: IngresoUrgenciaRequest): Promise<IngresoResponse> => {
  try {
    const response = await api.post<IngresoResponse>('/api/urgencias/ingresos', data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Obtener lista de ingresos pendientes
 */
export const obtenerIngresosPendientes = async (): Promise<IngresoListItem[]> => {
  try {
    const response = await api.get<IngresoListItem[]>('/api/urgencias/ingresos/pendientes');
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Obtener niveles de emergencia disponibles
 */
export const obtenerNivelesEmergencia = async (): Promise<NivelEmergenciaItem[]> => {
  try {
    const response = await api.get<NivelEmergenciaItem[]>('/api/urgencias/niveles-emergencia');
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};


