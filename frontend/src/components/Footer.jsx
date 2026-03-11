import { Github, Twitter, Linkedin, Dumbbell } from 'lucide-react'
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-surface border-t-2 border-primary/20 mt-32 relative z-10">
      <div className="max-w-[1400px] mx-auto py-16 px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-6 group">
              <div className="w-10 h-10 border border-primary flex items-center justify-center bg-black/50 skew-x-[-10deg]">
                <Dumbbell className="w-5 h-5 text-primary skew-x-[10deg]" />
              </div>
              <span className="text-3xl font-display font-bold text-white italic tracking-tighter">
                Fit<span className="text-primary">Well</span>
              </span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed max-w-md font-sans border-l-2 border-accent/50 pl-4">
              The premier operating system for human performance. <br/>
              Optimize. Adapt. Dominate.
            </p>
          </div>
          
          <div>
            <h4 className="text-secondary text-xs tracking-widest uppercase font-bold mb-6 font-display italic">System Map</h4>
            <ul className="space-y-4 text-xs text-gray-400 font-mono uppercase tracking-wider">
              <li><Link to="/" className="hover:text-white hover:text-primary transition-colors flex items-center"><span className="w-1 h-1 bg-primary mr-2 opacity-0 group-hover:opacity-100"></span>Latest Intel</Link></li>
              <li><Link to="/category/strength" className="hover:text-white hover:text-primary transition-colors">Elite Strength</Link></li>
              <li><Link to="/category/nutrition" className="hover:text-white hover:text-primary transition-colors">Fueling</Link></li>
              <li><Link to="/category/bio-hacking" className="hover:text-white hover:text-primary transition-colors">Bio-Hacking</Link></li>
              <li><Link to="/category/recovery" className="hover:text-white hover:text-primary transition-colors">Recovery Protocols</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-secondary text-xs tracking-widest uppercase font-bold mb-6 font-display italic">Network</h4>
            <div className="flex space-x-4">
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-accent hover:text-accent transition-all skew-x-[-10deg] bg-black/30">
                <Github className="w-4 h-4 skew-x-[10deg]" />
              </a>
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-accent hover:text-accent transition-all skew-x-[-10deg] bg-black/30">
                <Twitter className="w-4 h-4 skew-x-[10deg]" />
              </a>
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-accent hover:text-accent transition-all skew-x-[-10deg] bg-black/30">
                <Linkedin className="w-4 h-4 skew-x-[10deg]" />
              </a>
            </div>
          </div>
        </div>
        
        <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-[10px] text-gray-600 font-mono uppercase tracking-widest">
          <p>
            © {new Date().getFullYear()} FITWELL SYSTEMS INC. ALL RIGHTS RESERVED.
          </p>
          <div className="flex space-x-8 mt-4 md:mt-0">
            <a href="#" className="hover:text-white transition-colors">Privacy Protocol</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Engagement</a>
            <a href="#" className="hover:text-white transition-colors">System Status</a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
