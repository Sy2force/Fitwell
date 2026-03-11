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
      toast.error('ACCESS DENIED: Authentication Required')
      return
    }

    const prevLiked = liked
    const prevCount = likesCount
    
    setLiked(!liked)
    setLikesCount(liked ? likesCount - 1 : likesCount + 1)

    try {
      const response = await axios.post(`blog/articles/${article.id}/like/`)
      setLiked(response.data.status === 'liked')
      setLikesCount(response.data.likes_count)
    } catch (error) {
      setLiked(prevLiked)
      setLikesCount(prevCount)
      toast.error('System Error: Like Failed')
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="group relative bg-surface border border-white/10 hover:border-primary transition-all duration-300 overflow-hidden"
    >
      <div className="relative h-64 overflow-hidden clip-path-slant">
        {article.image_url ? (
          <img 
            src={article.image_url} 
            alt={article.title}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 filter grayscale group-hover:grayscale-0 opacity-80 group-hover:opacity-100"
          />
        ) : (
          <div className="w-full h-full bg-surface-highlight flex items-center justify-center border-b border-white/5">
            <div className="w-16 h-16 rounded-full bg-primary/5 flex items-center justify-center">
              <Calendar className="w-8 h-8 text-primary/20" />
            </div>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent opacity-90" />
        
        <div className="absolute top-4 left-0 flex justify-between w-full px-4 items-start z-10">
          <span className="px-3 py-1 bg-primary text-black text-[10px] uppercase tracking-widest font-bold transform skew-x-[-10deg]">
            <span className="block skew-x-[10deg]">{article.category_name || 'INTEL'}</span>
          </span>
          
          <button 
            onClick={handleLike}
            className={`p-2 border transition-all duration-300 transform skew-x-[-10deg] ${liked ? 'bg-accent text-white border-accent' : 'bg-black/50 text-gray-400 border-white/20 hover:border-accent hover:text-accent'}`}
          >
            <Heart className={`w-4 h-4 transform skew-x-[10deg] ${liked ? 'fill-current' : ''}`} />
          </button>
        </div>
      </div>
      
      <div className="p-6 relative">
        <div className="flex items-center justify-between text-[10px] text-gray-500 mb-4 font-mono uppercase tracking-wider">
          <div className="flex items-center">
            <Calendar className="w-3 h-3 mr-2 text-secondary" />
            {format(new Date(article.created_at), 'MM.dd.yyyy')}
          </div>
          <div className="flex items-center">
            <Heart className="w-3 h-3 mr-1 text-accent" />
            <span>{likesCount}</span>
          </div>
        </div>
        
        <h3 className="text-xl font-display font-bold mb-3 leading-tight text-white group-hover:text-primary transition-colors italic">
          {article.title}
        </h3>
        
        <p className="text-gray-400 text-xs mb-6 line-clamp-2 leading-relaxed font-sans border-l-2 border-white/10 pl-3">
          {article.content}
        </p>
        
        <div className="flex items-center justify-between pt-4 border-t border-white/10">
          <div className="flex items-center text-[10px] text-gray-400 uppercase tracking-widest font-bold">
            <User className="w-3 h-3 mr-2 text-primary" />
            {article.author_username || 'OPERATOR'}
          </div>
          
          <Link 
            to={`/articles/${article.id}`}
            className="flex items-center text-primary text-[10px] font-bold uppercase tracking-widest hover:translate-x-1 transition-transform group-hover:text-white"
          >
            Access Data <ArrowRight className="w-3 h-3 ml-2" />
          </Link>
        </div>
      </div>
      
      {/* Decorative Corner */}
      <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-primary opacity-0 group-hover:opacity-100 transition-opacity"></div>
    </motion.div>
  )
}

export default ArticleCard
