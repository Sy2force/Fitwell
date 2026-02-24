/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0f", // Darker, richer background
        primary: "#d4af37", // Luxury Gold
        secondary: "#c0c0c0", // Platinum
        accent: "#ff007a", // Keep the pop of color but maybe use sparingly
        surface: "rgba(255, 255, 255, 0.03)",
        "surface-highlight": "rgba(255, 255, 255, 0.08)",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Orbitron', 'sans-serif'],
        serif: ['Playfair Display', 'serif'], // Add a serif for that luxury feel
      },
      backgroundImage: {
        'luxury-gradient': 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%)',
        'gold-gradient': 'linear-gradient(to right, #d4af37, #f2d06b, #d4af37)',
      },
      animation: {
        'gradient-x': 'gradient-x 15s ease infinite',
        'float': 'float 6s ease-in-out infinite',
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
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      }
    },
  },
  plugins: [],
}
