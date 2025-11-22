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
      
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Formulario de admisión */}
          <Grid item xs={12} lg={6}>
            <FormularioAdmision onSuccess={handleIngresoSuccess} />
          </Grid>

          {/* Lista de espera */}
          <Grid item xs={12} lg={6}>
            <ListaEspera refreshTrigger={refreshTrigger} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default UrgenciasPage;


