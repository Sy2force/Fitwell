const Input = ({ label, type = 'text', name, value, onChange, placeholder, required = false, className = '' }) => {
  return (
    <div className={`group ${className}`}>
      {label && (
        <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2 group-focus-within:text-white transition-colors">
          {label}
        </label>
      )}
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="w-full bg-surface-dark border-2 border-white/10 px-4 py-3 text-white placeholder-gray-600 rounded-lg focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all duration-300 font-sans"
      />
    </div>
  )
}

export default Input
