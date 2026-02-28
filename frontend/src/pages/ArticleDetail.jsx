import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, MessageSquare, Send, Trash2, Loader2, BookOpen, Heart } from 'lucide-react'
import { format } from 'date-fns'
import toast from 'react-hot-toast'
import axios from '../api/axios'
import useAuthStore from '../store/auth'
import ArticleCard from '../components/ArticleCard'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'

const ArticleDetail = () => {
  const { user, isAuthenticated } = useAuthStore()
  const { id } = useParams()
  const navigate = useNavigate()
  
  const [article, setArticle] = useState(null)
  const [comments, setComments] = useState([])
  const [relatedArticles, setRelatedArticles] = useState([])
  const [newComment, setNewComment] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [liked, setLiked] = useState(false)
  const [likesCount, setLikesCount] = useState(0)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [articleRes, commentsRes] = await Promise.all([
          axios.get(`blog/articles/${id}/`),
          axios.get(`blog/articles/${id}/comments/`)
        ])
        setArticle(articleRes.data)
        setLiked(articleRes.data.is_liked)
        setLikesCount(articleRes.data.likes_count || 0)
        setComments(commentsRes.data)
        
        // Fetch related articles if category exists
        if (articleRes.data.category_slug) {
          try {
            const relatedRes = await axios.get(`blog/categories/${articleRes.data.category_slug}/articles/`)
            const allRelated = relatedRes.data.results || relatedRes.data
            // Filter out current article and limit to 3
            setRelatedArticles(allRelated.filter(a => a.id !== articleRes.data.id).slice(0, 3))
          } catch (err) {
            console.error("Failed to fetch related articles", err)
          }
        }
      } catch (error) {
        toast.error('Failed to load article')
        navigate('/')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [id, navigate])

  const handleLike = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to like articles')
      return
    }

    const prevLiked = liked
    const prevCount = likesCount
    
    setLiked(!liked)
    setLikesCount(liked ? likesCount - 1 : likesCount + 1)

    try {
      const response = await axios.post(`blog/articles/${id}/like/`)
      setLiked(response.data.status === 'liked')
      setLikesCount(response.data.likes_count)
    } catch (error) {
      setLiked(prevLiked)
      setLikesCount(prevCount)
      toast.error('Failed to update like')
    }
  }

  const handleCommentSubmit = async (e) => {
    e.preventDefault()
    if (!newComment.trim()) return

    setIsSubmitting(true)
    try {
      const response = await axios.post(`blog/articles/${id}/comments/`, {
        content: newComment,
        article: id
      })
      setComments([...comments, response.data])
      setNewComment('')
      toast.success('Comment posted!')
    } catch (error) {
      toast.error('Failed to post comment')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('Are you sure?')) return

    try {
      await axios.delete(`blog/comments/${commentId}/`)
      setComments(comments.filter(c => c.id !== commentId))
      toast.success('Comment deleted')
    } catch (error) {
      toast.error('Failed to delete comment')
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-12 h-12 text-primary animate-spin" />
      </div>
    )
  }
  
  if (!article) return null

  return (
    <div className="min-h-screen pb-20">
      {/* Hero Header */}
      <div className="relative h-[60vh] w-full">
        <div className="absolute inset-0">
          {article.image_url ? (
            <img 
              src={article.image_url} 
              alt={article.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-gray-900 to-black" />
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/60 to-transparent" />
        </div>

        <div className="absolute bottom-0 left-0 w-full p-6 md:p-12 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex items-center space-x-4 text-sm text-primary uppercase tracking-[0.2em] font-bold mb-6">
              <Badge variant="primary">{article.category_name}</Badge>
              <span>•</span>
              <span>{format(new Date(article.created_at), 'MMMM d, yyyy')}</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-serif font-bold mb-8 leading-tight text-white shadow-lg">
              {article.title}
            </h1>

            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 border border-white/20 flex items-center justify-center bg-black/30 backdrop-blur-sm">
                <User className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-white font-serif italic text-lg">By {article.author_username}</p>
                <p className="text-gray-400 text-xs uppercase tracking-widest">Elite Contributor</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 -mt-10 relative z-10">
        {/* Article Content */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-10 md:p-16 mb-16 border-t border-primary/20 relative"
        >
          <button 
            onClick={handleLike}
            className={`absolute top-10 right-10 p-4 rounded-full backdrop-blur-sm border transition-all duration-300 flex flex-col items-center ${liked ? 'bg-primary/20 text-primary border-primary' : 'bg-black/30 text-gray-400 border-white/10 hover:border-primary/50 hover:text-primary'}`}
          >
            <Heart className={`w-6 h-6 mb-1 ${liked ? 'fill-current' : ''}`} />
            <span className="text-[10px] font-bold">{likesCount}</span>
          </button>

          <div className="prose prose-invert prose-lg max-w-none prose-headings:font-serif prose-headings:text-primary prose-p:font-light prose-p:leading-loose prose-p:text-gray-300">
            <p className="whitespace-pre-wrap first-letter:text-7xl first-letter:font-serif first-letter:text-primary first-letter:float-left first-letter:mr-3 first-letter:mt-[-10px]">
              {article.content}
            </p>
          </div>
        </motion.div>

        {/* Related Articles */}
        {relatedArticles.length > 0 && (
          <div className="mb-20 border-t border-white/10 pt-16">
            <h3 className="text-2xl font-serif font-bold mb-8 flex items-center">
              <BookOpen className="w-6 h-6 mr-3 text-primary" />
              More in {article.category_name}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {relatedArticles.map((related, index) => (
                <ArticleCard key={related.id} article={related} index={index} />
              ))}
            </div>
          </div>
        )}

        {/* Comments Section */}
        <div className="max-w-3xl mx-auto">
          <h3 className="text-3xl font-serif font-bold mb-8 flex items-center border-b border-white/10 pb-4">
            <MessageSquare className="w-6 h-6 mr-3 text-primary" />
            Discussion <span className="text-lg text-gray-500 ml-2 font-sans font-normal">({comments.length})</span>
          </h3>

          {isAuthenticated ? (
            <form onSubmit={handleCommentSubmit} className="mb-12 glass-card p-8">
              <label className="block text-xs font-bold text-primary uppercase tracking-[0.2em] mb-4">Leave a thought</label>
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Share your perspective..."
                className="input-field min-h-[120px] mb-6 bg-black/20 focus:bg-black/40"
              />
              <Button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full"
              >
                {isSubmitting ? <Loader2 className="animate-spin w-4 h-4" /> : (
                  <>
                    Post Comment <Send className="w-4 h-4 ml-2" />
                  </>
                )}
              </Button>
            </form>
          ) : (
            <div className="glass-card p-8 text-center mb-12 border border-white/5">
              <p className="text-gray-400 font-serif italic text-lg mb-4">Join the conversation</p>
              <p className="text-sm text-gray-500 uppercase tracking-widest">Please login to leave a comment.</p>
            </div>
          )}

          <div className="space-y-6">
            {comments.map((comment) => (
              <motion.div 
                key={comment.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card p-8 relative border-l-2 border-l-primary/30"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 border border-white/10 flex items-center justify-center bg-surface">
                      <User className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <span className="font-bold text-sm block text-white tracking-wide">{comment.username}</span>
                      <span className="text-[10px] text-primary uppercase tracking-widest">
                        {format(new Date(comment.created_at), 'MMM d, yyyy')}
                      </span>
                    </div>
                  </div>
                  
                  {user && user.username === comment.username && (
                    <button 
                      onClick={() => handleDeleteComment(comment.id)}
                      className="text-gray-600 hover:text-red-400 transition-colors p-2"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <p className="text-gray-300 pl-14 font-light leading-relaxed">{comment.content}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ArticleDetail
