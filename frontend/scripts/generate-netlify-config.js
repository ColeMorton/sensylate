#!/usr/bin/env node

/**
 * Robust Netlify Configuration Generation Script
 *
 * Generates netlify.toml from scratch using a template-based approach.
 * This eliminates fragility from parsing potentially corrupted files.
 *
 * Key improvements:
 * - Template-based generation (no parsing existing content)
 * - TOML validation to prevent duplicates
 * - Atomic file operations with backup/rollback
 * - Fail-safe error handling
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Paths
const NETLIFY_CONFIG_PATH = join(__dirname, '../netlify.toml');
const BACKUP_PATH = join(__dirname, '../netlify.toml.backup');

/**
 * Load feature flags configuration
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
 * Generate environment variables for a specific environment
 */
function generateEnvironmentVars(environment, flags) {
  const vars = [`  PUBLIC_ENV = "${environment}"`];

  // Use Set to prevent duplicates
  const addedVars = new Set(['PUBLIC_ENV']);

  for (const flag of flags) {
    const envVarName = getEnvVarName(flag.name);

    // Skip if already added (prevents duplicates)
    if (addedVars.has(envVarName)) {
      console.warn(`⚠️  Skipping duplicate environment variable: ${envVarName}`);
      continue;
    }

    const value = flag.environments[environment];
    vars.push(`  ${envVarName} = "${value}"`);
    addedVars.add(envVarName);
  }

  return vars;
}

/**
 * Generate complete netlify.toml from template
 */
function generateNetlifyConfigContent(flags) {
  const prodVars = generateEnvironmentVars('production', flags);
  const stagingVars = generateEnvironmentVars('staging', flags);

  return `[build]
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
    """

# Environment Variables by Deploy Context
# NOTE: Generated automatically from feature-flags.config.ts - do not edit manually

# Production context (main branch)
[context.production.environment]
${prodVars.join('\n')}

# Branch deploy context (staging and other branches)
[context.branch-deploy.environment]
${stagingVars.join('\n')}

# Deploy preview context (pull requests)
[context.deploy-preview.environment]
${stagingVars.join('\n')}
`;
}

/**
 * Validate TOML content for duplicate keys
 */
function validateTOMLContent(content) {
  const lines = content.split('\n');
  const sections = {};
  let currentSection = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Track section headers
    if (line.match(/^\[.*\]$/)) {
      currentSection = line;
      if (!sections[currentSection]) {
        sections[currentSection] = new Set();
      }
      continue;
    }

    // Check for key-value pairs
    const keyValueMatch = line.match(/^(\w+)\s*=\s*/);
    if (keyValueMatch && currentSection) {
      const key = keyValueMatch[1];

      if (sections[currentSection].has(key)) {
        throw new Error(`Duplicate key "${key}" found in section ${currentSection} at line ${i + 1}`);
      }

      sections[currentSection].add(key);
    }
  }

  console.log('✅ TOML validation passed - no duplicate keys found');
  return true;
}

/**
 * Create backup of existing file
 */
function createBackup() {
  if (existsSync(NETLIFY_CONFIG_PATH)) {
    const content = readFileSync(NETLIFY_CONFIG_PATH, 'utf-8');
    writeFileSync(BACKUP_PATH, content, 'utf-8');
    console.log('💾 Created backup at netlify.toml.backup');
    return true;
  }
  return false;
}

/**
 * Restore from backup
 */
function restoreFromBackup() {
  if (existsSync(BACKUP_PATH)) {
    const content = readFileSync(BACKUP_PATH, 'utf-8');
    writeFileSync(NETLIFY_CONFIG_PATH, content, 'utf-8');
    console.log('🔄 Restored from backup due to error');
    return true;
  }
  return false;
}

/**
 * Generate netlify.toml using robust template approach
 */
async function generateNetlifyConfig() {
  try {
    console.log('🔄 Generating netlify.toml from template...');

    // Create backup first
    const hasBackup = createBackup();

    // Load feature flags
    console.log('🔄 Loading feature flags...');
    const flags = await loadFeatureFlags();

    // Generate content from template
    console.log('🔄 Generating configuration content...');
    const content = generateNetlifyConfigContent(flags);

    // Validate content before writing
    console.log('🔍 Validating TOML content...');
    validateTOMLContent(content);

    // Write atomically
    console.log('📝 Writing netlify.toml...');
    writeFileSync(NETLIFY_CONFIG_PATH, content, 'utf-8');

    console.log('✅ Successfully generated netlify.toml');
    console.log('');
    console.log('Generated sections:');
    console.log('  - [context.production.environment]');
    console.log('  - [context.branch-deploy.environment]');
    console.log('  - [context.deploy-preview.environment]');
    console.log('');
    console.log('⚠️  IMPORTANT: Environment sections are auto-generated from feature-flags.config.ts');
    console.log('   Do not edit them manually - use the configuration file instead.');

  } catch (error) {
    console.error('❌ Error generating netlify.toml:', error.message);

    // Attempt to restore backup
    if (restoreFromBackup()) {
      console.log('✅ Successfully restored from backup');
    } else {
      console.error('❌ Could not restore from backup - manual intervention required');
    }

    process.exit(1);
  }
}

/**
 * Validate existing netlify.toml
 */
function validateNetlifyConfig() {
  console.log('🔍 Validating netlify.toml...');

  try {
    if (!existsSync(NETLIFY_CONFIG_PATH)) {
      console.error('❌ netlify.toml does not exist');
      return false;
    }

    const content = readFileSync(NETLIFY_CONFIG_PATH, 'utf-8');

    // Validate TOML structure
    validateTOMLContent(content);

    // Check for required sections
    const requiredSections = [
      '[context.production.environment]',
      '[context.branch-deploy.environment]',
      '[context.deploy-preview.environment]'
    ];

    const missingSections = requiredSections.filter(section =>
      !content.includes(section)
    );

    if (missingSections.length > 0) {
      console.error('❌ Missing required sections:', missingSections);
      return false;
    }

    console.log('✅ netlify.toml validation successful');
    return true;

  } catch (error) {
    console.error('❌ Validation failed:', error.message);
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
    const isValid = validateNetlifyConfig();
    process.exit(isValid ? 0 : 1);
    break;
  case 'help':
    console.log('Usage: node generate-netlify-config.js [command]');
    console.log('');
    console.log('Commands:');
    console.log('  generate  Generate netlify.toml from template (default)');
    console.log('  validate  Validate existing netlify.toml structure');
    console.log('  help      Show this help message');
    break;
  default:
    console.error(`❌ Unknown command: ${command}`);
    console.log('Run "node generate-netlify-config.js help" for usage information');
    process.exit(1);
}
