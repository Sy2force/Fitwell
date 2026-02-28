import { useState, useEffect, useCallback } from 'react'
import { Users, FileDown, ShieldAlert, Check, X, Loader2 } from 'lucide-react'
import axios from '../../api/axios'
import toast from 'react-hot-toast'
import Button from '../../components/ui/Button'
import { useTranslation } from 'react-i18next'

const AdminDashboard = () => {
  const { t } = useTranslation()
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const fetchUsers = useCallback(async () => {
    try {
      const response = await axios.get(`auth/admin/users/?search=${searchQuery}`)
      setUsers(response.data.results || response.data)
    } catch (error) {
      toast.error('Failed to load user database')
    } finally {
      setIsLoading(false)
    }
  }, [searchQuery])

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const handleSearch = (e) => {
    e.preventDefault()
    setIsLoading(true)
    fetchUsers()
  }

  const handleExport = async () => {
    try {
      const response = await axios.get('auth/admin/export/', {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'fitwell_leads.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('Database exported successfully')
    } catch (error) {
      toast.error('Export failed')
    }
  }

  return (
    <div className="page-container py-20 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
          <div>
            <h1 className="text-4xl font-display font-bold text-white mb-2 flex items-center">
              <ShieldAlert className="w-8 h-8 text-accent mr-3" />
              {t('admin.title')}
            </h1>
            <p className="text-gray-400 font-mono text-xs uppercase tracking-widest">Restricted Access // Level 5 Clearance</p>
          </div>
          
          <div className="flex gap-4">
            <Button variant="outline" onClick={handleExport}>
              <FileDown className="w-4 h-4 mr-2" />
              {t('admin.export_btn')}
            </Button>
          </div>
        </div>

        {/* User Database */}
        <div className="glass-card border-l-4 border-accent p-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-2xl font-display font-bold text-white flex items-center">
              <Users className="w-6 h-6 mr-3 text-accent" />
              {t('admin.users')}
            </h2>
            
            <form onSubmit={handleSearch} className="flex gap-2">
              <input 
                type="text" 
                placeholder="Search database..." 
                className="bg-black/30 border border-white/10 px-4 py-2 text-sm text-white focus:border-accent outline-none font-mono w-64"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button type="submit" className="bg-accent text-white px-4 py-2 font-bold uppercase text-xs hover:bg-white hover:text-black transition-colors">
                Scan
              </button>
            </form>
          </div>

          {isLoading ? (
            <div className="flex justify-center py-20">
              <Loader2 className="w-12 h-12 text-accent animate-spin" />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b-2 border-white/10">
                    <th className="py-4 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Callsign</th>
                    <th className="py-4 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Comms Link</th>
                    <th className="py-4 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Clearance</th>
                    <th className="py-4 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Opt-In</th>
                    <th className="py-4 px-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                      <td className="py-4 px-4 font-mono text-white font-bold">{user.username}</td>
                      <td className="py-4 px-4 text-gray-400 text-sm">{user.email}</td>
                      <td className="py-4 px-4">
                        {user.is_staff ? (
                          <span className="inline-block px-2 py-1 bg-accent/20 text-accent text-[10px] font-bold uppercase tracking-widest border border-accent/30">
                            Command
                          </span>
                        ) : (
                          <span className="inline-block px-2 py-1 bg-primary/20 text-primary text-[10px] font-bold uppercase tracking-widest border border-primary/30">
                            Operative
                          </span>
                        )}
                      </td>
                      <td className="py-4 px-4">
                        {user.marketing_opt_in ? (
                          <Check className="w-4 h-4 text-green-500" />
                        ) : (
                          <X className="w-4 h-4 text-red-500 opacity-50" />
                        )}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center">
                          <div className={`w-2 h-2 rounded-full mr-2 ${user.is_verified ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
                          <span className="text-xs text-gray-400 uppercase">{user.is_verified ? 'Active' : 'Pending'}</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
