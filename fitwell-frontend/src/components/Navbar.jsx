import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Dumbbell, LogOut, User } from 'lucide-react'
import useAuthStore from '../store/auth'
import clsx from 'clsx'

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const NavLink = ({ to, children, className }) => {
    const isActive = location.pathname === to
    return (
      <Link 
        to={to} 
        className={clsx(
          "relative px-2 py-1 transition-colors duration-300 font-medium tracking-wide text-sm uppercase",
          isActive ? "text-primary" : "text-gray-400 hover:text-white",
          className
        )}
      >
        {children}
        {isActive && (
          <motion.div 
            layoutId="navbar-indicator"
            className="absolute bottom-0 left-0 w-full h-[1px] bg-primary shadow-[0_0_10px_rgba(212,175,55,0.5)]"
            transition={{ duration: 0.3 }}
          />
        )}
      </Link>
    )
  }

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-white/5"
    >
      <div className="max-w-[1400px] mx-auto px-6">
        <div className="flex items-center justify-between h-24">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-12 h-12 border border-primary/30 flex items-center justify-center group-hover:bg-primary/10 transition-all duration-500 transform group-hover:rotate-[360deg]">
              <Dumbbell className="w-6 h-6 text-primary" />
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-serif font-bold tracking-tighter text-white leading-none">
                Fit<span className="text-primary italic">Well</span>
              </span>
              <span className="text-[8px] uppercase tracking-[0.4em] text-primary/60 font-bold">Sport OS</span>
            </div>
          </Link>

          <div className="flex items-center space-x-10">
            <div className="hidden lg:flex items-center space-x-8">
              <NavLink to="/">Home</NavLink>
              <NavLink to="/articles">Discover</NavLink>
              <NavLink to="/categories">Journals</NavLink>
            </div>
            
            <div className="h-8 w-[1px] bg-white/5 hidden lg:block"></div>
            
            {isAuthenticated ? (
              <>
                <NavLink to="/create-article">Write</NavLink>
                <NavLink to="/profile">Profile</NavLink>
                
                <div className="h-6 w-[1px] bg-white/10 mx-4"></div>
                
                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-none border border-primary/30 flex items-center justify-center bg-surface">
                      <User className="w-4 h-4 text-primary" />
                    </div>
                    <span className="font-serif italic text-gray-300 hidden md:block">{user?.username}</span>
                  </div>
                  
                  <button 
                    onClick={handleLogout}
                    className="text-gray-500 hover:text-red-400 transition-colors"
                    title="Logout"
                  >
                    <LogOut className="w-5 h-5" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="h-6 w-[1px] bg-white/10 mx-2"></div>
                <div className="flex items-center space-x-6">
                  <NavLink to="/login">Login</NavLink>
                  <Link 
                    to="/register" 
                    className="glass-button text-[10px] px-6 py-3"
                  >
                    Join Elite
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </motion.nav>
  )
}

export default Navbar
