/**
 * Página para revisar y registrar atención de un paciente
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Divider,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Card,
  CardContent
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import FavoriteIcon from '@mui/icons-material/Favorite';
import AirIcon from '@mui/icons-material/Air';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import { Navbar } from '../components/common/Navbar';
import { useUrgencias } from '../hooks/useUrgencias';
import { NIVELES_EMERGENCIA } from '../utils/constants';
import type { IngresoDetalleResponse } from '../services/urgenciasService';

export const RevisionPacientePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { obtenerDetalle, crearAtencion, loading } = useUrgencias();
  
  const [ingreso, setIngreso] = useState<IngresoDetalleResponse | null>(null);
  const [informe, setInforme] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loadingDetalle, setLoadingDetalle] = useState(true);

  useEffect(() => {
    const cargarDetalle = async () => {
      if (!id) {
        setError('ID de ingreso no válido');
        setLoadingDetalle(false);
        return;
      }

      setLoadingDetalle(true);
      const detalle = await obtenerDetalle(id);
      
      if (detalle) {
        setIngreso(detalle);
      } else {
        setError('No se pudo cargar la información del paciente');
      }
      setLoadingDetalle(false);
    };

    cargarDetalle();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!informe.trim()) {
      setError('El informe es obligatorio');
      return;
    }

    if (!id) {
      setError('ID de ingreso no válido');
      return;
    }

    const response = await crearAtencion({
      ingreso_id: id,
      informe: informe.trim()
    });

    if (response) {
      setSuccess('Atención registrada exitosamente');
      setTimeout(() => {
        navigate('/urgencias');
      }, 2000);
    }
  };

  const handleVolver = () => {
    navigate('/urgencias');
  };

  if (loadingDetalle) {
    return (
      <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
        <Navbar />
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
            <CircularProgress />
          </Box>
        </Container>
      </Box>
    );
  }

  if (!ingreso) {
    return (
      <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
        <Navbar />
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Alert severity="error">
            {error || 'No se pudo cargar la información del paciente'}
          </Alert>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleVolver}
            sx={{ mt: 2 }}
          >
            Volver a Urgencias
          </Button>
        </Container>
      </Box>
    );
  }

  const nivelInfo = Object.values(NIVELES_EMERGENCIA).find(
    n => n.valor === ingreso.nivel_emergencia
  );
  const color = nivelInfo?.color || '#757575';

  const fechaIngreso = new Date(ingreso.fecha_ingreso);
  const fechaFormateada = fechaIngreso.toLocaleString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      <Navbar />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleVolver}
          sx={{ mb: 3 }}
        >
          Volver a Urgencias
        </Button>

        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Revisión de Paciente
          </Typography>
          
          <Divider sx={{ my: 3 }} />

          {/* Información del Paciente */}
          <Card sx={{ mb: 3, borderLeft: `6px solid ${color}` }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                <Box>
                  <Typography variant="h5">
                    {ingreso.apellido_paciente}, {ingreso.nombre_paciente}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    CUIL: {ingreso.cuil_paciente}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Fecha de ingreso: {fechaFormateada}
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

              {/* Signos Vitales */}
              <Typography variant="h6" gutterBottom>
                Signos Vitales
              </Typography>
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <ThermostatIcon color="action" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Temperatura
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {ingreso.temperatura}°C
                      </Typography>
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <FavoriteIcon color="action" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Frecuencia Cardíaca
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {ingreso.frecuencia_cardiaca} lpm
                      </Typography>
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <AirIcon color="action" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Frecuencia Respiratoria
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {ingreso.frecuencia_respiratoria} rpm
                      </Typography>
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={6} sm={3}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <MonitorHeartIcon color="action" />
                    <Box>
                      <Typography variant="caption" color="text.secondary">
                        Tensión Arterial
                      </Typography>
                      <Typography variant="body1" fontWeight="bold">
                        {ingreso.frecuencia_sistolica}/{ingreso.frecuencia_diastolica}
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              {/* Descripción de Enfermera */}
              <Typography variant="h6" gutterBottom>
                Descripción del Ingreso
              </Typography>
              <Typography variant="body1" paragraph>
                {ingreso.descripcion}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Registrado por: {ingreso.enfermera_nombre} {ingreso.enfermera_apellido}
              </Typography>
            </CardContent>
          </Card>

          {/* Formulario de Atención */}
          <Box component="form" onSubmit={handleSubmit}>
            <Typography variant="h6" gutterBottom>
              Informe de Atención Médica
            </Typography>
            
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {success && (
              <Alert severity="success" sx={{ mb: 2 }}>
                {success}
              </Alert>
            )}

            <TextField
              fullWidth
              multiline
              rows={8}
              label="Informe de Atención *"
              value={informe}
              onChange={(e) => setInforme(e.target.value)}
              placeholder="Ingrese el informe detallado de la atención médica..."
              required
              disabled={loading}
              sx={{ mb: 3 }}
            />

            <Box display="flex" gap={2} justifyContent="flex-end">
              <Button
                variant="outlined"
                onClick={handleVolver}
                disabled={loading}
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                startIcon={<SaveIcon />}
                disabled={loading || !informe.trim()}
              >
                {loading ? 'Guardando...' : 'Finalizar Atención'}
              </Button>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default RevisionPacientePage;

