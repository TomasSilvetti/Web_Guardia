/**
 * Lista de pacientes en espera ordenada por prioridad
 */
import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  Button,
  Divider
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import PeopleIcon from '@mui/icons-material/People';
import { TarjetaPaciente } from './TarjetaPaciente';
import { useUrgencias } from '../../hooks/useUrgencias';
import type { IngresoListItem } from '../../services/urgenciasService';

interface ListaEsperaProps {
  refreshTrigger?: number;
}

export const ListaEspera: React.FC<ListaEsperaProps> = ({ refreshTrigger = 0 }) => {
  const { obtenerPendientes, loading, error } = useUrgencias();
  const [ingresos, setIngresos] = useState<IngresoListItem[]>([]);

  const cargarIngresos = async () => {
    const data = await obtenerPendientes();
    setIngresos(data);
  };

  useEffect(() => {
    cargarIngresos();
  }, [refreshTrigger]);

  // Auto-refresh cada 30 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      cargarIngresos();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box display="flex" alignItems="center" gap={1}>
          <PeopleIcon color="primary" />
          <Typography variant="h5">
            Lista de Espera
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={cargarIngresos}
          disabled={loading}
          size="small"
        >
          Actualizar
        </Button>
      </Box>

      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Pacientes ordenados por prioridad y hora de llegada
      </Typography>

      <Divider sx={{ mb: 3 }} />

      {loading && (
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!loading && !error && ingresos.length === 0 && (
        <Alert severity="info">
          No hay pacientes en espera en este momento
        </Alert>
      )}

      {!loading && !error && ingresos.length > 0 && (
        <>
          <Alert severity="info" sx={{ mb: 2 }}>
            Total de pacientes en espera: <strong>{ingresos.length}</strong>
          </Alert>
          
          <Box>
            {ingresos.map((ingreso) => (
              <TarjetaPaciente key={ingreso.id} ingreso={ingreso} />
            ))}
          </Box>
        </>
      )}
    </Paper>
  );
};

export default ListaEspera;


