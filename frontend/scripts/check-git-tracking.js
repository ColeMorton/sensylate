#!/usr/bin/env node
/**
 * Check for untracked files that are being imported
 * Helps prevent Netlify build failures due to missing files
 */

import { execSync } from 'child_process';
import { readFileSync } from 'fs';
import { glob } from 'glob';
import path from 'path';

const IMPORT_PATTERNS = [
  /import\s+.*\s+from\s+['"`]([^'"`]+)['"`]/g,
  /import\(['"`]([^'"`]+)['"`]\)/g,
  /require\(['"`]([^'"`]+)['"`]\)/g
];

function getUntrackedFiles() {
  try {
    const output = execSync('git ls-files --others --exclude-standard', { encoding: 'utf8' });
    return output.trim().split('\n').filter(line => line.length > 0);
  } catch (error) {
    console.error('Error getting untracked files:', error.message);
    return [];
  }
}

function getTrackedFiles() {
  try {
    const output = execSync('git ls-files', { encoding: 'utf8' });
    return new Set(output.trim().split('\n'));
  } catch (error) {
    console.error('Error getting tracked files:', error.message);
    return new Set();
  }
}

function extractImports(filePath) {
  try {
    const content = readFileSync(filePath, 'utf8');
    const imports = [];

    IMPORT_PATTERNS.forEach(pattern => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        imports.push(match[1]);
      }
    });

    return imports;
  } catch (error) {
    console.warn(`Could not read file ${filePath}:`, error.message);
    return [];
  }
}

function resolveImportPath(importPath, fromFile) {
  // Handle relative imports
  if (importPath.startsWith('./') || importPath.startsWith('../')) {
    const dir = path.dirname(fromFile);
    let resolved = path.resolve(dir, importPath);

    // Try different extensions
    const extensions = ['.ts', '.tsx', '.js', '.jsx', '.astro'];
    for (const ext of extensions) {
      const withExt = resolved + ext;
      if (withExt.startsWith(process.cwd())) {
        return path.relative(process.cwd(), withExt);
      }
    }

    // Return original if no extension works
    return path.relative(process.cwd(), resolved);
  }

  // Handle @ alias imports (map to src/)
  if (importPath.startsWith('@/')) {
    const resolved = importPath.replace('@/', 'src/');
    const extensions = ['.ts', '.tsx', '.js', '.jsx', '.astro'];

    for (const ext of extensions) {
      const withExt = resolved + ext;
      return withExt;
    }

    return resolved;
  }

  // Skip node_modules imports
  if (!importPath.startsWith('.') && !importPath.startsWith('/')) {
    return null;
  }

  return importPath;
}

async function main() {
  console.log('🔍 Checking for untracked files that are being imported...\n');

  const untrackedFiles = getUntrackedFiles();
  const trackedFiles = getTrackedFiles();

  console.log(`📊 Found ${untrackedFiles.length} untracked files`);
  console.log(`📊 Found ${trackedFiles.size} tracked files\n`);

  // Get all source files
  const sourceFiles = await glob('src/**/*.{ts,tsx,js,jsx,astro}', {
    ignore: ['node_modules/**', 'dist/**', '.astro/**']
  });

  const issues = [];

  for (const file of sourceFiles) {
    const imports = extractImports(file);

    for (const importPath of imports) {
      const resolvedPath = resolveImportPath(importPath, file);

      if (resolvedPath && untrackedFiles.includes(resolvedPath)) {
        issues.push({
          file,
          import: importPath,
          resolvedPath,
          exists: untrackedFiles.includes(resolvedPath)
        });
      }
    }
  }

  if (issues.length > 0) {
    console.log('❌ Found imports to untracked files:');
    console.log('═'.repeat(60));

    issues.forEach(issue => {
      console.log(`📄 File: ${issue.file}`);
      console.log(`📦 Import: ${issue.import}`);
      console.log(`🎯 Resolves to: ${issue.resolvedPath}`);
      console.log(`⚠️  Status: UNTRACKED (will cause build failures)`);
      console.log('─'.repeat(40));
    });

    console.log('\n🚨 RECOMMENDED ACTIONS:');
    console.log('1. Review the untracked files above');
    console.log('2. Add important files to git: git add <file>');
    console.log('3. Or update .gitignore if they should not be tracked');
    console.log('4. Run this script before pushing to catch issues early\n');

    process.exit(1);
  } else {
    console.log('✅ All imports point to tracked files or external modules');
    console.log('✅ No build issues detected\n');
  }

  // Also check for untracked files in key directories
  const criticalUntrackedFiles = untrackedFiles.filter(file =>
    file.startsWith('src/lib/') ||
    file.startsWith('src/layouts/components/') ||
    file.startsWith('src/hooks/') ||
    file.endsWith('.ts') ||
    file.endsWith('.tsx') ||
    file.endsWith('.astro')
  );

  if (criticalUntrackedFiles.length > 0) {
    console.log('⚠️  Found untracked files in critical directories:');
    criticalUntrackedFiles.forEach(file => {
      console.log(`   📄 ${file}`);
    });
    console.log('\n💡 Consider if these should be tracked in git\n');
  }
}

main().catch(console.error);
