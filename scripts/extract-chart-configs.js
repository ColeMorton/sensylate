#!/usr/bin/env node
/**
 * Chart Configuration Extractor
 *
 * Extracts chart configurations from TypeScript files and makes them
 * available to the Python dashboard generation pipeline.
 * This eliminates hardcoded chart configurations in Python.
 */

const fs = require('fs');
const path = require('path');

// Path to the frontend charts directory
const CHARTS_DIR = path.join(__dirname, '..', 'frontend', 'src', 'charts');
const OUTPUT_FILE = path.join(__dirname, 'chart-configs.json');

/**
 * Extract chart configuration from TypeScript file
 * This is a simple parser - in production could use TypeScript compiler API
 */
function extractChartConfig(configPath) {
  try {
    const content = fs.readFileSync(configPath, 'utf8');

    // Simple regex extraction (would be more robust with AST parsing)
    const titleMatch = content.match(/title:\s*["']([^"']+)["']/);
    const categoryMatch = content.match(/category:\s*["']([^"']+)["']/);
    const descriptionMatch = content.match(/description:\s*["']([^"']+)["']/);
    const chartTypeMatch = content.match(/chartType:\s*["']([^"']+)["']/);

    if (!titleMatch || !categoryMatch || !descriptionMatch || !chartTypeMatch) {
      console.warn(`Could not parse configuration from: ${configPath}`);
      return null;
    }

    return {
      title: titleMatch[1],
      category: categoryMatch[1],
      description: descriptionMatch[1],
      chartType: chartTypeMatch[1]
    };
  } catch (error) {
    console.error(`Error reading ${configPath}:`, error.message);
    return null;
  }
}

/**
 * Dashboard to chart type mappings
 * Maps dashboard IDs to the chart types they contain
 */
const DASHBOARD_CHART_MAPPINGS = {
  'bitcoin_cycle_intelligence': ['btc-price'],
  // Add more mappings as charts are migrated to colocation
};

/**
 * Discover all chart configurations and organize by dashboard
 */
function discoverChartConfigs() {
  const chartConfigs = {};

  if (!fs.existsSync(CHARTS_DIR)) {
    console.warn(`Charts directory not found: ${CHARTS_DIR}`);
    return chartConfigs;
  }

  // First, collect all available chart configurations
  const availableCharts = {};

  // Scan for chart directories
  const entries = fs.readdirSync(CHARTS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory() || entry.name.startsWith('.')) {
      continue;
    }

    const chartDir = path.join(CHARTS_DIR, entry.name);
    const configPath = path.join(chartDir, 'chart.config.ts');

    if (fs.existsSync(configPath)) {
      const config = extractChartConfig(configPath);
      if (config) {
        availableCharts[config.chartType] = config;
        console.log(`✅ Extracted config for chart type: ${config.chartType}`);
      }
    } else {
      console.warn(`⏭️  No chart.config.ts found in: ${chartDir}`);
    }
  }

  // Now organize charts by dashboard based on mappings
  for (const [dashboardId, chartTypes] of Object.entries(DASHBOARD_CHART_MAPPINGS)) {
    const dashboardCharts = [];

    for (const chartType of chartTypes) {
      if (availableCharts[chartType]) {
        dashboardCharts.push(availableCharts[chartType]);
        console.log(`✅ Mapped ${chartType} to dashboard: ${dashboardId}`);
      } else {
        console.warn(`⚠️  Chart type ${chartType} not found for dashboard: ${dashboardId}`);
      }
    }

    if (dashboardCharts.length > 0) {
      chartConfigs[dashboardId] = dashboardCharts;
    }
  }

  return chartConfigs;
}

/**
 * Main execution
 */
function main() {
  console.log('🔨 Extracting chart configurations...');
  console.log(`📁 Scanning: ${CHARTS_DIR}`);

  const chartConfigs = discoverChartConfigs();

  // Write to JSON file for Python consumption
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(chartConfigs, null, 2));

  console.log(`✅ Extracted ${Object.keys(chartConfigs).length} chart configurations`);
  console.log(`📄 Output written to: ${OUTPUT_FILE}`);
}

if (require.main === module) {
  main();
}

module.exports = { discoverChartConfigs, extractChartConfig };
