/**
 * Test Plotly.js Import Pattern
 *
 * This script tests the exact import pattern used in ChartRenderer
 * to see if it's working correctly
 */

import puppeteer from 'puppeteer';

async function testPlotlyImport() {
  console.log('🧪 Testing Plotly.js Import Pattern\n');

  const browser = await puppeteer.launch({
    headless: false,
    devtools: true
  });

  const page = await browser.newPage();

  // Enable console logging
  page.on('console', (msg) => {
    console.log(`   [${msg.type().toUpperCase()}] ${msg.text()}`);
  });

  page.on('pageerror', (error) => {
    console.log(`   💥 Page Error: ${error.message}`);
  });

  try {
    await page.goto('http://localhost:4321/charts', {
      waitUntil: 'networkidle2'
    });

    // Test the exact import pattern from ChartRenderer
    const importTest = await page.evaluate(async () => {
      try {
        console.log('Testing import pattern...');

        // Test step 1: Import factory
        const factoryModule = await import('react-plotly.js/factory');
        console.log('Factory module:', Object.keys(factoryModule));
        console.log('Factory default exists:', typeof factoryModule.default);

        // Test step 2: Import Plotly
        const plotlyModule = await import('plotly.js-dist');
        console.log('Plotly module:', Object.keys(plotlyModule));
        console.log('Plotly default exists:', typeof plotlyModule.default);

        // Test step 3: Create component
        if (factoryModule.default && plotlyModule.default) {
          const PlotComponent = factoryModule.default(plotlyModule.default);
          console.log('Plot component created:', typeof PlotComponent);
          return { success: true, component: typeof PlotComponent };
        } else {
          return { success: false, error: 'Missing factory or plotly' };
        }

      } catch (error) {
        console.log('Import test error:', error.message);
        return { success: false, error: error.message };
      }
    });

    console.log('\n📊 Import Test Result:');
    console.log(JSON.stringify(importTest, null, 2));

    // Also test alternative patterns
    console.log('\n🔄 Testing Alternative Import Patterns...');

    const altTest = await page.evaluate(async () => {
      try {
        // Alternative 1: Import plotly differently
        const plotlyModule = await import('plotly.js-dist');
        console.log('Plotly module keys:', Object.keys(plotlyModule));

        // Alternative 2: Check what's actually exported
        if (plotlyModule.default) {
          console.log('Plotly default keys:', Object.keys(plotlyModule.default));
        }

        return {
          plotlyKeys: Object.keys(plotlyModule),
          plotlyDefaultKeys: plotlyModule.default ? Object.keys(plotlyModule.default) : null
        };

      } catch (error) {
        return { error: error.message };
      }
    });

    console.log('Alternative test result:');
    console.log(JSON.stringify(altTest, null, 2));

    // Keep browser open
    console.log('\n🔍 Browser kept open. Check DevTools for more details.');
    await new Promise(resolve => setTimeout(resolve, 30000));

  } catch (error) {
    console.error('💥 Test failed:', error);
  } finally {
    await browser.close();
  }
}

testPlotlyImport().catch(console.error);
