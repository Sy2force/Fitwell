import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { PenSquare, Loader2, Send } from 'lucide-react'
import toast from 'react-hot-toast'
import axios from '../api/axios'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'

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
        const response = await axios.get('blog/categories/')
        const categoriesData = response.data.results || response.data
        setCategories(categoriesData)
        if (categoriesData.length > 0) {
          setFormData(prev => ({ ...prev, category: categoriesData[0].id }))
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
      await axios.post('blog/articles/', formData)
      toast.success('Transmission Uploaded Successfully!')
      navigate('/')
    } catch (error) {
      console.error('Create article error:', error)
      if (error.response?.data) {
        const errors = Object.values(error.response.data).flat()
        toast.error(errors[0] || 'Upload Failed')
      } else {
        toast.error('Upload Failed. Check Connection.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  return (
    <div className="page-container max-w-5xl py-20 relative overflow-hidden bg-background">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 -right-20 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none animate-pulse-fast"></div>
      <div className="absolute bottom-1/4 -left-20 w-80 h-80 bg-accent/5 rounded-full blur-[100px] pointer-events-none"></div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="glass-card p-1 border-l-4 border-primary relative overflow-hidden"
      >
        <div className="bg-surface/90 p-10 md:p-20 backdrop-blur-xl relative z-10">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-16 relative z-10">
            <div className="flex items-center space-x-8">
                <div className="p-6 border-2 border-primary bg-black/50 flex items-center justify-center transform skew-x-[-10deg]">
                    <div className="skew-x-[10deg]">
                        <PenSquare className="w-10 h-10 text-primary" />
                    </div>
                </div>
                <div>
                <h1 className="text-4xl md:text-6xl font-display font-bold text-white mb-3 tracking-tighter italic">
                    NEW <span className="text-primary">INTEL</span>
                </h1>
                <p className="text-gray-400 font-mono text-sm tracking-widest uppercase">
                    Contribute to the collective knowledge base.
                </p>
                </div>
            </div>
            <div className="hidden lg:block text-right">
                <span className="text-[10px] uppercase tracking-[0.4em] text-primary font-bold block mb-1">Terminal v2.0</span>
                <span className="text-[10px] uppercase tracking-[0.4em] text-gray-500 font-bold block">Secure Connection</span>
            </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-12 relative z-10">
            <Input
              label="Headline"
              type="text"
              name="title"
              placeholder="ENTER TITLE..."
              value={formData.title}
              onChange={handleChange}
              required
              className="text-2xl"
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div className="group">
                <label className="block text-[10px] font-bold text-primary uppercase tracking-widest mb-4">Classification (Category)</label>
                <div className="relative">
                    <select
                    name="category"
                    className="input-field bg-black/50 border-l-2 border-white/10 focus:border-primary transition-all py-5 px-8 appearance-none cursor-pointer font-mono text-sm uppercase text-gray-300"
                    value={formData.category}
                    onChange={handleChange}
                    required
                    >
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id} className="bg-black text-white py-4 px-6">
                        {cat.name}
                        </option>
                    ))}
                    </select>
                    <div className="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none">
                    <div className="w-2 h-2 border-r-2 border-b-2 border-primary transform rotate-45"></div>
                    </div>
                </div>
                </div>

                <div className="group">
                  <Input
                    label="Visual Data (Image URL)"
                    type="url"
                    name="image_url"
                    placeholder="HTTPS://SOURCE..."
                    value={formData.image_url}
                    onChange={handleChange}
                  />
                </div>
            </div>

            <div className="group">
                <div className="flex justify-between items-end mb-4">
                <label className="block text-[10px] font-bold text-primary uppercase tracking-widest">Report Content</label>
                <span className="text-[9px] uppercase tracking-widest text-gray-500 font-mono">{formData.content.length} CHARS</span>
                </div>
                <textarea
                name="content"
                className="input-field bg-black/50 border-l-2 border-white/10 focus:border-primary transition-all min-h-[500px] py-8 px-8 leading-relaxed font-sans text-lg text-gray-300 placeholder-gray-800 scrollbar-hide"
                placeholder="INITIATE REPORT..."
                value={formData.content}
                onChange={handleChange}
                required
                />
            </div>

            <div className="flex flex-col md:flex-row items-center justify-between gap-8 pt-8 border-t border-white/5">
                <div 
                className="flex items-center space-x-6 group cursor-pointer" 
                onClick={() => setFormData({ ...formData, is_published: !formData.is_published })}
                >
                <div className={`w-6 h-6 border-2 transition-all duration-300 flex items-center justify-center transform skew-x-[-10deg] ${formData.is_published ? 'border-secondary bg-secondary/20' : 'border-white/20 bg-transparent'}`}>
                    {formData.is_published && <div className="w-3 h-3 bg-secondary"></div>}
                </div>
                <div className="flex flex-col">
                    <span className="text-xs text-white font-bold uppercase tracking-widest group-hover:text-secondary transition-colors">Immediate Broadcast</span>
                    <span className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">Available to all units</span>
                </div>
                </div>

                <div className="flex items-center gap-4 w-full md:w-auto">
                <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => navigate('/')}
                    className="border-white/10 text-gray-500 hover:text-white"
                >
                    Abort
                </Button>
                <Button 
                    type="submit" 
                    variant="primary"
                    disabled={isLoading}
                    className="min-w-[200px]"
                >
                    {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : (
                        <>
                            Upload Data <Send className="w-4 h-4 ml-3" />
                        </>
                    )}
                </Button>
                </div>
            </div>
            </form>
        </div>
      </motion.div>
    </div>
  )
}

export default CreateArticle
