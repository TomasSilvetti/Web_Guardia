/**
 * Página principal del módulo de urgencias
 */
import React, { useState } from 'react';
import { Container, Grid, Box } from '@mui/material';
import { Navbar } from '../components/common/Navbar';
import { FormularioAdmision } from '../components/urgencias/FormularioAdmision';
import { ListaEspera } from '../components/urgencias/ListaEspera';

export const UrgenciasPage: React.FC = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleIngresoSuccess = () => {
    // Incrementar el trigger para refrescar la lista
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#f5f5f5' }}>
  <Navbar />
  
  {/* Formulario en container */}
  <Container maxWidth="xl" sx={{ py: 4 }}>
    <FormularioAdmision onSuccess={handleIngresoSuccess} />
  </Container>

  {/* Lista de espera ocupando todo el ancho */}
  <Box sx={{ px: 9, pb: 4 }}>
    <ListaEspera refreshTrigger={refreshTrigger} />
  </Box>
</Box>
  );
};

export default UrgenciasPage;


