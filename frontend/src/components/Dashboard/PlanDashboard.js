import React, { useContext, useEffect } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Grid, Typography, Paper } from '@mui/material';
import PlanCard from './PlanCard';
import SimulationTabs from './SimulationTabs';
import ChatInterface from './ChatInterface';
import EvaluationDisplay from './EvaluationDisplay'; // <-- IMPORT THE NEW COMPONENT
import { evaluateGeneratedPlan } from '../../services/api'; // <-- IMPORT THE NEW API FUNCTION

const PlanDashboard = () => {
  const { 
    generatedPlan, 
    userInput, 
    setEvaluationResult, 
    setIsEvaluating 
  } = useContext(AppContext);

  // --- NEW: useEffect to trigger evaluation after plan is generated ---
  useEffect(() => {
    const runEvaluation = async () => {
      // Ensure we only run this once when the plan is first generated
      if (generatedPlan && userInput) {
        setIsEvaluating(true);
        setEvaluationResult(null); // Clear previous results
        try {
          const result = await evaluateGeneratedPlan(userInput, generatedPlan);
          setEvaluationResult(result);
        } catch (error) {
          console.error("Failed to fetch plan evaluation:", error);
          // Optionally, set an error state for the evaluation component
          setEvaluationResult({ error: "Could not retrieve plan analysis." });
        } finally {
          setIsEvaluating(false);
        }
      }
    };

    runEvaluation();
  }, [generatedPlan, userInput, setEvaluationResult, setIsEvaluating]); // Dependencies array ensures this runs only when a new plan is created

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
      
      {/* --- RENDER THE NEW EVALUATION COMPONENT --- */}
      <EvaluationDisplay />

      <Grid container spacing={4} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <PlanCard plan={generatedPlan.sentinel_plan} title="The Sentinel Plan" />
        </Grid>
        <Grid item xs={12} md={6}>
          <PlanCard plan={generatedPlan.voyager_plan} title="The Voyager Plan" />
        </Grid>
      </Grid>

      <SimulationTabs />
      <ChatInterface />
    </Box>
  );
};

export default PlanDashboard;