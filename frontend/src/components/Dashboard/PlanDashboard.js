import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Grid, Typography, Paper } from '@mui/material';
import PlanCard from './PlanCard';
import SimulationTabs from './SimulationTabs'; // <-- IMPORT THE REAL COMPONENT
import ChatInterface from './ChatInterface';   // <-- IMPORT THE REAL COMPONENT

const PlanDashboard = () => {
  const { generatedPlan, userInput } = useContext(AppContext);

  if (!generatedPlan) {
    return <Typography>No plan generated yet.</Typography>;
  }

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 3, mb: 4, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Your Personalized Financial Plans, {userInput.name}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here are two distinct strategies our AI has crafted based on your unique profile and goals.
        </Typography>
      </Paper>
      
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <PlanCard plan={generatedPlan.sentinel_plan} title="The Sentinel Plan" />
        </Grid>
        <Grid item xs={12} md={6}>
          <PlanCard plan={generatedPlan.voyager_plan} title="The Voyager Plan" />
        </Grid>
      </Grid>

      {/* --- RENDER THE REAL COMPONENTS --- */}
      <SimulationTabs />
      <ChatInterface />
    </Box>
  );
};

export default PlanDashboard;