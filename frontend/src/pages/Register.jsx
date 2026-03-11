import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserPlus, Loader2, ShieldCheck } from 'lucide-react'
import toast from 'react-hot-toast'
import useAuthStore from '../store/auth'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (formData.password !== formData.confirmPassword) {
      toast.error('Security Check Failed: Passwords Mismatch')
      return
    }

    setIsLoading(true)
    const result = await register({
      username: formData.username,
      email: formData.email,
      password: formData.password
    })
    
    if (result.success) {
      toast.success('Registration Complete. Welcome, Athlete.')
      navigate('/login')
    } else {
      toast.error(result.error || 'Registration Failed')
    }
    setIsLoading(false)
  }

  return (
    <div className="page-container flex items-center justify-center min-h-[95vh] py-20 relative overflow-hidden bg-background">
      {/* Decorative background elements */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent/5 rounded-full blur-[150px] pointer-events-none animate-pulse"></div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="glass-card p-1 border-l-4 border-accent w-full max-w-2xl relative overflow-hidden"
      >
        <div className="bg-surface/90 p-8 md:p-12 backdrop-blur-xl relative z-10">
            <div className="text-center mb-10">
                <div className="inline-flex p-4 border-2 border-accent mb-6 bg-black/50 transform skew-x-[-10deg]">
                    <ShieldCheck className="w-10 h-10 text-accent transform skew-x-[10deg]" />
                </div>
                <h2 className="text-3xl md:text-5xl font-display font-bold mb-2 text-white italic tracking-tighter">
                    ATHLETE <span className="text-accent">REGISTRATION</span>
                </h2>
                <p className="text-gray-400 font-mono text-xs uppercase tracking-widest">Create Your Legacy</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                    label="Callsign (Username)"
                    placeholder="USERNAME"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
                
                <Input
                    label="Comms Link (Email)"
                    type="email"
                    placeholder="EMAIL@DOMAIN.COM"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                    label="Security Key"
                    type="password"
                    placeholder="PASSWORD"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />

                <Input
                    label="Confirm Key"
                    type="password"
                    placeholder="CONFIRM PASSWORD"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="pt-8">
                <Button 
                    type="submit" 
                    variant="energy" 
                    size="lg" 
                    className="w-full bg-accent border-accent hover:text-accent"
                    disabled={isLoading}
                >
                    {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : (
                    <>
                        Initialize Profile <UserPlus className="ml-4 w-5 h-5 group-hover:scale-110 transition-transform" />
                    </>
                    )}
                </Button>
                <p className="mt-4 text-[9px] text-gray-500 uppercase tracking-widest text-center font-mono">
                By registering, you commit to the pursuit of excellence.
                </p>
            </div>
            </form>

            <div className="mt-8 text-center border-t border-white/5 pt-6">
            <p className="text-xs text-gray-500 font-mono">
                ALREADY REGISTERED?{' '}
                <Link to="/login" className="text-primary hover:text-white transition-colors font-bold uppercase ml-2">
                LOGIN HERE
                </Link>
            </p>
            </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Register
