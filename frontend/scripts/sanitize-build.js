/**
 * Build-time Secret Sanitization Script
 *
 * Ensures no sensitive environment variables are exposed in the client-side bundle.
 * This script runs during the build process to validate and sanitize configuration.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define sensitive patterns that should never appear in builds
const SENSITIVE_PATTERNS = [
  // Actual secret patterns (with value constraints)
  /api[_-]?key\s*[:=]\s*["'][^"']{8,}["']/i,
  /secret[_-]?key\s*[:=]\s*["'][^"']{8,}["']/i,
  /private[_-]?key\s*[:=]\s*["'][^"']{8,}["']/i,
  /auth[_-]?token\s*[:=]\s*["'][^"']{8,}["']/i,
  /access[_-]?token\s*[:=]\s*["'][^"']{8,}["']/i,
  /refresh[_-]?token\s*[:=]\s*["'][^"']{8,}["']/i,
  /session[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,
  /jwt[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,
  /database[_-]?url\s*[:=]\s*["'][^"']{8,}["']/i,

  // Service-specific patterns with values
  /stripe[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,
  /paypal[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,
  /aws[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,
  /google[_-]?client[_-]?secret\s*[:=]\s*["'][^"']{8,}["']/i,

  // Actual secret values (common formats)
  /['""][A-Za-z0-9]{32,}['""]/, // Base64-like strings
  /['""]sk_[A-Za-z0-9]{24,}['""]/, // Stripe secret keys
  /['""]pk_[A-Za-z0-9]{24,}['""]/, // Stripe public keys (still sensitive)
  /['""]\w{8}-\w{4}-\w{4}-\w{4}-\w{12}['""]/, // UUID format
];

// Patterns to ignore (legitimate uses)
const IGNORE_PATTERNS = [
  // HTML input types
  /type\s*=\s*["']password["']/i,
  /\[type=password\]/i,

  // Blog content references
  /Password sharing/i,
  /password rotation/i,
  /complex passwords/i,
  /strong password/i,

  // Library code patterns
  /\.password\s*!/i, // TypeScript non-null assertion
  /use-credentials/i, // HTML attribute value
  /credentialless/i, // HTML attribute value
  /api_key.*apiKey/i, // Disqus library mapping

  // CSS selectors
  /input\[type=password\]/i,

  // Plotly.js library patterns (legitimate library code)
  /plotly.*api_key/i, // Plotly mapbox integration
  /stamen.*api_key/i, // Plotly stamen map tiles
  /mapbox.*access_token/i, // Plotly mapbox integration
  /StructArrayLayout.*[A-Za-z0-9]{32,}/i, // Plotly WebGL struct layouts
  /plotly.*access_token/i, // Plotly access token examples
  /EVENTS_URL.*access_token/i, // Plotly analytics
  /"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"/i, // Plotly character set
  /StructArrayLayout[0-9a-zA-Z]+/i, // Plotly WebGL layouts
  /'my-access-token'/i, // Plotly documentation example
  /slice\(-9\).*api_key/i, // Plotly API key slice check
  /indexOf.*access_token/i, // Plotly access token index check
  /\.params\.push.*access_token/i, // Plotly URL parameter building
  /_mapboxAccessToken/i, // Plotly mapbox token variable
  /styleValueDflt/i, // Plotly style defaults
];

// Allowed public prefixes (these are safe to expose)
const ALLOWED_PUBLIC_PREFIXES = [
  'PUBLIC_',
  'VITE_',
  'REACT_APP_',
  'NEXT_PUBLIC_',
  'NUXT_PUBLIC_',
];

/**
 * Check if an environment variable name is safe to expose publicly
 */
function isPublicVariable(name) {
  // Check if it starts with an allowed public prefix
  const hasPublicPrefix = ALLOWED_PUBLIC_PREFIXES.some(prefix =>
    name.startsWith(prefix)
  );

  if (!hasPublicPrefix) {
    return false;
  }

  // Even with public prefix, check for sensitive patterns
  const hasSensitivePattern = SENSITIVE_PATTERNS.some(pattern =>
    pattern.test(name)
  );

  return !hasSensitivePattern;
}

/**
 * Validate environment variables before build
 */
