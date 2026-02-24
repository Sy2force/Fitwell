import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { LogIn, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import useAuthStore from '../store/auth'

const Login = () => {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [formData, setFormData] = useState({ username: '', password: '' })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    
    const success = await login(formData.username, formData.password)
    
    if (success) {
      toast.success('Welcome back!')
      navigate('/')
    } else {
      toast.error('Invalid credentials')
    }
    setIsLoading(false)
  }

  return (
    <div className="page-container flex items-center justify-center min-h-[90vh] relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 -left-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="glass-card p-8 md:p-16 w-full max-w-xl relative overflow-hidden border-t border-primary/30 shadow-2xl"
      >
        <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-transparent via-primary to-transparent" />
        
        <div className="text-center mb-12 relative z-10">
          <div className="inline-block p-4 border border-primary/20 bg-primary/5 mb-6 rounded-full">
            <LogIn className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-4xl md:text-5xl font-serif font-bold mb-4 text-white tracking-tight">Welcome Back</h2>
          <p className="text-gray-400 font-light text-base tracking-wide max-w-xs mx-auto">Enter your credentials to access the elite wellness collective.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8 relative z-10">
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-3 transition-colors group-focus-within:text-white">Username</label>
            <input
              type="text"
              className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all py-4 px-6 text-lg font-serif italic"
              placeholder="e.g. alex_elite"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
            />
          </div>

          <div className="group">
            <div className="flex justify-between items-end mb-3">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] transition-colors group-focus-within:text-white">Password</label>
              <button type="button" className="text-[9px] uppercase tracking-widest text-gray-500 hover:text-primary transition-colors">Forgot?</button>
            </div>
            <input
              type="password"
              className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all py-4 px-6 text-lg"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          </div>

          <div className="pt-4">
            <button 
              type="submit" 
              disabled={isLoading}
              className="glass-button w-full flex items-center justify-center py-5 text-sm tracking-[0.4em] uppercase font-bold group overflow-hidden relative"
            >
              <span className="relative z-10 flex items-center">
                {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : (
                  <>
                    Sign In <LogIn className="ml-3 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </span>
            </button>
          </div>
        </form>

        <p className="mt-8 text-center text-xs text-gray-500 font-light tracking-wide relative z-10">
          Don&apos;t have an account?{' '}
          <Link to="/register" className="text-primary hover:text-white transition-colors border-b border-primary/30 pb-0.5 font-bold">
            Join the Elite
          </Link>
        </p>
      </motion.div>
    </div>
  )
}

export default Login
