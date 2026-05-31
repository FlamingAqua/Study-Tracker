import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './hooks/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eefbf9',
          100: '#d3f6f1',
          200: '#a7ebe2',
          300: '#78d8cf',
          400: '#4bc0b5',
          500: '#2aa69d',
          600: '#1f827d',
          700: '#1d6864',
          800: '#1d5552',
          900: '#184746',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(15, 23, 42, 0.08)',
      },
      backgroundImage: {
        'medical-gradient': 'linear-gradient(135deg, rgba(42,166,157,0.12), rgba(255,255,255,0.8))',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.25s ease-out',
      },
    },
  },
  plugins: [],
}

export default config
