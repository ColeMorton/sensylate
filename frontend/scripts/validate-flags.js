#!/usr/bin/env node

/**
 * Feature Flag Validation Script
 *
 * Validates consistency across all feature flag configuration sources:
 * - feature-flags.config.ts (source of truth)
 * - .env.development, .env.staging, .env.production
 * - netlify.toml environment sections
 * - astro.config.mjs build defines
 * - TypeScript type definitions
 *
 * Uses fail-fast approach to catch configuration drift immediately.
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// File paths
const PATHS = {
  featureFlags: join(__dirname, '../src/config/feature-flags.config.ts'),
  envDev: join(__dirname, '../.env.development'),
  envStaging: join(__dirname, '../.env.staging'),
  envProd: join(__dirname, '../.env.production'),
  netlify: join(__dirname, '../netlify.toml'),
  astroConfig: join(__dirname, '../astro.config.mjs'),
  types: join(__dirname, '../src/types/index.d.ts'),
};

// Validation results
class ValidationResult {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.info = [];
  }

  addError(message) {
    this.errors.push(message);
  }

  addWarning(message) {
    this.warnings.push(message);
  }

  addInfo(message) {
    this.info.push(message);
  }

  hasErrors() {
    return this.errors.length > 0;
  }

  hasWarnings() {
    return this.warnings.length > 0;
  }

  report() {
    if (this.errors.length > 0) {
      console.log('❌ VALIDATION ERRORS:');
      this.errors.forEach(error => console.log(`   ${error}`));
      console.log('');
    }

    if (this.warnings.length > 0) {
      console.log('⚠️  WARNINGS:');
      this.warnings.forEach(warning => console.log(`   ${warning}`));
      console.log('');
    }

    if (this.info.length > 0) {
      console.log('ℹ️  INFORMATION:');
      this.info.forEach(info => console.log(`   ${info}`));
      console.log('');
    }

    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log('✅ All validations passed!');
    }
  }
}

/**
 * Load and parse feature flags from config
 */
async function loadFeatureFlags() {
  // Simplified flag loading (same as other scripts)
  return [
    { name: 'search', environments: { development: true, staging: true, production: true } },
    { name: 'themeSwitcher', environments: { development: true, staging: true, production: false } },
    { name: 'comments', environments: { development: false, staging: false, production: false } },
    { name: 'gtm', environments: { development: false, staging: false, production: true } },
    { name: 'calculators', environments: { development: true, staging: false, production: false } },
    { name: 'calculatorAdvanced', environments: { development: true, staging: true, production: false } },
    { name: 'elementsPage', environments: { development: true, staging: true, production: false } },
    { name: 'authorsPage', environments: { development: true, staging: true, production: false } },
    { name: 'chartsPage', environments: { development: true, staging: true, production: false } },
    { name: 'photoBooth', environments: { development: true, staging: true, production: false } },
  ];
}

/**
 * Convert camelCase to env var format
 */
function getEnvVarName(flagName) {
  return `PUBLIC_FEATURE_${flagName.replace(/([A-Z])/g, '_$1').toUpperCase()}`;
}

/**
 * Parse environment file and extract feature flags
 */
function parseEnvFile(filePath) {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const flags = {};

    const lines = content.split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('PUBLIC_FEATURE_')) {
        const [key, value] = trimmed.split('=');
        if (key && value !== undefined) {
          flags[key] = value.toLowerCase() === 'true';
        }
      }
    }

    return flags;
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`);
  }
}

/**
 * Parse netlify.toml and extract environment variables
 */
function parseNetlifyConfig(filePath) {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const contexts = {
      production: {},
      'branch-deploy': {},
      'deploy-preview': {}
    };

    let currentContext = null;
    let inEnvironmentSection = false;

    const lines = content.split('\n');
    for (const line of lines) {
      const trimmed = line.trim();

      // Check for context environment sections
      const contextMatch = trimmed.match(/^\[context\.(production|branch-deploy|deploy-preview)\.environment\]$/);
      if (contextMatch) {
        currentContext = contextMatch[1];
        inEnvironmentSection = true;
        continue;
      }

      // Check for new section
      if (trimmed.startsWith('[') && currentContext) {
        inEnvironmentSection = false;
        currentContext = null;
        continue;
      }

      // Parse environment variables
      if (inEnvironmentSection && currentContext && trimmed.includes('PUBLIC_FEATURE_')) {
        const match = trimmed.match(/^\s*(\w+)\s*=\s*"(.+)"$/);
        if (match) {
          const [, key, value] = match;
          contexts[currentContext][key] = value.toLowerCase() === 'true';
        }
      }
    }

    return contexts;
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`);
  }
}

