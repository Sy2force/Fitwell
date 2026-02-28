import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Loader2, Dumbbell, Apple, Brain, Activity, Zap } from 'lucide-react'
import axios from '../api/axios'
import ArticleCard from '../components/ArticleCard'

const CategoryPage = () => {
  const { slug } = useParams()
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  // Map slugs to display info
  const categoryConfig = {
    'strength': {
      title: 'Elite Strength',
      subtitle: 'Forging the body through iron and will.',
      icon: Dumbbell,
      image: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop'
    },
    'nutrition': {
      title: 'Precision Nutrition',
      subtitle: 'Fueling performance with scientific precision.',
      icon: Apple,
      image: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2000&auto=format&fit=crop'
    },
    'mindset': {
      title: 'Stoic Mindset',
      subtitle: 'The mind leads, the body follows.',
      icon: Brain,
      image: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=2000&auto=format&fit=crop'
    },
    'recovery': {
      title: 'Active Recovery',
      subtitle: 'Restoration protocols for longevity.',
      icon: Activity,
      image: 'https://images.unsplash.com/photo-1544367563-12123d8965cd?q=80&w=2000&auto=format&fit=crop'
    },
    'bio-hacking': {
      title: 'Bio-Hacking',
      subtitle: 'Optimizing human performance through science.',
      icon: Zap,
      image: 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?q=80&w=2000&auto=format&fit=crop'
    }
  }

  const currentConfig = categoryConfig[slug] || {
    title: slug ? slug.charAt(0).toUpperCase() + slug.slice(1) : 'Collection',
    subtitle: 'Curated insights for the elite.',
    icon: Activity,
    image: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2000&auto=format&fit=crop'
  }

  useEffect(() => {
    const fetchArticles = async () => {
      setIsLoading(true)
      try {
        let backendSlug = slug;
        if (slug === 'workouts') backendSlug = 'strength'; 
        
        const response = await axios.get(`blog/articles/?category__slug=${backendSlug}`)
        setArticles(response.data.results || response.data)
        
        if ((response.data.results || response.data).length === 0) {
             const allRes = await axios.get('blog/articles/')
             const all = allRes.data.results || allRes.data
             const filtered = all.filter(a => 
                a.category_slug === slug || 
                (a.category_name && a.category_name.toLowerCase() === slug) ||
                (slug === 'workouts' && a.category_name?.toLowerCase() === 'strength')
             )
             setArticles(filtered)
        }

      } catch (err) {
        console.error(err)
        setError('Failed to load category content.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchArticles()
  }, [slug])

  const Icon = currentConfig.icon

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative h-[60vh] flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/60 to-background z-10" />
          <img 
            src={currentConfig.image} 
            alt={currentConfig.title} 
            className="w-full h-full object-cover grayscale opacity-60"
          />
        </div>
        
        <div className="relative z-20 text-center px-4 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex p-4 border-2 border-primary bg-black/50 transform skew-x-[-10deg] mb-8">
                <Icon className="w-12 h-12 text-primary transform skew-x-[10deg]" />
            </div>
            <h1 className="text-6xl md:text-8xl font-display font-bold mb-6 text-white tracking-tighter italic">
              {currentConfig.title.split(' ')[0]} <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">{currentConfig.title.split(' ').slice(1).join(' ')}</span>
            </h1>
            <p className="text-xl text-gray-300 font-mono uppercase tracking-widest max-w-2xl mx-auto">
              {currentConfig.subtitle}
            </p>
          </motion.div>
        </div>
      </div>

      {/* Content */}
      <div className="page-container py-20 relative z-10">
        {isLoading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-12 h-12 text-primary animate-spin" />
          </div>
        ) : error ? (
          <div className="text-center text-accent py-10 font-mono uppercase tracking-widest border border-accent/20 bg-accent/5 p-4">{error}</div>
        ) : articles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {articles.map((article, index) => (
              <ArticleCard key={article.id} article={article} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 border border-white/5 bg-white/5 p-10 skew-x-[-5deg]">
            <p className="text-gray-400 font-display italic text-2xl mb-4 skew-x-[5deg]">
              No Intel Available
            </p>
            <p className="text-sm text-gray-600 uppercase tracking-widest skew-x-[5deg]">
              Data upload pending for this sector.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CategoryPage
