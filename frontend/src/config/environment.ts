/**
 * Environment Configuration and Validation
 *
 * Provides type-safe environment variable access with validation
 * and fail-fast error handling for missing or invalid configuration.
 */

export interface EnvironmentConfig {
  // Environment Identification
  env: "development" | "staging" | "production";
  nodeEnv: string;

  // Site Configuration
  siteUrl: string;
  siteTitle: string;
  siteDescription: string;

  // Feature Flags
  features: {
    search: boolean;
    themeSwitcher: boolean;
    comments: boolean;
    gtm: boolean;
    calculators: boolean;
    calculatorAdvanced: boolean;
    elementsPage: boolean;
    authorsPage: boolean;
  };

  // Build Configuration
  astroDevMode: boolean;

  // API Configuration
  apiBaseUrl: string;
  contactFormEndpoint: string;

  // Performance Configuration
  enableWebVitals: boolean;
  enablePerformanceMonitoring: boolean;

  // Security Configuration
  cspReportUri: string;
  securityHeadersEnabled: boolean;

  // Analytics Configuration
  analyticsEnabled: boolean;
}

/**
 * Validation errors for environment configuration
 */
export class EnvironmentValidationError extends Error {
  constructor(
    public readonly field: string,
    public readonly value: unknown,
    public readonly expectedType: string,
    message?: string,
  ) {
    super(
      message ||
        `Invalid environment variable: ${field}. Expected ${expectedType}, got ${typeof value}`,
    );
    this.name = "EnvironmentValidationError";
  }
}

/**
 * Parse a string environment variable to boolean
 * Accepts: 'true', 'false', '1', '0', 'yes', 'no' (case insensitive)
 */
