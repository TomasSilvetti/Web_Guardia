/**
 * Lista de pacientes en revisión (estado EN_PROCESO)
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
import AssignmentIcon from '@mui/icons-material/Assignment';
import { useNavigate } from 'react-router-dom';
import { TarjetaPaciente } from './TarjetaPaciente';
import { useUrgencias } from '../../hooks/useUrgencias';
import { isMedico } from '../../services/authService';
import type { IngresoListItem } from '../../services/urgenciasService';

interface ListaRevisionEnProcesoProps {
  refreshTrigger?: number;
}

export const ListaRevisionEnProceso: React.FC<ListaRevisionEnProcesoProps> = ({ refreshTrigger = 0 }) => {
  const navigate = useNavigate();
  const { obtenerEnProceso, loading, error } = useUrgencias();
  const [ingresos, setIngresos] = useState<IngresoListItem[]>([]);
  const esMedico = isMedico();

  const cargarIngresos = async () => {
    const data = await obtenerEnProceso();
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

  const handleContinuar = (ingresoId: string) => {
    navigate(`/urgencias/revision/${ingresoId}`);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box display="flex" alignItems="center" gap={1}>
          <AssignmentIcon color="secondary" />
          <Typography variant="h5">
            Revisión en Progreso
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
        Pacientes que están siendo atendidos actualmente
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
          No hay pacientes en revisión en este momento
        </Alert>
      )}

      {!loading && !error && ingresos.length > 0 && (
        <>
          <Alert severity="success" sx={{ mb: 2 }}>
            Pacientes en revisión: <strong>{ingresos.length}</strong>
          </Alert>
          
          <Box>
            {ingresos.map((ingreso) => (
              <TarjetaPaciente 
                key={ingreso.id} 
                ingreso={ingreso}
                showContinuarButton={esMedico}
                onContinuar={handleContinuar}
              />
            ))}
          </Box>
        </>
      )}
    </Paper>
  );
};

export default ListaRevisionEnProceso;