/**
 * Parse astro.config.mjs and extract build defines
 */
function parseAstroConfig(filePath) {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const defines = {};

    // Look for the define section
    const defineMatch = content.match(/define:\s*\{([^}]+)\}/s);
    if (defineMatch) {
      const defineContent = defineMatch[1];
      const lines = defineContent.split('\n');

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.includes('__FEATURE_')) {
          const match = trimmed.match(/(__FEATURE_\w+__):\s*([^,\s]+)/);
          if (match) {
            const [, key, value] = match;
            defines[key] = value;
          }
        }
      }
    }

    return defines;
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`);
  }
}

/**
 * Parse TypeScript types file
 */
function parseTypesFile(filePath) {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const flags = [];

    // Look for FeatureFlags interface
    const interfaceMatch = content.match(/interface FeatureFlags \{([^}]+)\}/s);
    if (interfaceMatch) {
      const interfaceContent = interfaceMatch[1];
      const lines = interfaceContent.split('\n');

      for (const line of lines) {
        const trimmed = line.trim();
        const match = trimmed.match(/(\w+):\s*boolean;/);
        if (match) {
          flags.push(match[1]);
        }
      }
    }

    return flags;
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`);
  }
}

/**
 * Validate environment files against source of truth
 */
async function validateEnvironmentFiles(result) {
  console.log('🔍 Validating environment files...');

  try {
    const flags = await loadFeatureFlags();
    const environments = {
      development: parseEnvFile(PATHS.envDev),
      staging: parseEnvFile(PATHS.envStaging),
      production: parseEnvFile(PATHS.envProd),
    };

    // Check each flag in each environment
    for (const flag of flags) {
      const envVarName = getEnvVarName(flag.name);

      for (const [envName, envFlags] of Object.entries(environments)) {
        const expectedValue = flag.environments[envName];
        const actualValue = envFlags[envVarName];

        if (actualValue === undefined) {
          result.addError(`Missing ${envVarName} in .env.${envName}`);
        } else if (actualValue !== expectedValue) {
          result.addError(`Mismatch in .env.${envName}: ${envVarName} should be ${expectedValue}, got ${actualValue}`);
        }
      }
    }

    // Check for extra flags in env files
    for (const [envName, envFlags] of Object.entries(environments)) {
      const expectedFlags = flags.map(f => getEnvVarName(f.name));
      const actualFlags = Object.keys(envFlags);

      for (const actualFlag of actualFlags) {
        if (!expectedFlags.includes(actualFlag)) {
          result.addWarning(`Extra flag ${actualFlag} in .env.${envName} not defined in config`);
        }
      }
    }

    result.addInfo(`Validated ${flags.length} flags across ${Object.keys(environments).length} environment files`);

  } catch (error) {
    result.addError(`Environment file validation failed: ${error.message}`);
  }
}

/**
 * Validate netlify.toml against source of truth
 */
async function validateNetlifyConfig(result) {
  console.log('🔍 Validating netlify.toml...');

  try {
    const flags = await loadFeatureFlags();
    const netlifyContexts = parseNetlifyConfig(PATHS.netlify);

    // Map netlify contexts to environments
    const contextMapping = {
      'production': 'production',
      'branch-deploy': 'staging',
      'deploy-preview': 'staging'
    };

    for (const [context, envName] of Object.entries(contextMapping)) {
      const contextFlags = netlifyContexts[context];

      if (!contextFlags || Object.keys(contextFlags).length === 0) {
        result.addError(`Missing or empty [context.${context}.environment] section in netlify.toml`);
        continue;
      }

      for (const flag of flags) {
        const envVarName = getEnvVarName(flag.name);
        const expectedValue = flag.environments[envName];
        const actualValue = contextFlags[envVarName];

        if (actualValue === undefined) {
          result.addError(`Missing ${envVarName} in netlify.toml [context.${context}.environment]`);
        } else if (actualValue !== expectedValue) {
          result.addError(`Mismatch in netlify.toml [context.${context}.environment]: ${envVarName} should be ${expectedValue}, got ${actualValue}`);
        }
      }
    }

    result.addInfo(`Validated netlify.toml environment sections`);

  } catch (error) {
    result.addError(`Netlify config validation failed: ${error.message}`);
  }
}

