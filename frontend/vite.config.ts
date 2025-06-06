import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@/components': path.resolve('./src/layouts/components'),
      '@/shortcodes': path.resolve('./src/layouts/shortcodes'),
      '@/helpers': path.resolve('./src/layouts/helpers'),
      '@/partials': path.resolve('./src/layouts/partials'),
      '@/lib': path.resolve('./src/lib'),
      '@/config': path.resolve('./src/config'),
      '@/layouts': path.resolve('./src/layouts'),
      '@': path.resolve('./src')
    }
  }
});