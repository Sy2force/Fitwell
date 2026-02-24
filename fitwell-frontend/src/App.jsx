import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { Toaster } from 'react-hot-toast'

// Layout
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import ProtectedRoute from './components/ProtectedRoute'

// Pages
import Home from './pages/Home'
import ArticleDetail from './pages/ArticleDetail'
import CategoryPage from './pages/CategoryPage'
import Tools from './pages/Tools'
import Login from './pages/Login'
import Register from './pages/Register'
import CreateArticle from './pages/CreateArticle'
import Profile from './pages/Profile'

function App() {
  const location = useLocation()

  return (
    <div className="min-h-screen gradient-bg flex flex-col">
      <Navbar />
      
      <main className="flex-grow relative">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/articles/:id" element={<ArticleDetail />} />
            <Route path="/category/:slug" element={<CategoryPage />} />
            <Route path="/tools" element={<Tools />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/create-article" element={<CreateArticle />} />
              <Route path="/profile" element={<Profile />} />
            </Route>
          </Routes>
        </AnimatePresence>
      </main>

      <Footer />
      <Toaster 
        position="bottom-right"
        toastOptions={{
          style: {
            background: 'rgba(15, 15, 22, 0.8)',
            backdropFilter: 'blur(10px)',
            color: '#fff',
            border: '1px solid rgba(212, 175, 55, 0.3)',
            fontFamily: 'serif',
            padding: '16px',
            borderRadius: '0px'
          },
          success: {
            iconTheme: {
              primary: '#d4af37',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  )
}

export default App
