/**
 * Enhanced Debug Script for Chart Loading Issue
 *
 * Focuses on the specific issue where charts show "Loading chart data..."
 * then disappear completely
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const DEV_SERVER_URL = 'http://localhost:4321';
const DEBUG_OUTPUT_DIR = path.join(process.cwd(), 'debug-chart-issue');

// Ensure output directory exists
if (!fs.existsSync(DEBUG_OUTPUT_DIR)) {
  fs.mkdirSync(DEBUG_OUTPUT_DIR, { recursive: true });
}

class ChartLoadingDebugger {
  constructor() {
    this.browser = null;
    this.page = null;
    this.results = {
      timestamp: new Date().toISOString(),
      errors: [],
      warnings: [],
      networkErrors: [],
      dataRequests: [],
      componentStates: [],
      plotlyStatus: null
    };
  }

  async init() {
    console.log('🔍 Enhanced Chart Loading Debugger\n');

    this.browser = await puppeteer.launch({
      headless: false,
      slowMo: 50,
      devtools: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1400, height: 900 });

    // Enhanced console logging
    this.page.on('console', (msg) => {
      const type = msg.type();
      const text = msg.text();
      const args = msg.args();

      console.log(`   [${type.toUpperCase()}] ${text}`);

      if (type === 'error') {
        this.results.errors.push({
          text,
          timestamp: Date.now(),
          stackTrace: msg.stackTrace()
        });
      } else if (type === 'warn') {
        this.results.warnings.push({
          text,
          timestamp: Date.now()
        });
      }
    });

    // Monitor all network requests
    this.page.on('request', (request) => {
      const url = request.url();

      // Track data requests
      if (url.includes('/data/') || url.includes('.csv')) {
        console.log(`   📊 Data Request: ${request.method()} ${url}`);
        this.results.dataRequests.push({
          url,
          method: request.method(),
          timestamp: Date.now()
        });
      }
    });

    // Monitor network failures
    this.page.on('requestfailed', (request) => {
      const failure = request.failure();
      console.log(`   ❌ Request Failed: ${request.url()}`);
      console.log(`      Reason: ${failure ? failure.errorText : 'Unknown'}`);

      this.results.networkErrors.push({
        url: request.url(),
        error: failure ? failure.errorText : 'Unknown',
        timestamp: Date.now()
      });
    });

    // Monitor responses
    this.page.on('response', (response) => {
      const url = response.url();
      const status = response.status();

      if (url.includes('/data/') || url.includes('.csv')) {
        console.log(`   📥 Data Response: ${status} ${url}`);

        if (status >= 400) {
          this.results.networkErrors.push({
            url,
            status,
            statusText: response.statusText(),
            timestamp: Date.now()
          });
        }
      }
    });

    // Catch page errors
    this.page.on('pageerror', (error) => {
      console.log(`   💥 Page Error: ${error.message}`);
      this.results.errors.push({
        message: error.message,
        stack: error.stack,
        timestamp: Date.now()
      });
    });
  }

  async monitorChartLifecycle() {
    console.log('\n📊 Monitoring Chart Component Lifecycle...\n');

    // Navigate to charts page
    console.log('   Loading /charts page...');
    const response = await this.page.goto(`${DEV_SERVER_URL}/charts`, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    console.log(`   Page loaded with status: ${response.status()}\n`);

    // Monitor component states over time
    const checkInterval = 500; // Check every 500ms
    const totalDuration = 15000; // Monitor for 15 seconds
    let elapsed = 0;

    while (elapsed < totalDuration) {
      const state = await this.captureComponentState();
      this.results.componentStates.push({
        timestamp: elapsed,
        ...state
      });

      // Log significant changes
      if (elapsed === 0 || elapsed % 2000 === 0) {
        console.log(`\n   ⏱️  Time: ${elapsed}ms`);
        console.log(`   📊 Charts visible: ${state.chartsVisible}`);
        console.log(`   ⏳ Loading spinners: ${state.loadingSpinners}`);
        console.log(`   ❌ Error messages: ${state.errorMessages.length}`);
        console.log(`   📈 Plotly elements: ${state.plotlyElements}`);
      }

      await new Promise(resolve => setTimeout(resolve, checkInterval));
      elapsed += checkInterval;
    }
  }

  async captureComponentState() {
    return await this.page.evaluate(() => {
      // Count various elements
      const loadingSpinners = document.querySelectorAll('.animate-spin, [class*="loading"]').length;
      const errorElements = document.querySelectorAll('.text-red-500, .text-red-600, [class*="error"]');
      const plotlyElements = document.querySelectorAll('.plotly, .js-plotly-plot').length;
      const chartContainers = document.querySelectorAll('[class*="chart-container"], [class*="chart-display"]');

      // Check if charts are visible
      const chartsVisible = Array.from(chartContainers).filter(container => {
        const rect = container.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0 && container.offsetParent !== null;
      }).length;

      // Get error messages
      const errorMessages = Array.from(errorElements).map(el => el.textContent?.trim() || '');

      // Check for "Loading chart data..." text
      const loadingTexts = Array.from(document.querySelectorAll('*')).filter(el =>
        el.textContent?.includes('Loading chart data')
      ).length;

      // Check Plotly status
      const plotlyStatus = {
        loaded: typeof window.Plotly !== 'undefined',
        version: typeof window.Plotly !== 'undefined' ? window.Plotly.version : null
      };

      // Check React components
      const reactComponents = Array.from(document.querySelectorAll('[data-reactroot], [class*="ChartDisplay"]')).length;

      return {
        loadingSpinners,
        errorMessages,
        plotlyElements,
        chartContainers: chartContainers.length,
        chartsVisible,
        loadingTexts,
        plotlyStatus,
        reactComponents,
        documentHeight: document.documentElement.scrollHeight,
        visibleHeight: window.innerHeight
      };
    });
  }

  async checkDataAvailability() {
    console.log('\n📂 Checking Data File Availability...\n');

    const dataFiles = [
      '/data/raw/stocks/AAPL/daily.csv',
      '/data/raw/stocks/MSTR/daily.csv',
      '/data/portfolio/multi_strategy_portfolio_portfolio_value.csv',
      '/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv',
      '/data/portfolio/live-signals/live_signals_equity.csv',
      '/data/portfolio/closed_positions_pnl_progression.csv',
      '/data/portfolio/open_positions_pnl_current.csv'
    ];

    for (const file of dataFiles) {
      try {
        const response = await this.page.evaluate(async (url) => {
          try {
            const res = await fetch(url);
            return {
              status: res.status,
              ok: res.ok,
              statusText: res.statusText
            };
          } catch (error) {
            return {
              status: 0,
              ok: false,
              error: error.message
            };
          }
        }, `${DEV_SERVER_URL}${file}`);

        const icon = response.ok ? '✅' : '❌';
        console.log(`   ${icon} ${file}: ${response.status} ${response.statusText || response.error || ''}`);
      } catch (error) {
        console.log(`   ❌ ${file}: Error - ${error.message}`);
      }
    }
  }

  async captureDebugInfo() {
    console.log('\n📸 Capturing Debug Information...\n');

    // Take screenshots
    const screenshotPath = path.join(DEBUG_OUTPUT_DIR, 'chart-issue-state.png');
    await this.page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`   📸 Screenshot saved: ${screenshotPath}`);

    // Capture HTML snapshot
    const htmlContent = await this.page.content();
    const htmlPath = path.join(DEBUG_OUTPUT_DIR, 'chart-issue-snapshot.html');
    fs.writeFileSync(htmlPath, htmlContent);
    console.log(`   📄 HTML snapshot saved: ${htmlPath}`);

    // Check for React DevTools
    const reactInfo = await this.page.evaluate(() => {
      const reactRoot = document.querySelector('#__next') || document.querySelector('[data-reactroot]');
      const hasReactDevTools = window.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== undefined;

      return {
        hasReactRoot: !!reactRoot,
        hasReactDevTools,
        reactVersion: window.React ? window.React.version : 'Not found'
      };
    });

    console.log(`\n   ⚛️  React Status:`);
    console.log(`      Root Element: ${reactInfo.hasReactRoot ? 'Found' : 'Not found'}`);
    console.log(`      DevTools: ${reactInfo.hasReactDevTools ? 'Available' : 'Not available'}`);
    console.log(`      Version: ${reactInfo.reactVersion}`);
  }

  async generateReport() {
    console.log('\n📝 Generating Debug Report...\n');

    const report = {
      ...this.results,
      summary: {
        totalErrors: this.results.errors.length,
        totalWarnings: this.results.warnings.length,
        totalNetworkErrors: this.results.networkErrors.length,
        totalDataRequests: this.results.dataRequests.length,
        chartsEverVisible: this.results.componentStates.some(s => s.chartsVisible > 0),
        plotlyEverLoaded: this.results.componentStates.some(s => s.plotlyStatus?.loaded),
        loadingPhaseDetected: this.results.componentStates.some(s => s.loadingSpinners > 0)
      }
    };

    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'debug-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`   📄 Report saved: ${reportPath}`);

    // Print summary
    console.log('\n📊 Debug Summary:');
    console.log(`   ❌ Errors: ${report.summary.totalErrors}`);
    console.log(`   ⚠️  Warnings: ${report.summary.totalWarnings}`);
    console.log(`   🌐 Network Errors: ${report.summary.totalNetworkErrors}`);
    console.log(`   📊 Data Requests: ${report.summary.totalDataRequests}`);
    console.log(`   👁️  Charts Ever Visible: ${report.summary.chartsEverVisible ? 'Yes' : 'No'}`);
    console.log(`   📈 Plotly Loaded: ${report.summary.plotlyEverLoaded ? 'Yes' : 'No'}`);

    return report;
  }

  async cleanup() {
    if (this.browser) {
      console.log('\n🔍 Browser kept open for manual inspection. Press Ctrl+C to exit.');
      // Keep browser open for inspection
      await new Promise(() => {}); // Wait indefinitely
    }
  }

  async run() {
    try {
      await this.init();
      await this.monitorChartLifecycle();
      await this.checkDataAvailability();
      await this.captureDebugInfo();
      const report = await this.generateReport();

      // Analyze results
      if (report.summary.totalErrors > 0) {
        console.log('\n❌ Errors found! Check the report for details.');
      }

      if (!report.summary.chartsEverVisible && report.summary.loadingPhaseDetected) {
        console.log('\n⚠️  Charts showed loading state but never became visible!');
        console.log('   This matches the reported issue.');
      }

    } catch (error) {
      console.error('💥 Debug script failed:', error);
    } finally {
      await this.cleanup();
    }
  }
}

// Check if dev server is running
async function checkDevServer() {
  try {
    const response = await fetch(DEV_SERVER_URL);
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Main execution
async function main() {
  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  const chartDebugger = new ChartLoadingDebugger();
  await chartDebugger.run();
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n👋 Shutting down...');
  process.exit(0);
});

main().catch(console.error);
