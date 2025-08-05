/**
 * Build-time Feature Flag Constants
 *
 * This module provides access to build-time feature flags that are defined
 * in astro.config.mjs using Vite's define option. These constants enable
 * dead code elimination when features are disabled.
 *
 * IMPORTANT: These constants are replaced at build time with their actual
 * boolean values, allowing bundlers to eliminate unused code branches.
 */

// Declare global build-time constants that are defined by Vite
declare const __FEATURE_PHOTO_BOOTH__: boolean;
declare const __FEATURE_ELEMENTS_PAGE__: boolean;
declare const __FEATURE_CHARTS_PAGE__: boolean;

// Debug logging for build-time constants
console.log("🔍 Build-time constants debug:");
console.log(
  "  __FEATURE_PHOTO_BOOTH__:",
  typeof __FEATURE_PHOTO_BOOTH__ !== "undefined"
    ? __FEATURE_PHOTO_BOOTH__
    : "UNDEFINED",
);
console.log(
  "  __FEATURE_ELEMENTS_PAGE__:",
  typeof __FEATURE_ELEMENTS_PAGE__ !== "undefined"
    ? __FEATURE_ELEMENTS_PAGE__
    : "UNDEFINED",
);
console.log(
  "  __FEATURE_CHARTS_PAGE__:",
  typeof __FEATURE_CHARTS_PAGE__ !== "undefined"
    ? __FEATURE_CHARTS_PAGE__
    : "UNDEFINED",
);

/**
 * Build-time feature flags for conditional imports and dead code elimination.
 * These values are resolved at build time and allow for complete removal
 * of disabled features from the final bundle.
 */
export const BuildTimeFeatures = {
  /**
   * Photo booth feature flag
   * Controls whether PhotoBoothDisplay component is included in the build
   */
  photoBooth: __FEATURE_PHOTO_BOOTH__,

  /**
   * Elements page feature flag
   * Controls whether TablerIconShowcase component is included in the build
   */
  elementsPage: __FEATURE_ELEMENTS_PAGE__,

  /**
   * Charts page feature flag
   * Controls whether ChartDisplay component is included in the build
   */
  chartsPage: __FEATURE_CHARTS_PAGE__,
} as const;

export type BuildTimeFeaturesType = typeof BuildTimeFeatures;
