/**
 * Página principal del módulo de urgencias
 */
import React, { useState } from 'react';
import { Container, Box, Snackbar, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/common/Navbar';
import { FormularioAdmision } from '../components/urgencias/FormularioAdmision';
import { ListaEspera } from '../components/urgencias/ListaEspera';
import { ListaRevisionEnProceso } from '../components/urgencias/ListaRevisionEnProceso';
import { useUrgencias } from '../hooks/useUrgencias';
import { isMedico } from '../services/authService';

export const UrgenciasPage: React.FC = () => {
  const navigate = useNavigate();
  const { reclamar } = useUrgencias();
  const [refreshTriggerPendientes, setRefreshTriggerPendientes] = useState(0);
  const [refreshTriggerEnProceso, setRefreshTriggerEnProceso] = useState(0);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success'
  });

  const esMedico = isMedico();

  const handleIngresoSuccess = () => {
    // Incrementar el trigger para refrescar la lista de pendientes
    setRefreshTriggerPendientes(prev => prev + 1);
  };

  const handleReclamar = async () => {
    try {
      const response = await reclamar();
      
      if (response) {
        setSnackbar({
          open: true,
          message: `Paciente ${response.nombre_paciente} ${response.apellido_paciente} reclamado exitosamente`,
          severity: 'success'
        });
        
        // Refrescar ambas listas
        setRefreshTriggerPendientes(prev => prev + 1);
        setRefreshTriggerEnProceso(prev => prev + 1);
        
        // Redirigir a la página de revisión
        navigate(`/urgencias/revision/${response.id}`);
      }
    } catch (error: any) {
      // Mostrar error en snackbar
      setSnackbar({
        open: true,
        message: error.message || 'Error al reclamar paciente',
        severity: 'error'
      });
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
      <Navbar />
      
      {/* Formulario en container - Solo visible para enfermeras */}
      {!esMedico && (
        <Container maxWidth="xl" sx={{ py: 4 }}>
          <FormularioAdmision onSuccess={handleIngresoSuccess} />
        </Container>
      )}

      {/* Listas ocupando todo el ancho */}
      <Box sx={{ px: 9, pb: 4 }}>
        {/* Lista de revisión en proceso - encima de lista de espera */}
        <ListaRevisionEnProceso refreshTrigger={refreshTriggerEnProceso} />
        
        {/* Lista de espera */}
        <ListaEspera 
          refreshTrigger={refreshTriggerPendientes}
          showReclamarButton={esMedico}
          onReclamar={handleReclamar}
        />
      </Box>

      {/* Snackbar para notificaciones */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default UrgenciasPage;


