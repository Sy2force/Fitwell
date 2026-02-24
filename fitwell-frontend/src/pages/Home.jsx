import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, Loader2, Sparkles, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import axios from '../api/axios'
import ArticleCard from '../components/ArticleCard'

const Home = () => {
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchArticles()
  }, [])

  const fetchArticles = async (query = '') => {
    setIsLoading(true)
    try {
      const endpoint = query 
        ? `articles/search/?q=${query}` 
        : 'articles/'
      const response = await axios.get(endpoint)
      setArticles(response.data.results || response.data)
    } catch (err) {
      setError(`Failed to fetch articles: ${err.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchArticles(searchTerm)
  }

  const handleNewsletterSubmit = (e) => {
    e.preventDefault()
    toast.success('Welcome to the Elite. Check your inbox.')
    e.target.reset()
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[85vh] flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-background/30 via-background/80 to-background z-10" />
          <img 
            src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop" 
            alt="Luxury Fitness" 
            className="w-full h-full object-cover opacity-40"
          />
        </div>
        
        <div className="relative z-20 text-center px-4 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <div className="flex items-center justify-center space-x-4 mb-8">
              <div className="h-[1px] w-12 bg-primary/50"></div>
              <span className="text-primary tracking-[0.4em] uppercase text-xs font-bold">
                Elite Wellness
              </span>
              <div className="h-[1px] w-12 bg-primary/50"></div>
            </div>
            
            <h1 className="text-6xl md:text-9xl font-serif font-bold mb-8 leading-tight tracking-tight text-white mix-blend-overlay opacity-90">
              Redefining <br />
              <span className="text-gradient italic font-light">Excellence</span>
            </h1>
            
            <p className="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto mb-12 font-light leading-relaxed tracking-wide">
              Experience the pinnacle of health and performance. 
              Curated insights for the modern athlete.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-6 mb-16">
              <button 
                onClick={() => document.getElementById('latest-stories').scrollIntoView({ behavior: 'smooth' })}
                className="glass-button px-12 py-5 text-sm tracking-[0.3em] uppercase group flex items-center"
              >
                Explore Collection
                <ArrowRight className="ml-3 w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
              <Link 
                to="/register"
                className="px-12 py-5 text-sm tracking-[0.3em] uppercase border border-white/10 hover:border-primary/50 transition-all font-bold text-white/80 hover:text-primary"
              >
                Join the Elite
              </Link>
            </div>

            <form onSubmit={handleSearch} className="max-w-xl mx-auto relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 via-primary/50 to-primary/20 rounded-none blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search for excellence..."
                  className="w-full bg-surface/80 backdrop-blur-md border border-white/10 rounded-none px-6 py-5 pl-14 text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 transition-all font-serif"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search className="absolute left-5 top-5 text-primary w-5 h-5" />
                <button type="submit" className="absolute right-3 top-3 p-2 hover:bg-white/5 transition-colors">
                  <ArrowRight className="w-5 h-5 text-gray-400" />
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>

      {/* Philosophy Section */}
      <div className="py-32 bg-surface relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-primary/20 to-transparent"></div>
        <div className="max-w-4xl mx-auto px-6 text-center">
          <Sparkles className="w-6 h-6 text-primary mx-auto mb-6" />
          <h2 className="text-4xl md:text-5xl font-serif font-bold mb-8">The FitWell Philosophy</h2>
          <p className="text-xl md:text-2xl text-gray-400 font-light leading-relaxed">
            &quot;True luxury is not just about aesthetics; it is about the optimization of the human machine. 
            We believe in a holistic approach where science meets spirit, and discipline meets design.&quot;
          </p>
          <div className="mt-12 flex justify-center">
            <div className="w-24 h-1 bg-primary"></div>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div id="latest-stories" className="page-container py-32 relative z-30">
        <div className="flex items-end justify-between mb-16 border-b border-white/10 pb-6">
          <div>
            <span className="text-primary text-xs tracking-widest uppercase block mb-3">Latest Stories</span>
            <h2 className="text-4xl font-serif">Curated Articles</h2>
          </div>
          <div className="hidden md:block text-xs text-gray-500 tracking-widest uppercase font-mono">
            Volume 01 — 2026
          </div>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-32">
            <Loader2 className="w-12 h-12 text-primary animate-spin" />
          </div>
        ) : error ? (
          <div className="text-center text-red-400 py-20 border border-red-500/20 bg-red-500/5 font-serif">{error}</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {articles.map((article, index) => (
              <ArticleCard key={article.id} article={article} index={index} />
            ))}
          </div>
        )}

        {!isLoading && articles.length === 0 && (
          <div className="text-center text-gray-400 py-32 font-serif italic text-xl">
            No articles found matching your criteria.
          </div>
        )}
      </div>

      {/* Newsletter Section */}
      <div className="py-32 border-t border-white/5 bg-gradient-to-b from-background to-black">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-serif font-bold mb-4">Join the Elite</h2>
          <p className="text-gray-400 mb-10 font-light">Receive curated wellness insights directly to your inbox.</p>
          <form onSubmit={handleNewsletterSubmit} className="flex flex-col md:flex-row gap-4">
            <input 
              type="email" 
              placeholder="Your email address" 
              className="flex-1 bg-white/5 border border-white/10 px-6 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 font-serif"
            />
            <button className="glass-button px-10 py-4">Subscribe</button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Home
