import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import postcssNesting from 'postcss-nesting';

// https://vitejs.dev/config/
export default defineConfig({
  base: '/diary/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  css: {
    postcss: {
      plugins: [
        postcssNesting(),
      ],
    },
  },
})

