import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Typography, TextField, Button, Stack } from '@mui/material';

const Step1Profile = () => {
  const { nextStep, handleInputChange, userInput } = useContext(AppContext);

  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom>
        Step 1: Your Profile
      </Typography>
      <TextField
        label="Full Name"
        name="name"
        value={userInput.name}
        onChange={handleInputChange}
        variant="outlined"
        required
      />
      <TextField
        label="Age"
        name="age"
        type="number"
        value={userInput.age}
        onChange={handleInputChange}
        variant="outlined"
        required
      />
      <TextField
        label="Monthly Take-Home Income (₹)"
        name="monthly_income"
        type="number"
        value={userInput.monthly_income}
        onChange={handleInputChange}
        variant="outlined"
        required
      />
      <TextField
        label="Average Monthly Expenses (₹)"
        name="monthly_expenses"
        type="number"
        value={userInput.monthly_expenses}
        onChange={handleInputChange}
        variant="outlined"
        required
      />
      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="contained" onClick={nextStep}>
          Next
        </Button>
      </Box>
    </Stack>
  );
};

export default Step1Profile;