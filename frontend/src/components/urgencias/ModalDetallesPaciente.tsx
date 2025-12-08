/**
 * Modal para mostrar detalles completos de un paciente
 */
import React, { useEffect, useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Grid,
  Divider,
  CircularProgress,
  Alert,
  Chip,
  Paper
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import PersonIcon from '@mui/icons-material/Person';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import HomeIcon from '@mui/icons-material/Home';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import AirIcon from '@mui/icons-material/Air';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import DescriptionIcon from '@mui/icons-material/Description';
import { obtenerDetalleIngreso, type IngresoDetalleResponse } from '../../services/urgenciasService';
import { NIVELES_EMERGENCIA } from '../../utils/constants';

interface ModalDetallesPacienteProps {
  open: boolean;
  onClose: () => void;
  ingresoId: string;
}

export const ModalDetallesPaciente: React.FC<ModalDetallesPacienteProps> = ({ 
  open, 
  onClose, 
  ingresoId 
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detalle, setDetalle] = useState<IngresoDetalleResponse | null>(null);

  useEffect(() => {
    if (open && ingresoId) {
      cargarDetalle();
    }
  }, [open, ingresoId]);

  const cargarDetalle = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await obtenerDetalleIngreso(ingresoId);
      setDetalle(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar los detalles del paciente');
    } finally {
      setLoading(false);
    }
  };

  // Obtener información del nivel de emergencia
  const nivelInfo = detalle 
    ? Object.values(NIVELES_EMERGENCIA).find(n => n.valor === detalle.nivel_emergencia)
    : null;

  const color = nivelInfo?.color || '#757575';

  // Formatear fecha
  const fechaFormateada = detalle 
    ? new Date(detalle.fecha_ingreso).toLocaleString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    : '';

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      scroll="paper"
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        borderBottom: '1px solid #e0e0e0',
        pb: 2
      }}>
        <Box display="flex" alignItems="center" gap={1}>
          <PersonIcon color="primary" />
          <Typography variant="h6">
            Detalles del Paciente
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ pt: 3 }}>
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

        {!loading && !error && detalle && (
          <Box>
            {/* Datos Personales */}
            <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <PersonIcon color="primary" />
                <Typography variant="h6">Datos Personales</Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary">
                    Nombre Completo
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.apellido_paciente}, {detalle.nombre_paciente}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary">
                    CUIL
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.cuil_paciente}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            {/* Nivel de Emergencia y Estado */}
            <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary" display="block" mb={1}>
                    Nivel de Emergencia
                  </Typography>
                  <Chip
                    label={nivelInfo?.nombre || detalle.nivel_emergencia_nombre}
                    sx={{
                      backgroundColor: color,
                      color: 'white',
                      fontWeight: 'bold'
                    }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary" display="block" mb={1}>
                    Estado
                  </Typography>
                  <Chip
                    label={detalle.estado}
                    color={
                      detalle.estado === 'PENDIENTE' ? 'warning' :
                      detalle.estado === 'EN_PROCESO' ? 'info' :
                      'success'
                    }
                  />
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="caption" color="text.secondary">
                    Fecha de Ingreso
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {fechaFormateada}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            {/* Signos Vitales */}
            <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <FavoriteIcon color="error" />
                <Typography variant="h6">Signos Vitales</Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <ThermostatIcon fontSize="small" color="action" />
                    <Typography variant="caption" color="text.secondary">
                      Temperatura
                    </Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.temperatura}°C
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <FavoriteIcon fontSize="small" color="action" />
                    <Typography variant="caption" color="text.secondary">
                      FC
                    </Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.frecuencia_cardiaca} lpm
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <AirIcon fontSize="small" color="action" />
                    <Typography variant="caption" color="text.secondary">
                      FR
                    </Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.frecuencia_respiratoria} rpm
                  </Typography>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <MonitorHeartIcon fontSize="small" color="action" />
                    <Typography variant="caption" color="text.secondary">
                      TA
                    </Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.frecuencia_sistolica}/{detalle.frecuencia_diastolica}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            {/* Informe de Ingreso */}
            <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <DescriptionIcon color="primary" />
                <Typography variant="h6">Informe de Ingreso</Typography>
              </Box>
              <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                {detalle.descripcion}
              </Typography>
            </Paper>

            {/* Personal Médico */}
            <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
              <Box display="flex" alignItems="center" gap={1} mb={2}>
                <LocalHospitalIcon color="primary" />
                <Typography variant="h6">Personal Médico</Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary">
                    Enfermera que Registró
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {detalle.enfermera_nombre} {detalle.enfermera_apellido}
                  </Typography>
                </Grid>
                {detalle.atencion_doctor_nombre && (
                  <Grid item xs={12} sm={6}>
                    <Typography variant="caption" color="text.secondary">
                      Doctor que Atendió
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {detalle.atencion_doctor_nombre} {detalle.atencion_doctor_apellido}
                    </Typography>
                  </Grid>
                )}
              </Grid>
            </Paper>

            {/* Informe de Atención (si existe) */}
            {detalle.atencion_informe && (
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Box display="flex" alignItems="center" gap={1} mb={2}>
                  <DescriptionIcon color="secondary" />
                  <Typography variant="h6">Informe de Atención Médica</Typography>
                </Box>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                  {detalle.atencion_informe}
                </Typography>
              </Paper>
            )}
          </Box>
        )}
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2, borderTop: '1px solid #e0e0e0' }}>
        <Button 
          onClick={onClose} 
          variant="contained"
          startIcon={<CloseIcon />}
        >
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ModalDetallesPaciente;

