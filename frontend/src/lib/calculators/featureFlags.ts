import { features } from "@/lib/featureFlags";

/**
 * Calculator feature flag integration example
 * Demonstrates how to use feature flags in the calculator system
 */

/**
 * Get available calculators based on feature flags
 */
export function getAvailableCalculators(): string[] {
  const baseCalculators = ["pocket", "dca", "mortgage"];

  if (features.calculator_advanced) {
    return [
      ...baseCalculators,
      "compound-interest",
      "roi-tracker",
      "tax-calculator",
    ];
  }

  return baseCalculators;
}

/**
 * Check if advanced calculator features are enabled
 */
export function isAdvancedCalculatorEnabled(): boolean {
  return features.calculator_advanced;
}

/**
 * Get calculator configuration based on feature flags
 */
export function getCalculatorConfig() {
  return {
    enableAdvancedFeatures: features.calculator_advanced,
    enableGraphicalDisplay: features.calculator_advanced,
    enableExportFunctions: features.calculator_advanced,
    enableHistoryTracking: features.calculator_advanced,
  };
}
