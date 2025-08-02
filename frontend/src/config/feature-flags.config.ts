/**
 * Feature Flag System Configuration - Single Source of Truth
 *
 * This file defines all feature flags and their environment-specific values.
 * All other configuration files (.env.*, netlify.toml) are generated from this schema.
 *
 * IMPORTANT: This is the ONLY place to define feature flags.
 * DO NOT manually edit environment files - use the generation scripts.
 */

// Schema Types
export interface FeatureFlagDefinition {
  /** Unique identifier for the feature flag (camelCase) */
  name: string;
  /** Human-readable description of what this flag controls */
  description: string;
  /** Category for organizing flags */
  category: "ui" | "api" | "experimental" | "analytics" | "performance";
  /** Default value if no environment-specific value is set */
  defaultValue: boolean;
  /** Environment-specific flag values */
  environments: {
    development: boolean;
    staging: boolean;
    production: boolean;
  };
  /** Optional dependencies - other flags that must be enabled for this to work */
  dependencies?: string[];
  /** Whether this flag should be available for build-time dead code elimination */
  buildTimeOptimization?: boolean;
}

export interface FeatureFlagConfig {
  flags: FeatureFlagDefinition[];
  metadata: {
    version: string;
    lastUpdated: string;
    generatedFrom: string;
  };
}

// Feature Flag Definitions
export const FEATURE_FLAGS: FeatureFlagDefinition[] = [
  {
    name: "search",
    description: "Enable site-wide search functionality",
    category: "ui",
    defaultValue: true,
    environments: {
      development: true,
      staging: true,
      production: true,
    },
    buildTimeOptimization: true,
  },
  {
    name: "themeSwitcher",
    description: "Enable dark/light theme switcher in header",
    category: "ui",
    defaultValue: true,
    environments: {
      development: true,
      staging: true,
      production: true,
    },
    buildTimeOptimization: true,
  },
  {
    name: "comments",
    description: "Enable Disqus comments on blog posts",
    category: "ui",
    defaultValue: false,
    environments: {
      development: false,
      staging: false,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "gtm",
    description: "Enable Google Tag Manager analytics tracking",
    category: "analytics",
    defaultValue: false,
    environments: {
      development: false,
      staging: false,
      production: true,
    },
    buildTimeOptimization: true,
  },
  {
    name: "calculators",
    description: "Enable financial calculators section",
    category: "ui",
    defaultValue: true,
    environments: {
      development: true,
      staging: false,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "calculatorAdvanced",
    description: "Enable advanced calculator features",
    category: "ui",
    defaultValue: false,
    dependencies: ["calculators"],
    environments: {
      development: true,
      staging: true,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "elementsPage",
    description: "Enable UI elements showcase page",
    category: "ui",
    defaultValue: true,
    environments: {
      development: true,
      staging: true,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "authorsPage",
    description: "Enable authors listing page",
    category: "ui",
    defaultValue: true,
    environments: {
      development: true,
      staging: true,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "chartsPage",
    description: "Enable interactive charts page",
    category: "ui",
    defaultValue: false,
    environments: {
      development: true,
      staging: true,
      production: false,
    },
    buildTimeOptimization: true,
  },
  {
    name: "photoBooth",
    description: "Enable photo booth feature",
    category: "experimental",
    defaultValue: false,
    environments: {
      development: true,
      staging: true,
      production: false,
    },
    buildTimeOptimization: true,
  },
];

// Configuration Export
export const featureFlagConfig: FeatureFlagConfig = {
  flags: FEATURE_FLAGS,
  metadata: {
    version: "1.0.0",
    lastUpdated: new Date().toISOString(),
    generatedFrom: "frontend/src/config/feature-flags.config.ts",
  },
};

// Helper Functions
export function getFlagByName(name: string): FeatureFlagDefinition | undefined {
  return FEATURE_FLAGS.find((flag) => flag.name === name);
}

export function getFlagsByCategory(
  category: FeatureFlagDefinition["category"],
): FeatureFlagDefinition[] {
  return FEATURE_FLAGS.filter((flag) => flag.category === category);
}

export function getFlagsForEnvironment(
  environment: keyof FeatureFlagDefinition["environments"],
): Record<string, boolean> {
  return FEATURE_FLAGS.reduce(
    (acc, flag) => {
      acc[flag.name] = flag.environments[environment];
      return acc;
    },
    {} as Record<string, boolean>,
  );
}

export function validateFlagDependencies(): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];
  const flagNames = FEATURE_FLAGS.map((f) => f.name);

  for (const flag of FEATURE_FLAGS) {
    if (flag.dependencies) {
      for (const dep of flag.dependencies) {
        if (!flagNames.includes(dep)) {
          errors.push(
            `Flag '${flag.name}' depends on non-existent flag '${dep}'`,
          );
        }
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

// Environment Variable Name Mapping
export function getEnvVarName(flagName: string): string {
  // Convert camelCase to SCREAMING_SNAKE_CASE for environment variables
  return `PUBLIC_FEATURE_${flagName.replace(/([A-Z])/g, "_$1").toUpperCase()}`;
}

export function getBuildDefineName(flagName: string): string {
  // Convert camelCase to SCREAMING_SNAKE_CASE for build defines
  return `__FEATURE_${flagName.replace(/([A-Z])/g, "_$1").toUpperCase()}__`;
}

export default featureFlagConfig;
