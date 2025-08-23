/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  safelist: [
    'text-cyber-blue',
    'text-cyber-green', 
    'text-cyber-purple',
    'text-cyber-yellow',
    'bg-cyber-dark',
    'bg-cyber-blue',
    'bg-cyber-green',
    'bg-cyber-purple',
    'border-cyber-blue',
    'border-cyber-green',
    'neon-text',
    'glass-panel'
  ],
  theme: {
    extend: {
      colors: {
        // Cyberpunk color scheme
        cyber: {
          dark: '#0a0a0f',
          darker: '#050508',
          blue: '#00d4ff',
          green: '#00ff88',
          purple: '#8b5cf6',
          pink: '#ff0080',
          yellow: '#ffff00',
          red: '#ff3333',
          gray: '#1a1a2e',
          'gray-light': '#16213e',
          'blue-glow': '#00d4ff33',
          'green-glow': '#00ff8833',
          'purple-glow': '#8b5cf633',
        }
      },
      fontFamily: {
        'cyber': ['Orbitron', 'Inter', 'monospace'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'scan': 'scan 2s linear infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px currentColor' },
          '100%': { boxShadow: '0 0 20px currentColor, 0 0 30px currentColor' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        scan: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'cyber-grid': 'linear-gradient(rgba(0, 212, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 212, 255, 0.1) 1px, transparent 1px)',
      },
      backgroundSize: {
        'grid': '20px 20px',
      },
    },
  },
  plugins: [],
}
