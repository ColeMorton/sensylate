#!/usr/bin/env node

/**
 * Feature Flag Synchronization CLI Tool
 *
 * Main orchestrator for feature flag management. Provides commands to:
 * - Synchronize all configurations from single source of truth
 * - Add/remove feature flags
 * - Validate consistency across all sources
 * - Generate all configuration files
 *
 * This is the primary tool developers should use for flag management.
 */

import { spawn } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m'
};

function colorLog(color, message) {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Run a script and return promise
 */
function runScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const scriptPath = join(__dirname, scriptName);
    const child = spawn('node', [scriptPath, ...args], {
      stdio: 'inherit',
      cwd: __dirname
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Script ${scriptName} exited with code ${code}`));
      }
    });

    child.on('error', (error) => {
      reject(error);
    });
  });
}

/**
 * Synchronize all configurations from source of truth
 */
async function syncAll() {
  try {
    colorLog('bold', '🚀 Starting feature flag synchronization...\n');

    // Step 1: Validate current state
    colorLog('blue', '📋 Step 1: Pre-sync validation');
    try {
      await runScript('validate-flags.js', ['quick']);
      colorLog('green', '✅ Pre-sync validation passed\n');
    } catch (error) {
      colorLog('yellow', '⚠️  Pre-sync validation found issues (continuing anyway)\n');
    }

    // Step 2: Generate environment files
    colorLog('blue', '📋 Step 2: Generating environment files');
    await runScript('generate-env-files.js');
    colorLog('green', '✅ Environment files generated\n');

    // Step 3: Generate netlify configuration
    colorLog('blue', '📋 Step 3: Generating Netlify configuration');
    await runScript('generate-netlify-config.js');
    colorLog('green', '✅ Netlify configuration generated\n');

    // Step 4: Post-sync validation
    colorLog('blue', '📋 Step 4: Post-sync validation');
    await runScript('validate-flags.js', ['full']);
    colorLog('green', '✅ Post-sync validation passed\n');

    colorLog('bold', '🎉 Synchronization completed successfully!');
    colorLog('cyan', 'All feature flag configurations are now consistent.');

  } catch (error) {
    colorLog('red', `❌ Synchronization failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Validate all configurations
 */
async function validate(mode = 'full') {
  try {
    colorLog('bold', '🔍 Validating feature flag configurations...\n');
    await runScript('validate-flags.js', [mode]);
  } catch (error) {
    colorLog('red', `❌ Validation failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Generate only environment files
 */
async function generateEnv() {
  try {
    colorLog('bold', '📝 Generating environment files...\n');
    await runScript('generate-env-files.js');
    colorLog('green', '✅ Environment files generated successfully!');
  } catch (error) {
    colorLog('red', `❌ Environment file generation failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Generate only netlify configuration
 */
async function generateNetlify() {
  try {
    colorLog('bold', '📝 Generating Netlify configuration...\n');
    await runScript('generate-netlify-config.js');
    colorLog('green', '✅ Netlify configuration generated successfully!');
  } catch (error) {
    colorLog('red', `❌ Netlify configuration generation failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Add a new feature flag (placeholder for future implementation)
 */
async function addFlag(flagName) {
  if (!flagName) {
    colorLog('red', '❌ Flag name is required');
    console.log('Usage: yarn flags:add <flagName>');
    process.exit(1);
  }

  colorLog('yellow', '⚠️  Adding new flags is not yet implemented.');
  colorLog('cyan', 'For now, please manually add the flag to src/config/feature-flags.config.ts');
  colorLog('cyan', 'Then run "yarn flags:sync" to update all configurations.');
}

/**
 * Remove a feature flag (placeholder for future implementation)
 */
async function removeFlag(flagName) {
  if (!flagName) {
    colorLog('red', '❌ Flag name is required');
    console.log('Usage: yarn flags:remove <flagName>');
    process.exit(1);
  }

  colorLog('yellow', '⚠️  Removing flags is not yet implemented.');
  colorLog('cyan', 'For now, please manually remove the flag from src/config/feature-flags.config.ts');
  colorLog('cyan', 'Then run "yarn flags:sync" to update all configurations.');
}

/**
 * List all feature flags
 */
async function listFlags() {
  try {
    colorLog('bold', '📋 Feature Flags Configuration\n');

    // Read and display basic flag info
    const configPath = join(__dirname, '../src/config/feature-flags.config.ts');
    const content = readFileSync(configPath, 'utf-8');

    // Simple parsing to extract flag names and descriptions
    const flagMatches = content.match(/\{\s*name:\s*['"`](\w+)['"`],\s*description:\s*['"`]([^'"`]+)['"`]/g);

    if (flagMatches) {
      console.log('Available flags:');
      flagMatches.forEach(match => {
        const nameMatch = match.match(/name:\s*['"`](\w+)['"`]/);
        const descMatch = match.match(/description:\s*['"`]([^'"`]+)['"`]/);

        if (nameMatch && descMatch) {
          console.log(`  ${colors.cyan}${nameMatch[1]}${colors.reset}: ${descMatch[1]}`);
        }
      });
    } else {
      colorLog('yellow', 'No flags found in configuration');
    }

    console.log('\nFor detailed configuration, see: src/config/feature-flags.config.ts');

  } catch (error) {
    colorLog('red', `❌ Failed to list flags: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Show help information
 */
function showHelp() {
  console.log(`
${colors.bold}Feature Flag Management CLI${colors.reset}

${colors.cyan}Usage:${colors.reset}
  yarn flags:sync [command] [options]

${colors.cyan}Commands:${colors.reset}
  ${colors.green}sync${colors.reset}           Synchronize all configurations from source of truth (default)
  ${colors.green}validate${colors.reset}       Validate consistency across all configurations
  ${colors.green}validate-quick${colors.reset}  Quick validation (environment files only)
  ${colors.green}generate-env${colors.reset}   Generate only environment files
  ${colors.green}generate-netlify${colors.reset} Generate only Netlify configuration
  ${colors.green}add <name>${colors.reset}     Add a new feature flag (coming soon)
  ${colors.green}remove <name>${colors.reset}  Remove a feature flag (coming soon)
  ${colors.green}list${colors.reset}          List all feature flags
  ${colors.green}help${colors.reset}          Show this help message

${colors.cyan}Examples:${colors.reset}
  yarn flags:sync                    # Sync all configurations
  yarn flags:sync validate           # Validate all configurations
  yarn flags:sync generate-env       # Generate only .env files
  yarn flags:sync list               # List all feature flags

${colors.cyan}Files managed by this tool:${colors.reset}
  • .env.development, .env.staging, .env.production
  • netlify.toml environment sections
  • Generated from: src/config/feature-flags.config.ts

${colors.yellow}⚠️  Important:${colors.reset}
  Do not manually edit generated files. Use the source configuration file instead.
`);
}

/**
 * Get system status
 */
async function status() {
  try {
    colorLog('bold', '📊 Feature Flag System Status\n');

    // Quick validation
    colorLog('blue', 'Running validation...');
    try {
      await runScript('validate-flags.js', ['quick']);
      colorLog('green', '✅ System status: HEALTHY');
    } catch (error) {
      colorLog('red', '❌ System status: NEEDS ATTENTION');
      colorLog('yellow', 'Run "yarn flags:sync validate" for details');
    }

    // Flag count
    const configPath = join(__dirname, '../src/config/feature-flags.config.ts');
    const content = readFileSync(configPath, 'utf-8');
    const flagCount = (content.match(/name:\s*['"`]\w+['"`]/g) || []).length;

    console.log(`\nConfiguration summary:`);
    console.log(`  • Feature flags: ${flagCount}`);
    console.log(`  • Environments: 3 (development, staging, production)`);
    console.log(`  • Source of truth: src/config/feature-flags.config.ts`);

  } catch (error) {
    colorLog('red', `❌ Failed to get status: ${error.message}`);
    process.exit(1);
  }
}

// CLI command handling
const args = process.argv.slice(2);
const command = args[0];
const flagName = args[1];

async function main() {
  switch (command) {
    case undefined:
    case 'sync':
      await syncAll();
      break;
    case 'validate':
      await validate('full');
      break;
    case 'validate-quick':
      await validate('quick');
      break;
    case 'generate-env':
      await generateEnv();
      break;
    case 'generate-netlify':
      await generateNetlify();
      break;
    case 'add':
      await addFlag(flagName);
      break;
    case 'remove':
      await removeFlag(flagName);
      break;
    case 'list':
      await listFlags();
      break;
    case 'status':
      await status();
      break;
    case 'help':
      showHelp();
      break;
    default:
      colorLog('red', `❌ Unknown command: ${command}`);
      console.log('Run "yarn flags:sync help" for usage information');
      process.exit(1);
  }
}

main().catch(error => {
  colorLog('red', `❌ Unexpected error: ${error.message}`);
  process.exit(1);
});
