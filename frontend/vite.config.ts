import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // Adres Twojego backendu
        changeOrigin: true,
        secure: false,
        // Jeśli backend nie ma prefiksu '/api', usuń go:
        // rewrite: (path) => path.replace(/^\/api/, ''),
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  }
})