function parseBoolean(
  value: string | undefined,
  defaultValue: boolean = false,
): boolean {
  if (!value) {
    return defaultValue;
  }

  const normalized = value.toLowerCase().trim();
  if (["true", "1", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["false", "0", "no", "off"].includes(normalized)) {
    return false;
  }

  throw new EnvironmentValidationError(
    "boolean_value",
    value,
    "boolean",
    `Invalid boolean value: "${value}". Expected: true/false, 1/0, yes/no, on/off`,
  );
}

/**
 * Validate required string environment variable
 */
function requireString(value: string | undefined, fieldName: string): string {
  if (!value || value.trim() === "") {
    throw new EnvironmentValidationError(
      fieldName,
      value,
      "non-empty string",
      `Required environment variable ${fieldName} is missing or empty`,
    );
  }
  return value.trim();
}

/**
 * Validate URL format
 */
function validateUrl(value: string, fieldName: string): string {
  try {
    new URL(value);
    return value;
  } catch {
    throw new EnvironmentValidationError(
      fieldName,
      value,
      "valid URL",
      `Invalid URL format for ${fieldName}: "${value}"`,
    );
  }
}

/**
 * Validate environment value against allowed options
 */
function validateEnum<T extends string>(
  value: string | undefined,
  fieldName: string,
  allowedValues: readonly T[],
  defaultValue?: T,
): T {
  if (!value) {
    if (defaultValue !== undefined) {
      return defaultValue;
    }
    throw new EnvironmentValidationError(
      fieldName,
      value,
      `one of: ${allowedValues.join(", ")}`,
      `Required environment variable ${fieldName} is missing`,
    );
  }

  if (!allowedValues.includes(value as T)) {
    throw new EnvironmentValidationError(
      fieldName,
      value,
      `one of: ${allowedValues.join(", ")}`,
      `Invalid value for ${fieldName}: "${value}"`,
    );
  }

  return value as T;
}

/**
 * Load and validate environment configuration
 * Throws EnvironmentValidationError for any validation failures
 */
export function loadEnvironmentConfig(): EnvironmentConfig {
  try {
    // Environment identification
    const env = validateEnum(import.meta.env.PUBLIC_ENV, "PUBLIC_ENV", [
      "development",
      "staging",
      "production",
    ] as const);

    const nodeEnv = import.meta.env.NODE_ENV || "development";

    // Site configuration
    const siteUrl = validateUrl(
      requireString(import.meta.env.PUBLIC_SITE_URL, "PUBLIC_SITE_URL"),
      "PUBLIC_SITE_URL",
    );

    const siteTitle = requireString(
      import.meta.env.PUBLIC_SITE_TITLE,
      "PUBLIC_SITE_TITLE",
    );
    const siteDescription = requireString(
      import.meta.env.PUBLIC_SITE_DESCRIPTION,
      "PUBLIC_SITE_DESCRIPTION",
    );

    // Feature flags with defaults
    const features = {
      search: parseBoolean(import.meta.env.PUBLIC_FEATURE_SEARCH, true),
      themeSwitcher: parseBoolean(
        import.meta.env.PUBLIC_FEATURE_THEME_SWITCHER,
        true,
      ),
      comments: parseBoolean(import.meta.env.PUBLIC_FEATURE_COMMENTS, false),
      gtm: parseBoolean(import.meta.env.PUBLIC_FEATURE_GTM, false),
      calculators: parseBoolean(
        import.meta.env.PUBLIC_FEATURE_CALCULATORS,
        true,
      ),
      calculatorAdvanced: parseBoolean(
        import.meta.env.PUBLIC_FEATURE_CALCULATOR_ADVANCED,
        false,
      ),
      elementsPage: parseBoolean(
        import.meta.env.PUBLIC_FEATURE_ELEMENTS_PAGE,
        true,
      ),
      authorsPage: parseBoolean(
        import.meta.env.PUBLIC_FEATURE_AUTHORS_PAGE,
        true,
      ),
    };

    // Build configuration
    const astroDevMode = parseBoolean(
      import.meta.env.ASTRO_DEV_MODE,
      env === "development",
    );

    // API configuration
    const apiBaseUrl = validateUrl(
      requireString(import.meta.env.PUBLIC_API_BASE_URL, "PUBLIC_API_BASE_URL"),
      "PUBLIC_API_BASE_URL",
    );

    const contactFormEndpoint = requireString(
      import.meta.env.PUBLIC_CONTACT_FORM_ENDPOINT,
      "PUBLIC_CONTACT_FORM_ENDPOINT",
    );

    // Performance configuration
    const enableWebVitals = parseBoolean(
      import.meta.env.PUBLIC_ENABLE_WEB_VITALS,
      env !== "production",
    );
    const enablePerformanceMonitoring = parseBoolean(
      import.meta.env.PUBLIC_ENABLE_PERFORMANCE_MONITORING,
      true,
    );

    // Security configuration
    const cspReportUri = import.meta.env.PUBLIC_CSP_REPORT_URI || "";
    const securityHeadersEnabled = parseBoolean(
      import.meta.env.PUBLIC_SECURITY_HEADERS_ENABLED,
      env !== "development",
    );

    // Analytics configuration
    const analyticsEnabled = parseBoolean(
      import.meta.env.PUBLIC_ANALYTICS_ENABLED,
      env === "production",
    );

    return {
      env,
      nodeEnv,
      siteUrl,
      siteTitle,
      siteDescription,
      features,
      astroDevMode,
      apiBaseUrl,
      contactFormEndpoint,
      enableWebVitals,
      enablePerformanceMonitoring,
      cspReportUri,
      securityHeadersEnabled,
      analyticsEnabled,
    };
  } catch (error) {
    if (error instanceof EnvironmentValidationError) {
      // Re-throw with enhanced context
      throw new EnvironmentValidationError(
        error.field,
        error.value,
        error.expectedType,
        `Environment validation failed: ${error.message}`,
      );
    }

    // Wrap unexpected errors
    throw new EnvironmentValidationError(
      "unknown",
      error,
      "valid configuration",
      `Unexpected error during environment validation: ${error instanceof Error ? error.message : String(error)}`,
    );
  }
}

/**
 * Cached environment configuration
 * Loaded once and reused throughout the application
 */
let cachedConfig: EnvironmentConfig | null = null;

/**
 * Get the validated environment configuration
 * Uses caching to avoid repeated validation
 */
export function getEnvironmentConfig(): EnvironmentConfig {
  if (!cachedConfig) {
    cachedConfig = loadEnvironmentConfig();
  }
  return cachedConfig;
}

/**
 * Check if we're running in development mode
 */
export function isDevelopment(): boolean {
  return getEnvironmentConfig().env === "development";
}

/**
 * Check if we're running in staging mode
 */
export function isStaging(): boolean {
  return getEnvironmentConfig().env === "staging";
}

/**
 * Check if we're running in production mode
 */
export function isProduction(): boolean {
  return getEnvironmentConfig().env === "production";
}

/**
 * Get feature flag status
 */
export function isFeatureEnabled(
  feature: keyof EnvironmentConfig["features"],
): boolean {
  return getEnvironmentConfig().features[feature];
}
