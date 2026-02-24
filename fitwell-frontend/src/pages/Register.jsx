import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserPlus, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import useAuthStore from '../store/auth'

const Register = () => {
  const navigate = useNavigate()
  const register = useAuthStore((state) => state.register)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    setIsLoading(true)
    const result = await register({
      username: formData.username,
      email: formData.email,
      password: formData.password
    })
    
    if (result.success) {
      toast.success('Account created! Please login.')
      navigate('/login')
    } else {
      toast.error(result.error || 'Registration failed')
    }
    setIsLoading(false)
  }

  return (
    <div className="page-container flex items-center justify-center min-h-[95vh] py-20 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 -right-20 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-1/4 -left-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="glass-card p-10 md:p-20 w-full max-w-2xl relative overflow-hidden border-t border-primary/40 shadow-2xl"
      >
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-transparent via-primary to-transparent" />
        
        <div className="text-center mb-12 relative z-10">
          <div className="inline-block p-5 border border-primary/30 bg-primary/10 mb-8 rounded-full transform hover:scale-110 transition-transform">
            <UserPlus className="w-10 h-10 text-primary" />
          </div>
          <h2 className="text-4xl md:text-6xl font-serif font-bold mb-6 text-white tracking-tight leading-tight">
            Join the <span className="text-primary italic">Elite</span>
          </h2>
          <p className="text-gray-400 font-light text-lg tracking-wide max-w-md mx-auto">
            Become a part of our exclusive community for optimal wellness and performance.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Elite Identifier</label>
              <input
                type="text"
                className="input-field bg-white/5 border-white/10 focus:border-primary/60 focus:bg-white/10 transition-all py-5 px-6 font-serif italic text-lg"
                placeholder="Choose a username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
              />
            </div>

            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Direct Link (Email)</label>
              <input
                type="email"
                className="input-field bg-white/5 border-white/10 focus:border-primary/60 focus:bg-white/10 transition-all py-5 px-6 italic"
                placeholder="you@domain.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Security Key</label>
              <input
                type="password"
                className="input-field bg-white/5 border-white/10 focus:border-primary/60 focus:bg-white/10 transition-all py-5 px-6 font-mono text-xl"
                placeholder="Create password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
              />
            </div>

            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Verification</label>
              <input
                type="password"
                className="input-field bg-white/5 border-white/10 focus:border-primary/60 focus:bg-white/10 transition-all py-5 px-6 font-mono text-xl"
                placeholder="Confirm password"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="pt-8">
            <button 
              type="submit" 
              disabled={isLoading}
              className="glass-button w-full flex items-center justify-center py-6 text-sm tracking-[0.5em] uppercase font-bold group relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-primary opacity-0 group-hover:opacity-10 transition-opacity" />
              <span className="relative z-10 flex items-center">
                {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : (
                  <>
                    Initialize Membership <UserPlus className="ml-4 w-5 h-5 group-hover:scale-110 transition-transform" />
                  </>
                )}
              </span>
            </button>
            <p className="mt-6 text-[9px] text-gray-500 uppercase tracking-[0.3em] text-center max-w-sm mx-auto leading-relaxed">
              By joining, you agree to our elite code of conduct and exclusive terms of membership.
            </p>
          </div>
        </form>

        <p className="mt-8 text-center text-xs text-gray-500 font-light tracking-wide relative z-10">
          Already have an account?{' '}
          <Link to="/login" className="text-primary hover:text-white transition-colors border-b border-primary/30 pb-0.5 font-bold">
            Login here
          </Link>
        </p>
      </motion.div>
    </div>
  )
}

export default Register
