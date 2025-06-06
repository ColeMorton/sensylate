import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@/components': path.resolve('./src/layouts/components'),
      '@/shortcodes': path.resolve('./src/layouts/shortcodes'),
      '@/helpers': path.resolve('./src/layouts/helpers'),
      '@/partials': path.resolve('./src/layouts/partials'),
      '@': path.resolve('./src')
    }
  }
});