import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion, useScroll, useTransform } from 'framer-motion'
import { Loader2, Zap, ArrowRight, Lock, Activity, TrendingUp, Users } from 'lucide-react'
import axios from '../api/axios'
import ArticleCard from '../components/ArticleCard'
import Button from '../components/ui/Button'

const Home = () => {
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const { scrollY } = useScroll()
  const y1 = useTransform(scrollY, [0, 500], [0, 200])

  useEffect(() => {
    // Fetch a few teaser articles
    const fetchTeasers = async () => {
      try {
        const response = await axios.get('blog/articles/')
        setArticles(response.data.results?.slice(0, 3) || response.data?.slice(0, 3) || [])
      } catch (err) {
        // Silent fail for teasers
      } finally {
        setIsLoading(false)
      }
    }
    fetchTeasers()
  }, [])

  return (
    <div className="min-h-screen bg-background overflow-hidden selection:bg-primary selection:text-white">
      {/* Hero Section */}
      <div className="relative h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/80 to-background z-10" />
          <motion.div style={{ y: y1 }} className="absolute inset-0">
            <img 
              src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop" 
              alt="High Performance" 
              className="w-full h-full object-cover opacity-50 grayscale hover:grayscale-0 transition-all duration-700"
            />
          </motion.div>
        </div>
        
        <div className="relative z-20 text-center px-4 max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "circOut" }}
          >
            <h1 className="text-7xl md:text-[10rem] font-display font-bold mb-6 leading-[0.85] tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-white via-gray-200 to-gray-600 italic">
              UNLOCK <br />
              <span className="text-transparent bg-clip-text bg-neon-gradient">POTENTIAL</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto mb-12 font-sans font-light tracking-wide border-l-4 border-primary pl-6 text-left">
              The premier ecosystem for biological optimization. <br/>
              <span className="text-primary font-bold">Train. Analyze. Evolve.</span>
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-8">
              <Link to="/register">
                <Button variant="energy" size="lg" className="w-full md:w-auto">
                  Start Transformation <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <Link to="/login">
                <Button variant="outline" size="lg" className="w-full md:w-auto">
                  Member Login
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Floating Elements */}
        <div className="absolute bottom-10 left-10 hidden md:block">
            <div className="flex items-center space-x-4 text-gray-500 font-mono text-xs">
                <span className="flex items-center"><div className="w-2 h-2 bg-primary rounded-full animate-pulse mr-2"></div> SYSTEM ONLINE</span>
                <span>V 2.0.4</span>
            </div>
        </div>
      </div>

      {/* Features Marquee/Carousel */}
      <div className="py-20 border-y border-white/10 bg-black relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.02] bg-[length:50px_50px]" />
        <div className="max-w-7xl mx-auto px-6 relative z-10">
            <div className="text-center mb-16">
                <h2 className="text-3xl md:text-5xl font-display font-bold text-white mb-4 italic">The <span className="text-energy">Ecosystem</span></h2>
                <div className="w-24 h-1 bg-energy mx-auto"></div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Feature 1 */}
                <div className="glass-card p-8 group">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-6 group-hover:bg-primary group-hover:text-black transition-colors text-primary">
                        <Activity className="w-8 h-8" />
                    </div>
                    <h3 className="text-xl font-display font-bold text-white mb-3">Smart Planner</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">
                        AI-driven workout and nutrition protocols tailored to your biometrics and goals.
                    </p>
                </div>

                {/* Feature 2 */}
                <div className="glass-card p-8 group border-transparent hover:border-energy">
                    <div className="w-16 h-16 bg-energy/10 rounded-full flex items-center justify-center mb-6 group-hover:bg-energy group-hover:text-black transition-colors text-energy">
                        <TrendingUp className="w-8 h-8" />
                    </div>
                    <h3 className="text-xl font-display font-bold text-white mb-3">Gamified Growth</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">
                        Track your XP, Health Score, and Level up as you adhere to your fitness regime.
                    </p>
                </div>

                {/* Feature 3 */}
                <div className="glass-card p-8 group border-transparent hover:border-health">
                    <div className="w-16 h-16 bg-health/10 rounded-full flex items-center justify-center mb-6 group-hover:bg-health group-hover:text-white transition-colors text-health">
                        <Users className="w-8 h-8" />
                    </div>
                    <h3 className="text-xl font-display font-bold text-white mb-3">Elite Community</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">
                        Access curated content and connect with high-performers worldwide.
                    </p>
                </div>
            </div>
        </div>
      </div>

      {/* Restricted Content Teaser */}
      <div className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6">
            <div className="flex justify-between items-end mb-12">
                <h2 className="text-4xl font-display font-bold text-white italic">Latest <span className="text-primary">Intel</span></h2>
                <Link to="/register" className="hidden md:flex items-center text-sm font-bold text-energy uppercase tracking-widest hover:text-white transition-colors">
                    Unlock Full Access <Lock className="w-4 h-4 ml-2" />
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 opacity-50 hover:opacity-100 transition-opacity duration-500">
                {isLoading ? (
                    <div className="col-span-3 flex justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>
                ) : (
                    articles.map((article, idx) => (
                        <div key={idx} className="relative group cursor-not-allowed">
                            <div className="absolute inset-0 bg-black/60 z-10 flex flex-col items-center justify-center text-center p-4 backdrop-blur-[2px] group-hover:backdrop-blur-none transition-all">
                                <Lock className="w-8 h-8 text-white mb-2" />
                                <span className="text-xs font-bold uppercase tracking-widest text-white">Member Only Content</span>
                            </div>
                            <ArticleCard article={article} index={idx} />
                        </div>
                    ))
                )}
            </div>
            
            <div className="mt-16 text-center">
                <Link to="/register">
                    <Button variant="primary" size="lg">Join to Read</Button>
                </Link>
            </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-energy opacity-10"></div>
        <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
            <Zap className="w-12 h-12 text-energy mx-auto mb-6 animate-pulse" />
            <h2 className="text-5xl md:text-7xl font-display font-bold text-white mb-8 italic">Don&apos;t Spectate.<br/>Dominate.</h2>
            <p className="text-xl text-gray-300 mb-12 font-light">Your potential is infinite. Your time is not.</p>
            <form className="max-w-lg mx-auto flex gap-2">
                <input type="email" placeholder="ENTER YOUR EMAIL" className="input-field" />
                <Button variant="energy" size="md">
                    Get Access
                </Button>
            </form>
        </div>
      </div>
    </div>
  )
}

export default Home
