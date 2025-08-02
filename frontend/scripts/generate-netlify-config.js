#!/usr/bin/env node

/**
 * Netlify Configuration Generation Script
 *
 * Generates netlify.toml environment sections from the feature-flags.config.ts
 * single source of truth. This ensures Netlify deployments use consistent
 * feature flag configurations.
 *
 * This script only updates the environment variable sections, preserving
 * other netlify.toml configurations like build settings and form handling.
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Paths
const NETLIFY_CONFIG_PATH = join(__dirname, '../netlify.toml');
const BACKUP_PATH = join(__dirname, '../netlify.toml.backup');

/**
 * Load feature flags (same as generate-env-files.js)
 */
async function loadFeatureFlags() {
  const flags = [
    { name: 'search', environments: { development: true, staging: true, production: true } },
    { name: 'themeSwitcher', environments: { development: true, staging: true, production: true } },
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
}

/**
 * Convert camelCase to SCREAMING_SNAKE_CASE for environment variables
 */
function getEnvVarName(flagName) {
  return `PUBLIC_FEATURE_${flagName.replace(/([A-Z])/g, '_$1').toUpperCase()}`;
}

/**
 * Parse existing netlify.toml and extract non-environment sections
 */
function parseNetlifyConfig(content) {
  const lines = content.split('\n');
  const preservedSections = [];
  let currentSection = [];
  let inEnvironmentSection = false;
  let skipUntilNextSection = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Check if we're entering an environment section
    if (line.match(/^\[context\.(production|branch-deploy|deploy-preview)\.environment\]$/)) {
      // Save current section before starting environment section
      if (currentSection.length > 0 && !inEnvironmentSection) {
        preservedSections.push(currentSection.join('\n'));
        currentSection = [];
      }
      inEnvironmentSection = true;
      skipUntilNextSection = true;
      continue;
    }

    // Check if we're entering a new section
    if (line.startsWith('[') && !line.includes('.environment]')) {
      // If we were in an environment section, we're done skipping
      if (inEnvironmentSection) {
        inEnvironmentSection = false;
        skipUntilNextSection = false;
        currentSection = [lines[i]]; // Start new section
        continue;
      }

      // Save previous section
      if (currentSection.length > 0) {
        preservedSections.push(currentSection.join('\n'));
      }
      currentSection = [lines[i]];
      continue;
    }

    // Skip lines in environment sections
    if (skipUntilNextSection && inEnvironmentSection) {
      continue;
    }

    // Add line to current section
    if (!skipUntilNextSection) {
      currentSection.push(lines[i]);
    }
  }

  // Add final section
  if (currentSection.length > 0 && !inEnvironmentSection) {
    preservedSections.push(currentSection.join('\n'));
  }

  return preservedSections;
}

/**
 * Generate environment section for a specific context
 */
function generateEnvironmentSection(context, environment, flags) {
  const lines = [`[context.${context}.environment]`];

  // Add environment identification
  lines.push(`  PUBLIC_ENV = "${environment}"`);

  // Add feature flags
  for (const flag of flags) {
    const envVarName = getEnvVarName(flag.name);
    const value = flag.environments[environment];
    lines.push(`  ${envVarName} = "${value}"`);
  }

  return lines.join('\n');
}

/**
 * Generate complete netlify.toml content
 */
