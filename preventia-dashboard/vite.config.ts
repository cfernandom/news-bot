import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    // Optimize chunk splitting for better performance
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunk for React and core libraries
          vendor: ['react', 'react-dom'],
          // UI libraries chunk
          ui: ['@tanstack/react-query', 'framer-motion'],
          // Charts chunk
          charts: ['recharts'],
          // Utils chunk
          utils: ['axios', 'clsx', 'tailwind-merge']
        }
      }
    },
    // Increase chunk size warning limit for medical dashboard
    chunkSizeWarningLimit: 1000,
    // Enable source maps for production debugging
    sourcemap: false,
    // Optimize for production
    minify: 'esbuild'
  },
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})
