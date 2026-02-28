const Badge = ({ children, variant = 'default', className = '' }) => {
  const variants = {
    default: "bg-white/10 text-gray-300 border-white/20",
    primary: "bg-primary/10 text-primary border-primary/30",
    energy: "bg-energy/10 text-energy border-energy/30",
    health: "bg-health/10 text-health border-health/30",
    outline: "bg-transparent border-white/40 text-gray-400"
  }

  return (
    <span className={`inline-flex items-center px-3 py-1 border text-[10px] font-display font-bold uppercase tracking-widest transform skew-x-[-10deg] ${variants[variant]} ${className}`}>
      <span className="skew-x-[10deg]">{children}</span>
    </span>
  )
}

export default Badge
