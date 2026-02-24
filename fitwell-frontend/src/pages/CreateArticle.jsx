import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { PenSquare, Loader2, Image as ImageIcon } from 'lucide-react'
import toast from 'react-hot-toast'
import axios from '../api/axios'

const CreateArticle = () => {
  const navigate = useNavigate()
  const [categories, setCategories] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category: '',
    image_url: '',
    is_published: true
  })

  useEffect(() => {
    // Fetch categories
    const fetchCategories = async () => {
      try {
        const response = await axios.get('categories/')
        setCategories(response.data)
        if (response.data.length > 0) {
          setFormData(prev => ({ ...prev, category: response.data[0].id }))
        }
      } catch (error) {
        // Silent error for categories
      }
    }
    fetchCategories()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await axios.post('articles/', formData)
      toast.success('Article created successfully!')
      navigate('/')
    } catch (error) {
      console.error('Create article error:', error)
      if (error.response?.data) {
        const errors = Object.values(error.response.data).flat()
        toast.error(errors[0] || 'Failed to create article')
      } else {
        toast.error('Failed to create article. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="page-container max-w-5xl py-20 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 -right-20 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 -left-20 w-80 h-80 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="glass-card p-10 md:p-20 border-t border-primary/40 relative overflow-hidden shadow-2xl"
      >
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-transparent via-primary to-transparent" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-16 relative z-10">
          <div className="flex items-center space-x-8">
            <div className="p-6 border border-primary/30 bg-primary/5 flex items-center justify-center rounded-full transform hover:rotate-12 transition-transform duration-500 shadow-[0_0_30px_rgba(212,175,55,0.1)]">
              <PenSquare className="w-10 h-10 text-primary" />
            </div>
            <div>
              <h1 className="text-4xl md:text-6xl font-serif font-bold text-white mb-3 tracking-tight">Compose <span className="text-primary italic">Article</span></h1>
              <p className="text-gray-400 font-light tracking-[0.1em] text-base max-w-md">Craft your contribution to the elite wellness collective.</p>
            </div>
          </div>
          <div className="hidden lg:block text-right">
            <span className="text-[10px] uppercase tracking-[0.4em] text-primary/40 font-bold block mb-1">Editor v1.0</span>
            <span className="text-[10px] uppercase tracking-[0.4em] text-white/20 font-bold block">Draft Auto-saved</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-12 relative z-10">
          <div className="group">
            <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Headline</label>
            <input
              type="text"
              className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all py-6 px-8 text-2xl md:text-4xl font-serif italic text-white placeholder-white/10"
              placeholder="The Future of Human Optimization"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Journal Category</label>
              <div className="relative">
                <select
                  className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all py-5 px-8 appearance-none cursor-pointer font-serif italic"
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  required
                >
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id} className="bg-[#0a0a0f] text-white py-4 px-6">
                      {cat.name}
                    </option>
                  ))}
                </select>
                <div className="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none">
                  <div className="w-2.5 h-2.5 border-r-2 border-b-2 border-primary/50 transform rotate-45"></div>
                </div>
              </div>
            </div>

            <div className="group">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] mb-4 group-focus-within:text-white transition-colors">Visual Link (Cover Image)</label>
              <div className="relative">
                <input
                  type="url"
                  className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all py-5 pl-14 pr-8 italic"
                  placeholder="https://images.unsplash.com/..."
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                />
                <div className="absolute left-6 top-1/2 -translate-y-1/2">
                  <ImageIcon className="w-5 h-5 text-primary/40" />
                </div>
              </div>
            </div>
          </div>

          <div className="group">
            <div className="flex justify-between items-end mb-4">
              <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.3em] group-focus-within:text-white transition-colors">Manuscript Content</label>
              <span className="text-[9px] uppercase tracking-widest text-gray-500 font-mono">{formData.content.length} characters</span>
            </div>
            <textarea
              className="input-field bg-white/5 border-white/10 focus:border-primary/50 focus:bg-white/10 transition-all min-h-[500px] py-8 px-8 leading-relaxed font-sans font-light text-xl text-gray-200 placeholder-white/5 scrollbar-hide"
              placeholder="Begin your narrative journey here..."
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              required
            />
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between gap-8 pt-8 border-t border-white/5">
            <div 
              className="flex items-center space-x-6 group cursor-pointer" 
              onClick={() => setFormData({ ...formData, is_published: !formData.is_published })}
            >
              <div className={`w-6 h-6 border-2 transition-all duration-500 flex items-center justify-center ${formData.is_published ? 'border-primary bg-primary/20 shadow-[0_0_15px_rgba(212,175,55,0.3)]' : 'border-white/20 bg-transparent'}`}>
                {formData.is_published && <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="w-2.5 h-2.5 bg-primary"></motion.div>}
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-white font-bold uppercase tracking-widest group-hover:text-primary transition-colors">Immediate Publication</span>
                <span className="text-[10px] text-gray-500 uppercase tracking-widest">Available to all elite members</span>
              </div>
            </div>

            <div className="flex items-center gap-4 w-full md:w-auto">
              <button 
                type="button" 
                onClick={() => navigate('/')}
                className="px-10 py-5 border border-white/10 text-gray-500 hover:text-white hover:bg-white/5 transition-all text-[10px] font-bold uppercase tracking-[0.3em] flex-1 md:flex-none"
              >
                Discard
              </button>
              <button 
                type="submit" 
                disabled={isLoading}
                className="glass-button flex-1 md:flex-none flex items-center justify-center text-[10px] py-5 px-12 tracking-[0.4em] uppercase font-bold min-w-[200px]"
              >
                {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : 'Publish to Feed'}
              </button>
            </div>
          </div>
        </form>
      </motion.div>
    </div>
  )
}

export default CreateArticle
