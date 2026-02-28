import { motion } from 'framer-motion'

const ProgressBar = ({ value, max = 100, color = 'primary', label, showValue = true }) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const colors = {
    primary: "bg-primary shadow-[0_0_10px_rgba(37,99,235,0.5)]",
    energy: "bg-energy shadow-[0_0_10px_rgba(255,107,0,0.5)]",
    health: "bg-health shadow-[0_0_10px_rgba(20,184,166,0.5)]"
  }

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="flex justify-between items-end mb-2">
          {label && <span className="text-xs font-display font-bold uppercase tracking-widest text-gray-400">{label}</span>}
          {showValue && <span className="text-xs font-mono text-white">{Math.round(percentage)}%</span>}
        </div>
      )}
      <div className="h-2 bg-white/5 w-full overflow-hidden skew-x-[-10deg]">
        <motion.div 
          className={`h-full ${colors[color]}`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </div>
    </div>
  )
}

export default ProgressBar
