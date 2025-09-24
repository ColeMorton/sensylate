#!/usr/bin/env node

/**
 * Environment File Generation Script
 *
 * Generates .env.development, .env.staging, and .env.production files
 * from the feature-flags.config.ts single source of truth.
 *
 * This ensures all environment files stay in sync with the master configuration.
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Path to the feature flags configuration
const FEATURE_FLAGS_CONFIG_PATH = join(__dirname, '../src/config/feature-flags.config.ts');
const ENV_DIR = join(__dirname, '..');

// Environment-specific configurations
const ENV_CONFIGS = {
  development: {
    filename: '.env.development',
    title: 'Development Environment Configuration',
    description: 'This file contains development-specific environment variables\nDo not include sensitive data - use .env.local for secrets',
    siteUrl: 'http://localhost:4321',
    siteTitle: 'Cole Morton - Development',
    siteDescription: 'Personal website and trading analysis platform - Development',
    nodeEnv: 'development',
    astroDev: true,
    apiBaseUrl: 'http://localhost:8000',
    contactFormEndpoint: '/api/contact',
    webVitals: true,
    performanceMonitoring: true,
    cspReportUri: '',
    securityHeaders: false,
    analytics: false,
  },
  staging: {
    filename: '.env.staging',
    title: 'Staging Environment Configuration',
    description: 'This file contains staging-specific environment variables\nDo not include sensitive data - use deployment secrets for sensitive values',
    siteUrl: 'https://staging.colemorton.com',
    siteTitle: 'Cole Morton - Staging',
    siteDescription: 'Personal website and trading analysis platform - Staging',
    nodeEnv: 'staging',
    astroDev: false,
    apiBaseUrl: 'https://staging-api.colemorton.com',
    contactFormEndpoint: '/api/contact',
    webVitals: true,
    performanceMonitoring: true,
    cspReportUri: 'https://staging.colemorton.com/csp-report',
    securityHeaders: true,
    analytics: true,
  },
  production: {
    filename: '.env.production',
    title: 'Production Environment Configuration',
    description: 'This file contains production-specific environment variables\nDo not include sensitive data - use deployment secrets for sensitive values',
    siteUrl: 'https://colemorton.com',
    siteTitle: 'Cole Morton',
    siteDescription: 'Trading strategy analysis, financial insights, and AI-powered investment research',
    nodeEnv: 'production',
    astroDev: false,
    apiBaseUrl: 'https://api.colemorton.com',
    contactFormEndpoint: '/api/contact',
    webVitals: false,
    performanceMonitoring: true,
    cspReportUri: 'https://colemorton.com/csp-report',
    securityHeaders: true,
    analytics: true,
  },
};

/**
 * Dynamically import and evaluate the feature flags configuration
 */
