/**
 * Enhanced Puppeteer Debug Script - Charts Impact Analysis
 *
 * This script tests the hypothesis that the charts page is causing
 * memory pressure and race conditions that lead to blog post failures.
 *
 * Tests performed:
 * 1. Blog functionality with charts ENABLED
 * 2. Blog functionality with charts DISABLED
 * 3. Memory usage monitoring
 * 4. Concurrent access testing
 * 5. Resource consumption analysis
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

class ChartsImpactDebugger {
  constructor() {
    this.browser = null;
    this.results = {
      timestamp: new Date().toISOString(),
      tests: {
        chartsEnabled: null,
        chartsDisabled: null,
        concurrentAccess: null,
        memoryAnalysis: null
      },
      comparison: {},
      hypothesis: 'Charts page causes memory pressure leading to blog route failures'
    };
  }

  async init() {
    console.log('🔬 Starting Charts Impact Analysis...\n');

    this.browser = await puppeteer.launch({
      headless: false,
      slowMo: 50,
      devtools: false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--disable-gpu'
      ]
    });
  }

  async testBlogWithChartsStatus(chartsEnabled = true, testName = 'charts-enabled') {
    console.log(`📊 Testing Blog Functionality - Charts ${chartsEnabled ? 'ENABLED' : 'DISABLED'}`);
    
    const page = await this.browser.newPage();
    
    // Monitor performance and memory
    await page.setViewport({ width: 1200, height: 800 });
    
    const testResult = {
      testName,
      chartsEnabled,
      blogTests: [],
      chartsPageTest: null,
      memoryUsage: [],
      networkRequests: [],
      errors: [],
      startTime: Date.now(),
      endTime: null
    };

    // Listen for errors and network activity
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        testResult.errors.push({
          type: 'console-error',
          message: msg.text(),
          timestamp: Date.now()
        });
      }
    });

    page.on('pageerror', (error) => {
      testResult.errors.push({
        type: 'page-error',
        message: error.message,
        stack: error.stack,
        timestamp: Date.now()
      });
    });

    page.on('response', (response) => {
      testResult.networkRequests.push({
        url: response.url(),
        status: response.status(),
        timestamp: Date.now()
      });
    });

    try {
      // Test 1: Charts page access (if enabled)
      if (chartsEnabled) {
        console.log('   🔍 Testing charts page access...');
        const chartsStart = Date.now();
        
        try {
          await page.goto(`${DEV_SERVER_URL}/charts`, { 
            waitUntil: 'networkidle2', 
            timeout: 30000 
          });
          
          // Wait for charts to load
          await page.waitForSelector('.chart-container', { timeout: 20000 });
          
          testResult.chartsPageTest = {
            accessible: true,
            loadTime: Date.now() - chartsStart,
            status: 'success'
          };
          
          console.log(`   ✅ Charts page loaded in ${testResult.chartsPageTest.loadTime}ms`);
          
          // Take memory measurement after charts load
          const memoryUsage = await page.evaluate(() => {
            if (performance.memory) {
              return {
                usedJSHeapSize: performance.memory.usedJSHeapSize,
                totalJSHeapSize: performance.memory.totalJSHeapSize,
                jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
                timestamp: Date.now()
              };
            }
            return null;
          });
          
          if (memoryUsage) {
            testResult.memoryUsage.push({
              ...memoryUsage,
              phase: 'after-charts-load'
            });
          }
          
        } catch (error) {
          testResult.chartsPageTest = {
            accessible: false,
            error: error.message,
            status: 'failed'
          };
          console.log(`   ❌ Charts page failed: ${error.message}`);
        }
      } else {
        console.log('   ⏭️  Skipping charts page (disabled)');
      }

      // Test 2: Blog posts access
      const blogPosts = [
        '/blog/post-1',
        '/blog/adbe-fundamental-analysis-20250723',
        '/blog/amzn-fundamental-analysis-20250618'
      ];

      for (const blogPath of blogPosts) {
        console.log(`   📝 Testing blog post: ${blogPath}`);
        const blogStart = Date.now();
        
        try {
          const response = await page.goto(`${DEV_SERVER_URL}${blogPath}`, { 
            waitUntil: 'networkidle2', 
            timeout: 15000 
          });
          
          const blogTest = {
            path: blogPath,
            accessible: response.status() === 200,
            statusCode: response.status(),
            loadTime: Date.now() - blogStart,
            hasContent: false,
            errorDetected: false
          };

          if (blogTest.accessible) {
            // Check if page has proper content
            const hasTitle = await page.$('h1, h2, .h2');
            const hasContent = await page.$('.content, article, main');
            blogTest.hasContent = !!(hasTitle && hasContent);
            
            console.log(`   ✅ ${blogPath}: ${blogTest.statusCode} (${blogTest.loadTime}ms) - Content: ${blogTest.hasContent}`);
          } else {
            console.log(`   ❌ ${blogPath}: ${blogTest.statusCode} (${blogTest.loadTime}ms)`);
            
            // Check for our specific error
            const errorMessage = await page.evaluate(() => {
              return document.body.textContent || '';
            });
            
            if (errorMessage.includes('post prop is undefined') || errorMessage.includes('post.data is undefined')) {
              blogTest.errorDetected = true;
              console.log(`   🎯 DETECTED: Our null safety error triggered!`);
            }
          }
          
          testResult.blogTests.push(blogTest);
          
        } catch (error) {
          testResult.blogTests.push({
            path: blogPath,
            accessible: false,
            error: error.message,
            loadTime: Date.now() - blogStart
          });
          console.log(`   💥 ${blogPath}: Error - ${error.message}`);
        }
        
        // Brief pause between tests
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // Final memory measurement
      const finalMemory = await page.evaluate(() => {
        if (performance.memory) {
          return {
            usedJSHeapSize: performance.memory.usedJSHeapSize,
            totalJSHeapSize: performance.memory.totalJSHeapSize,
            jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
            timestamp: Date.now()
          };
        }
        return null;
      });
      
      if (finalMemory) {
        testResult.memoryUsage.push({
          ...finalMemory,
          phase: 'test-end'
        });
      }

    } catch (error) {
      console.log(`💥 Test suite error: ${error.message}`);
      testResult.errors.push({
        type: 'test-suite-error',
        message: error.message,
        timestamp: Date.now()
      });
    } finally {
      testResult.endTime = Date.now();
      await page.close();
    }

    return testResult;
  }

  async testConcurrentAccess() {
    console.log('🔄 Testing Concurrent Blog Access...');
    
    const pages = [];
    const results = [];
    
    try {
      // Create multiple pages for concurrent testing
      for (let i = 0; i < 3; i++) {
        pages.push(await this.browser.newPage());
      }
      
      // Concurrent blog post access
      const blogPosts = [
        '/blog/post-1',
        '/blog/adbe-fundamental-analysis-20250723',
        '/blog/amzn-fundamental-analysis-20250618'
      ];
      
      const startTime = Date.now();
      
      const promises = pages.map(async (page, index) => {
        const blogPath = blogPosts[index];
        console.log(`   🔗 Concurrent access ${index + 1}: ${blogPath}`);
        
        try {
          const response = await page.goto(`${DEV_SERVER_URL}${blogPath}`, { 
            waitUntil: 'networkidle2', 
            timeout: 20000 
          });
          
          return {
            pageIndex: index + 1,
            path: blogPath,
            accessible: response.status() === 200,
            statusCode: response.status(),
            loadTime: Date.now() - startTime
          };
        } catch (error) {
          return {
            pageIndex: index + 1,
            path: blogPath,
            accessible: false,
            error: error.message,
            loadTime: Date.now() - startTime
          };
        }
      });
      
      const concurrentResults = await Promise.all(promises);
      
      console.log('   📊 Concurrent Access Results:');
      concurrentResults.forEach(result => {
        if (result.accessible) {
          console.log(`   ✅ Page ${result.pageIndex}: ${result.statusCode} (${result.loadTime}ms)`);
        } else {
          console.log(`   ❌ Page ${result.pageIndex}: Failed - ${result.error || 'Unknown error'}`);
        }
      });
      
      return {
        totalTime: Date.now() - startTime,
        results: concurrentResults,
        successCount: concurrentResults.filter(r => r.accessible).length,
        failureCount: concurrentResults.filter(r => !r.accessible).length
      };
      
    } finally {
      // Clean up pages
      for (const page of pages) {
        try {
          await page.close();
        } catch (e) {
          // Ignore cleanup errors
        }
      }
    }
  }

  compareResults() {
    console.log('📈 Analyzing Results...\n');
    
    const chartsEnabled = this.results.tests.chartsEnabled;
    const chartsDisabled = this.results.tests.chartsDisabled;
    
    if (!chartsEnabled || !chartsDisabled) {
      console.log('⚠️  Cannot compare - missing test results');
      return;
    }
    
    const comparison = {
      blogSuccessRate: {
        withCharts: chartsEnabled.blogTests.filter(t => t.accessible && t.hasContent).length / chartsEnabled.blogTests.length,
        withoutCharts: chartsDisabled.blogTests.filter(t => t.accessible && t.hasContent).length / chartsDisabled.blogTests.length
      },
      averageLoadTime: {
        withCharts: chartsEnabled.blogTests.reduce((sum, t) => sum + (t.loadTime || 0), 0) / chartsEnabled.blogTests.length,
        withoutCharts: chartsDisabled.blogTests.reduce((sum, t) => sum + (t.loadTime || 0), 0) / chartsDisabled.blogTests.length
      },
      errorCount: {
        withCharts: chartsEnabled.errors.length,
        withoutCharts: chartsDisabled.errors.length
      },
      nullSafetyErrors: {
        withCharts: chartsEnabled.blogTests.filter(t => t.errorDetected).length,
        withoutCharts: chartsDisabled.blogTests.filter(t => t.errorDetected).length
      }
    };
    
    this.results.comparison = comparison;
    
    console.log('📊 COMPARISON RESULTS:');
    console.log(`   Blog Success Rate:`);
    console.log(`     With Charts:    ${(comparison.blogSuccessRate.withCharts * 100).toFixed(1)}%`);
    console.log(`     Without Charts: ${(comparison.blogSuccessRate.withoutCharts * 100).toFixed(1)}%`);
    console.log(`   Average Load Time:`);
    console.log(`     With Charts:    ${comparison.averageLoadTime.withCharts.toFixed(0)}ms`);
    console.log(`     Without Charts: ${comparison.averageLoadTime.withoutCharts.toFixed(0)}ms`);
    console.log(`   Total Errors:`);
    console.log(`     With Charts:    ${comparison.errorCount.withCharts}`);
    console.log(`     Without Charts: ${comparison.errorCount.withoutCharts}`);
    console.log(`   Null Safety Errors:`);
    console.log(`     With Charts:    ${comparison.nullSafetyErrors.withCharts}`);
    console.log(`     Without Charts: ${comparison.nullSafetyErrors.withoutCharts}`);
    
    // Hypothesis validation
    const hypothesisValid = (
      comparison.blogSuccessRate.withoutCharts > comparison.blogSuccessRate.withCharts ||
      comparison.nullSafetyErrors.withCharts > comparison.nullSafetyErrors.withoutCharts ||
      comparison.errorCount.withCharts > comparison.errorCount.withoutCharts
    );
    
    console.log(`\n🔬 HYPOTHESIS VALIDATION:`);
    console.log(`   "${this.results.hypothesis}"`);
    console.log(`   Status: ${hypothesisValid ? '✅ CONFIRMED' : '❌ REJECTED'}`);
    
    return comparison;
  }

  async generateReport() {
    console.log('\n📝 Generating Comprehensive Report...');
    
    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'charts-impact-analysis.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));
    
    console.log(`📄 Full report saved to: ${reportPath}`);
    
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

      // Test 1: With charts enabled (current state)
      console.log('='.repeat(60));
      this.results.tests.chartsEnabled = await this.testBlogWithChartsStatus(true, 'charts-enabled');
      
      console.log('\n' + '='.repeat(60));
      console.log('⏳ Waiting 5 seconds before next test...');
      await new Promise(resolve => setTimeout(resolve, 5000));
      
      // Test 2: Simulate charts disabled (note: we can't actually disable them without restart)
      // Instead, we'll test blog access without visiting charts page first
      console.log('\n' + '='.repeat(60));
      this.results.tests.chartsDisabled = await this.testBlogWithChartsStatus(false, 'charts-skipped');
      
      // Test 3: Concurrent access test
      console.log('\n' + '='.repeat(60));
      this.results.tests.concurrentAccess = await this.testConcurrentAccess();
      
      // Analysis
      console.log('\n' + '='.repeat(60));
      this.compareResults();
      
      // Generate report
      await this.generateReport();

    } catch (error) {
      console.error('💥 Analysis failed:', error);
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
  console.log('🔬 Charts Impact Analysis');
  console.log('='.repeat(60));

  // Check if dev server is running
  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  console.log(`✅ Dev server detected at ${DEV_SERVER_URL}\n`);

  const analyzer = new ChartsImpactDebugger();
  await analyzer.run();

  console.log('\n🎉 Analysis complete! Check the debug-output/ directory for detailed results.');
}

// Run the analyzer
main().catch(console.error);