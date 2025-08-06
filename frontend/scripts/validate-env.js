/**
 * Environment Variable Validation Script
 *
 * Validates environment variables before build without scanning build output.
 * This runs before the build process to catch configuration issues early.
 */

import { validateEnvironmentVariables } from './sanitize-build.js';

/**
 * Main environment validation function
 */
function validateEnv() {
  console.log('🔍 Environment Validation Starting');
  console.log('==================================\n');

  // Validate environment variables only
  const validation = validateEnvironmentVariables();

  // Report warnings
  if (validation.warnings.length > 0) {
    console.log('\n⚠️  Warnings:');
    validation.warnings.forEach(warning => {
      console.log(`   ${warning}`);
    });
  }

  // Report errors
  if (validation.errors.length > 0) {
    console.log('\n❌ Errors:');
    validation.errors.forEach(error => {
      console.log(`   ${error}`);
    });

    console.log('\n🚫 Environment validation failed due to configuration issues');
    process.exit(1);
  }

  // Success
  console.log('✅ Environment validation completed successfully');
  console.log(`   ${Object.keys(validation.publicVars).length} public variables validated`);
  console.log(`   ${Object.keys(validation.privateVars).length} private variables secured\n`);
}

// Run validation if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  validateEnv();
}

export { validateEnv };
