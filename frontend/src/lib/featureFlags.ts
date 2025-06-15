import { features } from "@/lib/config";
import type { FeatureFlags } from "@/types";

/**
 * Check if a specific feature flag is enabled
 * For use in Astro components and server-side rendering
 */
export function isFeatureEnabled(flag: keyof FeatureFlags): boolean {
  return features[flag];
}

/**
 * Check if multiple feature flags are ALL enabled
 * Returns true only if ALL specified flags are enabled
 */
export function areAllFeaturesEnabled(flags: (keyof FeatureFlags)[]): boolean {
  return flags.every((flag) => features[flag]);
}

/**
 * Check if ANY of the specified feature flags are enabled
 * Returns true if at least ONE of the specified flags is enabled
 */
export function isAnyFeatureEnabled(flags: (keyof FeatureFlags)[]): boolean {
  return flags.some((flag) => features[flag]);
}

/**
 * Get all feature flags
 * Direct access to the features object
 */
export { features };

/**
 * Feature flag debugging utilities
 * Only available in development mode
 */
export const debug = {
  /**
   * Log all feature flags to console (development only)
   */
  logFlags: () => {
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.log("🚩 Feature Flags:", features);
    }
  },

  /**
   * Get feature flag summary as string (development only)
   */
  getFlagSummary: (): string => {
    if (!import.meta.env.DEV) {
      return "";
    }

    const enabled = Object.entries(features)
      .filter(([_, value]) => value)
      .map(([key]) => key);

    const disabled = Object.entries(features)
      .filter(([_, value]) => !value)
      .map(([key]) => key);

    return `Enabled: ${enabled.join(", ")} | Disabled: ${disabled.join(", ")}`;
  },
};
