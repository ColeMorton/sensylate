import config from "@/config/config.json";
import type { FeatureFlags, EnhancedConfig } from "@/types";

/**
 * Environment variable utilities
 */
function envToBoolean(value: string | undefined): boolean | undefined {
  if (value === undefined || value === "") {
    return undefined;
  }
  return value.toLowerCase() === "true";
}

function isDevelopment(): boolean {
  return import.meta.env.DEV || import.meta.env.PUBLIC_ENV === "development";
}

function isProduction(): boolean {
  return import.meta.env.PROD || import.meta.env.PUBLIC_ENV === "production";
}

function isStaging(): boolean {
  return import.meta.env.PUBLIC_ENV === "staging";
}

/**
 * Feature flag configuration with environment variable overrides
 * Environment variables take precedence over static configuration
 */
function getFeatureFlags(): FeatureFlags {
  return {
    search:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_SEARCH) ??
      config.settings.search,
    theme_switcher:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_THEME_SWITCHER) ??
      config.settings.theme_switcher,
    comments:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_COMMENTS) ??
      (isDevelopment() ? config.disqus.enable : false),
    gtm:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_GTM) ??
      config.google_tag_manager.enable,
    calculators: true, // Always enabled - critical feature
    calculator_advanced:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_CALCULATOR_ADVANCED) ?? false,
    elements_page:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_ELEMENTS_PAGE) ?? true,
    authors_page:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_AUTHORS_PAGE) ?? true,
    charts_page:
      envToBoolean(import.meta.env.PUBLIC_FEATURE_CHARTS_PAGE) ??
      isDevelopment(),
  };
}

/**
 * Validate feature flag configuration
 */
function validateFeatureFlags(flags: FeatureFlags): void {
  const requiredFlags = [
    "search",
    "theme_switcher",
    "comments",
    "gtm",
    "calculators",
    "calculator_advanced",
    "elements_page",
    "authors_page",
    "charts_page",
  ];

  for (const flag of requiredFlags) {
    if (typeof flags[flag as keyof FeatureFlags] !== "boolean") {
      throw new Error(
        `Invalid feature flag configuration: ${flag} must be boolean`,
      );
    }
  }
}

/**
 * Enhanced configuration object with feature flags
 */
function createEnhancedConfig(): EnhancedConfig {
  const features = getFeatureFlags();

  // Validate configuration in development
  if (isDevelopment()) {
    validateFeatureFlags(features);
  }

  return {
    ...config,
    features,
  };
}

/**
 * Main configuration export with environment-aware feature flags
 */
export const enhancedConfig = createEnhancedConfig();

/**
 * Environment detection utilities
 */
export const env = {
  isDevelopment,
  isProduction,
  isStaging,
  current:
    import.meta.env.PUBLIC_ENV ||
    (import.meta.env.DEV ? "development" : "production"),
};

/**
 * Direct feature flag access
 */
export const features = enhancedConfig.features;

/**
 * Legacy config for backward compatibility
 */
export default enhancedConfig;
