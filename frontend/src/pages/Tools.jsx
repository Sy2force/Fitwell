import { useState } from 'react'
import { motion } from 'framer-motion'
import { Calculator, Activity, Scale, Zap } from 'lucide-react'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

const Tools = () => {
  const [activeTab, setActiveTab] = useState('bmi')
  
  return (
    <div className="page-container py-20 min-h-screen bg-background relative overflow-hidden">
      {/* Background FX */}
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_0%,rgba(37,99,235,0.1),transparent_50%)] pointer-events-none" />

      <div className="max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex p-4 border-2 border-primary bg-black/50 transform skew-x-[-10deg] mb-6 hover:shadow-[0_0_20px_rgba(37,99,235,0.4)] transition-all"
          >
            <div className="skew-x-[10deg]">
                <Calculator className="w-10 h-10 text-primary" />
            </div>
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-display font-bold text-white mb-4 italic tracking-tighter">
            PERFORMANCE <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-energy">METRICS</span>
          </h1>
          <p className="text-gray-400 text-lg font-mono uppercase tracking-widest">
            Quantify your biological output.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-16">
            <div className="inline-flex bg-white/5 p-1 border border-white/10 skew-x-[-10deg]">
                <button
                    onClick={() => setActiveTab('bmi')}
                    className={`px-8 py-3 text-sm uppercase tracking-widest font-bold transition-all duration-300 ${
                    activeTab === 'bmi' 
                        ? 'bg-primary text-white shadow-[0_0_15px_rgba(37,99,235,0.5)]' 
                        : 'text-gray-500 hover:text-white'
                    }`}
                >
                    <span className="block skew-x-[10deg]">BMI Index</span>
                </button>
                <button
                    onClick={() => setActiveTab('calories')}
                    className={`px-8 py-3 text-sm uppercase tracking-widest font-bold transition-all duration-300 ${
                    activeTab === 'calories' 
                        ? 'bg-energy text-white shadow-[0_0_15px_rgba(255,107,0,0.5)]' 
                        : 'text-gray-500 hover:text-white'
                    }`}
                >
                    <span className="block skew-x-[10deg]">TDEE / Macros</span>
                </button>
            </div>
        </div>

        <div className="glass-card p-1 border-l-4 border-primary relative overflow-hidden">
          <div className="bg-surface/90 p-8 md:p-12 backdrop-blur-xl">
            {activeTab === 'bmi' ? <BMICalculator /> : <MacroCalculator />}
          </div>
        </div>
      </div>
    </div>
  )
}

