/**
 * Formulario de registro
 */
import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Paper,
  MenuItem
} from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { MENSAJES_VALIDACION, ROLES } from '../../utils/constants';

interface RegisterFormProps {
  onSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onSwitchToLogin }) => {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rol, setRol] = useState('ENFERMERA');
  const [matricula, setMatricula] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validaciones
    if (!email || !password || !rol || !matricula) {
      setError('Por favor complete todos los campos');
      return;
    }

    if (password.length < 6) {
      setError(MENSAJES_VALIDACION.PASSWORD_MIN);
      return;
    }

    setLoading(true);
    try {
      await register({ email, password, rol, matricula });
      setSuccess('Usuario registrado exitosamente. Ya puedes iniciar sesión.');
      
      // Limpiar formulario
      setEmail('');
      setPassword('');
      setMatricula('');
      
      // Esperar un momento antes de cambiar a login
      setTimeout(() => {
        if (onSuccess) {
          onSuccess();
        }
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al registrar usuario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 400, width: '100%' }}>
      <Typography variant="h5" component="h1" gutterBottom align="center">
        Registro
      </Typography>
      <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
        Crear nueva cuenta
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

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <TextField
          fullWidth
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          margin="normal"
          required
          autoComplete="email"
          autoFocus
          disabled={loading}
        />

        <TextField
          fullWidth
          label="Contraseña"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          margin="normal"
          required
          autoComplete="new-password"
          disabled={loading}
          helperText="Mínimo 6 caracteres"
        />

        <TextField
          fullWidth
          select
          label="Rol"
          value={rol}
          onChange={(e) => setRol(e.target.value)}
          margin="normal"
          required
          disabled={loading}
        >
          <MenuItem value={ROLES.ENFERMERA}>Enfermera</MenuItem>
          <MenuItem value={ROLES.DOCTOR}>Doctor</MenuItem>
        </TextField>

        <TextField
          fullWidth
          label="Matrícula"
          value={matricula}
          onChange={(e) => setMatricula(e.target.value)}
          margin="normal"
          required
          disabled={loading}
          helperText="Número de matrícula profesional"
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          size="large"
          disabled={loading}
          sx={{ mt: 3, mb: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Registrarse'}
        </Button>

        {onSwitchToLogin && (
          <Button
            fullWidth
            variant="text"
            onClick={onSwitchToLogin}
            disabled={loading}
          >
            ¿Ya tienes cuenta? Inicia sesión
          </Button>
        )}
      </Box>
    </Paper>
  );
};

export default RegisterForm;


