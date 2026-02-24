import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, Dumbbell, Apple, ChevronRight, Check, Loader2, Target } from 'lucide-react'
import axios from '../api/axios'
import toast from 'react-hot-toast'

const Planner = () => {
  const [step, setStep] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [plan, setPlan] = useState(null)
  const [formData, setFormData] = useState({
    age: '',
    gender: 'male',
    height: '',
    weight: '',
    goal: 'weight_loss',
    activity_level: 'moderate',
    dietary_preferences: ''
  })

  // Check if plan already exists
  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const response = await axios.get('plans/')
        if (response.data && response.data.length > 0) {
          setPlan(response.data[0])
        }
      } catch (error) {
        // No plan found, that's okay
      }
    }
    fetchPlan()
  }, [])

  const handleNext = () => {
    setStep(step + 1)
  }

  const handleBack = () => {
    setStep(step - 1)
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    try {
      const response = await axios.post('plans/', formData)
      setPlan(response.data)
      toast.success('Protocol generated successfully')
    } catch (error) {
      toast.error('Failed to generate protocol')
    } finally {
      setIsLoading(false)
    }
  }

  const steps = [
    { id: 1, title: 'Biometrics', icon: Activity },
    { id: 2, title: 'Objectives', icon: Target },
    { id: 3, title: 'Execution', icon: Check }
  ]

  if (plan) {
    return <PlanView plan={plan} onReset={() => setPlan(null)} />
  }

  return (
    <div className="page-container py-20 min-h-screen">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-serif font-bold text-white mb-4">
            Elite <span className="text-primary italic">Planner</span>
          </h1>
          <p className="text-gray-400 font-light tracking-wide max-w-xl mx-auto">
            Design your roadmap to physical excellence. Our algorithm crafts a bespoke protocol based on your unique physiology.
          </p>
        </div>

        {/* Progress Bar */}
        <div className="flex justify-between items-center mb-16 relative">
          <div className="absolute top-1/2 left-0 w-full h-[1px] bg-white/10 -z-10"></div>
          {steps.map((s) => {
            const Icon = s.icon
            const isActive = step >= s.id
            const isCurrent = step === s.id
            return (
              <div key={s.id} className="flex flex-col items-center bg-background px-4">
                <div className={`w-12 h-12 rounded-full border-2 flex items-center justify-center transition-all duration-500 ${
                  isActive ? 'border-primary bg-primary/10 text-primary' : 'border-white/10 text-gray-600'
                } ${isCurrent ? 'shadow-[0_0_20px_rgba(212,175,55,0.3)] scale-110' : ''}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className={`mt-4 text-[10px] uppercase tracking-[0.2em] font-bold ${
                  isActive ? 'text-white' : 'text-gray-600'
                }`}>
                  {s.title}
                </span>
              </div>
            )
          })}
        </div>

        {/* Form Container */}
        <div className="glass-card p-8 md:p-12 border-t border-primary/20 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px] -mr-20 -mt-20 pointer-events-none"></div>
          
          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <h2 className="text-2xl font-serif font-bold text-white mb-6">Biometric Data</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Age</label>
                    <input 
                      type="number" 
                      value={formData.age}
                      onChange={(e) => setFormData({...formData, age: e.target.value})}
                      className="input-field"
                      placeholder="e.g. 28"
                    />
                  </div>
                  
                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Biological Sex</label>
                    <div className="flex space-x-4">
                      {['male', 'female'].map(g => (
                        <button
                          key={g}
                          onClick={() => setFormData({...formData, gender: g})}
                          className={`flex-1 py-4 border transition-all uppercase text-xs tracking-widest ${
                            formData.gender === g 
                              ? 'border-primary bg-primary/10 text-white' 
                              : 'border-white/10 text-gray-500 hover:border-white/30'
                          }`}
                        >
                          {g}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Height (cm)</label>
                    <input 
                      type="number" 
                      value={formData.height}
                      onChange={(e) => setFormData({...formData, height: e.target.value})}
                      className="input-field"
                      placeholder="e.g. 180"
                    />
                  </div>

                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">Weight (kg)</label>
                    <input 
                      type="number" 
                      value={formData.weight}
                      onChange={(e) => setFormData({...formData, weight: e.target.value})}
                      className="input-field"
                      placeholder="e.g. 75"
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-8">
                  <button 
                    onClick={handleNext}
                    disabled={!formData.age || !formData.height || !formData.weight}
                    className="glass-button flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next Phase <ChevronRight className="ml-2 w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <h2 className="text-2xl font-serif font-bold text-white mb-6">Mission Parameters</h2>
                
                <div className="space-y-8">
                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-4">Primary Objective</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        { id: 'weight_loss', label: 'Weight Loss', desc: 'Shed excess mass, reveal definition.' },
                        { id: 'muscle_gain', label: 'Hypertrophy', desc: 'Build lean contractile tissue.' },
                        { id: 'endurance', label: 'Endurance', desc: 'Optimize cardiovascular output.' },
                        { id: 'maintenance', label: 'Maintenance', desc: 'Sustain peak performance.' }
                      ].map((goal) => (
                        <button
                          key={goal.id}
                          onClick={() => setFormData({...formData, goal: goal.id})}
                          className={`p-6 border text-left transition-all ${
                            formData.goal === goal.id 
                              ? 'border-primary bg-primary/10' 
                              : 'border-white/10 hover:border-white/30 bg-white/5'
                          }`}
                        >
                          <span className={`block text-xs font-bold uppercase tracking-widest mb-2 ${
                            formData.goal === goal.id ? 'text-primary' : 'text-white'
                          }`}>
                            {goal.label}
                          </span>
                          <span className="text-xs text-gray-400 font-light">{goal.desc}</span>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="group">
                    <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-4">Current Activity Level</label>
                    <select
                      value={formData.activity_level}
                      onChange={(e) => setFormData({...formData, activity_level: e.target.value})}
                      className="input-field appearance-none cursor-pointer"
                    >
                      <option value="sedentary">Sedentary (Office Role)</option>
                      <option value="moderate">Moderate (Training 3-4x/week)</option>
                      <option value="active">Active (Training 5-6x/week)</option>
                      <option value="elite">Elite (Double sessions/Physical job)</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-between pt-8">
                  <button 
                    onClick={handleBack}
                    className="text-gray-500 hover:text-white text-xs uppercase tracking-widest font-bold py-3 px-6"
                  >
                    Back
                  </button>
                  <button 
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="glass-button flex items-center"
                  >
                    {isLoading ? <Loader2 className="animate-spin w-4 h-4" /> : (
                      <>
                        Generate Protocol <Check className="ml-2 w-4 h-4" />
                      </>
                    )}
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}

const PlanView = ({ plan, onReset }) => {
  return (
    <div className="page-container py-20">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16">
          <span className="text-primary text-xs uppercase tracking-[0.3em] font-bold block mb-4">Protocol Generated</span>
          <h1 className="text-4xl md:text-6xl font-serif font-bold text-white mb-6">
            Your Elite <span className="italic text-gray-400">Blueprint</span>
          </h1>
          <button 
            onClick={onReset}
            className="text-xs text-gray-500 hover:text-red-400 uppercase tracking-widest border-b border-transparent hover:border-red-400 transition-all pb-1"
          >
            Reset & Recalculate
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Workout Plan */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass-card p-10 border-t-2 border-t-blue-500/50"
          >
            <div className="flex items-center space-x-4 mb-8">
              <div className="p-3 bg-blue-500/10 rounded-full border border-blue-500/30">
                <Dumbbell className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h3 className="text-2xl font-serif font-bold">Training Protocol</h3>
                <span className="text-xs text-gray-400 uppercase tracking-widest">{plan.workout_plan.focus}</span>
              </div>
            </div>

            <div className="space-y-8">
              <div>
                <span className="block text-[10px] uppercase tracking-[0.2em] text-blue-400 font-bold mb-3">Schedule</span>
                <p className="text-xl text-white font-light">{plan.workout_plan.schedule}</p>
              </div>

              <div>
                <span className="block text-[10px] uppercase tracking-[0.2em] text-blue-400 font-bold mb-3">Core Exercises</span>
                <ul className="space-y-3">
                  {plan.workout_plan.exercises.map((ex, i) => (
                    <li key={i} className="flex items-center text-gray-300 font-light border-b border-white/5 pb-2">
                      <span className="w-6 h-6 flex items-center justify-center bg-white/5 rounded-full text-xs mr-3 text-blue-400 font-bold">{i + 1}</span>
                      {ex}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </motion.div>

          {/* Nutrition Plan */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-10 border-t-2 border-t-green-500/50"
          >
            <div className="flex items-center space-x-4 mb-8">
              <div className="p-3 bg-green-500/10 rounded-full border border-green-500/30">
                <Apple className="w-6 h-6 text-green-400" />
              </div>
              <div>
                <h3 className="text-2xl font-serif font-bold">Nutrition Fueling</h3>
                <span className="text-xs text-gray-400 uppercase tracking-widest">Daily Macros</span>
              </div>
            </div>

            <div className="flex flex-col items-center justify-center py-6 mb-8 bg-green-500/5 border border-green-500/10">
              <span className="text-5xl font-serif font-bold text-white mb-2">{plan.nutrition_plan.calories}</span>
              <span className="text-xs text-green-400 uppercase tracking-[0.3em] font-bold">Daily Calories</span>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="text-center p-4 bg-white/5">
                <span className="block text-xl font-bold text-white mb-1">{plan.nutrition_plan.macros.protein}</span>
                <span className="text-[9px] uppercase tracking-widest text-gray-500">Protein</span>
              </div>
              <div className="text-center p-4 bg-white/5">
                <span className="block text-xl font-bold text-white mb-1">{plan.nutrition_plan.macros.carbs}</span>
                <span className="text-[9px] uppercase tracking-widest text-gray-500">Carbs</span>
              </div>
              <div className="text-center p-4 bg-white/5">
                <span className="block text-xl font-bold text-white mb-1">{plan.nutrition_plan.macros.fats}</span>
                <span className="text-[9px] uppercase tracking-widest text-gray-500">Fats</span>
              </div>
            </div>

            <div className="space-y-4">
               <span className="block text-[10px] uppercase tracking-[0.2em] text-green-400 font-bold mb-3">Sample Day</span>
               {Object.entries(plan.nutrition_plan.meals).map(([meal, food]) => (
                 <div key={meal} className="flex justify-between border-b border-white/5 pb-2">
                    <span className="text-xs text-gray-400 uppercase tracking-wider w-24">{meal}</span>
                    <span className="text-sm text-white font-light text-right flex-1">{food}</span>
                 </div>
               ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Planner