const BMICalculator = () => {
  const [height, setHeight] = useState('')
  const [weight, setWeight] = useState('')
  const [bmi, setBmi] = useState(null)
  const [status, setStatus] = useState('')

  const calculateBMI = (e) => {
    e.preventDefault()
    if (height && weight) {
      const h = height / 100
      const val = (weight / (h * h)).toFixed(1)
      setBmi(val)
      
      if (val < 18.5) setStatus('Underweight')
      else if (val < 25) setStatus('Optimal')
      else if (val < 30) setStatus('Overweight')
      else setStatus('Obese')
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="max-w-2xl mx-auto"
    >
      <div className="flex items-center mb-8 space-x-4 border-b border-white/10 pb-4">
        <Scale className="w-8 h-8 text-primary" />
        <h2 className="text-3xl font-display font-bold italic text-white">Body Mass Index</h2>
      </div>

      <form onSubmit={calculateBMI} className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Input
            label="Height (cm)"
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            placeholder="180"
            required
          />
          <Input
            label="Weight (kg)"
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="75"
            required
          />
        </div>

        <Button type="submit" variant="primary" size="lg" className="w-full">
            Calculate Score
        </Button>
      </form>

      {bmi && (
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mt-12 p-8 bg-white/5 border border-primary/20 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-primary/5 animate-pulse"></div>
          <div className="relative z-10">
            <span className="text-gray-400 text-xs uppercase tracking-[0.3em] block mb-2">Analysis Complete</span>
            <div className="text-7xl font-display font-bold text-white mb-4 italic">{bmi}</div>
            <div className={`inline-block px-6 py-2 text-xs uppercase tracking-[0.2em] font-bold border transform skew-x-[-10deg] ${
              status === 'Optimal' 
                ? 'border-secondary text-secondary bg-secondary/10' 
                : 'border-accent text-accent bg-accent/10'
            }`}>
              <span className="block skew-x-[10deg]">{status}</span>
            </div>
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

const MacroCalculator = () => {
  const [formData, setFormData] = useState({
    gender: 'male',
    age: '',
    height: '',
    weight: '',
    activity: '1.2'
  })
  const [result, setResult] = useState(null)

  const calculateMacros = (e) => {
    e.preventDefault()
    // Mifflin-St Jeor Equation
    let bmr = (10 * formData.weight) + (6.25 * formData.height) - (5 * formData.age)
    bmr += formData.gender === 'male' ? 5 : -161
    
    const tdee = Math.round(bmr * parseFloat(formData.activity))
    
    setResult({
      tdee,
      protein: Math.round(formData.weight * 2.2), // 1g per lb (approx 2.2g per kg)
      fats: Math.round((tdee * 0.25) / 9),
      carbs: Math.round((tdee - ((formData.weight * 2.2 * 4) + ((tdee * 0.25)))) / 4)
    })
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="max-w-3xl mx-auto"
    >
      <div className="flex items-center mb-8 space-x-4 border-b border-white/10 pb-4">
        <Activity className="w-8 h-8 text-energy" />
        <h2 className="text-3xl font-display font-bold italic text-white">Metabolic Profile</h2>
      </div>

      <form onSubmit={calculateMacros} className="space-y-8">
        <div className="flex space-x-4 mb-6">
          {['male', 'female'].map(g => (
            <label key={g} className="flex-1 cursor-pointer group relative">
              <input 
                type="radio" 
                name="gender" 
                value={g}
                checked={formData.gender === g}
                onChange={(e) => setFormData({...formData, gender: e.target.value})}
                className="hidden"
              />
              <div className={`py-4 border text-center transition-all uppercase text-xs tracking-widest font-bold ${
                  formData.gender === g 
                    ? 'border-energy bg-energy/10 text-white shadow-[0_0_15px_rgba(255,107,0,0.2)]' 
                    : 'border-white/10 text-gray-500 hover:border-white/30'
                }`}>
                {g}
              </div>
            </label>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Input
            label="Age"
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({...formData, age: e.target.value})}
            required
          />
          <Input
            label="Height (cm)"
            type="number"
            value={formData.height}
            onChange={(e) => setFormData({...formData, height: e.target.value})}
            required
          />
          <Input
            label="Weight (kg)"
            type="number"
            value={formData.weight}
            onChange={(e) => setFormData({...formData, weight: e.target.value})}
            required
          />
        </div>

        <div className="group">
          <label className="block text-[10px] font-bold text-energy uppercase tracking-widest mb-3">Activity Level</label>
          <select 
            value={formData.activity}
            onChange={(e) => setFormData({...formData, activity: e.target.value})}
            className="input-field bg-black/50 border-l-2 border-white/10 focus:border-energy appearance-none cursor-pointer"
          >
            <option value="1.2">Sedentary (Base)</option>
            <option value="1.375">Light Activity (1-2 days/week)</option>
            <option value="1.55">Moderate Training (3-5 days/week)</option>
            <option value="1.725">High Performance (6-7 days/week)</option>
            <option value="1.9">Elite / Athlete (2x per day)</option>
          </select>
        </div>

        <Button type="submit" variant="energy" size="lg" className="w-full">
            Generate Fueling Data
        </Button>
      </form>

      {result && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6"
        >
          <div className="p-6 bg-energy/10 border border-energy/30 text-center flex flex-col justify-center">
            <Zap className="w-6 h-6 text-energy mx-auto mb-2" />
            <span className="block text-[9px] uppercase tracking-widest text-energy mb-1">Total Calories</span>
            <span className="block text-3xl font-display font-bold text-white italic">{result.tdee}</span>
          </div>
          <div className="p-4 bg-white/5 border-l-2 border-white/20 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Protein</span>
            <span className="block text-2xl font-bold text-white">{result.protein}g</span>
          </div>
          <div className="p-4 bg-white/5 border-l-2 border-white/20 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Fats</span>
            <span className="block text-2xl font-bold text-white">{result.fats}g</span>
          </div>
          <div className="p-4 bg-white/5 border-l-2 border-white/20 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Carbs</span>
            <span className="block text-2xl font-bold text-white">{result.carbs}g</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

export default Tools
