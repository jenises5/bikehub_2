/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: '#FAF7F2',
          deep: '#F5F1E8',
          dark: '#EDE6D6',
        },
        clay: {
          50:  '#FBF1ED',
          100: '#F4D9CB',
          200: '#EBBAA1',
          300: '#DC8A66',
          400: '#C2603A',
          500: '#A8451F',
          600: '#993C1D',
          700: '#7E2F15',
          800: '#5A2410',
          900: '#3D180B',
        },
        forest: {
          50:  '#EFF5EC',
          100: '#D4E5C9',
          400: '#5C8A3F',
          600: '#3F6B26',
          800: '#1F3D14',
          900: '#163E2A',
        },
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        sans:    ['Geist', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.6875rem', { lineHeight: '1rem' }],
      },
      letterSpacing: {
        wider: '0.04em',
        widest: '0.08em',
      },
      borderRadius: {
        DEFAULT: '6px',
        lg: '10px',
        xl: '14px',
      },
      boxShadow: {
        soft: '0 1px 2px rgba(28,25,23,0.04), 0 4px 12px rgba(28,25,23,0.04)',
      },
    },
  },
  plugins: [],
}