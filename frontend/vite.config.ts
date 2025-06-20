import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: true,
  },  
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@/components/*": path.resolve(__dirname, "./src/components/*"),
      "@/lib/*": path.resolve(__dirname, "./src/lib/*"),
      "@/assets/*": path.resolve(__dirname, "./src/assets/*"),
      "@/pages/*": path.resolve(__dirname, "./src/pages/*"),
    },
  },
  assetsInclude: ['**/*.svg'],
})
