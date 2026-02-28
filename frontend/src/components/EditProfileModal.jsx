import { useState } from 'react'
import { Loader2, Save } from 'lucide-react'
import axios from '../api/axios'
import toast from 'react-hot-toast'
import Modal from './ui/Modal'
import Input from './ui/Input'
import Button from './ui/Button'

const EditProfileModal = ({ isOpen, onClose, user, onUpdate }) => {
  const [formData, setFormData] = useState({
    email: user?.email || '',
    bio: user?.bio || '',
    avatar: user?.avatar || ''
  })
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      const payload = {
        email: formData.email,
        profile: {
            bio: formData.bio,
            avatar: formData.avatar
        }
      }

      const res = await axios.patch('auth/profile/', payload)
      onUpdate(res.data)
      toast.success('Profile updated successfully')
      onClose()
    } catch (error) {
      toast.error('Failed to update profile')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="EDIT PROFILE">
      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Comms Link (Email)"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="your@email.com"
        />

        <Input
          label="Avatar Source (URL)"
          type="url"
          name="avatar"
          value={formData.avatar}
          onChange={handleChange}
          placeholder="https://images.fitwell.net/avatar.jpg"
        />

        <div>
          <label className="block text-[10px] font-bold text-primary uppercase tracking-[0.2em] mb-2">
            Bio Data
          </label>
          <textarea
            name="bio"
            value={formData.bio}
            onChange={handleChange}
            className="w-full bg-surface-dark border-2 border-white/10 px-4 py-3 text-white placeholder-gray-600 rounded-lg focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all duration-300 font-sans min-h-[100px]"
            placeholder="Brief personnel file..."
          />
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4 mr-2" />}
            Save Updates
          </Button>
        </div>
      </form>
    </Modal>
  )
}

export default EditProfileModal
