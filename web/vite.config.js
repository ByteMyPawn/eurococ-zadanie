import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true
    },
    hmr: {
      host: '0.0.0.0'
    }
  },
  preview: {
    port: 5173,
    host: '0.0.0.0'
  },
  optimizeDeps: {
    esbuildOptions: {
      target: 'es2020'
    }
  },
  esbuild: {
    version: '0.19.12',
    target: 'es2020'
  },
  build: {
    target: 'es2020',
    rollupOptions: {
      external: ['esbuild']
    }
  }
})
