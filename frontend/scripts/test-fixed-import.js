/**
 * Test Fixed Import Pattern
 */

import puppeteer from 'puppeteer';

async function testFixedImport() {
  console.log('🧪 Testing Fixed Import Pattern\n');

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

    // Test the new simplified import pattern
    const importTest = await page.evaluate(async () => {
      try {
        console.log('Testing simplified import...');

        // Test the simplified import
        const plotlyModule = await import('react-plotly.js');
        console.log('React-plotly.js module:', Object.keys(plotlyModule));
        console.log('Default export exists:', typeof plotlyModule.default);

        if (plotlyModule.default) {
          console.log('Plot component type:', typeof plotlyModule.default);
          return { success: true, component: typeof plotlyModule.default };
        } else {
          return { success: false, error: 'No default export' };
        }

      } catch (error) {
        console.log('Import test error:', error.message);
        return { success: false, error: error.message };
      }
    });

    console.log('\n📊 Fixed Import Test Result:');
    console.log(JSON.stringify(importTest, null, 2));

    // Wait a bit for charts to render
    console.log('\n⏳ Waiting for charts to render...');
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Check if Plotly elements are now present
    const plotlyCheck = await page.evaluate(() => {
      const plotlyElements = document.querySelectorAll('.plotly, .js-plotly-plot').length;
      const chartContainers = document.querySelectorAll('[class*="chart-container"], [class*="chart-display"]').length;

      return {
        plotlyElements,
        chartContainers,
        plotlyGlobal: typeof window.Plotly !== 'undefined'
      };
    });

    console.log('\n📈 Chart Rendering Status:');
    console.log(`   Plotly Elements: ${plotlyCheck.plotlyElements}`);
    console.log(`   Chart Containers: ${plotlyCheck.chartContainers}`);
    console.log(`   Plotly Global: ${plotlyCheck.plotlyGlobal}`);

    // Take screenshot
    await page.screenshot({ path: 'debug-chart-issue/fixed-import-test.png', fullPage: true });
    console.log('\n📸 Screenshot saved: debug-chart-issue/fixed-import-test.png');

    console.log('\n🔍 Browser kept open for inspection. Press Ctrl+C to exit.');
    await new Promise(resolve => setTimeout(resolve, 30000));

  } catch (error) {
    console.error('💥 Test failed:', error);
  } finally {
    await browser.close();
  }
}

testFixedImport().catch(console.error);