async function generateNetlifyConfig() {
  try {
    console.log('🔄 Reading existing netlify.toml...');

    // Read existing config
    let existingContent = '';
    try {
      existingContent = readFileSync(NETLIFY_CONFIG_PATH, 'utf-8');
    } catch (error) {
      console.log('📝 No existing netlify.toml found, creating new one...');
    }

    // Create backup
    if (existingContent) {
      writeFileSync(BACKUP_PATH, existingContent, 'utf-8');
      console.log('💾 Created backup at netlify.toml.backup');
    }

    console.log('🔄 Loading feature flags...');
    const flags = await loadFeatureFlags();

    console.log('🔄 Generating new configuration...');

    // Parse existing config to preserve non-environment sections
    const preservedSections = existingContent ? parseNetlifyConfig(existingContent) : [];

    // If no existing config, add basic build configuration
    if (!existingContent) {
      preservedSections.unshift(`[build]
  publish = "dist"
  command = "yarn build"

[build.environment]
DISABLE_PYTHON = "true"
DISABLE_MISE = "true"

[functions]
  directory = "netlify/functions"

# Form notifications
[[form]]
  name = "contact"
  action = "/contact-success"

  [form.settings]
    send_confirmation = true
    confirmation_template = "contact-confirmation"

  [[form.notification]]
    type = "email"
    event = "submission"
    to = "\${CONTACT_EMAIL}"
    subject = "\${CONTACT_NOTIFICATION_SUBJECT}"
    body = """
    You have received a new contact form submission:

    Name: {{name}}
    Email: {{email}}
    Message: {{message}}

    Submitted at: {{created_at}}
    """`);
    }

    // Generate environment sections
    const environmentSections = [
      '# Environment Variables by Deploy Context',
      '# Production context (main branch)',
      generateEnvironmentSection('production', 'production', flags),
      '',
      '# Branch deploy context (staging and other branches)',
      generateEnvironmentSection('branch-deploy', 'staging', flags),
      '',
      '# Deploy preview context (pull requests)',
      generateEnvironmentSection('deploy-preview', 'staging', flags),
    ];

    // Combine all sections
    const finalContent = [
      ...preservedSections,
      '',
      ...environmentSections,
      '',
    ].join('\n');

    // Write new config
    writeFileSync(NETLIFY_CONFIG_PATH, finalContent, 'utf-8');

    console.log('✅ Generated netlify.toml with environment sections');
    console.log('');
    console.log('Generated sections:');
    console.log('  - [context.production.environment]');
    console.log('  - [context.branch-deploy.environment]');
    console.log('  - [context.deploy-preview.environment]');
    console.log('');
    console.log('⚠️  IMPORTANT: Environment sections are auto-generated from feature-flags.config.ts');
    console.log('   Do not edit them manually - use the configuration file instead.');

  } catch (error) {
    console.error('❌ Error generating netlify.toml:', error);

    // Restore backup if it exists
    try {
      const backup = readFileSync(BACKUP_PATH, 'utf-8');
      writeFileSync(NETLIFY_CONFIG_PATH, backup, 'utf-8');
      console.log('🔄 Restored from backup due to error');
    } catch (restoreError) {
      console.error('❌ Could not restore from backup:', restoreError);
    }

    process.exit(1);
  }
}

/**
 * Validate netlify.toml environment sections
 */
function validateNetlifyConfig() {
  console.log('🔍 Validating netlify.toml environment sections...');

  try {
    const content = readFileSync(NETLIFY_CONFIG_PATH, 'utf-8');

    // Check for required sections
    const requiredSections = [
      'context.production.environment',
      'context.branch-deploy.environment',
      'context.deploy-preview.environment'
    ];

    const missingSections = requiredSections.filter(section =>
      !content.includes(`[${section}]`)
    );

    if (missingSections.length > 0) {
      console.log('⚠️  Missing environment sections:', missingSections);
      return false;
    }

    console.log('✅ All required environment sections found');
    return true;

  } catch (error) {
    console.error('❌ Error validating netlify.toml:', error);
    return false;
  }
}

// CLI handling
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'generate':
  case undefined:
    generateNetlifyConfig();
    break;
  case 'validate':
    validateNetlifyConfig();
    break;
  case 'help':
    console.log('Usage: node generate-netlify-config.js [command]');
    console.log('');
    console.log('Commands:');
    console.log('  generate  Generate netlify.toml environment sections (default)');
    console.log('  validate  Validate existing netlify.toml');
    console.log('  help      Show this help message');
    break;
  default:
    console.error(`❌ Unknown command: ${command}`);
    console.log('Run "node generate-netlify-config.js help" for usage information');
    process.exit(1);
}
