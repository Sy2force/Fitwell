import { Github, Twitter, Linkedin, Dumbbell } from 'lucide-react'
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-black/50 backdrop-blur-md border-t border-white/5 mt-32 relative z-10">
      <div className="max-w-[1400px] mx-auto py-16 px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <Dumbbell className="w-6 h-6 text-primary" />
              <span className="text-2xl font-serif font-bold text-white">
                Fit<span className="text-primary italic">Well</span>
              </span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed max-w-md font-light">
              Elevating the standard of personal wellness through curated knowledge and elite community. 
              Join the movement towards excellence.
            </p>
          </div>
          
          <div>
            <h4 className="text-primary text-xs tracking-[0.2em] uppercase font-bold mb-6">Explore</h4>
            <ul className="space-y-4 text-sm text-gray-400 font-light">
              <li><Link to="/" className="hover:text-white transition-colors">Latest Stories</Link></li>
              <li><Link to="/category/workouts" className="hover:text-white transition-colors">Elite Training</Link></li>
              <li><Link to="/category/nutrition" className="hover:text-white transition-colors">Nutrition Guide</Link></li>
              <li><Link to="/category/mindset" className="hover:text-white transition-colors">Mindset</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-primary text-xs tracking-[0.2em] uppercase font-bold mb-6">Connect</h4>
            <div className="flex space-x-4">
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-primary hover:text-primary transition-all rounded-none">
                <Github className="w-4 h-4" />
              </a>
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-primary hover:text-primary transition-all rounded-none">
                <Twitter className="w-4 h-4" />
              </a>
              <a href="#" className="w-10 h-10 border border-white/10 flex items-center justify-center text-gray-400 hover:border-primary hover:text-primary transition-all rounded-none">
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
        
        <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-xs text-gray-500 font-light tracking-wider">
          <p>
            © {new Date().getFullYear()} FITWELL INC. ALL RIGHTS RESERVED.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0 uppercase">
            <a href="#" className="hover:text-gray-300 transition-colors">Privacy</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Terms</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Sitemap</a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