function validateEnvironmentVariables() {
  const errors = [];
  const warnings = [];

  // Get all environment variables
  const allEnvVars = { ...process.env };

  // Separate public and private variables
  const publicVars = {};
  const privateVars = {};

  Object.entries(allEnvVars).forEach(([name, value]) => {
    if (isPublicVariable(name)) {
      publicVars[name] = value;
    } else {
      privateVars[name] = value;
    }
  });

  console.log('🔍 Environment Variable Analysis');
  console.log('================================');
  console.log(`✅ Public variables: ${Object.keys(publicVars).length}`);
  console.log(`🔒 Private variables: ${Object.keys(privateVars).length}`);

  // Check for potential issues
  Object.entries(publicVars).forEach(([name, value]) => {
    // Check for suspicious values in public variables
    if (value && typeof value === 'string') {
      // Check for potential secrets in values
      if (value.length > 32 && /^[A-Za-z0-9+/=]+$/.test(value)) {
        warnings.push(`PUBLIC variable ${name} has a value that looks like a base64-encoded secret`);
      }

      // Check for URLs with credentials
      if (value.includes('://') && (value.includes('@') || value.includes('password'))) {
        errors.push(`PUBLIC variable ${name} contains a URL with embedded credentials`);
      }

      // Check for common secret formats
      if (/^[0-9a-f]{32,}$/i.test(value) || /^[A-Z0-9]{20,}$/.test(value)) {
        warnings.push(`PUBLIC variable ${name} has a value that looks like a secret key`);
      }
    }
  });

  // Check for accidentally exposed private variables
  Object.keys(privateVars).forEach(name => {
    if (name.startsWith('REACT_APP_') || name.startsWith('VITE_') || name.startsWith('NEXT_PUBLIC_')) {
      errors.push(`Variable ${name} uses a public prefix but is not marked as PUBLIC_`);
    }
  });

  return { errors, warnings, publicVars, privateVars };
}

/**
 * Scan build output for potential secret exposure
 */
function scanBuildOutput(buildDir) {
  const issues = [];

  if (!fs.existsSync(buildDir)) {
    console.log(`⚠️  Build directory ${buildDir} does not exist, skipping scan`);
    return issues;
  }

  // Recursively scan all files in build directory
  function scanDirectory(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    entries.forEach(entry => {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        scanDirectory(fullPath);
      } else if (entry.isFile() && (entry.name.endsWith('.js') || entry.name.endsWith('.html') || entry.name.endsWith('.css'))) {
        try {
          const content = fs.readFileSync(fullPath, 'utf8');

          // Check for sensitive patterns in content
          SENSITIVE_PATTERNS.forEach(pattern => {
            const matches = content.match(new RegExp(pattern.source, 'gi'));
            if (matches) {
              matches.forEach(match => {
                const context = content.substring(
                  Math.max(0, content.indexOf(match) - 50),
                  content.indexOf(match) + match.length + 50
                );

                // Check if this match should be ignored
                const shouldIgnore = IGNORE_PATTERNS.some(ignorePattern =>
                  ignorePattern.test(context) || ignorePattern.test(match)
                );

                if (!shouldIgnore) {
                  issues.push({
                    file: path.relative(buildDir, fullPath),
                    pattern: pattern.source,
                    match: match,
                    context: context
                  });
                }
              });
            }
          });

        } catch (error) {
          console.log(`⚠️  Could not scan file ${fullPath}: ${error.message}`);
        }
      }
    });
  }

  scanDirectory(buildDir);
  return issues;
}

/**
 * Main sanitization function
 */
function sanitizeBuild() {
  console.log('🛡️  Build Sanitization Starting');
  console.log('===============================\n');

  // Validate environment variables
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

    console.log('\n🚫 Build sanitization failed due to security issues');
    process.exit(1);
  }

  // Scan build output if it exists
  const buildDir = path.join(__dirname, '..', 'dist');
  const buildIssues = scanBuildOutput(buildDir);

  if (buildIssues.length > 0) {
    console.log('\n🚨 Sensitive content found in build output:');
    buildIssues.forEach(issue => {
      console.log(`   File: ${issue.file}`);
      console.log(`   Pattern: ${issue.pattern}`);
      console.log(`   Match: ${issue.match}`);
      console.log(`   Context: ...${issue.context}...`);
      console.log('');
    });

    console.log('🚫 Build contains sensitive information and cannot be deployed');
    process.exit(1);
  }

  // Success
  console.log('\n✅ Build sanitization completed successfully');
  console.log(`   ${Object.keys(validation.publicVars).length} public variables validated`);
  console.log(`   ${Object.keys(validation.privateVars).length} private variables secured`);
  console.log('   No sensitive content found in build output\n');
}

// Run sanitization if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  sanitizeBuild();
}

export { sanitizeBuild, validateEnvironmentVariables, scanBuildOutput };
