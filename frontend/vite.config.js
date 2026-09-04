import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve('./src'),
    },
    css: {
      preprocessorOptions: {
        scss: {
          // Automatically injects the global file into all SCSS modules
          additionalData: `@use "@/styles/_globals.scss" as *;`
        }
      }
    }
  },  
})