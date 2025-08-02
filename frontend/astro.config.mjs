import mdx from "@astrojs/mdx";
import netlify from "@astrojs/netlify";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import AutoImport from "astro-auto-import";
import { defineConfig } from "astro/config";
import remarkCollapse from "remark-collapse";
import remarkToc from "remark-toc";
import sharp from "sharp";
import path from "path";
import config from "./src/config/config.json";
import { FEATURE_FLAGS, getFlagsForEnvironment, getBuildDefineName } from "./src/config/feature-flags.config.ts";

// Build-time feature flag optimization using single source of truth
const getFeatureFlags = () => {
  const envToBoolean = (value) => value?.toLowerCase() === 'true';
  const currentEnv = process.env.NODE_ENV === 'development' ? 'development' :
                    process.env.PUBLIC_ENV === 'staging' ? 'staging' : 'production';

  // Get environment-specific flags from single source
  const configFlags = getFlagsForEnvironment(currentEnv);

  // Allow environment variable overrides (maintains backward compatibility)
  const flags = {};
  for (const flag of FEATURE_FLAGS) {
    const envVar = `PUBLIC_FEATURE_${flag.name.replace(/([A-Z])/g, '_$1').toUpperCase()}`;
    const envValue = envToBoolean(process.env[envVar]);

    // Use env override if present, otherwise use config value
    flags[flag.name] = envValue !== undefined ? envValue : configFlags[flag.name];
  }

  return flags;
};

const buildTimeFlags = getFeatureFlags();

// Use Netlify adapter only for Netlify builds
const adapter = process.env.NETLIFY ? netlify() : undefined;

// Use server mode in development to fix route detection issues, static in production
const outputMode = process.env.NODE_ENV === "development" ? "server" : "static";

// https://astro.build/config
export default defineConfig({
  output: outputMode,
  ...(adapter && { adapter }),
  site: config.site.base_url ? config.site.base_url : "http://examplesite.com",
  base: config.site.base_path ? config.site.base_path : "/",
  trailingSlash: config.site.trailing_slash ? "always" : "never",
  image: {
    service: sharp({
      limitInputPixels: false,
      failOn: 'none',
      quality: 100,
      lossless: true
    }),
    remotePatterns: [{ protocol: "https" }]
  },
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      include: ["three"],
    },
    ssr: {
      noExternal: ["three"],
    },
    define: {
      // Build-time feature flags for dead code elimination
      // Generated from single source of truth with consistent naming
      ...Object.fromEntries(
        FEATURE_FLAGS
          .filter(flag => flag.buildTimeOptimization)
          .map(flag => [getBuildDefineName(flag.name), buildTimeFlags[flag.name]])
      ),
    },
    resolve: {
      alias: {
        '@/components': path.resolve('./src/layouts/components'),
        '@/shortcodes': path.resolve('./src/layouts/shortcodes'),
        '@/helpers': path.resolve('./src/layouts/helpers'),
        '@/partials': path.resolve('./src/layouts/partials'),
        '@/lib': path.resolve('./src/lib'),
        '@/config': path.resolve('./src/config'),
        '@/layouts': path.resolve('./src/layouts'),
        '@/hooks': path.resolve('./src/hooks'),
        '@/types': path.resolve('./src/types'),
        '@': path.resolve('./src')
      }
    }
  },
  integrations: [
    react(),
    sitemap(),
    AutoImport({
      imports: [
        "@/shortcodes/Button",
        "@/shortcodes/Accordion",
        "@/shortcodes/Notice",
        "@/shortcodes/Video",
        "@/shortcodes/Youtube",
        "@/shortcodes/Tabs",
        "@/shortcodes/Tab",
        // Conditional components for tree-shaking
        "@/shortcodes/ConditionalTablerIconShowcase",
        "@/shortcodes/ConditionalChartDisplay",
        "@/shortcodes/ConditionalPhotoBoothDisplay",
        // Original large components replaced with conditional versions:
        // - ChartDisplay -> ConditionalChartDisplay
        // - PhotoBoothDisplay -> ConditionalPhotoBoothDisplay
        // - TablerIconShowcase -> ConditionalTablerIconShowcase
      ],
    }),
    mdx(),
  ],
  markdown: {
    remarkPlugins: [remarkToc, [remarkCollapse, { test: "Table of contents" }]],
    shikiConfig: { theme: "one-dark-pro", wrap: true },
    extendDefaultPlugins: true,
  },
});
