import React, { useContext, useEffect } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Typography, Paper } from '@mui/material';
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
      if (generatedPlan && userInput) {
        setIsEvaluating(true);
        setEvaluationResult(null); // Clear previous results
        try {
          const result = await evaluateGeneratedPlan(userInput, generatedPlan);
          setEvaluationResult(result);
        } catch (error) {
          console.error("Failed to fetch plan evaluation:", error);
          setEvaluationResult({ error: "Could not retrieve plan analysis." });
        } finally {
          setIsEvaluating(false);
        }
      }
    };

    runEvaluation();
  }, [generatedPlan, userInput, setEvaluationResult, setIsEvaluating]);

  if (!generatedPlan) {
    return <Typography>No plan generated yet.</Typography>;
  }

  return (
    <Box sx={{ width: '100%' }}>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 3, mb: 4, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#9e81d7ff' }}>
          Your Personalized Financial Plans, {userInput.name}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here are two distinct strategies our AI has crafted based on your unique profile and goals.
        </Typography>
      </Paper>

      {/* --- RENDER THE NEW EVALUATION COMPONENT --- */}
      <Box sx={{ mb: 4 }}>
        <EvaluationDisplay />
      </Box>

      {/* Plans Section */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          gap: 4,
          width: '100%',
        }}
      >
        {/* Sentinel Plan */}
        <Box
          sx={{
            flex: 1,
            backgroundColor: '#9e81d7ff',
            p: 0.2,
            borderRadius: 2,
            display: 'flex',
            alignItems: 'stretch',
            boxShadow: '0 0 6px rgba(158, 129, 215, 0.7)',
          }}
        >
          <PlanCard plan={generatedPlan.sentinel_plan} title="The Sentinel Plan" />
        </Box>

        {/* Voyager Plan */}
        <Box
          sx={{
            flex: 1,
            backgroundColor: '#9e81d7ff',
            p: 0.2,
            borderRadius: 2,
            display: 'flex',
            alignItems: 'stretch',
            boxShadow: '0 0 6px rgba(158, 129, 215, 0.7)',
          }}
        >
          <PlanCard plan={generatedPlan.voyager_plan} title="The Voyager Plan" />
        </Box>
      </Box>

      {/* Simulation + Chat */}
      <SimulationTabs />
      <ChatInterface />
    </Box>
  );
};

export default PlanDashboard;