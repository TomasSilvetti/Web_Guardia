/**
 * Página de login y registro
 */
import React, { useState } from 'react';
import { Box, Container, Tabs, Tab } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { RegisterForm } from '../components/auth/RegisterForm';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);

  const handleLoginSuccess = () => {
    navigate('/urgencias');
  };

  const handleRegisterSuccess = () => {
    setTabValue(0); // Cambiar a la pestaña de login
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        py: 4
      }}
    >
      <Container maxWidth="sm">
        <Box
          sx={{
            backgroundColor: 'white',
            borderRadius: 2,
            overflow: 'hidden',
            boxShadow: 3
          }}
        >
          <Tabs
            value={tabValue}
            onChange={(_, newValue) => setTabValue(newValue)}
            variant="fullWidth"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab label="Iniciar Sesión" />
            <Tab label="Registrarse" />
          </Tabs>

          <Box sx={{ p: 3 }}>
            {tabValue === 0 ? (
              <LoginForm
                onSuccess={handleLoginSuccess}
                onSwitchToRegister={() => setTabValue(1)}
              />
            ) : (
              <RegisterForm
                onSuccess={handleRegisterSuccess}
                onSwitchToLogin={() => setTabValue(0)}
              />
            )}
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default LoginPage;






