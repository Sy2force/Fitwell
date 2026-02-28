import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Dumbbell, LogOut, User, Sun, Moon, Globe, ShieldAlert } from 'lucide-react'
import useAuthStore from '../store/auth'
import { useTheme } from '../context/ThemeContext'
import { useTranslation } from 'react-i18next'
import clsx from 'clsx'

const NavLink = ({ to, children, className }) => {
  const location = useLocation()
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

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()
  const { theme, toggleTheme } = useTheme()
  const { t, i18n } = useTranslation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'fr' : 'en'
    i18n.changeLanguage(newLang)
  }

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-xl border-b border-white/10"
    >
      <div className="max-w-[1400px] mx-auto px-6">
        <div className="flex items-center justify-between h-24">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-12 h-12 border-2 border-primary flex items-center justify-center group-hover:bg-primary group-hover:text-black transition-all duration-500 transform skew-x-[-10deg]">
              <div className="skew-x-[10deg]">
                <Dumbbell className="w-6 h-6 text-inherit" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-display font-bold tracking-tighter text-white leading-none italic">
                Fit<span className="text-primary">Well</span>
              </span>
              <span className="text-[10px] uppercase tracking-[0.3em] text-secondary font-bold">Sport OS</span>
            </div>
          </Link>

          <div className="flex items-center space-x-6 md:space-x-10">
            <div className="hidden lg:flex items-center space-x-8">
              <NavLink to="/">{t('nav.home')}</NavLink>
              <NavLink to="/category/strength">Strength</NavLink>
              <NavLink to="/category/nutrition">Nutrition</NavLink>
              <NavLink to="/tools">{t('nav.tools')}</NavLink>
            </div>
            
            <div className="h-8 w-[2px] bg-white/10 hidden lg:block skew-x-[-10deg]"></div>
            
            {/* Utilities */}
            <div className="flex items-center space-x-4">
                <button onClick={toggleTheme} className="text-gray-400 hover:text-white transition-colors">
                    {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                </button>
                <button onClick={toggleLanguage} className="text-gray-400 hover:text-white transition-colors flex items-center text-xs font-bold uppercase">
                    <Globe className="w-4 h-4 mr-1" /> {i18n.language}
                </button>
            </div>

            <div className="h-8 w-[2px] bg-white/10 hidden md:block skew-x-[-10deg]"></div>

            {isAuthenticated ? (
              <>
                <div className="hidden md:flex items-center space-x-6">
                    <NavLink to="/planner">{t('nav.planner')}</NavLink>
                    <NavLink to="/profile">Profile</NavLink>
                    
                    {user?.is_staff && (
                        <NavLink to="/admin" className="text-accent hover:text-accent/80">
                            <span className="flex items-center"><ShieldAlert className="w-4 h-4 mr-1" /> {t('nav.admin')}</span>
                        </NavLink>
                    )}
                </div>
                
                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 border border-primary flex items-center justify-center bg-surface skew-x-[-10deg]">
                      <User className="w-4 h-4 text-primary skew-x-[10deg]" />
                    </div>
                    <span className="font-display font-bold italic text-white hidden md:block">{user?.username}</span>
                  </div>
                  
                  <button 
                    onClick={handleLogout}
                    className="text-gray-500 hover:text-accent transition-colors"
                    title="Logout"
                  >
                    <LogOut className="w-5 h-5" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-center space-x-6">
                  <NavLink to="/login">{t('nav.login')}</NavLink>
                  <Link 
                    to="/register" 
                    className="glass-button text-[10px] px-6 py-3 border-accent text-accent hover:bg-accent hover:text-white hover:shadow-[0_0_20px_rgba(255,0,60,0.4)]"
                  >
                    <span className="block">{t('nav.register')}</span>
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
