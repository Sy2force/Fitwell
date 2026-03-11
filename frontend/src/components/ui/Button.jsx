import { motion } from 'framer-motion'

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  onClick, 
  disabled = false,
  type = 'button'
}) => {
  const baseStyles = "font-display font-bold uppercase tracking-widest transition-all duration-300 transform skew-x-[-10deg] flex items-center justify-center relative group overflow-hidden"
  
  const variants = {
    primary: "bg-primary text-white hover:bg-white hover:text-primary shadow-[0_0_20px_rgba(37,99,235,0.5)] hover:shadow-[0_0_30px_rgba(255,255,255,0.8)] border border-primary",
    energy: "bg-energy text-white hover:bg-white hover:text-energy shadow-[0_0_20px_rgba(255,107,0,0.5)] hover:shadow-[0_0_30px_rgba(255,255,255,0.8)] border border-energy",
    outline: "bg-transparent text-white border border-white/20 hover:border-primary hover:text-primary hover:bg-white/5",
    ghost: "bg-transparent text-gray-400 hover:text-white"
  }
  
  const sizes = {
    sm: "px-4 py-2 text-xs",
    md: "px-8 py-3 text-sm",
    lg: "px-10 py-4 text-base"
  }

  const innerContent = (
    <div className="skew-x-[10deg] flex items-center gap-2 relative z-10">
      {children}
    </div>
  )

  return (
    <motion.button
      type={type}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
      whileHover={!disabled && variant !== 'ghost' ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
    >
      {variant !== 'ghost' && (
        <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
      )}
      {innerContent}
    </motion.button>
  )
}

export default Button
