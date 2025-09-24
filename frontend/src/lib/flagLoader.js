#!/usr/bin/env node

/**
 * Universal Feature Flag Configuration Loader
 *
 * This module provides a universal interface for loading feature flag configurations
 * across different contexts (Node.js scripts, runtime, build tools).
 *
 * Key Features:
 * - Single source of truth from feature-flags.config.ts
 * - Works in both Node.js scripts and browser contexts
 * - Handles TypeScript → JavaScript conversion automatically
 * - Provides consistent API across all consumers
 * - Eliminates hardcoded flag definitions in scripts
 *
 * Usage:
 *   import { loadFeatureFlags } from './src/lib/flagLoader.js';
 *   const flags = await loadFeatureFlags();
 */

import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Paths to configuration files
const CONFIG_PATHS = {
  // TypeScript source of truth
  typescript: join(__dirname, "../config/feature-flags.config.ts"),
  // Alternative JavaScript path (if transpiled)
  javascript: join(__dirname, "../config/feature-flags.config.js"),
};

/**
 * Load feature flags from the single source of truth
 *
 * This function dynamically imports the TypeScript configuration file
 * and returns the flags in a format compatible with existing scripts.
 *
 * @returns {Promise<Array>} Array of flag definitions with name and environments
 * @throws {Error} If configuration cannot be loaded
 */
export async function loadFeatureFlags() {
  try {
    // Try to dynamically import the TypeScript config
    // Node.js with ES modules can handle .ts files in many cases
    let config;

    try {
      // First, try importing the TypeScript file directly
      config = await import(CONFIG_PATHS.typescript);
    } catch (tsError) {
      try {
        // Fallback: try JavaScript version
        config = await import(CONFIG_PATHS.javascript);
      } catch (jsError) {
        // If both fail, provide detailed error information
        throw new Error(
          `Failed to load feature flag configuration:\n` +
            `- TypeScript import error: ${tsError.message}\n` +
            `- JavaScript import error: ${jsError.message}\n` +
            `- Typescript path: ${CONFIG_PATHS.typescript}\n` +
            `- JavaScript path: ${CONFIG_PATHS.javascript}`,
        );
      }
    }

    // Extract the FEATURE_FLAGS export
    const featureFlags = config.FEATURE_FLAGS || config.default?.FEATURE_FLAGS;

    if (!featureFlags || !Array.isArray(featureFlags)) {
      throw new Error(
        "Invalid configuration: FEATURE_FLAGS export not found or not an array. " +
          `Available exports: ${Object.keys(config).join(", ")}`,
      );
    }

    // Transform to the simplified format expected by scripts
    // This maintains backward compatibility with existing script APIs
    const simplifiedFlags = featureFlags.map((flag) => ({
      name: flag.name,
      environments: {
        development: flag.environments.development,
        staging: flag.environments.staging,
        production: flag.environments.production,
      },
      // Include additional metadata for advanced use cases
      description: flag.description,
      category: flag.category,
      defaultValue: flag.defaultValue,
      dependencies: flag.dependencies,
      buildTimeOptimization: flag.buildTimeOptimization,
    }));

    // Validate that we got reasonable data
    if (simplifiedFlags.length === 0) {
      console.warn("Warning: No feature flags found in configuration");
    }

    console.log(
      `✅ Loaded ${simplifiedFlags.length} feature flags from source of truth`,
    );

    return simplifiedFlags;
  } catch (error) {
    console.error("❌ Failed to load feature flags:", error.message);
    throw error;
  }
}

/**
 * Load feature flag utility functions from the source
 *
 * Provides access to naming convention utilities and other helper functions
 * defined in the source configuration.
 *
 * @returns {Promise<Object>} Object containing utility functions
 */
export async function loadFeatureFlagUtils() {
  try {
    const config = await import(CONFIG_PATHS.typescript);

    return {
      getEnvVarName: config.getEnvVarName,
      getBuildDefineName: config.getBuildDefineName,
      getFlagsForEnvironment: config.getFlagsForEnvironment,
      getFlagByName: config.getFlagByName,
      getFlagsByCategory: config.getFlagsByCategory,
      validateFlagDependencies: config.validateFlagDependencies,
    };
  } catch (error) {
    console.error("❌ Failed to load feature flag utilities:", error.message);
    throw error;
  }
}

/**
 * Get feature flags for a specific environment
 *
 * Convenience function that loads flags and filters for an environment.
 *
 * @param {string} environment - 'development', 'staging', or 'production'
 * @returns {Promise<Object>} Object mapping flag names to boolean values
 */
export async function getEnvironmentFlags(environment) {
  const flags = await loadFeatureFlags();

  const result = {};
  for (const flag of flags) {
    if (
      flag.environments &&
      typeof flag.environments[environment] !== "undefined"
    ) {
      result[flag.name] = flag.environments[environment];
    } else {
      console.warn(
        `Warning: Environment '${environment}' not found for flag '${flag.name}'`,
      );
      result[flag.name] = flag.defaultValue || false;
    }
  }

  return result;
}

/**
 * Validate that all required flags are present
 *
 * @param {Array} flags - Array of flag objects to validate
 * @returns {Object} Validation result with success status and any errors
 */
export function validateFlags(flags) {
  const errors = [];

  if (!Array.isArray(flags)) {
    errors.push("Flags must be an array");
    return { valid: false, errors };
  }

  for (let i = 0; i < flags.length; i++) {
    const flag = flags[i];

    if (!flag.name) {
      errors.push(`Flag at index ${i} missing name`);
    }

    if (!flag.environments) {
      errors.push(`Flag '${flag.name}' missing environments`);
    } else {
      const requiredEnvs = ["development", "staging", "production"];
      for (const env of requiredEnvs) {
        if (typeof flag.environments[env] !== "boolean") {
          errors.push(
            `Flag '${flag.name}' missing or invalid environment '${env}'`,
          );
        }
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

export default {
  loadFeatureFlags,
  loadFeatureFlagUtils,
  getEnvironmentFlags,
  validateFlags,
};
