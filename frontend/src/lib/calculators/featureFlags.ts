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

  if (features.calculatorAdvanced) {
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
  return features.calculatorAdvanced;
}

/**
 * Get calculator configuration based on feature flags
 */
export function getCalculatorConfig() {
  return {
    enableAdvancedFeatures: features.calculatorAdvanced,
    enableGraphicalDisplay: features.calculatorAdvanced,
    enableExportFunctions: features.calculatorAdvanced,
    enableHistoryTracking: features.calculatorAdvanced,
  };
}
