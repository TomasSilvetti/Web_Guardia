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

export interface DomicilioResponse {
  calle: string;
  numero: number;
  localidad: string;
  ciudad: string;
  provincia: string;
  pais: string;
}

export interface PacienteResponse {
  cuil: string;
  nombre: string;
  apellido: string;
  obra_social?: string;
  domicilio: DomicilioResponse;
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

export interface ReclamarResponse {
  id: string;
  cuil_paciente: string;
  nombre_paciente: string;
  apellido_paciente: string;
  nivel_emergencia: string;
  estado: string;
  mensaje: string;
}

export interface AtencionRequest {
  ingreso_id: string;
  informe: string;
}

export interface AtencionResponse {
  ingreso_id: string;
  estado: string;
  mensaje: string;
}

export interface IngresoDetalleResponse {
  id: string;
  cuil_paciente: string;
  nombre_paciente: string;
  apellido_paciente: string;
  nivel_emergencia: string;
  nivel_emergencia_nombre: string;
  estado: string;
  fecha_ingreso: string;
  descripcion: string;
  temperatura: number;
  frecuencia_cardiaca: number;
  frecuencia_respiratoria: number;
  frecuencia_sistolica: number;
  frecuencia_diastolica: number;
  enfermera_nombre: string;
  enfermera_apellido: string;
  atencion_informe?: string;
  atencion_doctor_nombre?: string;
  atencion_doctor_apellido?: string;
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

/**
 * Reclamar el siguiente paciente en la lista de espera
 */
export const reclamarPaciente = async (): Promise<ReclamarResponse> => {
  try {
    const response = await api.post<ReclamarResponse>('/api/urgencias/reclamar');
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Obtener lista de ingresos en proceso
 */
export const obtenerIngresosEnProceso = async (): Promise<IngresoListItem[]> => {
  try {
    const response = await api.get<IngresoListItem[]>('/api/urgencias/ingresos/en-proceso');
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Registrar atención médica de un paciente
 */
export const registrarAtencion = async (data: AtencionRequest): Promise<AtencionResponse> => {
  try {
    const response = await api.post<AtencionResponse>('/api/urgencias/atencion', data);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Obtener detalle completo de un ingreso
 */
export const obtenerDetalleIngreso = async (ingresoId: string): Promise<IngresoDetalleResponse> => {
  try {
    const response = await api.get<IngresoDetalleResponse>(`/api/urgencias/ingresos/${ingresoId}`);
    return response.data;
  } catch (error) {
    throw new Error(getErrorMessage(error));
  }
};

/**
 * Buscar paciente por CUIL
 */
export const buscarPacientePorCuil = async (cuil: string): Promise<PacienteResponse | null> => {
  try {
    const response = await api.get<PacienteResponse>(`/api/urgencias/pacientes/${cuil}`);
    return response.data;
  } catch (error: any) {
    if (error.response?.status === 404) {
      return null; // Paciente no encontrado
    }
    throw new Error(getErrorMessage(error));
  }
};


