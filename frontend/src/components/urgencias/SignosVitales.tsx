/**
 * Componente para ingresar signos vitales
 */
import React from 'react';
import {
  Box,
  TextField,
  Grid,
  Typography,
  Paper,
  InputAdornment,
  Tooltip
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import { RANGOS_SIGNOS_VITALES } from '../../utils/constants';

interface SignosVitalesProps {
  temperatura: string;
  frecuenciaCardiaca: string;
  frecuenciaRespiratoria: string;
  frecuenciaSistolica: string;
  frecuenciaDiastolica: string;
  onTemperaturaChange: (value: string) => void;
  onFrecuenciaCardiacaChange: (value: string) => void;
  onFrecuenciaRespiratoriaChange: (value: string) => void;
  onFrecuenciaSistolicaChange: (value: string) => void;
  onFrecuenciaDiastolicaChange: (value: string) => void;
  errors?: {
    temperatura?: string;
    frecuenciaCardiaca?: string;
    frecuenciaRespiratoria?: string;
    frecuenciaSistolica?: string;
    frecuenciaDiastolica?: string;
  };
  disabled?: boolean;
}

export const SignosVitales: React.FC<SignosVitalesProps> = ({
  temperatura,
  frecuenciaCardiaca,
  frecuenciaRespiratoria,
  frecuenciaSistolica,
  frecuenciaDiastolica,
  onTemperaturaChange,
  onFrecuenciaCardiacaChange,
  onFrecuenciaRespiratoriaChange,
  onFrecuenciaSistolicaChange,
  onFrecuenciaDiastolicaChange,
  errors = {},
  disabled = false
}) => {
  return (
    <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h6">Signos Vitales</Typography>
        <Tooltip title="Todos los signos vitales son obligatorios">
          <InfoIcon fontSize="small" color="action" />
        </Tooltip>
      </Box>

      <Grid container spacing={2}>
        {/* Temperatura */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Temperatura"
            type="number"
            value={temperatura}
            onChange={(e) => onTemperaturaChange(e.target.value)}
            error={!!errors.temperatura}
            helperText={
              errors.temperatura || 
              `Normal: ${RANGOS_SIGNOS_VITALES.temperatura.min}-${RANGOS_SIGNOS_VITALES.temperatura.max} ${RANGOS_SIGNOS_VITALES.temperatura.unidad}`
            }
            disabled={disabled}
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {RANGOS_SIGNOS_VITALES.temperatura.unidad}
                </InputAdornment>
              ),
              inputProps: { step: '0.1' }
            }}
          />
        </Grid>

        {/* Frecuencia Cardíaca */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Frecuencia Cardíaca"
            type="number"
            value={frecuenciaCardiaca}
            onChange={(e) => onFrecuenciaCardiacaChange(e.target.value)}
            error={!!errors.frecuenciaCardiaca}
            helperText={
              errors.frecuenciaCardiaca || 
              `Normal: ${RANGOS_SIGNOS_VITALES.frecuenciaCardiaca.min}-${RANGOS_SIGNOS_VITALES.frecuenciaCardiaca.max} ${RANGOS_SIGNOS_VITALES.frecuenciaCardiaca.unidad}`
            }
            disabled={disabled}
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {RANGOS_SIGNOS_VITALES.frecuenciaCardiaca.unidad}
                </InputAdornment>
              ),
              inputProps: { min: 0 }
            }}
          />
        </Grid>

        {/* Frecuencia Respiratoria */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Frecuencia Respiratoria"
            type="number"
            value={frecuenciaRespiratoria}
            onChange={(e) => onFrecuenciaRespiratoriaChange(e.target.value)}
            error={!!errors.frecuenciaRespiratoria}
            helperText={
              errors.frecuenciaRespiratoria || 
              `Normal: ${RANGOS_SIGNOS_VITALES.frecuenciaRespiratoria.min}-${RANGOS_SIGNOS_VITALES.frecuenciaRespiratoria.max} ${RANGOS_SIGNOS_VITALES.frecuenciaRespiratoria.unidad}`
            }
            disabled={disabled}
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {RANGOS_SIGNOS_VITALES.frecuenciaRespiratoria.unidad}
                </InputAdornment>
              ),
              inputProps: { min: 0 }
            }}
          />
        </Grid>

        {/* Tensión Arterial */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Tensión Arterial *
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Sistólica"
                type="number"
                value={frecuenciaSistolica}
                onChange={(e) => onFrecuenciaSistolicaChange(e.target.value)}
                error={!!errors.frecuenciaSistolica}
                helperText={
                  errors.frecuenciaSistolica || 
                  `Normal: ${RANGOS_SIGNOS_VITALES.tensionSistolica.min}-${RANGOS_SIGNOS_VITALES.tensionSistolica.max} ${RANGOS_SIGNOS_VITALES.tensionSistolica.unidad}`
                }
                disabled={disabled}
                required
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      {RANGOS_SIGNOS_VITALES.tensionSistolica.unidad}
                    </InputAdornment>
                  ),
                  inputProps: { min: 0 }
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Diastólica"
                type="number"
                value={frecuenciaDiastolica}
                onChange={(e) => onFrecuenciaDiastolicaChange(e.target.value)}
                error={!!errors.frecuenciaDiastolica}
                helperText={
                  errors.frecuenciaDiastolica || 
                  `Normal: ${RANGOS_SIGNOS_VITALES.tensionDiastolica.min}-${RANGOS_SIGNOS_VITALES.tensionDiastolica.max} ${RANGOS_SIGNOS_VITALES.tensionDiastolica.unidad}`
                }
                disabled={disabled}
                required
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      {RANGOS_SIGNOS_VITALES.tensionDiastolica.unidad}
                    </InputAdornment>
                  ),
                  inputProps: { min: 0 }
                }}
              />
            </Grid>
          </Grid>
          {frecuenciaSistolica && frecuenciaDiastolica && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Formato: {frecuenciaSistolica}/{frecuenciaDiastolica} mmHg
            </Typography>
          )}
        </Grid>
      </Grid>
    </Paper>
  );
};

export default SignosVitales;




