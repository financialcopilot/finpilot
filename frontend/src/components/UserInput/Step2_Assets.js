import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { Box, Typography, TextField, Button, Stack } from '@mui/material';

const Step2Assets = () => {
  const { nextStep, prevStep, handleNestedInputChange, userInput } = useContext(AppContext);

  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom>
        Step 2: Your Financials
      </Typography>
      
      <Typography variant="h6">Assets</Typography>
      <TextField
        label="Cash & Savings (₹)"
        name="cash_equivalents"
        type="number"
        value={userInput.assets.cash_equivalents}
        onChange={(e) => handleNestedInputChange('assets', e)}
        variant="outlined"
        required
      />
      <TextField
        label="Equity Investments (Stocks, MFs) (₹)"
        name="equity_investments"
        type="number"
        value={userInput.assets.equity_investments}
        onChange={(e) => handleNestedInputChange('assets', e)}
        variant="outlined"
        required
      />

      <Typography variant="h6" sx={{ mt: 2 }}>Liabilities</Typography>
      <TextField
        label="High-Interest Debt (Credit Cards) (₹)"
        name="high_interest_debt"
        type="number"
        value={userInput.liabilities.high_interest_debt}
        onChange={(e) => handleNestedInputChange('liabilities', e)}
        variant="outlined"
        required
      />
      <TextField
        label="Total Loan EMIs per month (₹)"
        name="loans_emi"
        type="number"
        value={userInput.liabilities.loans_emi}
        onChange={(e) => handleNestedInputChange('liabilities', e)}
        variant="outlined"
        required
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
        <Button onClick={prevStep}>Back</Button>
        <Button variant="contained" onClick={nextStep}>Next</Button>
      </Box>
    </Stack>
  );
};

export default Step2Assets;