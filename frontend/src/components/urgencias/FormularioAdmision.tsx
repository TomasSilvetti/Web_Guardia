/**
 * Formulario principal de admisión de pacientes a urgencias
 */
import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  Grid,
  Collapse
} from '@mui/material';
import PersonSearchIcon from '@mui/icons-material/PersonSearch';
import SaveIcon from '@mui/icons-material/Save';
import { SignosVitales } from './SignosVitales';
import { NivelEmergenciaSelector } from './NivelEmergenciaSelector';
import { useUrgencias } from '../../hooks/useUrgencias';
import { validarCuil } from '../../services/pacientesService';
import { MENSAJES_VALIDACION } from '../../utils/constants';

interface FormularioAdmisionProps {
  onSuccess?: () => void;
}

export const FormularioAdmision: React.FC<FormularioAdmisionProps> = ({ onSuccess }) => {
  const { registrar, loading, error: serviceError } = useUrgencias();

  // Datos del paciente
  const [cuil, setCuil] = useState('');
  const [pacienteExiste, setPacienteExiste] = useState<boolean | null>(null);
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [obraSocial, setObraSocial] = useState('');
  const [numeroAfiliado, setNumeroAfiliado] = useState('');

  // Datos del domicilio (para pacientes nuevos)
  const [calle, setCalle] = useState('');
  const [numero, setNumero] = useState('');
  const [localidad, setLocalidad] = useState('');
  const [ciudad, setCiudad] = useState('');
  const [provincia, setProvincia] = useState('');
  const [pais, setPais] = useState('Argentina');

  // Datos del ingreso
  const [informe, setInforme] = useState('');
  const [nivelEmergencia, setNivelEmergencia] = useState('');

  // Signos vitales
  const [temperatura, setTemperatura] = useState('');
  const [frecuenciaCardiaca, setFrecuenciaCardiaca] = useState('');
  const [frecuenciaRespiratoria, setFrecuenciaRespiratoria] = useState('');
  const [frecuenciaSistolica, setFrecuenciaSistolica] = useState('');
  const [frecuenciaDiastolica, setFrecuenciaDiastolica] = useState('');

  // Estados de UI
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);

  const buscarPaciente = async () => {
    setErrors({});
    setSuccess(null);
    setWarning(null);
    setPacienteExiste(null);

    // Validar CUIL
    if (!cuil) {
      setErrors({ cuil: MENSAJES_VALIDACION.CAMPO_REQUERIDO });
      return;
    }

    if (!validarCuil(cuil)) {
      setErrors({ cuil: MENSAJES_VALIDACION.CUIL_INVALIDO });
      return;
    }

    try {
      // Importar función de servicio
      const { buscarPacientePorCuil } = await import('../../services/urgenciasService');
      const paciente = await buscarPacientePorCuil(cuil.replace(/[-\s]/g, ''));
      
      if (paciente) {
        // Paciente encontrado - autocompletar datos
        setPacienteExiste(true);
        setNombre(paciente.nombre);
        setApellido(paciente.apellido);
        setObraSocial(paciente.obra_social || '');
        setCalle(paciente.domicilio.calle);
        setNumero(paciente.domicilio.numero.toString());
        setLocalidad(paciente.domicilio.localidad);
        setCiudad(paciente.domicilio.ciudad);
        setProvincia(paciente.domicilio.provincia);
        setPais(paciente.domicilio.pais);
        setSuccess('Paciente encontrado. Los datos han sido autocompletados.');
      } else {
        // Paciente no existe
        setPacienteExiste(false);
        setWarning('El paciente no existe en el sistema. Complete los datos adicionales para registrarlo.');
      }
    } catch (error) {
      setErrors({ cuil: 'Error al buscar paciente' });
    }
  };

  const validarFormulario = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Validar CUIL
    if (!cuil) {
      newErrors.cuil = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else if (!validarCuil(cuil)) {
      newErrors.cuil = MENSAJES_VALIDACION.CUIL_INVALIDO;
    }

    // Si el paciente no existe, validar datos adicionales
    if (pacienteExiste === false) {
      if (!nombre) newErrors.nombre = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!apellido) newErrors.apellido = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      
      // Validar obra social y número de afiliado
      if (obraSocial && obraSocial.trim()) {
        // Si hay obra social, el número de afiliado es obligatorio
        if (!numeroAfiliado || !numeroAfiliado.trim()) {
          newErrors.numero_afiliado = 'El número de afiliado es obligatorio cuando se ingresa una obra social';
        }
      }
      
      // Validar domicilio
      if (!calle) newErrors.calle = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!numero) newErrors.numero = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!localidad) newErrors.localidad = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!ciudad) newErrors.ciudad = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!provincia) newErrors.provincia = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
      if (!pais) newErrors.pais = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    }

    // Validar informe
    if (!informe) {
      newErrors.informe = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    }

    // Validar nivel de emergencia
    if (!nivelEmergencia) {
      newErrors.nivel_emergencia = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    }

    // Validar signos vitales
    if (!temperatura) {
      newErrors.temperatura = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else {
      const temp = parseFloat(temperatura);
      if (temp < 30 || temp > 45) {
        newErrors.temperatura = MENSAJES_VALIDACION.TEMPERATURA_INVALIDA;
      }
    }

    if (!frecuenciaCardiaca) {
      newErrors.frecuenciaCardiaca = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else if (parseFloat(frecuenciaCardiaca) < 0) {
      newErrors.frecuenciaCardiaca = MENSAJES_VALIDACION.VALOR_NEGATIVO;
    }

    if (!frecuenciaRespiratoria) {
      newErrors.frecuenciaRespiratoria = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else if (parseFloat(frecuenciaRespiratoria) < 0) {
      newErrors.frecuenciaRespiratoria = MENSAJES_VALIDACION.VALOR_NEGATIVO;
    }

    if (!frecuenciaSistolica) {
      newErrors.frecuenciaSistolica = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else if (parseFloat(frecuenciaSistolica) < 0) {
      newErrors.frecuenciaSistolica = MENSAJES_VALIDACION.VALOR_NEGATIVO;
    }

    if (!frecuenciaDiastolica) {
      newErrors.frecuenciaDiastolica = MENSAJES_VALIDACION.CAMPO_REQUERIDO;
    } else if (parseFloat(frecuenciaDiastolica) < 0) {
      newErrors.frecuenciaDiastolica = MENSAJES_VALIDACION.VALOR_NEGATIVO;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccess(null);
    setWarning(null);

    if (!validarFormulario()) {
      return;
    }

    // Preparar datos para enviar
    const data = {
      cuil: cuil.replace(/[-\s]/g, ''), // Limpiar CUIL
      informe,
      nivel_emergencia: nivelEmergencia,
      temperatura: parseFloat(temperatura),
      frecuencia_cardiaca: parseFloat(frecuenciaCardiaca),
      frecuencia_respiratoria: parseFloat(frecuenciaRespiratoria),
      frecuencia_sistolica: parseFloat(frecuenciaSistolica),
      frecuencia_diastolica: parseFloat(frecuenciaDiastolica),
      ...(pacienteExiste === false && {
        nombre,
        apellido,
        obra_social: obraSocial && obraSocial.trim() ? obraSocial : 'sin obra social',
        numero_afiliado: numeroAfiliado && numeroAfiliado.trim() ? numeroAfiliado : undefined,
        domicilio: {
          calle,
          numero: parseInt(numero),
          localidad,
          ciudad,
          provincia,
          pais
        }
      })
    };

    const response = await registrar(data);

    if (response) {
      setSuccess('Ingreso registrado exitosamente');
      
      // Mostrar advertencia si el paciente fue creado
      if (response.mensaje_advertencia) {
        setWarning(response.mensaje_advertencia);
      }

      // Limpiar formulario
      limpiarFormulario();

      // Notificar éxito
      if (onSuccess) {
        setTimeout(() => onSuccess(), 1500);
      }
    }
  };

  const limpiarFormulario = () => {
    setCuil('');
    setNombre('');
    setApellido('');
    setObraSocial('');
    setNumeroAfiliado('');
    setCalle('');
    setNumero('');
    setLocalidad('');
    setCiudad('');
    setProvincia('');
    setPais('Argentina');
    setInforme('');
    setNivelEmergencia('');
    setTemperatura('');
    setFrecuenciaCardiaca('');
    setFrecuenciaRespiratoria('');
    setFrecuenciaSistolica('');
    setFrecuenciaDiastolica('');
    setPacienteExiste(null);
    setErrors({});
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Registro de Admisión a Urgencias
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Complete el formulario para registrar el ingreso del paciente
      </Typography>

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {warning && (
        <Alert severity="warning" sx={{ mb: 2 }} onClose={() => setWarning(null)}>
          {warning}
        </Alert>
      )}

      {serviceError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {serviceError}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        {/* Búsqueda de paciente */}
        <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Datos del Paciente
          </Typography>
          
          <Grid container spacing={2} alignItems="flex-start">
            <Grid item xs={12} sm={8}>
              <TextField
                fullWidth
                label="CUIL del Paciente"
                value={cuil}
                onChange={(e) => setCuil(e.target.value)}
                error={!!errors.cuil}
                helperText={errors.cuil || 'Formato: XX-XXXXXXXX-X (11 dígitos)'}
                disabled={loading}
                required
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<PersonSearchIcon />}
                onClick={buscarPaciente}
                disabled={loading}
                sx={{ height: 56 }}
              >
                Buscar
              </Button>
            </Grid>
          </Grid>

          {/* Campos adicionales si el paciente no existe */}
          <Collapse in={pacienteExiste === false}>
            <Box sx={{ mt: 2 }}>
              <Alert severity="info" sx={{ mb: 2 }}>
                Complete los siguientes datos para crear el paciente
              </Alert>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    error={!!errors.nombre}
                    helperText={errors.nombre}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Apellido"
                    value={apellido}
                    onChange={(e) => setApellido(e.target.value)}
                    error={!!errors.apellido}
                    helperText={errors.apellido}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Obra Social"
                    value={obraSocial}
                    onChange={(e) => setObraSocial(e.target.value)}
                    error={!!errors.obra_social}
                    helperText={errors.obra_social || 'Dejar vacío si no tiene obra social'}
                    disabled={pacienteExiste === true || loading}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Número de Afiliado"
                    value={numeroAfiliado}
                    onChange={(e) => setNumeroAfiliado(e.target.value)}
                    error={!!errors.numero_afiliado}
                    helperText={errors.numero_afiliado || 'Obligatorio si tiene obra social'}
                    disabled={pacienteExiste === true || loading}
                    required={!!obraSocial && obraSocial.trim() !== ''}
                  />
                </Grid>
              </Grid>
              
              {/* Campos de domicilio */}
              <Typography variant="subtitle2" sx={{ mt: 2, mb: 1, fontWeight: 600 }}>
                Domicilio
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={8}>
                  <TextField
                    fullWidth
                    label="Calle"
                    value={calle}
                    onChange={(e) => setCalle(e.target.value)}
                    error={!!errors.calle}
                    helperText={errors.calle}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Número"
                    type="number"
                    value={numero}
                    onChange={(e) => setNumero(e.target.value)}
                    error={!!errors.numero}
                    helperText={errors.numero}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Localidad"
                    value={localidad}
                    onChange={(e) => setLocalidad(e.target.value)}
                    error={!!errors.localidad}
                    helperText={errors.localidad}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Ciudad"
                    value={ciudad}
                    onChange={(e) => setCiudad(e.target.value)}
                    error={!!errors.ciudad}
                    helperText={errors.ciudad}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Provincia"
                    value={provincia}
                    onChange={(e) => setProvincia(e.target.value)}
                    error={!!errors.provincia}
                    helperText={errors.provincia}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="País"
                    value={pais}
                    onChange={(e) => setPais(e.target.value)}
                    error={!!errors.pais}
                    helperText={errors.pais}
                    disabled={pacienteExiste === true || loading}
                    required
                  />
                </Grid>
              </Grid>
            </Box>
          </Collapse>
        </Paper>

        {/* Nivel de emergencia */}
        <Box sx={{ mb: 3 }}>
          <NivelEmergenciaSelector
            value={nivelEmergencia}
            onChange={setNivelEmergencia}
            error={!!errors.nivel_emergencia}
            helperText={errors.nivel_emergencia}
            disabled={loading}
          />
        </Box>

        {/* Informe */}
        <TextField
          fullWidth
          label="Informe"
          multiline
          rows={4}
          value={informe}
          onChange={(e) => setInforme(e.target.value)}
          error={!!errors.informe}
          helperText={errors.informe || 'Describa el motivo de consulta y observaciones'}
          disabled={loading}
          required
          sx={{ mb: 3 }}
        />

        {/* Signos vitales */}
        <SignosVitales
          temperatura={temperatura}
          frecuenciaCardiaca={frecuenciaCardiaca}
          frecuenciaRespiratoria={frecuenciaRespiratoria}
          frecuenciaSistolica={frecuenciaSistolica}
          frecuenciaDiastolica={frecuenciaDiastolica}
          onTemperaturaChange={setTemperatura}
          onFrecuenciaCardiacaChange={setFrecuenciaCardiaca}
          onFrecuenciaRespiratoriaChange={setFrecuenciaRespiratoria}
          onFrecuenciaSistolicaChange={setFrecuenciaSistolica}
          onFrecuenciaDiastolicaChange={setFrecuenciaDiastolica}
          errors={errors}
          disabled={loading}
        />

        {/* Botones */}
        <Box display="flex" gap={2} justifyContent="flex-end">
          <Button
            variant="outlined"
            onClick={limpiarFormulario}
            disabled={loading}
          >
            Limpiar
          </Button>
          <Button
            type="submit"
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
            disabled={loading}
          >
            Registrar Ingreso
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default FormularioAdmision;


