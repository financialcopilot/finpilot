import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AppProvider } from './context/AppContext';

// MUI Imports
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme(); // Using the default theme

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AppProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline /> {/* A simple baseline stylesheet */}
        <App />
      </ThemeProvider>
    </AppProvider>
  </React.StrictMode>
);