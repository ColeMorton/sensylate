import config from "@/config/config.json";
import type { FeatureFlags, EnhancedConfig } from "@/types";

/**
 * Feature flag validation error class
 */
export class FeatureFlagValidationError extends Error {
  constructor(
    public readonly field: string,
    public readonly value: unknown,
    public readonly expectedType: string,
    message?: string,
  ) {
    super(
      message ||
        `Invalid feature flag: ${field}. Expected ${expectedType}, got ${typeof value}`,
    );
    this.name = "FeatureFlagValidationError";
  }
}

/**
 * Enhanced environment variable utilities
 */
function envToBoolean(
  value: string | undefined,
  fieldName?: string,
): boolean | undefined {
  if (value === undefined || value === "") {
    return undefined;
  }

  const normalized = value.toLowerCase().trim();
  if (["true", "1", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["false", "0", "no", "off"].includes(normalized)) {
    return false;
  }

  throw new FeatureFlagValidationError(
    fieldName || "feature_flag",
    value,
    "boolean",
    `Invalid boolean value: "${value}". Expected: true/false, 1/0, yes/no, on/off`,
  );
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
  try {
    return {
      search:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_SEARCH,
          "PUBLIC_FEATURE_SEARCH",
        ) ?? config.settings.search,
      themeSwitcher:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_THEME_SWITCHER,
          "PUBLIC_FEATURE_THEME_SWITCHER",
        ) ?? config.settings.theme_switcher,
      comments:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_COMMENTS,
          "PUBLIC_FEATURE_COMMENTS",
        ) ?? (isDevelopment() ? config.disqus.enable : false),
      gtm:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_GTM,
          "PUBLIC_FEATURE_GTM",
        ) ?? config.google_tag_manager.enable,
      calculators:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_CALCULATORS,
          "PUBLIC_FEATURE_CALCULATORS",
        ) ?? true,
      calculatorAdvanced:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_CALCULATOR_ADVANCED,
          "PUBLIC_FEATURE_CALCULATOR_ADVANCED",
        ) ?? false,
      elementsPage:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_ELEMENTS_PAGE,
          "PUBLIC_FEATURE_ELEMENTS_PAGE",
        ) ?? true,
      authorsPage:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_AUTHORS_PAGE,
          "PUBLIC_FEATURE_AUTHORS_PAGE",
        ) ?? true,
      chartsPage:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_CHARTS_PAGE,
          "PUBLIC_FEATURE_CHARTS_PAGE",
        ) ??
        (isDevelopment() || isStaging()), // Enable in both development and staging branches
      resumePage:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_RESUME_PAGE,
          "PUBLIC_FEATURE_RESUME_PAGE",
        ) ??
        (isDevelopment() || isStaging()), // Enable in both development and staging
      photoBooth:
        envToBoolean(
          import.meta.env.PUBLIC_FEATURE_PHOTO_BOOTH,
          "PUBLIC_FEATURE_PHOTO_BOOTH",
        ) ?? true, // Enable in all environments for E2E testing
    };
  } catch (error) {
    if (error instanceof FeatureFlagValidationError) {
      // Re-throw with enhanced context
      throw new FeatureFlagValidationError(
        error.field,
        error.value,
        error.expectedType,
        `Feature flag validation failed: ${error.message}`,
      );
    }
    throw error;
  }
}

/**
 * Validate feature flag configuration with fail-fast approach
 */
function validateFeatureFlags(flags: FeatureFlags): void {
  const requiredFlags: (keyof FeatureFlags)[] = [
    "search",
    "themeSwitcher",
    "comments",
    "gtm",
    "calculators",
    "calculatorAdvanced",
    "elementsPage",
    "authorsPage",
    "chartsPage",
    "resumePage",
    "photoBooth",
  ];

  for (const flag of requiredFlags) {
    const value = flags[flag];
    if (typeof value !== "boolean") {
      throw new FeatureFlagValidationError(
        flag,
        value,
        "boolean",
        `Invalid feature flag configuration: ${flag} must be boolean, got ${typeof value}`,
      );
    }
  }
}

/**
 * Enhanced configuration object with feature flags
 * Uses fail-fast validation in all environments
 */
function createEnhancedConfig(): EnhancedConfig {
  const features = getFeatureFlags();

  // Always validate configuration for fail-fast approach
  validateFeatureFlags(features);

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
