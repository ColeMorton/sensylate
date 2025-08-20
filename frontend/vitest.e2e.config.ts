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
    testTimeout: 60000, // Longer timeout for E2E tests
    hookTimeout: 30000, // Longer hook timeout for setup/teardown
    globalSetup: [
      // E2E tests need the global setup for application build
      './src/test/photo-booth/e2e/globalSetup.ts'
    ],
    include: [
      // Only include E2E tests
      'src/test/e2e/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
      'src/test/photo-booth/e2e/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
      'src/test/**/e2e/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'
    ],
    exclude: [
      'node_modules/**',
      // Exclude unit tests from E2E runs
      'src/test/components/**',
      'src/test/hooks/**',
      'src/test/photo-booth/unit/**',
      'src/test/photo-booth/integration/**'
    ],
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
      '@/components': resolve(__dirname, './src/layouts/components'),
      '@/shortcodes': resolve(__dirname, './src/layouts/shortcodes'),
      '@/helpers': resolve(__dirname, './src/layouts/helpers'),
      '@/partials': resolve(__dirname, './src/layouts/partials'),
      '@/lib': resolve(__dirname, './src/lib'),
      '@/config': resolve(__dirname, './src/config'),
      '@/layouts': resolve(__dirname, './src/layouts'),
      '@/hooks': resolve(__dirname, './src/hooks'),
      '@/types': resolve(__dirname, './src/types'),
      '@/services': resolve(__dirname, './src/services'),
      '@': resolve(__dirname, './src')
    }
  }
});