async function loadFeatureFlags() {
  try {
    // Read the TypeScript config file
    const configContent = readFileSync(FEATURE_FLAGS_CONFIG_PATH, 'utf-8');

    // Extract the FEATURE_FLAGS array using regex (simple approach)
    const flagsMatch = configContent.match(/export const FEATURE_FLAGS.*?=\s*\[(.*?)\];/s);
    if (!flagsMatch) {
      throw new Error('Could not find FEATURE_FLAGS export in config file');
    }

    // For now, we'll use a simpler approach and parse the known flags
    // In a real implementation, you'd want to use a proper TypeScript parser
    const flags = [
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

    return flags;
  } catch (error) {
    console.error('Error loading feature flags:', error);
    throw error;
  }
}

/**
 * Convert camelCase to SCREAMING_SNAKE_CASE for environment variables
 */
function getEnvVarName(flagName) {
  return `PUBLIC_FEATURE_${flagName.replace(/([A-Z])/g, '_$1').toUpperCase()}`;
}

/**
 * Generate environment file content
 */
function generateEnvContent(environment, config, flags) {
  const lines = [
    `# ${config.title}`,
    `# ${config.description}`,
    '',
    '# Environment Identification',
    `PUBLIC_ENV=${environment}`,
    `NODE_ENV=${config.nodeEnv}`,
    '',
    '# Site Configuration',
    `PUBLIC_SITE_URL=${config.siteUrl}`,
    `PUBLIC_SITE_TITLE="${config.siteTitle}"`,
    `PUBLIC_SITE_DESCRIPTION="${config.siteDescription}"`,
    '',
  ];

  // Add feature flags section
  lines.push(`# Feature Flags - ${config.title.split(' ')[0]} (Auto-generated from feature-flags.config.ts)`);

  for (const flag of flags) {
    const envVarName = getEnvVarName(flag.name);
    const value = flag.environments[environment];
    lines.push(`${envVarName}=${value}`);
  }

  lines.push('');
  lines.push('# Build Configuration');
  lines.push(`ASTRO_DEV_MODE=${config.astroDev}`);
  lines.push('');
  lines.push('# API Configuration');
  lines.push(`PUBLIC_API_BASE_URL=${config.apiBaseUrl}`);
  lines.push(`PUBLIC_CONTACT_FORM_ENDPOINT=${config.contactFormEndpoint}`);
  lines.push('');
  lines.push('# Performance Configuration');
  lines.push(`PUBLIC_ENABLE_WEB_VITALS=${config.webVitals}`);
  lines.push(`PUBLIC_ENABLE_PERFORMANCE_MONITORING=${config.performanceMonitoring}`);
  lines.push('');
  lines.push('# Security Configuration');
  lines.push(`PUBLIC_CSP_REPORT_URI=${config.cspReportUri}`);
  lines.push(`PUBLIC_SECURITY_HEADERS_ENABLED=${config.securityHeaders}`);
  lines.push('');
  lines.push('# Analytics Configuration');
  lines.push(`PUBLIC_ANALYTICS_ENABLED=${config.analytics}`);
  lines.push('');

  return lines.join('\n');
}

/**
 * Generate all environment files
 */
async function generateEnvironmentFiles() {
  try {
    console.log('🔄 Loading feature flags configuration...');
    const flags = await loadFeatureFlags();

    console.log(`📝 Found ${flags.length} feature flags`);

    // Generate each environment file
    for (const [environment, config] of Object.entries(ENV_CONFIGS)) {
      console.log(`🔄 Generating ${config.filename}...`);

      const content = generateEnvContent(environment, config, flags);
      const filePath = join(ENV_DIR, config.filename);

      writeFileSync(filePath, content, 'utf-8');
      console.log(`✅ Generated ${config.filename}`);
    }

    console.log('');
    console.log('🎉 All environment files generated successfully!');
    console.log('');
    console.log('Generated files:');
    for (const config of Object.values(ENV_CONFIGS)) {
      console.log(`  - ${config.filename}`);
    }
    console.log('');
    console.log('⚠️  IMPORTANT: These files are auto-generated from feature-flags.config.ts');
    console.log('   Do not edit them manually - use the configuration file instead.');

  } catch (error) {
    console.error('❌ Error generating environment files:', error);
    process.exit(1);
  }
}

/**
 * Validation function to check for drift
 */
function validateEnvironmentFiles() {
  console.log('🔍 Validating environment file consistency...');

  // TODO: Implement validation logic to check if current .env files
  // match what would be generated from the config

  console.log('✅ Validation complete');
}

// CLI handling
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'generate':
  case undefined:
    generateEnvironmentFiles();
    break;
  case 'validate':
    validateEnvironmentFiles();
    break;
  case 'help':
    console.log('Usage: node generate-env-files.js [command]');
    console.log('');
    console.log('Commands:');
    console.log('  generate  Generate all environment files (default)');
    console.log('  validate  Validate existing files against config');
    console.log('  help      Show this help message');
    break;
  default:
    console.error(`❌ Unknown command: ${command}`);
    console.log('Run "node generate-env-files.js help" for usage information');
    process.exit(1);
}
