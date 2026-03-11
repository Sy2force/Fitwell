import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { LogIn, Loader2, Lock } from 'lucide-react'
import toast from 'react-hot-toast'
import useAuthStore from '../store/auth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

const Login = () => {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    
    const success = await login(formData.email, formData.password)
    
    if (success) {
      toast.success('System Access Granted')
      navigate('/')
    } else {
      toast.error('Access Denied: Invalid Credentials')
    }
    setIsLoading(false)
  }

  return (
    <div className="page-container flex items-center justify-center min-h-[90vh] relative overflow-hidden bg-background">
      {/* Decorative background elements */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] pointer-events-none animate-pulse-fast"></div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="glass-card p-1 border-l-4 border-primary w-full max-w-lg relative overflow-hidden"
      >
        <div className="bg-surface/90 p-8 md:p-12 backdrop-blur-xl relative z-10">
            <div className="text-center mb-10">
            <div className="inline-flex p-4 border-2 border-primary mb-6 bg-black/50 transform skew-x-[-10deg]">
                <Lock className="w-8 h-8 text-primary transform skew-x-[10deg]" />
            </div>
            <h2 className="text-3xl md:text-4xl font-display font-bold mb-2 text-white italic tracking-tighter">
                MEMBER <span className="text-primary">ACCESS</span>
            </h2>
            <p className="text-gray-400 font-mono text-xs uppercase tracking-widest">Secure Terminal</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
            <Input
                label="Identifier"
                type="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                name="email"
                required
            />

            <div className="group">
                <div className="flex justify-between items-end mb-2">
                <label className="block text-[10px] font-bold text-primary uppercase tracking-widest">Security Key</label>
                <button type="button" className="text-[9px] uppercase tracking-widest text-gray-500 hover:text-white transition-colors">Reset Key?</button>
                </div>
                <input
                type="password"
                className="w-full bg-surface-dark border-2 border-white/10 px-4 py-3 text-white placeholder-gray-600 rounded-lg focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all duration-300 font-sans"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                />
            </div>

            <div className="pt-6">
                <Button 
                    type="submit" 
                    variant="primary" 
                    size="lg" 
                    className="w-full"
                    disabled={isLoading}
                >
                    {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : (
                    <>
                        Initiate Session <LogIn className="ml-3 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </>
                    )}
                </Button>
            </div>
            </form>

            <div className="mt-8 text-center border-t border-white/5 pt-6">
            <p className="text-xs text-gray-500 font-mono">
                NEW RECRUIT?{' '}
                <Link to="/register" className="text-accent hover:text-white transition-colors font-bold uppercase ml-2">
                APPLY FOR ENTRY
                </Link>
            </p>
            </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Login
