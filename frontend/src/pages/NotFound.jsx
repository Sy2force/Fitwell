import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, AlertTriangle } from 'lucide-react'

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background">
      {/* Background Elements */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/5 rounded-full blur-[120px] pointer-events-none animate-pulse"></div>
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:50px_50px]" />
      
      <div className="relative z-10 text-center px-6">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="mb-8 flex justify-center"
        >
          <div className="p-6 border-2 border-accent bg-black/50 transform skew-x-[-10deg]">
            <div className="skew-x-[10deg]">
                <AlertTriangle className="w-16 h-16 text-accent" />
            </div>
          </div>
        </motion.div>
        
        <h1 className="text-8xl md:text-[10rem] font-display font-bold text-white mb-2 tracking-tighter opacity-90 leading-none italic">
          404
        </h1>
        <h2 className="text-2xl md:text-3xl font-display text-primary uppercase tracking-widest mb-8 font-bold italic">
          System Error: <span className="text-white">Path Unknown</span>
        </h2>
        
        <p className="text-gray-400 mb-12 font-mono max-w-md mx-auto leading-relaxed border-l-2 border-white/10 pl-4 text-sm">
          &gt; NAVIGATION FAILURE DETECTED <br/>
          &gt; THE REQUESTED COORDINATES DO NOT EXIST IN THE MAINFRAME. <br/>
          &gt; RETURN TO BASE IMMEDIATELY.
        </p>
        
        <Link 
          to="/"
          className="inline-block bg-primary text-black font-display font-bold text-lg uppercase tracking-widest py-4 px-10 hover:bg-white hover:shadow-[0_0_20px_rgba(0,240,255,0.5)] transition-all skew-x-[-10deg] group"
        >
          <div className="flex items-center skew-x-[10deg]">
            <Home className="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" />
            <span>Return to Base</span>
          </div>
        </Link>
      </div>
    </div>
  )
}

export default NotFound
