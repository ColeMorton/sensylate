/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
    testTimeout: 30000, // Increased timeout for E2E tests
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/**',
        'dist/**',
        '.astro/**',
        'src/test/**',
        '**/*.d.ts',
        '**/*.config.*',
        'scripts/**'
      ]
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@/components': resolve(__dirname, './src/layouts/components'),
      '@/shortcodes': resolve(__dirname, './src/layouts/shortcodes'),
      '@/helpers': resolve(__dirname, './src/layouts/helpers'),
      '@/partials': resolve(__dirname, './src/layouts/partials'),
      '@/lib': resolve(__dirname, './src/lib'),
      '@/config': resolve(__dirname, './src/config'),
      '@/layouts': resolve(__dirname, './src/layouts'),
      '@/hooks': resolve(__dirname, './src/hooks'),
      '@/types': resolve(__dirname, './src/types')
    }
  }
});