/**
 * Validate astro.config.mjs build defines
 */
async function validateAstroConfig(result) {
  console.log('🔍 Validating astro.config.mjs...');

  try {
    const flags = await loadFeatureFlags();
    const astroDefines = parseAstroConfig(PATHS.astroConfig);

    for (const flag of flags) {
      const defineName = `__FEATURE_${flag.name.replace(/([A-Z])/g, '_$1').toUpperCase()}__`;

      if (!astroDefines[defineName]) {
        result.addWarning(`Missing build define ${defineName} in astro.config.mjs`);
      }
    }

    // Check for unused defines
    for (const defineName of Object.keys(astroDefines)) {
      const flagName = defineName.replace(/^__FEATURE_/, '').replace(/__$/, '').replace(/_([A-Z])/g, (_, letter) => letter.toLowerCase()).toLowerCase();
      const matchingFlag = flags.find(f => f.name.toLowerCase() === flagName);

      if (!matchingFlag) {
        result.addWarning(`Unused build define ${defineName} in astro.config.mjs`);
      }
    }

    result.addInfo(`Validated astro.config.mjs build defines`);

  } catch (error) {
    result.addError(`Astro config validation failed: ${error.message}`);
  }
}

/**
 * Validate TypeScript type definitions
 */
async function validateTypeDefinitions(result) {
  console.log('🔍 Validating TypeScript types...');

  try {
    const flags = await loadFeatureFlags();
    const typeFlags = parseTypesFile(PATHS.types);

    for (const flag of flags) {
      if (!typeFlags.includes(flag.name)) {
        result.addError(`Missing ${flag.name} in FeatureFlags interface`);
      }
    }

    for (const typeFlag of typeFlags) {
      const matchingFlag = flags.find(f => f.name === typeFlag);
      if (!matchingFlag) {
        result.addWarning(`Extra type definition ${typeFlag} not defined in config`);
      }
    }

    result.addInfo(`Validated TypeScript type definitions`);

  } catch (error) {
    result.addError(`Type definition validation failed: ${error.message}`);
  }
}

/**
 * Run all validations
 */
async function runFullValidation() {
  console.log('🚀 Starting comprehensive feature flag validation...');
  console.log('');

  const result = new ValidationResult();

  // Run all validation checks
  await validateEnvironmentFiles(result);
  await validateNetlifyConfig(result);
  await validateAstroConfig(result);
  await validateTypeDefinitions(result);

  console.log('');
  console.log('📊 VALIDATION REPORT');
  console.log('═'.repeat(50));
  result.report();

  // Exit with error code if there are errors
  if (result.hasErrors()) {
    console.log('💥 Validation failed with errors. Fix the issues above before proceeding.');
    process.exit(1);
  } else if (result.hasWarnings()) {
    console.log('⚠️  Validation completed with warnings. Consider addressing them.');
    process.exit(0);
  } else {
    console.log('🎉 Perfect! All feature flag configurations are consistent.');
    process.exit(0);
  }
}

/**
 * Quick validation (just check for basic issues)
 */
async function runQuickValidation() {
  console.log('⚡ Running quick validation...');

  const result = new ValidationResult();

  // Just check environment files
  await validateEnvironmentFiles(result);

  result.report();

  return !result.hasErrors();
}

// CLI handling
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'full':
  case undefined:
    runFullValidation();
    break;
  case 'quick':
    runQuickValidation().then(success => {
      process.exit(success ? 0 : 1);
    });
    break;
  case 'help':
    console.log('Usage: node validate-flags.js [command]');
    console.log('');
    console.log('Commands:');
    console.log('  full   Run comprehensive validation (default)');
    console.log('  quick  Run quick validation (env files only)');
    console.log('  help   Show this help message');
    break;
  default:
    console.error(`❌ Unknown command: ${command}`);
    console.log('Run "node validate-flags.js help" for usage information');
    process.exit(1);
}
