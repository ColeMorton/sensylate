/**
 * Debug Plotly Loading Issues
 *
 * Simple script to debug why Plotly.js is not loading on the charts page
 */

import puppeteer from 'puppeteer';

const DEV_SERVER_URL = 'http://localhost:4321';

async function debugPlotlyLoading() {
  console.log('🔍 Debugging Plotly.js Loading Issues\n');

  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    devtools: true
  });

  const page = await browser.newPage();

  // Enable console logging
  page.on('console', (msg) => {
    const type = msg.type();
    const text = msg.text();
    const icon = type === 'error' ? '❌' : type === 'warn' ? '⚠️' : '📝';
    console.log(`   ${icon} [${type}] ${text}`);
  });

  // Enable request/response monitoring
  page.on('request', (request) => {
    if (request.url().includes('plotly') || request.url().includes('chart')) {
      console.log(`   📤 Request: ${request.method()} ${request.url()}`);
    }
  });

  page.on('response', (response) => {
    if (response.url().includes('plotly') || response.url().includes('chart')) {
      console.log(`   📥 Response: ${response.status()} ${response.url()}`);
    }
  });

  try {
    console.log('📍 Loading charts page...');
    await page.goto(`${DEV_SERVER_URL}/charts`, {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    console.log('✅ Page loaded, analyzing chart containers...');

    // Wait a bit for React components to initialize
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Check current state
    const pageState = await page.evaluate(() => {
      const chartContainers = document.querySelectorAll('.chart-container');
      const chartDisplayComponents = document.querySelectorAll('[data-chart-type], .chart-display');
      const loadingElements = document.querySelectorAll('.animate-spin');
      const errorElements = document.querySelectorAll('.text-red-500');
      const plotlyElements = document.querySelectorAll('.plotly');

      return {
        chartContainers: chartContainers.length,
        chartDisplayComponents: chartDisplayComponents.length,
        loadingElements: loadingElements.length,
        errorElements: errorElements.length,
        plotlyElements: plotlyElements.length,
        windowPlotly: typeof window.Plotly,
        reactVersion: window.React ? 'loaded' : 'not loaded',
        chartContainerContent: Array.from(chartContainers).map(container => ({
          html: container.innerHTML.substring(0, 200),
          hasError: container.querySelector('.text-red-500') !== null,
          hasLoading: container.querySelector('.animate-spin') !== null,
          hasPlotly: container.querySelector('.plotly') !== null
        }))
      };
    });

    console.log('\n📊 Page Analysis:');
    console.log(`   Chart Containers: ${pageState.chartContainers}`);
    console.log(`   Chart Components: ${pageState.chartDisplayComponents}`);
    console.log(`   Loading Elements: ${pageState.loadingElements}`);
    console.log(`   Error Elements: ${pageState.errorElements}`);
    console.log(`   Plotly Elements: ${pageState.plotlyElements}`);
    console.log(`   Window.Plotly: ${pageState.windowPlotly}`);
    console.log(`   React: ${pageState.reactVersion}`);

    // Show first few chart containers
    console.log('\n📋 Chart Container Details:');
    pageState.chartContainerContent.slice(0, 3).forEach((container, index) => {
      console.log(`   Container ${index + 1}:`);
      console.log(`     Has Error: ${container.hasError}`);
      console.log(`     Has Loading: ${container.hasLoading}`);
      console.log(`     Has Plotly: ${container.hasPlotly}`);
      if (container.hasError || container.hasLoading) {
        console.log(`     HTML Preview: ${container.html}...`);
      }
    });

    // Wait longer and check again
    console.log('\n⏳ Waiting 10 more seconds for components to load...');
    await new Promise(resolve => setTimeout(resolve, 10000));

    const finalState = await page.evaluate(() => {
      return {
        plotlyElements: document.querySelectorAll('.plotly').length,
        windowPlotly: typeof window.Plotly,
        loadingElements: document.querySelectorAll('.animate-spin').length,
        errorElements: document.querySelectorAll('.text-red-500').length,
        errorMessages: Array.from(document.querySelectorAll('.text-red-500')).map(el => el.textContent)
      };
    });

    console.log('\n📊 Final Analysis:');
    console.log(`   Plotly Elements: ${finalState.plotlyElements}`);
    console.log(`   Window.Plotly: ${finalState.windowPlotly}`);
    console.log(`   Still Loading: ${finalState.loadingElements}`);
    console.log(`   Errors: ${finalState.errorElements}`);

    if (finalState.errorMessages.length > 0) {
      console.log('\n❌ Error Messages:');
      finalState.errorMessages.forEach((msg, index) => {
        console.log(`   ${index + 1}. ${msg}`);
      });
    }

    // Keep browser open for manual inspection
    console.log('\n🔍 Browser kept open for manual inspection. Close when done.');
    await new Promise(resolve => setTimeout(resolve, 60000)); // Wait 1 minute

  } catch (error) {
    console.error('💥 Debug failed:', error);
  } finally {
    await browser.close();
  }
}

debugPlotlyLoading().catch(console.error);
