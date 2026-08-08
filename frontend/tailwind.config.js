/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        base: {
          50:  '#fafafa', 100: '#f4f4f5', 200: '#e4e4e7', 300: '#d4d4d8',
          400: '#a1a1aa', 500: '#71717a', 600: '#52525b', 700: '#3f3f46',
          800: '#27272a', 900: '#18181b', 950: '#09090b'
        },
        brand: {
          50:  '#ecfdf5', 100: '#d1fae5', 200: '#a7f3d0', 300: '#6ee7b7',
          400: '#34d399', 500: '#10b981', 600: '#059669', 700: '#047857',
          800: '#065f46', 900: '#064e3b', 950: '#022c22'
        },
        accent: {
          50:  '#eef2ff', 100: '#e0e7ff', 200: '#c7d2fe', 300: '#a5b4fc',
          400: '#818cf8', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca',
          800: '#3730a3', 900: '#312e81'
        },
        success: { 50: '#ecfdf5', 100: '#d1fae5', 400: '#34d399', 500: '#10b981', 600: '#059669', 700: '#047857' },
        warning: { 50: '#fffbeb', 100: '#fef3c7', 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706', 700: '#b45309' },
        danger:  { 50: '#fef2f2', 100: '#fee2e2', 400: '#f87171', 500: '#ef4444', 600: '#dc2626', 700: '#b91c1c' },

        // Flat structure for Tailwind
        app: {
          bg:      '#fafafa',
          'bg-dark': '#09090b',
          panel:   '#ffffff',
          'panel-dark': '#0f0f10',
          border:  '#e4e4e7',
          'border-dark': '#27272a',
          subtle:  '#f4f4f5',
          'subtle-dark': '#18181b',
          hover:   '#f4f4f5',
          'hover-dark': '#1f1f23',
          active:  '#e4e4e7',
          'active-dark': '#27272a'
        }
      },

      fontFamily: {
        sans: ['Vazirmatn', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace']
      },

      fontSize: {
        '2xs':  ['0.625rem',  { lineHeight: '0.875rem' }],
        'xs':   ['0.75rem',   { lineHeight: '1rem' }],
        'sm':   ['0.8125rem', { lineHeight: '1.25rem' }],
        'base': ['0.875rem',  { lineHeight: '1.25rem' }],
        'lg':   ['1rem',      { lineHeight: '1.5rem' }],
        'xl':   ['1.125rem',  { lineHeight: '1.75rem' }],
        '2xl':  ['1.5rem',    { lineHeight: '2rem' }],
        '3xl':  ['1.875rem',  { lineHeight: '2.25rem' }],
        '4xl':  ['2.25rem',   { lineHeight: '2.5rem' }]
      },

      letterSpacing: { tighter: '-0.035em', tight: '-0.025em', wide: '0.025em' },

      borderRadius: { sm: '4px', md: '6px', lg: '8px', xl: '10px', '2xl': '14px' },

      boxShadow: {
        'xs':    '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'sm':    '0 1px 3px 0 rgb(0 0 0 / 0.08), 0 1px 2px -1px rgb(0 0 0 / 0.05)',
        'md':    '0 4px 6px -1px rgb(0 0 0 / 0.06), 0 2px 4px -2px rgb(0 0 0 / 0.05)',
        'lg':    '0 10px 15px -3px rgb(0 0 0 / 0.06), 0 4px 6px -4px rgb(0 0 0 / 0.04)',
        'xl':    '0 20px 25px -5px rgb(0 0 0 / 0.08), 0 8px 10px -6px rgb(0 0 0 / 0.04)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.04)',
        'focus': '0 0 0 3px rgb(16 185 129 / 0.15)',
        'glow':  '0 0 40px -10px rgb(16 185 129 / 0.4)'
      },

      animation: {
        'fade-in':       'fadeIn 0.2s ease-out',
        'slide-up':      'slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-down':    'slideDown 0.2s ease-out',
        'scale-in':      'scaleIn 0.15s ease-out',
        'shimmer':       'shimmer 1.8s linear infinite',
        'pulse-subtle':  'pulseSubtle 2s ease-in-out infinite'
      },

      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp: { '0%': { transform: 'translateY(8px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } },
        slideDown: { '0%': { transform: 'translateY(-4px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } },
        scaleIn: { '0%': { transform: 'scale(0.96)', opacity: '0' }, '100%': { transform: 'scale(1)', opacity: '1' } },
        shimmer: { '0%': { backgroundPosition: '-400px 0' }, '100%': { backgroundPosition: '400px 0' } },
        pulseSubtle: { '0%, 100%': { opacity: '1' }, '50%': { opacity: '0.6' } }
      },

      maxWidth: { sidebar: '240px', 'sidebar-lg': '280px', content: '1400px' },

      zIndex: { dropdown: 1000, sticky: 1020, sidebar: 1030, modal: 1060, command: 1070, toast: 1080, tooltip: 1090 }
    }
  },
  plugins: []
}
