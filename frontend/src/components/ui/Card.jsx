import { motion } from 'framer-motion'

const Card = ({ children, className = '', hover = true }) => {
  return (
    <motion.div 
      className={`bg-surface border border-white/10 p-6 relative overflow-hidden group ${className}`}
      whileHover={hover ? { y: -5, borderColor: 'var(--color-primary)' } : {}}
      transition={{ duration: 0.3 }}
    >
      {hover && (
        <>
          <div className="absolute top-0 right-0 w-20 h-20 bg-primary/5 rounded-full blur-2xl -mr-10 -mt-10 transition-opacity duration-500 opacity-0 group-hover:opacity-100 pointer-events-none"></div>
          <div className="absolute bottom-0 left-0 w-16 h-16 bg-energy/5 rounded-full blur-xl -ml-8 -mb-8 transition-opacity duration-500 opacity-0 group-hover:opacity-100 pointer-events-none"></div>
        </>
      )}
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  )
}

export default Card
