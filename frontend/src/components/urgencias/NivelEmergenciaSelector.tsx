/**
 * Selector de nivel de emergencia con colores
 */
import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  Chip,
  FormHelperText
} from '@mui/material';
import { NIVELES_EMERGENCIA } from '../../utils/constants';

interface NivelEmergenciaSelectorProps {
  value: string;
  onChange: (value: string) => void;
  error?: boolean;
  helperText?: string;
  disabled?: boolean;
}

export const NivelEmergenciaSelector: React.FC<NivelEmergenciaSelectorProps> = ({
  value,
  onChange,
  error = false,
  helperText,
  disabled = false
}) => {
  const niveles = Object.values(NIVELES_EMERGENCIA);

  return (
    <FormControl fullWidth error={error} disabled={disabled}>
      <InputLabel id="nivel-emergencia-label">Nivel de Emergencia *</InputLabel>
      <Select
        labelId="nivel-emergencia-label"
        id="nivel-emergencia"
        value={value}
        label="Nivel de Emergencia *"
        onChange={(e) => onChange(e.target.value)}
        renderValue={(selected) => {
          const nivel = niveles.find(n => n.valor === selected);
          if (!nivel) return '';
          
          return (
            <Box display="flex" alignItems="center" gap={1}>
              <Box
                sx={{
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  backgroundColor: nivel.color
                }}
              />
              <Typography>{nivel.nombre}</Typography>
            </Box>
          );
        }}
      >
        {niveles.map((nivel) => (
          <MenuItem key={nivel.valor} value={nivel.valor}>
            <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
              <Box display="flex" alignItems="center" gap={1}>
                <Box
                  sx={{
                    width: 20,
                    height: 20,
                    borderRadius: '50%',
                    backgroundColor: nivel.color
                  }}
                />
                <Typography>{nivel.nombre}</Typography>
              </Box>
              <Chip
                label={nivel.descripcion}
                size="small"
                sx={{
                  backgroundColor: `${nivel.color}20`,
                  color: nivel.color,
                  fontWeight: 'bold'
                }}
              />
            </Box>
          </MenuItem>
        ))}
      </Select>
      {helperText && <FormHelperText>{helperText}</FormHelperText>}
    </FormControl>
  );
};

export default NivelEmergenciaSelector;


