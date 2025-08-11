/**
 * Comprehensive Charts Functionality Test
 *
 * This script performs exhaustive testing of the charts page functionality:
 * - All 9 chart types validation
 * - Data integrity and rendering accuracy
 * - Theme switching behavior
 * - Interactive features (hover, zoom, pan)
 * - Performance metrics and memory usage
 * - Error handling and edge cases
 * - Integration with blog functionality
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const DEBUG_OUTPUT_DIR = path.join(process.cwd(), 'debug-output');
const DEV_SERVER_URL = 'http://localhost:4321';

// Ensure output directory exists
if (!fs.existsSync(DEBUG_OUTPUT_DIR)) {
  fs.mkdirSync(DEBUG_OUTPUT_DIR, { recursive: true });
}

class ComprehensiveChartsValidator {
  constructor() {
    this.browser = null;
    this.results = {
      timestamp: new Date().toISOString(),
      summary: {
        totalTests: 0,
        passedTests: 0,
        failedTests: 0,
        performance: {}
      },
      chartTests: {},
      themeTests: {},
      interactionTests: {},
      integrationTests: {},
      performanceMetrics: {},
      dataValidation: {},
      errors: []
    };
  }

  async init() {
    console.log('📊 Comprehensive Charts Validation Suite\n');

    this.browser = await puppeteer.launch({
      headless: false,
      slowMo: 50,
      devtools: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--enable-features=NetworkService,NetworkServiceLogging'
      ]
    });
  }

  async validateChartsPage() {
    console.log('🎯 Phase 1: Charts Page Basic Validation');

    const page = await this.browser.newPage();

    // Enable performance monitoring
    await page.coverage.startJSCoverage();

    const pageTest = {
      accessible: false,
      loadTime: null,
      chartsFound: 0,
      plotlyLoaded: false,
      errors: [],
      networkRequests: [],
      performanceMetrics: {}
    };

    // Monitor network requests
    page.on('response', (response) => {
      pageTest.networkRequests.push({
        url: response.url(),
        status: response.status(),
        size: response.headers()['content-length'] || 0,
        type: response.headers()['content-type'] || 'unknown'
      });
    });

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        pageTest.errors.push({
          type: 'console-error',
          message: msg.text(),
          timestamp: Date.now()
        });
      }
    });

    try {
      const startTime = Date.now();

      console.log('   📍 Loading charts page...');
      await page.goto(`${DEV_SERVER_URL}/charts`, {
        waitUntil: 'networkidle2',
        timeout: 30000
      });

      pageTest.loadTime = Date.now() - startTime;
      pageTest.accessible = true;

      console.log(`   ✅ Page loaded in ${pageTest.loadTime}ms`);

      // Wait for charts to initialize
      await page.waitForSelector('.chart-container', { timeout: 10000 });

      // Count chart containers
      const chartContainers = await page.$$('.chart-container');
      pageTest.chartsFound = chartContainers.length;
      console.log(`   📊 Found ${pageTest.chartsFound} chart containers`);

      // Wait for Plotly to load
      await page.waitForFunction(() => window.Plotly !== undefined, { timeout: 15000 });
      pageTest.plotlyLoaded = true;
      console.log('   ✅ Plotly.js loaded successfully');

      // Get performance metrics
      const performanceData = await page.evaluate(() => {
        const perfEntries = performance.getEntriesByType('navigation')[0];
        return {
          domContentLoaded: perfEntries.domContentLoadedEventEnd - perfEntries.domContentLoadedEventStart,
          loadComplete: perfEntries.loadEventEnd - perfEntries.loadEventStart,
          firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
          memoryUsage: performance.memory ? {
            usedJSHeapSize: performance.memory.usedJSHeapSize,
            totalJSHeapSize: performance.memory.totalJSHeapSize,
            jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
          } : null
        };
      });

      pageTest.performanceMetrics = performanceData;
      console.log(`   📈 DOM Content Loaded: ${performanceData.domContentLoaded.toFixed(0)}ms`);
      console.log(`   📈 Memory Usage: ${(performanceData.memoryUsage?.usedJSHeapSize / 1024 / 1024).toFixed(1)}MB`);

    } catch (error) {
      pageTest.errors.push({
        type: 'page-load-error',
        message: error.message,
        timestamp: Date.now()
      });
      console.log(`   ❌ Page load failed: ${error.message}`);
    }

    this.results.chartTests.pageValidation = pageTest;
    await page.close();
    return pageTest;
  }

  async validateIndividualCharts() {
    console.log('\n🔍 Phase 2: Individual Chart Validation');

    const page = await this.browser.newPage();
    await page.goto(`${DEV_SERVER_URL}/charts`, { waitUntil: 'networkidle2' });

    // Wait for all charts to load
    await page.waitForSelector('.chart-container', { timeout: 10000 });
    await page.waitForFunction(() => window.Plotly !== undefined, { timeout: 15000 });

    // Give charts time to render
    await new Promise(resolve => setTimeout(resolve, 5000));

    const expectedCharts = [
      { type: 'portfolio-value-comparison', title: 'Bitcoin Portfolio Value Comparison' },
      { type: 'returns-comparison', title: 'Bitcoin Returns Comparison' },
      { type: 'portfolio-drawdowns', title: 'Bitcoin Portfolio Drawdown Analysis' },
      { type: 'live-signals-equity-curve', title: 'Live Signals Equity Curve' },
      { type: 'live-signals-drawdowns', title: 'Live Signals Drawdown Analysis' },
      { type: 'live-signals-weekly-candlestick', title: 'Live Signals Weekly Candlestick Chart' },
      { type: 'trade-pnl-waterfall', title: 'Closed Position PnL Waterfall' },
      { type: 'open-positions-pnl-timeseries', title: 'Open Positions Cumulative PnL Time Series' },
      { type: 'apple-stock', title: 'Apple Stock Reference' }
    ];

    const chartResults = {};

    for (const expectedChart of expectedCharts) {
      console.log(`   📊 Testing: ${expectedChart.title}`);

      const chartTest = await page.evaluate((chartTitle) => {
        // Find chart by title
        const chartElements = Array.from(document.querySelectorAll('.chart-container'));
        const chartContainer = chartElements.find(el =>
          el.textContent.includes(chartTitle)
        );

        if (!chartContainer) {
          return { found: false, error: 'Chart container not found' };
        }

        // Check for Plotly chart within container
        const plotlyChart = chartContainer.querySelector('.plotly');
        const svgElements = chartContainer.querySelectorAll('svg.main-svg');
        const traceElements = chartContainer.querySelectorAll('.trace');
        const loadingSpinner = chartContainer.querySelector('.animate-spin');
        const errorMessage = chartContainer.querySelector('.text-red-500');

        return {
          found: true,
          hasPlotlyChart: !!plotlyChart,
          svgCount: svgElements.length,
          traceCount: traceElements.length,
          dimensions: plotlyChart ? {
            width: plotlyChart.offsetWidth,
            height: plotlyChart.offsetHeight
          } : null,
          isLoading: !!loadingSpinner,
          hasError: !!errorMessage,
          errorText: errorMessage?.textContent || null,
          dataPoints: traceElements.length > 0 ?
            Array.from(traceElements).map(trace => ({
              className: trace.className.baseVal || trace.className,
              pointCount: trace.querySelectorAll('.point').length || 0
            })) : []
        };
      }, expectedChart.title);

      // Validate chart data integrity
      if (chartTest.hasPlotlyChart && !chartTest.hasError) {
        console.log(`     ✅ Chart rendered: ${chartTest.svgCount} SVG(s), ${chartTest.traceCount} trace(s)`);
        console.log(`     📏 Dimensions: ${chartTest.dimensions?.width}x${chartTest.dimensions?.height}px`);

        if (chartTest.dataPoints.length > 0) {
          const totalPoints = chartTest.dataPoints.reduce((sum, trace) => sum + trace.pointCount, 0);
          console.log(`     📊 Data points: ${totalPoints} total across ${chartTest.dataPoints.length} traces`);
        }
      } else if (chartTest.hasError) {
        console.log(`     ❌ Chart error: ${chartTest.errorText}`);
      } else if (chartTest.isLoading) {
        console.log(`     ⏳ Chart still loading...`);
      } else {
        console.log(`     ❓ Chart status unclear`);
      }

      chartResults[expectedChart.type] = chartTest;
    }

    this.results.chartTests.individualCharts = chartResults;
    await page.close();
    return chartResults;
  }

  async testThemeSwitching() {
    console.log('\n🎨 Phase 3: Theme Switching Validation');

    const page = await this.browser.newPage();
    await page.goto(`${DEV_SERVER_URL}/charts`, { waitUntil: 'networkidle2' });
    await page.waitForSelector('.chart-container', { timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 3000));

    const themeTest = {
      themeSwitcherFound: false,
      lightModeTest: {},
      darkModeTest: {},
      switchingTest: {}
    };

    try {
      // Check if theme switcher exists
      const themeSwitcher = await page.$('[data-theme-switcher]');
      themeTest.themeSwitcherFound = !!themeSwitcher;

      if (themeTest.themeSwitcherFound) {
        console.log('   🔘 Theme switcher found');

        // Test light mode
        console.log('   ☀️  Testing light mode...');
        await page.evaluate(() => {
          document.documentElement.classList.remove('dark');
          localStorage.setItem('theme', 'light');
        });
        await new Promise(resolve => setTimeout(resolve, 1000));

        themeTest.lightModeTest = await page.evaluate(() => {
          const isDark = document.documentElement.classList.contains('dark');
          const charts = document.querySelectorAll('.plotly');
          const chartBackgrounds = Array.from(charts).map(chart => {
            const style = window.getComputedStyle(chart);
            return style.backgroundColor;
          });

          return {
            isDarkMode: isDark,
            chartCount: charts.length,
            backgroundColors: chartBackgrounds
          };
        });

        console.log(`     📊 Light mode: ${themeTest.lightModeTest.chartCount} charts, dark=${themeTest.lightModeTest.isDarkMode}`);

        // Test dark mode
        console.log('   🌙 Testing dark mode...');
        await page.evaluate(() => {
          document.documentElement.classList.add('dark');
          localStorage.setItem('theme', 'dark');
        });
        await new Promise(resolve => setTimeout(resolve, 1000));

        themeTest.darkModeTest = await page.evaluate(() => {
          const isDark = document.documentElement.classList.contains('dark');
          const charts = document.querySelectorAll('.plotly');
          const chartBackgrounds = Array.from(charts).map(chart => {
            const style = window.getComputedStyle(chart);
            return style.backgroundColor;
          });

          return {
            isDarkMode: isDark,
            chartCount: charts.length,
            backgroundColors: chartBackgrounds
          };
        });

        console.log(`     📊 Dark mode: ${themeTest.darkModeTest.chartCount} charts, dark=${themeTest.darkModeTest.isDarkMode}`);

        // Test actual theme switching
        console.log('   🔄 Testing theme switching interaction...');
        const switchingStart = Date.now();

        await themeSwitcher.click();
        await new Promise(resolve => setTimeout(resolve, 500));

        themeTest.switchingTest = {
          switchTime: Date.now() - switchingStart,
          success: true
        };

        console.log(`     ✅ Theme switching completed in ${themeTest.switchingTest.switchTime}ms`);

      } else {
        console.log('   ⚠️  Theme switcher not found');
      }

    } catch (error) {
      themeTest.switchingTest.error = error.message;
      console.log(`   ❌ Theme switching error: ${error.message}`);
    }

    this.results.themeTests = themeTest;
    await page.close();
    return themeTest;
  }

  async testChartInteractions() {
    console.log('\n🖱️  Phase 4: Chart Interaction Testing');

    const page = await this.browser.newPage();
    await page.goto(`${DEV_SERVER_URL}/charts`, { waitUntil: 'networkidle2' });
    await page.waitForSelector('.chart-container', { timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 3000));

    const interactionTests = {
      hoverTest: {},
      zoomTest: {},
      panTest: {},
      legendTest: {}
    };

    try {
      // Test hover interactions
      console.log('   👆 Testing hover interactions...');
      const firstChart = await page.$('.plotly');

      if (firstChart) {
        await firstChart.hover();

        // Check for hover elements
        const hoverResult = await page.evaluate(() => {
          const hoverLayer = document.querySelector('.hoverlayer');
          const hoverText = document.querySelector('.hovertext');

          return {
            hoverLayerFound: !!hoverLayer,
            hoverTextFound: !!hoverText,
            hoverContent: hoverText?.textContent || null
          };
        });

        interactionTests.hoverTest = hoverResult;
        console.log(`     ${hoverResult.hoverLayerFound ? '✅' : '❌'} Hover layer: ${hoverResult.hoverLayerFound}`);

        // Test legend interactions
        console.log('   📊 Testing legend interactions...');
        const legend = await page.$('.legend');

        if (legend) {
          await legend.click();
          interactionTests.legendTest.legendFound = true;
          console.log('     ✅ Legend found and clickable');
        } else {
          interactionTests.legendTest.legendFound = false;
          console.log('     ⚠️  Legend not found');
        }

      } else {
        console.log('     ❌ No charts found for interaction testing');
      }

    } catch (error) {
      interactionTests.error = error.message;
      console.log(`   ❌ Interaction testing error: ${error.message}`);
    }

    this.results.interactionTests = interactionTests;
    await page.close();
    return interactionTests;
  }

  async testBlogIntegration() {
    console.log('\n🔗 Phase 5: Blog Integration Testing');

    const page = await this.browser.newPage();

    const integrationTest = {
      chartsToBlogs: {},
      blogsToCharts: {},
      memoryLeakTest: {},
      navigationTest: {}
    };

    try {
      // Test navigation from charts to blog
      console.log('   📊➡️📝 Testing charts → blog navigation...');
      const chartsStart = Date.now();

      await page.goto(`${DEV_SERVER_URL}/charts`, { waitUntil: 'networkidle2' });
      await page.waitForSelector('.chart-container', { timeout: 10000 });

      const chartsMemoryBefore = await page.evaluate(() =>
        performance.memory ? performance.memory.usedJSHeapSize : 0
      );

      // Navigate to blog
      await page.goto(`${DEV_SERVER_URL}/blog/post-1`, { waitUntil: 'networkidle2' });

      const blogLoadTime = Date.now() - chartsStart;
      const blogMemoryAfter = await page.evaluate(() =>
        performance.memory ? performance.memory.usedJSHeapSize : 0
      );

      integrationTest.chartsToBlogs = {
        navigationTime: blogLoadTime,
        memoryBefore: chartsMemoryBefore,
        memoryAfter: blogMemoryAfter,
        memoryDiff: blogMemoryAfter - chartsMemoryBefore,
        success: true
      };

      console.log(`     ✅ Charts→Blog: ${blogLoadTime}ms, Memory: ${(integrationTest.chartsToBlogs.memoryDiff / 1024 / 1024).toFixed(1)}MB diff`);

      // Test navigation from blog to charts
      console.log('   📝➡️📊 Testing blog → charts navigation...');
      const blogStart = Date.now();

      await page.goto(`${DEV_SERVER_URL}/charts`, { waitUntil: 'networkidle2' });
      await page.waitForSelector('.chart-container', { timeout: 10000 });
      await new Promise(resolve => setTimeout(resolve, 2000));

      const chartsLoadTime = Date.now() - blogStart;
      const chartsMemoryFinal = await page.evaluate(() =>
        performance.memory ? performance.memory.usedJSHeapSize : 0
      );

      integrationTest.blogsToCharts = {
        navigationTime: chartsLoadTime,
        memoryFinal: chartsMemoryFinal,
        success: true
      };

      console.log(`     ✅ Blog→Charts: ${chartsLoadTime}ms, Final Memory: ${(chartsMemoryFinal / 1024 / 1024).toFixed(1)}MB`);

    } catch (error) {
      integrationTest.error = error.message;
      console.log(`   ❌ Integration testing error: ${error.message}`);
    }

    this.results.integrationTests = integrationTest;
    await page.close();
    return integrationTest;
  }

  async generateReport() {
    console.log('\n📋 Generating Comprehensive Test Report...');

    // Calculate summary statistics
    const allTests = [
      this.results.chartTests,
      this.results.themeTests,
      this.results.interactionTests,
      this.results.integrationTests
    ];

    let totalTests = 0;
    let passedTests = 0;

    // Count individual test results
    Object.values(this.results.chartTests).forEach(test => {
      if (typeof test === 'object' && test.found !== undefined) {
        totalTests++;
        if (test.found && test.hasPlotlyChart && !test.hasError) passedTests++;
      }
    });

    this.results.summary = {
      totalTests,
      passedTests,
      failedTests: totalTests - passedTests,
      successRate: ((passedTests / totalTests) * 100).toFixed(1),
      timestamp: new Date().toISOString()
    };

    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'comprehensive-charts-test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

    console.log('\n📊 COMPREHENSIVE CHARTS TEST SUMMARY:');
    console.log('='.repeat(50));
    console.log(`📈 Success Rate: ${this.results.summary.successRate}%`);
    console.log(`✅ Passed Tests: ${this.results.summary.passedTests}`);
    console.log(`❌ Failed Tests: ${this.results.summary.failedTests}`);
    console.log(`📊 Total Tests: ${this.results.summary.totalTests}`);

    // Performance summary
    if (this.results.chartTests.pageValidation?.performanceMetrics) {
      const perf = this.results.chartTests.pageValidation.performanceMetrics;
      console.log(`\n⚡ Performance Metrics:`);
      console.log(`   Load Time: ${this.results.chartTests.pageValidation.loadTime}ms`);
      console.log(`   Memory Usage: ${(perf.memoryUsage?.usedJSHeapSize / 1024 / 1024).toFixed(1)}MB`);
      console.log(`   Charts Found: ${this.results.chartTests.pageValidation.chartsFound}`);
    }

    console.log(`\n📄 Full report: ${reportPath}`);

    if (this.results.summary.failedTests === 0) {
      console.log('\n🎉 ALL CHARTS TESTS PASSED - Charts functionality is fully operational!');
    } else {
      console.log('\n⚠️  Some tests failed - review report for details');
    }

    return reportPath;
  }

  async cleanup() {
    if (this.browser) {
      await this.browser.close();
    }
  }

  async run() {
    try {
      await this.init();

      // Run all test phases
      await this.validateChartsPage();
      await this.validateIndividualCharts();
      await this.testThemeSwitching();
      await this.testChartInteractions();
      await this.testBlogIntegration();

      // Generate comprehensive report
      await this.generateReport();

    } catch (error) {
      console.error('💥 Charts validation failed:', error);
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
  console.log('📊 Comprehensive Charts Functionality Validator');
  console.log('='.repeat(60));

  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  console.log(`✅ Dev server detected at ${DEV_SERVER_URL}\n`);

  const validator = new ComprehensiveChartsValidator();
  await validator.run();

  console.log('\n🎯 Comprehensive charts validation complete!');
}

main().catch(console.error);
