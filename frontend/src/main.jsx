import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'
import './i18n'
import { ThemeProvider } from './context/ThemeContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <React.Suspense fallback="Loading...">
          <App />
        </React.Suspense>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
