import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { User, Mail, Shield, Loader2, PenSquare } from 'lucide-react'
import axios from '../api/axios'
import useAuthStore from '../store/auth'
import ArticleCard from '../components/ArticleCard'
import EditProfileModal from '../components/EditProfileModal'

const Profile = () => {
  const { user, logout, updateUser } = useAuthStore()
  const [myArticles, setMyArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)

  useEffect(() => {
    const fetchMyArticles = async () => {
      try {
        const response = await axios.get('articles/me/')
        setMyArticles(response.data.results || response.data)
      } catch (error) {
        // Silent error
      } finally {
        setIsLoading(false)
      }
    }

    if (user) fetchMyArticles()
  }, [user])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-12 h-12 text-primary animate-spin" />
      </div>
    )
  }

  return (
    <div className="page-container">
      <EditProfileModal 
        isOpen={isEditModalOpen} 
        onClose={() => setIsEditModalOpen(false)} 
        user={user}
        onUpdate={updateUser}
      />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto"
      >
        {/* Profile Header */}
        <div className="glass-card p-10 md:p-16 mb-16 flex flex-col md:flex-row items-center md:items-start space-y-10 md:space-y-0 md:space-x-16 relative overflow-hidden border-t border-primary/30 shadow-2xl">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[100px] -mr-32 -mt-32 pointer-events-none"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-primary/5 rounded-full blur-[80px] -ml-24 -mb-24 pointer-events-none"></div>
          
          <div className="relative group">
            <div className="w-32 h-32 md:w-40 md:h-40 border-2 border-primary/30 p-1.5 bg-background/50 relative z-10 rounded-none transform transition-transform duration-700 group-hover:rotate-3 shadow-[0_0_40px_rgba(212,175,55,0.1)]">
              {user?.avatar ? (
                <img src={user.avatar} alt={user.username} className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-500" />
              ) : (
                <div className="w-full h-full bg-surface-highlight flex items-center justify-center">
                  <User className="w-12 h-12 text-primary/40 group-hover:scale-110 transition-transform" />
                </div>
              )}
            </div>
            <div className="absolute -inset-2 border border-primary/10 -z-0 group-hover:inset-0 transition-all duration-500"></div>
          </div>
          
          <div className="flex-1 text-center md:text-left z-10">
            <div className="flex flex-col md:flex-row items-center md:items-end gap-6 mb-8">
              <h1 className="text-5xl md:text-7xl font-serif font-bold text-white tracking-tighter">{user?.username}</h1>
              <div className="flex gap-3">
                <button 
                  onClick={() => setIsEditModalOpen(true)}
                  className="px-6 py-2 bg-primary/10 border border-primary/30 text-primary text-[10px] uppercase tracking-[0.2em] font-bold hover:bg-primary hover:text-black transition-all"
                >
                  Edit Profile
                </button>
                <button 
                  onClick={logout}
                  className="px-6 py-2 bg-red-500/5 border border-red-500/20 text-red-400 text-[10px] uppercase tracking-[0.2em] font-bold hover:bg-red-500 hover:text-white transition-all"
                >
                  Terminate Session
                </button>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
              <div className="p-4 border border-white/5 bg-white/5 backdrop-blur-sm">
                <span className="text-[9px] uppercase tracking-[0.3em] text-primary/60 font-bold block mb-2">Status</span>
                <span className="flex items-center text-white text-xs font-serif italic">
                  <Shield className="w-3 h-3 mr-2 text-primary" /> Elite Contributor
                </span>
              </div>
              <div className="p-4 border border-white/5 bg-white/5 backdrop-blur-sm">
                <span className="text-[9px] uppercase tracking-[0.3em] text-primary/60 font-bold block mb-2">Secure Link</span>
                <span className="flex items-center text-white text-xs font-serif italic truncate">
                  <Mail className="w-3 h-3 mr-2 text-primary" /> {user?.email || 'Encrypted'}
                </span>
              </div>
              <div className="p-4 border border-white/5 bg-white/5 backdrop-blur-sm">
                <span className="text-[9px] uppercase tracking-[0.3em] text-primary/60 font-bold block mb-2">Portfolio</span>
                <span className="flex items-center text-white text-xs font-serif italic">
                  <PenSquare className="w-3 h-3 mr-2 text-primary" /> {myArticles.length} Journals Published
                </span>
              </div>
            </div>

            {user?.bio && (
              <div className="relative">
                <p className="text-xl text-gray-400 font-serif italic leading-relaxed max-w-2xl pl-8 border-l-2 border-primary/20">
                  &quot;{user.bio}&quot;
                </p>
              </div>
            )}
          </div>
        </div>

        {/* My Articles */}
        <div className="flex items-end justify-between mb-8 border-b border-white/5 pb-4">
          <h2 className="text-2xl font-serif font-bold">
            My Contributions <span className="text-primary text-lg ml-2">({myArticles.length})</span>
          </h2>
        </div>

        {isLoading ? (
          <div className="text-center py-20 text-gray-500 font-serif italic">Loading portfolio...</div>
        ) : myArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {myArticles.map((article, index) => (
              <ArticleCard key={article.id} article={article} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 glass-card border-t border-primary/10">
            <p className="text-gray-400 mb-6 font-serif text-lg">You haven&apos;t published any articles yet.</p>
            <p className="text-sm text-gray-500 uppercase tracking-widest mb-8">Start your legacy today</p>
            <Link to="/create-article" className="glass-button inline-flex items-center px-8 py-4">
              <PenSquare className="w-4 h-4 mr-2" /> Write Article
            </Link>
          </div>
        )}
      </motion.div>
    </div>
  )
}

export default Profile
