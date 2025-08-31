import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Typography, TextField, Button, Stack, Paper } from '@mui/material';

const Step3Goals = () => {
  const { nextStep, prevStep, userInput, addGoal, handleGoalChange } = useContext(AppContext);

  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom>
        Step 3: Your Goals
      </Typography>
      
      {userInput.goals.map((goal, index) => (
        <Paper key={index} elevation={2} sx={{ p: 2, mt: 1 }}>
          <Stack spacing={2}>
            <Typography variant="subtitle1">Goal #{index + 1}</Typography>
            <TextField
              label="Goal Name"
              name="name"
              value={goal.name}
              onChange={(e) => handleGoalChange(index, e)}
              variant="outlined"
              required
            />
            <TextField
              label="Target Amount (₹)"
              name="target_amount"
              type="number"
              value={goal.target_amount}
              onChange={(e) => handleGoalChange(index, e)}
              variant="outlined"
              required
            />
            <TextField
              label="Timeline (in years)"
              name="timeline_years"
              type="number"
              value={goal.timeline_years}
              onChange={(e) => handleGoalChange(index, e)}
              variant="outlined"
              required
            />
          </Stack>
        </Paper>
      ))}

      <Button variant="outlined" onClick={addGoal} sx={{ mt: 2 }}>
        Add Another Goal
      </Button>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
        <Button onClick={prevStep}>Back</Button>
        <Button variant="contained" onClick={nextStep}>Next</Button>
      </Box>
    </Stack>
  );
};

export default Step3Goals;