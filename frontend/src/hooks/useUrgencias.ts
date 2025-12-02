/**
 * Hook personalizado para operaciones de urgencias
 */
import { useState, useCallback } from 'react';
import {
  registrarIngreso,
  obtenerIngresosPendientes,
  obtenerNivelesEmergencia,
  reclamarPaciente,
  obtenerIngresosEnProceso,
  registrarAtencion,
  obtenerDetalleIngreso
} from '../services/urgenciasService';
import type {
  IngresoUrgenciaRequest,
  IngresoResponse,
  IngresoListItem,
  NivelEmergenciaItem,
  ReclamarResponse,
  AtencionRequest,
  AtencionResponse,
  IngresoDetalleResponse
} from '../services/urgenciasService';

export const useUrgencias = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrar = useCallback(async (data: IngresoUrgenciaRequest): Promise<IngresoResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await registrarIngreso(data);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al registrar ingreso';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const obtenerPendientes = useCallback(async (): Promise<IngresoListItem[]> => {
    setLoading(true);
    setError(null);
    try {
      const ingresos = await obtenerIngresosPendientes();
      return ingresos;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener ingresos pendientes';
      setError(errorMessage);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const obtenerNiveles = useCallback(async (): Promise<NivelEmergenciaItem[]> => {
    setLoading(true);
    setError(null);
    try {
      const niveles = await obtenerNivelesEmergencia();
      return niveles;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener niveles de emergencia';
      setError(errorMessage);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const reclamar = useCallback(async (): Promise<ReclamarResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await reclamarPaciente();
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al reclamar paciente';
      setError(errorMessage);
      // Propagar el error para que pueda ser manejado por el componente
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const obtenerEnProceso = useCallback(async (): Promise<IngresoListItem[]> => {
    setLoading(true);
    setError(null);
    try {
      const ingresos = await obtenerIngresosEnProceso();
      return ingresos;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener ingresos en proceso';
      setError(errorMessage);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const crearAtencion = useCallback(async (data: AtencionRequest): Promise<AtencionResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await registrarAtencion(data);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al registrar atención';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const obtenerDetalle = useCallback(async (ingresoId: string): Promise<IngresoDetalleResponse | null> => {
    setLoading(true);
    setError(null);
    try {
      const detalle = await obtenerDetalleIngreso(ingresoId);
      return detalle;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al obtener detalle del ingreso';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    registrar,
    obtenerPendientes,
    obtenerNiveles,
    reclamar,
    obtenerEnProceso,
    crearAtencion,
    obtenerDetalle,
    clearError: () => setError(null)
  };
};

export default useUrgencias;


