/**
 * Aplicación principal con routing
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { UrgenciasPage } from './pages/UrgenciasPage';

// Crear tema de Material UI
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            {/* Ruta raíz redirige a urgencias */}
            <Route path="/" element={<Navigate to="/urgencias" replace />} />
            
            {/* Ruta de login */}
            <Route path="/login" element={<LoginPage />} />
            
            {/* Ruta protegida de urgencias (solo enfermeras) */}
            <Route
              path="/urgencias"
              element={
                <ProtectedRoute requireEnfermera={true}>
                  <UrgenciasPage />
                </ProtectedRoute>
              }
            />
            
            {/* Ruta 404 */}
            <Route path="*" element={<Navigate to="/urgencias" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
