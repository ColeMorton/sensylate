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

// Build-time feature flag optimization
const getFeatureFlags = () => {
  const envToBoolean = (value) => value?.toLowerCase() === 'true';
  return {
    search: envToBoolean(process.env.PUBLIC_FEATURE_SEARCH) ?? config.settings.search,
    theme_switcher: envToBoolean(process.env.PUBLIC_FEATURE_THEME_SWITCHER) ?? config.settings.theme_switcher,
    comments: envToBoolean(process.env.PUBLIC_FEATURE_COMMENTS) ?? config.disqus.enable,
    gtm: envToBoolean(process.env.PUBLIC_FEATURE_GTM) ?? config.google_tag_manager.enable,
    calculators: envToBoolean(process.env.PUBLIC_FEATURE_CALCULATORS) ?? true,
    calculator_advanced: envToBoolean(process.env.PUBLIC_FEATURE_CALCULATOR_ADVANCED) ?? false,
    elements_page: envToBoolean(process.env.PUBLIC_FEATURE_ELEMENTS_PAGE) ?? true,
    authors_page: envToBoolean(process.env.PUBLIC_FEATURE_AUTHORS_PAGE) ?? true
  };
};

const buildTimeFlags = getFeatureFlags();

// Use Netlify adapter only for Netlify builds
const adapter = process.env.NETLIFY ? netlify() : undefined;

// https://astro.build/config
export default defineConfig({
  output: "static",
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
      __FEATURE_SEARCH__: buildTimeFlags.search,
      __FEATURE_THEME_SWITCHER__: buildTimeFlags.theme_switcher,
      __FEATURE_COMMENTS__: buildTimeFlags.comments,
      __FEATURE_GTM__: buildTimeFlags.gtm,
      __FEATURE_CALCULATORS__: buildTimeFlags.calculators,
      __FEATURE_CALCULATOR_ADVANCED__: buildTimeFlags.calculator_advanced,
      __FEATURE_ELEMENTS_PAGE__: buildTimeFlags.elements_page,
      __FEATURE_AUTHORS_PAGE__: buildTimeFlags.authors_page,
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
