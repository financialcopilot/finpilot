import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import AppProvider from './context/AppContext'; // default export, as per earlier context changes

// MUI Imports
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme(); // Default MUI theme

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <AppProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </AppProvider>
  </React.StrictMode>
);