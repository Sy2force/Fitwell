/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#F6F8FC", // Light background as requested, but we can override for dark mode sections
        "background-dark": "#0B1220", // Deep dark for Gym Mode
        primary: "#2563EB", // Royal Blue
        energy: "#FF6B00", // Blaze Orange
        health: "#14B8A6", // Teal
        surface: "#FFFFFF",
        "surface-dark": "#1F2937",
        text: "#0B1220",
        "text-light": "#F3F4F6",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Orbitron', 'sans-serif'],
        body: ['Inter', 'sans-serif'], 
      },
      backgroundImage: {
        'sport-gradient': 'linear-gradient(135deg, #2563EB 0%, #1a1a2e 100%)',
        'neon-gradient': 'linear-gradient(to right, #2563EB, #14B8A6)',
        'energy-gradient': 'linear-gradient(to right, #FF6B00, #F59E0B)',
      },
      animation: {
        'gradient-x': 'gradient-x 3s ease infinite',
        'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-up': 'slideUp 0.5s ease-out forwards',
      },
      keyframes: {
        'gradient-x': {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center',
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center',
          },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
