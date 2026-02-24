import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Loader2, Dumbbell, Apple, Brain, Activity } from 'lucide-react'
import axios from '../api/axios'
import ArticleCard from '../components/ArticleCard'

const CategoryPage = () => {
  const { slug } = useParams()
  const [articles, setArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  // Map slugs to display info
  const categoryConfig = {
    'workouts': {
      title: 'Elite Training',
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
        // First try to get by category slug
        // Note: You might need to adjust your backend to support filtering by category slug 
        // or ensure the category names match these slugs.
        // For now, assuming the backend has an endpoint or we filter client side if needed,
        // but ideally: /api/categories/{slug}/articles/
        
        // Let's try to map the frontend slug to the backend category name if possible,
        // or just query.
        let backendSlug = slug;
        if (slug === 'workouts') backendSlug = 'strength'; // Example mapping if needed
        
        // Trying a direct category filter endpoint
        const response = await axios.get(`articles/?category__slug=${backendSlug}`)
        
        // If the backend doesn't support that filter directly yet, we might get all and filter (not efficient but works for small apps)
        // Or better, use the search endpoint if implemented
        
        // Let's assume the standard list endpoint returns results
        setArticles(response.data.results || response.data)
        
        // If empty, try fetching filtered by name for robustness in this demo
        if ((response.data.results || response.data).length === 0) {
             // Fallback: fetch all and filter client side (temporary fix until backend is perfect)
             const allRes = await axios.get('articles/')
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
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[50vh] flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-black/60 z-10" />
          <img 
            src={currentConfig.image} 
            alt={currentConfig.title} 
            className="w-full h-full object-cover"
          />
        </div>
        
        <div className="relative z-20 text-center px-4 max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Icon className="w-16 h-16 text-primary mx-auto mb-6 opacity-90" />
            <h1 className="text-5xl md:text-7xl font-serif font-bold mb-6 text-white tracking-tight">
              {currentConfig.title}
            </h1>
            <p className="text-xl text-gray-300 font-light tracking-wide max-w-2xl mx-auto">
              {currentConfig.subtitle}
            </p>
          </motion.div>
        </div>
      </div>

      {/* Content */}
      <div className="page-container py-20">
        {isLoading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-10 h-10 text-primary animate-spin" />
          </div>
        ) : error ? (
          <div className="text-center text-red-400 py-10">{error}</div>
        ) : articles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {articles.map((article, index) => (
              <ArticleCard key={article.id} article={article} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <p className="text-gray-500 font-serif italic text-xl">
              No articles found in this collection yet.
            </p>
            <p className="text-sm text-gray-600 mt-2 uppercase tracking-widest">
              Check back soon for curated content.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CategoryPage
