/**
 * Tarjeta individual de paciente en la lista de espera
 */
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Grid,
  Divider,
  Button,
  CardActions,
  IconButton,
  Tooltip
} from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import FavoriteIcon from '@mui/icons-material/Favorite';
import AirIcon from '@mui/icons-material/Air';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import EditNoteIcon from '@mui/icons-material/EditNote';
import InfoIcon from '@mui/icons-material/Info';
import { NIVELES_EMERGENCIA } from '../../utils/constants';
import type { IngresoListItem } from '../../services/urgenciasService';
import { ModalDetallesPaciente } from './ModalDetallesPaciente';

interface TarjetaPacienteProps {
  ingreso: IngresoListItem;
  showReclamarButton?: boolean;
  showContinuarButton?: boolean;
  onReclamar?: (ingresoId: string) => void;
  onContinuar?: (ingresoId: string) => void;
}

export const TarjetaPaciente: React.FC<TarjetaPacienteProps> = ({ 
  ingreso,
  showReclamarButton = false,
  showContinuarButton = false,
  onReclamar,
  onContinuar
}) => {
  const [modalOpen, setModalOpen] = useState(false);

  // Obtener información del nivel de emergencia
  const nivelInfo = Object.values(NIVELES_EMERGENCIA).find(
    n => n.valor === ingreso.nivel_emergencia
  );

  const color = nivelInfo?.color || '#757575';

  const handleOpenModal = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  // Formatear fecha de ingreso
  const fechaIngreso = new Date(ingreso.fecha_ingreso);
  const horaIngreso = fechaIngreso.toLocaleTimeString('es-AR', {
    hour: '2-digit',
    minute: '2-digit'
  });
  const fechaFormateada = fechaIngreso.toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });

  // Calcular tiempo de espera
  const tiempoEspera = Math.floor((Date.now() - fechaIngreso.getTime()) / 60000); // minutos

  return (
    <Card 
      sx={{ 
        mb: 2,
        borderLeft: `6px solid ${color}`,
        '&:hover': {
          boxShadow: 4
        }
      }}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box display="flex" alignItems="center" gap={1}>
            <Box>
              <Typography variant="h6">
                {ingreso.apellido_paciente}, {ingreso.nombre_paciente}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                CUIL: {ingreso.cuil_paciente}
              </Typography>
            </Box>
            <Tooltip title="Ver detalles completos del paciente">
              <IconButton 
                color="primary" 
                size="small"
                onClick={handleOpenModal}
                sx={{ ml: 1 }}
              >
                <InfoIcon />
              </IconButton>
            </Tooltip>
          </Box>
          <Chip
            label={nivelInfo?.nombre || ingreso.nivel_emergencia_nombre}
            sx={{
              backgroundColor: color,
              color: 'white',
              fontWeight: 'bold'
            }}
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Signos vitales */}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6} sm={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <ThermostatIcon fontSize="small" color="action" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  Temperatura
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {ingreso.temperatura}°C
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={6} sm={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <FavoriteIcon fontSize="small" color="action" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  FC
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {ingreso.frecuencia_cardiaca} lpm
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={6} sm={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <AirIcon fontSize="small" color="action" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  FR
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {ingreso.frecuencia_respiratoria} rpm
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={6} sm={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <MonitorHeartIcon fontSize="small" color="action" />
              <Box>
                <Typography variant="caption" color="text.secondary">
                  TA
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {ingreso.frecuencia_sistolica}/{ingreso.frecuencia_diastolica}
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* Información de tiempo */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={1}>
            <AccessTimeIcon fontSize="small" color="action" />
            <Typography variant="caption" color="text.secondary">
              Ingreso: {horaIngreso} - {fechaFormateada}
            </Typography>
          </Box>
          <Chip
            label={`Esperando ${tiempoEspera} min`}
            size="small"
            variant="outlined"
            color={tiempoEspera > (nivelInfo?.tiempoMaximo || 0) ? 'error' : 'default'}
          />
        </Box>
      </CardContent>

      {/* Botones de acción */}
      {(showReclamarButton || showContinuarButton) && (
        <CardActions sx={{ justifyContent: 'flex-end', pt: 0 }}>
          {showReclamarButton && onReclamar && (
            <Button
              variant="contained"
              color="primary"
              startIcon={<PersonAddIcon />}
              onClick={() => onReclamar(ingreso.id)}
              size="medium"
            >
              Reclamar Paciente
            </Button>
          )}
          {showContinuarButton && onContinuar && (
            <Button
              variant="contained"
              color="secondary"
              startIcon={<EditNoteIcon />}
              onClick={() => onContinuar(ingreso.id)}
              size="medium"
            >
              Continuar Revisión
            </Button>
          )}
        </CardActions>
      )}

      {/* Modal de detalles */}
      <ModalDetallesPaciente
        open={modalOpen}
        onClose={handleCloseModal}
        ingresoId={ingreso.id}
      />
    </Card>
  );
};

export default TarjetaPaciente;


