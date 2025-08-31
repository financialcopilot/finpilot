import React, { useContext } from 'react';
import { AppContext } from './context/AppContext';
import { Container, Box, Typography, CircularProgress, Alert } from '@mui/material';
import MainForm from './components/UserInput/MainForm';
import PlanDashboard from './components/Dashboard/PlanDashboard'; // <-- IMPORT THE NEW COMPONENT

function App() {
  const { generatedPlan, isLoading, error } = useContext(AppContext);

  return (
    <Box sx={{ bgcolor: '#f7fafc', minHeight: '100vh', py: 5 }}>
      <Container maxWidth="md">
        <Typography variant="h3" component="h1" align="center" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          FinPilot 🚀
        </Typography>
        <Typography variant="h6" component="h2" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Your AI-Powered Financial Co-Pilot
        </Typography>

        {isLoading ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 10 }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Generating your personalized plan...
            </Typography>
          </Box>
        ) : error ? (
          <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>
        ) : generatedPlan ? (
          <PlanDashboard /> // <-- RENDER THE DASHBOARD HERE
        ) : (
          <MainForm />
        )}
      </Container>
    </Box>
  );
}

export default App;