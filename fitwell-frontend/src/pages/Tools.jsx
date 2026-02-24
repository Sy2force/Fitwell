import { useState } from 'react'
import { motion } from 'framer-motion'
import { Calculator, Activity, Scale } from 'lucide-react'

const Tools = () => {
  const [activeTab, setActiveTab] = useState('bmi')
  
  return (
    <div className="page-container py-20">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-block p-4 border border-primary/30 bg-primary/10 rounded-full mb-6"
          >
            <Calculator className="w-8 h-8 text-primary" />
          </motion.div>
          <h1 className="text-5xl font-serif font-bold text-white mb-4">Elite Tools</h1>
          <p className="text-gray-400 text-lg font-light tracking-wide">
            Quantify your progress with our precision calculators.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-12 border-b border-white/10">
          <button
            onClick={() => setActiveTab('bmi')}
            className={`px-8 py-4 text-sm uppercase tracking-[0.2em] font-bold border-b-2 transition-all ${
              activeTab === 'bmi' 
                ? 'border-primary text-primary' 
                : 'border-transparent text-gray-500 hover:text-white'
            }`}
          >
            BMI Index
          </button>
          <button
            onClick={() => setActiveTab('calories')}
            className={`px-8 py-4 text-sm uppercase tracking-[0.2em] font-bold border-b-2 transition-all ${
              activeTab === 'calories' 
                ? 'border-primary text-primary' 
                : 'border-transparent text-gray-500 hover:text-white'
            }`}
          >
            TDEE / Macros
          </button>
        </div>

        <div className="glass-card p-8 md:p-12 border-t border-primary/20 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px] -mr-20 -mt-20 pointer-events-none"></div>
          
          {activeTab === 'bmi' ? <BMICalculator /> : <MacroCalculator />}
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
      else if (val < 25) setStatus('Normal')
      else if (val < 30) setStatus('Overweight')
      else setStatus('Obese')
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-xl mx-auto"
    >
      <div className="flex items-center mb-8 space-x-4">
        <Scale className="w-6 h-6 text-primary" />
        <h2 className="text-2xl font-serif font-bold">Body Mass Index</h2>
      </div>

      <form onSubmit={calculateBMI} className="space-y-6">
        <div className="grid grid-cols-2 gap-6">
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Height (cm)</label>
            <input 
              type="number" 
              value={height}
              onChange={(e) => setHeight(e.target.value)}
              className="input-field"
              placeholder="180"
              required
            />
          </div>
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Weight (kg)</label>
            <input 
              type="number" 
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              className="input-field"
              placeholder="75"
              required
            />
          </div>
        </div>

        <button type="submit" className="glass-button w-full">Calculate</button>
      </form>

      {bmi && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 p-6 bg-white/5 border border-primary/30 text-center relative overflow-hidden"
        >
          <div className="relative z-10">
            <span className="text-gray-400 text-xs uppercase tracking-widest block mb-2">Your BMI Score</span>
            <div className="text-5xl font-serif font-bold text-white mb-2">{bmi}</div>
            <div className={`inline-block px-4 py-1 text-[10px] uppercase tracking-[0.2em] font-bold border ${
              status === 'Normal' ? 'border-green-500 text-green-400' : 'border-yellow-500 text-yellow-400'
            }`}>
              {status}
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
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-2xl mx-auto"
    >
      <div className="flex items-center mb-8 space-x-4">
        <Activity className="w-6 h-6 text-primary" />
        <h2 className="text-2xl font-serif font-bold">TDEE & Macros</h2>
      </div>

      <form onSubmit={calculateMacros} className="space-y-6">
        <div className="flex space-x-6 mb-6">
          {['male', 'female'].map(g => (
            <label key={g} className="flex items-center cursor-pointer group">
              <input 
                type="radio" 
                name="gender" 
                value={g}
                checked={formData.gender === g}
                onChange={(e) => setFormData({...formData, gender: e.target.value})}
                className="hidden"
              />
              <div className={`w-4 h-4 border border-primary/50 mr-3 flex items-center justify-center ${formData.gender === g ? 'bg-primary/20' : ''}`}>
                {formData.gender === g && <div className="w-2 h-2 bg-primary"></div>}
              </div>
              <span className="text-xs uppercase tracking-widest text-gray-400 group-hover:text-white">{g}</span>
            </label>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-6">
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Age</label>
            <input 
              type="number" 
              value={formData.age}
              onChange={(e) => setFormData({...formData, age: e.target.value})}
              className="input-field"
              required
            />
          </div>
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Height (cm)</label>
            <input 
              type="number" 
              value={formData.height}
              onChange={(e) => setFormData({...formData, height: e.target.value})}
              className="input-field"
              required
            />
          </div>
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Weight (kg)</label>
            <input 
              type="number" 
              value={formData.weight}
              onChange={(e) => setFormData({...formData, weight: e.target.value})}
              className="input-field"
              required
            />
          </div>
        </div>

        <div className="group">
          <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Activity Level</label>
          <select 
            value={formData.activity}
            onChange={(e) => setFormData({...formData, activity: e.target.value})}
            className="input-field appearance-none cursor-pointer"
          >
            <option value="1.2">Sedentary (Office job)</option>
            <option value="1.375">Light Exercise (1-2 days/week)</option>
            <option value="1.55">Moderate Exercise (3-5 days/week)</option>
            <option value="1.725">Heavy Exercise (6-7 days/week)</option>
            <option value="1.9">Athlete (2x per day)</option>
          </select>
        </div>

        <button type="submit" className="glass-button w-full">Calculate Protocol</button>
      </form>

      {result && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          <div className="p-4 bg-primary/10 border border-primary/30 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-primary mb-1">Calories</span>
            <span className="block text-2xl font-bold text-white">{result.tdee}</span>
          </div>
          <div className="p-4 bg-white/5 border border-white/10 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Protein</span>
            <span className="block text-xl font-bold text-white">{result.protein}g</span>
          </div>
          <div className="p-4 bg-white/5 border border-white/10 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Fats</span>
            <span className="block text-xl font-bold text-white">{result.fats}g</span>
          </div>
          <div className="p-4 bg-white/5 border border-white/10 text-center">
            <span className="block text-[9px] uppercase tracking-widest text-gray-400 mb-1">Carbs</span>
            <span className="block text-xl font-bold text-white">{result.carbs}g</span>
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

export default Tools
