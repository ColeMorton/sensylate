import { features } from "@/lib/config";
import type { FeatureFlags } from "@/types";

/**
 * Hook to check if a specific feature flag is enabled
 * Follows the pattern established by useTheme.ts
 */
export function useFeatureFlag(flag: keyof FeatureFlags): boolean {
  return features[flag];
}

/**
 * Hook to get all feature flags
 * Useful for components that need to check multiple flags
 */
export function useFeatureFlags(): FeatureFlags {
  return features;
}

/**
 * Hook to check multiple feature flags at once
 * Returns true only if ALL specified flags are enabled
 */
export function useAllFeatures(flags: (keyof FeatureFlags)[]): boolean {
  return flags.every((flag) => features[flag]);
}

/**
 * Hook to check if ANY of the specified feature flags are enabled
 * Returns true if at least ONE of the specified flags is enabled
 */
export function useAnyFeature(flags: (keyof FeatureFlags)[]): boolean {
  return flags.some((flag) => features[flag]);
}

export default useFeatureFlag;
