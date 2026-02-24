import { useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Calendar, User, ArrowRight, Heart } from 'lucide-react'
import { format } from 'date-fns'
import axios from '../api/axios'
import useAuthStore from '../store/auth'
import toast from 'react-hot-toast'

const ArticleCard = ({ article, index }) => {
  const { isAuthenticated } = useAuthStore()
  const [liked, setLiked] = useState(article.is_liked)
  const [likesCount, setLikesCount] = useState(article.likes_count || 0)

  const handleLike = async (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      toast.error('Please login to like articles')
      return
    }

    const prevLiked = liked
    const prevCount = likesCount
    
    setLiked(!liked)
    setLikesCount(liked ? likesCount - 1 : likesCount + 1)

    try {
      const response = await axios.post(`articles/${article.id}/like/`)
      setLiked(response.data.status === 'liked')
      setLikesCount(response.data.likes_count)
    } catch (error) {
      setLiked(prevLiked)
      setLikesCount(prevCount)
      toast.error('Failed to update like')
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="glass-card group"
    >
      <div className="relative h-64 overflow-hidden">
        {article.image_url ? (
          <img 
            src={article.image_url} 
            alt={article.title}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105 filter grayscale group-hover:grayscale-0"
          />
        ) : (
          <div className="w-full h-full bg-surface-highlight flex items-center justify-center border-b border-white/5">
            <div className="w-16 h-16 rounded-full bg-primary/5 flex items-center justify-center">
              <Calendar className="w-8 h-8 text-primary/20" />
            </div>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent opacity-80" />
        
        <div className="absolute top-4 left-4 flex justify-between w-[calc(100%-2rem)] items-start">
          <span className="px-3 py-1 bg-black/50 backdrop-blur-sm border border-primary/30 text-primary text-[10px] uppercase tracking-[0.2em] font-bold">
            {article.category_name || 'Featured'}
          </span>
          
          <button 
            onClick={handleLike}
            className={`p-2 rounded-full backdrop-blur-sm border transition-all duration-300 ${liked ? 'bg-primary text-black border-primary' : 'bg-black/30 text-gray-400 border-white/10 hover:border-primary/50 hover:text-primary'}`}
          >
            <Heart className={`w-4 h-4 ${liked ? 'fill-current' : ''}`} />
          </button>
        </div>
      </div>
      
      <div className="p-8">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-4 font-serif italic">
          <div className="flex items-center">
            <Calendar className="w-3 h-3 mr-2 text-primary" />
            {format(new Date(article.created_at), 'MMMM d, yyyy')}
          </div>
          <div className="flex items-center">
            <Heart className="w-3 h-3 mr-1 text-primary" />
            <span>{likesCount} likes</span>
          </div>
        </div>
        
        <h3 className="text-2xl font-serif font-bold mb-4 leading-tight group-hover:text-primary transition-colors">
          {article.title}
        </h3>
        
        <p className="text-gray-400 text-sm mb-8 line-clamp-3 leading-relaxed font-light">
          {article.content}
        </p>
        
        <div className="flex items-center justify-between pt-6 border-t border-white/5">
          <div className="flex items-center text-xs text-gray-300 uppercase tracking-widest">
            <User className="w-3 h-3 mr-2 text-primary" />
            {article.author_username || 'Elite Member'}
          </div>
          
          <Link 
            to={`/articles/${article.id}`}
            className="flex items-center text-primary text-xs font-bold uppercase tracking-widest hover:translate-x-1 transition-transform"
          >
            Read Story <ArrowRight className="w-3 h-3 ml-2" />
          </Link>
        </div>
      </div>
    </motion.div>
  )
}

export default ArticleCard
