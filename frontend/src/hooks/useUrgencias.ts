/**
 * Hook personalizado para operaciones de urgencias
 */
import { useState, useCallback } from 'react';
import {
  registrarIngreso,
  obtenerIngresosPendientes,
  obtenerNivelesEmergencia
} from '../services/urgenciasService';
import type {
  IngresoUrgenciaRequest,
  IngresoResponse,
  IngresoListItem,
  NivelEmergenciaItem
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

  return {
    loading,
    error,
    registrar,
    obtenerPendientes,
    obtenerNiveles,
    clearError: () => setError(null)
  };
};

export default useUrgencias;


