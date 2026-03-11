import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { User, Mail, Shield, Loader2, PenSquare } from 'lucide-react'
import axios from '../api/axios'
import useAuthStore from '../store/auth'
import ArticleCard from '../components/ArticleCard'
import EditProfileModal from '../components/EditProfileModal'
import Button from '../components/ui/Button'
import ProgressBar from '../components/ui/ProgressBar'
import Badge from '../components/ui/Badge'

const Profile = () => {
  const { user, logout, updateUser } = useAuthStore()
  const [myArticles, setMyArticles] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)

  useEffect(() => {
    const fetchMyArticles = async () => {
      try {
        const response = await axios.get('blog/articles/me/')
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
        className="max-w-6xl mx-auto"
      >
        {/* Profile Header */}
        <div className="glass-card p-10 md:p-12 mb-12 flex flex-col md:flex-row items-center md:items-start gap-10 relative overflow-hidden border-l-4 border-primary shadow-[0_0_40px_rgba(0,0,0,0.3)]">
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-[120px] -mr-32 -mt-32 pointer-events-none"></div>
          
          <div className="relative group shrink-0">
            <div className="w-32 h-32 md:w-40 md:h-40 border-2 border-primary/30 p-1 bg-background-dark relative z-10 transform skew-x-[-5deg] transition-transform duration-500 group-hover:scale-105">
              {user?.profile?.avatar ? (
                <img src={user.profile.avatar} alt={user.username} className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-500" />
              ) : (
                <div className="w-full h-full bg-surface-dark flex items-center justify-center">
                  <User className="w-16 h-16 text-primary/40 group-hover:scale-110 transition-transform" />
                </div>
              )}
            </div>
            {/* Decorative decorative elements */}
            <div className="absolute -bottom-2 -right-2 w-full h-full border border-energy/20 -z-0 skew-x-[-5deg]"></div>
          </div>
          
          <div className="flex-1 text-center md:text-left z-10 w-full">
            <div className="flex flex-col md:flex-row justify-between items-center md:items-start gap-6 mb-8">
              <div>
                <div className="flex items-center gap-3 justify-center md:justify-start mb-2">
                  <h1 className="text-4xl md:text-6xl font-display font-bold text-white tracking-tighter italic">{user?.username}</h1>
                  <Badge variant="primary">Lvl {user?.profile?.level || 1}</Badge>
                </div>
                <div className="flex items-center justify-center md:justify-start gap-4 text-sm text-gray-400 font-mono">
                  <span className="flex items-center"><Mail className="w-3 h-3 mr-2 text-primary" /> {user?.email || 'Encrypted'}</span>
                  <span className="flex items-center"><Shield className="w-3 h-3 mr-2 text-primary" /> Elite Member</span>
                </div>
              </div>

              <div className="flex gap-3">
                <Button variant="outline" size="sm" onClick={() => setIsEditModalOpen(true)}>
                  Edit Profile
                </Button>
                <Button variant="ghost" size="sm" onClick={logout} className="text-red-500 hover:text-red-400 hover:bg-red-500/10">
                  Log Out
                </Button>
              </div>
            </div>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="p-4 bg-surface-dark/50 border border-white/5 skew-x-[-5deg] hover:border-primary/30 transition-colors">
                <div className="skew-x-[5deg]">
                  <span className="text-[10px] uppercase tracking-widest text-gray-500 block mb-1">XP Points</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-display font-bold text-white">{user?.profile?.xp || 0}</span>
                    <span className="text-xs text-primary">XP</span>
                  </div>
                </div>
              </div>
              
              <div className="p-4 bg-surface-dark/50 border border-white/5 skew-x-[-5deg] hover:border-energy/30 transition-colors">
                <div className="skew-x-[5deg]">
                  <span className="text-[10px] uppercase tracking-widest text-gray-500 block mb-1">Streak</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-display font-bold text-white">{user?.profile?.current_streak || 0}</span>
                    <span className="text-xs text-energy">Days</span>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-surface-dark/50 border border-white/5 skew-x-[-5deg] hover:border-health/30 transition-colors">
                <div className="skew-x-[5deg]">
                  <span className="text-[10px] uppercase tracking-widest text-gray-500 block mb-1">Health Score</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-display font-bold text-white">{user?.profile?.health_score || 0}</span>
                    <span className="text-xs text-health">%</span>
                  </div>
                </div>
              </div>

              <div className="p-4 bg-surface-dark/50 border border-white/5 skew-x-[-5deg] hover:border-white/30 transition-colors">
                <div className="skew-x-[5deg]">
                  <span className="text-[10px] uppercase tracking-widest text-gray-500 block mb-1">Content</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-2xl font-display font-bold text-white">{myArticles.length}</span>
                    <span className="text-xs text-gray-400">Posts</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Score Breakdown */}
            {user?.profile?.scores && (
              <div className="mb-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
                 <ProgressBar value={user.profile.scores.fitness} color="primary" label="Fitness" />
                 <ProgressBar value={user.profile.scores.recovery} color="health" label="Recovery" />
                 <ProgressBar value={user.profile.scores.lifestyle} color="energy" label="Lifestyle" />
                 <ProgressBar value={user.profile.scores.consistency} color="primary" label="Consistency" />
              </div>
            )}

            {/* Level Progress */}
            <div className="bg-surface-dark/30 p-4 border-t border-white/5">
              <ProgressBar value={(user?.profile?.xp % 1000) / 10} color="energy" label="Progress to Next Level" />
            </div>

            {user?.profile?.bio && (
              <div className="mt-8 relative pl-6 border-l-2 border-primary/30">
                <p className="text-lg text-gray-300 font-light italic leading-relaxed">
                  &quot;{user.profile.bio}&quot;
                </p>
              </div>
            )}
          </div>
        </div>

        {/* My Articles */}
        <div className="flex items-end justify-between mb-8 border-b border-white/10 pb-4">
          <h2 className="text-3xl font-display font-bold text-white italic">
            Mission <span className="text-primary">Logs</span>
          </h2>
          <span className="text-sm font-mono text-gray-500">{myArticles.length} ENTRIES</span>
        </div>

        {isLoading ? (
          <div className="text-center py-20 text-gray-500 font-mono">Loading data...</div>
        ) : myArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {myArticles.map((article, index) => (
              <ArticleCard key={article.id} article={article} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-24 glass-card border-t border-white/5 flex flex-col items-center">
            <PenSquare className="w-12 h-12 text-gray-600 mb-4 opacity-50" />
            <p className="text-gray-400 mb-6 font-display text-lg tracking-wide">No mission logs recorded.</p>
            <Link to="/create-article">
              <Button variant="primary">Create First Entry</Button>
            </Link>
          </div>
        )}
      </motion.div>
    </div>
  )
}

export default Profile
