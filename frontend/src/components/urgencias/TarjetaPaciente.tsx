/**
 * Tarjeta individual de paciente en la lista de espera
 */
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Grid,
  Divider
} from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import FavoriteIcon from '@mui/icons-material/Favorite';
import AirIcon from '@mui/icons-material/Air';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import { NIVELES_EMERGENCIA } from '../../utils/constants';
import type { IngresoListItem } from '../../services/urgenciasService';

interface TarjetaPacienteProps {
  ingreso: IngresoListItem;
}

export const TarjetaPaciente: React.FC<TarjetaPacienteProps> = ({ ingreso }) => {
  // Obtener información del nivel de emergencia
  const nivelInfo = Object.values(NIVELES_EMERGENCIA).find(
    n => n.valor === ingreso.nivel_emergencia
  );

  const color = nivelInfo?.color || '#757575';

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
          <Box>
            <Typography variant="h6">
              {ingreso.apellido_paciente}, {ingreso.nombre_paciente}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              CUIL: {ingreso.cuil_paciente}
            </Typography>
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
    </Card>
  );
};

export default TarjetaPaciente;


