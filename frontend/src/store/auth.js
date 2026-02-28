import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from '../api/axios'

const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await axios.post('auth/token/', { email, password })
          const { access, refresh } = response.data
          
          localStorage.setItem('access_token', access)
          localStorage.setItem('refresh_token', refresh)
          
          // Fetch full user profile
          const profileResponse = await axios.get('auth/profile/')
          
          set({ 
            user: profileResponse.data, 
            isAuthenticated: true, 
            isLoading: false 
          })
          return true
        } catch (error) {
          set({ 
            error: error.response?.data?.detail || 'Login failed', 
            isLoading: false 
          })
          return false
        }
      },

      register: async (userData) => {
        set({ isLoading: true, error: null })
        try {
          await axios.post('auth/register/', userData)
          set({ isLoading: false })
          return { success: true }
        } catch (error) {
          let errorMessage = 'Registration failed'
          if (error.response?.data) {
            const data = error.response.data
            // Check for specific field errors
            if (data.username) errorMessage = data.username[0]
            else if (data.email) errorMessage = data.email[0]
            else if (data.password) errorMessage = data.password[0]
            else if (data.detail) errorMessage = data.detail
            else if (Array.isArray(data)) errorMessage = data[0]
            else {
              // Join all error messages if multiple
              const messages = Object.values(data).flat()
              if (messages.length > 0) errorMessage = messages[0]
            }
          }
          
          set({ 
            error: errorMessage, 
            isLoading: false 
          })
          return { success: false, error: errorMessage }
        }
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, isAuthenticated: false })
      },

      updateUser: (userData) => {
        set((state) => ({
          user: { ...state.user, ...userData }
        }))
      },
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage,
    }
  )
)

export default useAuthStore
