/**
 * Conditional Import Utilities for Build-time Dead Code Elimination
 *
 * These utilities enable tree-shaking based on feature flags by using
 * build-time defines (__FEATURE_*) to conditionally import components.
 */

import React, { type ComponentType } from "react";

/**
 * Conditionally import a React component based on a build-time feature flag
 *
 * @param featureEnabled - Build-time boolean define (e.g., __FEATURE_ELEMENTS_PAGE__)
 * @param importFn - Dynamic import function for the component
 * @returns Promise<ComponentType> or null if feature is disabled
 */
export async function conditionalImport<T extends ComponentType<unknown>>(
  featureEnabled: boolean,
  importFn: () => Promise<{ default: T }>,
): Promise<T | null> {
  if (!featureEnabled) {
    return null;
  }

  try {
    const module = await importFn();
    return module.default;
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error("Failed to conditionally import component:", error);
    return null;
  }
}

/**
 * Create a conditional component wrapper that only renders when feature is enabled
 *
 * @param featureEnabled - Build-time boolean define
 * @param importFn - Dynamic import function for the component
 * @returns React component that conditionally renders
 */
export function createConditionalComponent<P extends object>(
  featureEnabled: boolean,
  importFn: () => Promise<{ default: ComponentType<P> }>,
) {
  if (!featureEnabled) {
    // Return empty component for disabled features
    return () => null;
  }

  // Return lazy-loaded component for enabled features
  const LazyComponent = React.lazy(importFn);

  return function ConditionalComponent(props: P) {
    return (
      <React.Suspense fallback={<div>Loading...</div>}>
        <LazyComponent {...props} />
      </React.Suspense>
    );
  };
}

/**
 * Build-time feature flag constants
 * These are replaced by Vite with actual boolean values during build
 */
declare const __FEATURE_SEARCH__: boolean;
declare const __FEATURE_THEME_SWITCHER__: boolean;
declare const __FEATURE_COMMENTS__: boolean;
declare const __FEATURE_GTM__: boolean;
declare const __FEATURE_CALCULATORS__: boolean;
declare const __FEATURE_CALCULATOR_ADVANCED__: boolean;
declare const __FEATURE_ELEMENTS_PAGE__: boolean;
declare const __FEATURE_AUTHORS_PAGE__: boolean;
declare const __FEATURE_CHARTS_PAGE__: boolean;
declare const __FEATURE_PHOTO_BOOTH__: boolean;

/**
 * Build-time feature flag checks
 * These will be tree-shaken out when features are disabled
 */
export const BuildTimeFeatures = {
  search:
    typeof __FEATURE_SEARCH__ !== "undefined" ? __FEATURE_SEARCH__ : false,
  themeSwitcher:
    typeof __FEATURE_THEME_SWITCHER__ !== "undefined"
      ? __FEATURE_THEME_SWITCHER__
      : false,
  comments:
    typeof __FEATURE_COMMENTS__ !== "undefined" ? __FEATURE_COMMENTS__ : false,
  gtm: typeof __FEATURE_GTM__ !== "undefined" ? __FEATURE_GTM__ : false,
  calculators:
    typeof __FEATURE_CALCULATORS__ !== "undefined"
      ? __FEATURE_CALCULATORS__
      : false,
  calculatorAdvanced:
    typeof __FEATURE_CALCULATOR_ADVANCED__ !== "undefined"
      ? __FEATURE_CALCULATOR_ADVANCED__
      : false,
  elementsPage:
    typeof __FEATURE_ELEMENTS_PAGE__ !== "undefined"
      ? __FEATURE_ELEMENTS_PAGE__
      : false,
  authorsPage:
    typeof __FEATURE_AUTHORS_PAGE__ !== "undefined"
      ? __FEATURE_AUTHORS_PAGE__
      : false,
  chartsPage:
    typeof __FEATURE_CHARTS_PAGE__ !== "undefined"
      ? __FEATURE_CHARTS_PAGE__
      : false,
  photoBooth:
    typeof __FEATURE_PHOTO_BOOTH__ !== "undefined"
      ? __FEATURE_PHOTO_BOOTH__
      : false,
} as const;

/**
 * Conditional component imports for major features
 * These will be tree-shaken when features are disabled
 */

// Search Modal - conditionally imported based on search feature
export const SearchModal = BuildTimeFeatures.search
  ? React.lazy(() => import("@/layouts/helpers/SearchModal"))
  : () => null;

// TablerIconShowcase - conditionally imported based on elements page feature
export const TablerIconShowcase = BuildTimeFeatures.elementsPage
  ? React.lazy(() => import("@/layouts/shortcodes/TablerIconShowcase"))
  : () => null;

// ChartDisplay - conditionally imported based on charts feature
export const ChartDisplay = BuildTimeFeatures.chartsPage
  ? React.lazy(() => import("@/layouts/shortcodes/ChartDisplay"))
  : () => null;

// PhotoBoothDisplay - conditionally imported based on photo booth feature
export const PhotoBoothDisplay = BuildTimeFeatures.photoBooth
  ? React.lazy(() => import("@/layouts/shortcodes/PhotoBoothDisplay"))
  : () => null;

// Comments - conditionally imported based on comments feature
export const Disqus = BuildTimeFeatures.comments
  ? React.lazy(() => import("@/layouts/helpers/Disqus"))
  : () => null;

export default BuildTimeFeatures;
