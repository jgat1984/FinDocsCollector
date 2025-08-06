import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css'; // ✅ Ensure this file exists
import App from './App'; // ✅ App.js must have `export default App`

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
