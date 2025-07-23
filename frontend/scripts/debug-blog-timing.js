/**
 * Puppeteer Debug Script for Blog Post Timing Issue
 *
 * Reproduces and debugs the specific error:
 * "Cannot read properties of undefined (reading 'data')"
 * that occurs after 10-20 seconds on blog/analysis pages
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

class BlogTimingDebugger {
  constructor() {
    this.browser = null;
    this.page = null;
    this.results = {
      timestamp: new Date().toISOString(),
      testRuns: [],
      errors: [],
      network: [],
      console: [],
      targetError: null,
      timing: {
        errorOccurredAt: null,
        totalWaitTime: 25000 // 25 seconds to be safe
      }
    };
  }

  async init() {
    console.log('🚀 Starting Blog Post Timing Debug...\n');

    this.browser = await puppeteer.launch({
      headless: false, // Show browser for debugging
      slowMo: 50,
      devtools: true
    });

    this.page = await this.browser.newPage();

    // Set viewport for consistent testing
    await this.page.setViewport({ width: 1200, height: 800 });

    // Listen for network requests
    this.page.on('request', (request) => {
      this.results.network.push({
        type: 'request',
        url: request.url(),
        method: request.method(),
        timestamp: Date.now()
      });
    });

    // Listen for network responses
    this.page.on('response', (response) => {
      this.results.network.push({
        type: 'response',
        url: response.url(),
        status: response.status(),
        statusText: response.statusText(),
        timestamp: Date.now()
      });
    });

    // Listen for console logs and errors
    this.page.on('console', (msg) => {
      const logEntry = {
        type: msg.type(),
        text: msg.text(),
        timestamp: Date.now()
      };
      
      this.results.console.push(logEntry);
      
      // Check for our specific error
      if (msg.type() === 'error' && msg.text().includes("Cannot read properties of undefined (reading 'data')")) {
        console.log('🎯 TARGET ERROR DETECTED!');
        console.log(`   Time: ${new Date().toLocaleTimeString()}`);
        console.log(`   Message: ${msg.text()}`);
        
        this.results.targetError = {
          ...logEntry,
          detectedAt: Date.now()
        };
      }
    });

    // Listen for page errors
    this.page.on('pageerror', (error) => {
      console.log('💥 Page Error:', error.message);
      
      const errorEntry = {
        type: 'pageerror',
        message: error.message,
        stack: error.stack,
        timestamp: Date.now()
      };
      
      this.results.errors.push(errorEntry);
      
      // Check if this is our target error
      if (error.message.includes("Cannot read properties of undefined (reading 'data')")) {
        console.log('🎯 TARGET PAGE ERROR DETECTED!');
        console.log(`   Time: ${new Date().toLocaleTimeString()}`);
        console.log(`   Message: ${error.message}`);
        
        this.results.targetError = {
          ...errorEntry,
          detectedAt: Date.now()
        };
      }
    });
  }

  async testBlogRoute(routePath, description, waitTime = 25000) {
    console.log(`📍 Testing: ${routePath} (${description})`);
    console.log(`   Waiting ${waitTime/1000} seconds for timing issue...`);

    const testResult = {
      path: routePath,
      description,
      startTime: Date.now(),
      endTime: null,
      accessible: false,
      statusCode: null,
      title: null,
      screenshots: [],
      errorDetected: false,
      errorTime: null,
      loadTime: null,
      errors: []
    };

    try {
      const navigationStart = Date.now();

      // Navigate to the route
      const response = await this.page.goto(`${DEV_SERVER_URL}${routePath}`, {
        waitUntil: 'networkidle2',
        timeout: 10000
      });

      testResult.loadTime = Date.now() - navigationStart;
      testResult.statusCode = response.status();
      testResult.accessible = response.status() === 200;

      if (testResult.accessible) {
        testResult.title = await this.page.title();
        console.log(`   ✅ Status: ${testResult.statusCode} | Load Time: ${testResult.loadTime}ms`);
        console.log(`   📄 Title: "${testResult.title}"`);

        // Take initial screenshot
        const initialScreenshot = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}_initial.png`);
        await this.page.screenshot({
          path: initialScreenshot,
          fullPage: false
        });
        testResult.screenshots.push({ type: 'initial', path: initialScreenshot, timestamp: Date.now() });

        // Wait with periodic screenshots to capture the timing issue
        const startWait = Date.now();
        const checkInterval = 5000; // Check every 5 seconds
        let intervalCount = 0;

        while ((Date.now() - startWait) < waitTime) {
          await new Promise(resolve => setTimeout(resolve, checkInterval));
          intervalCount++;

          // Take periodic screenshot
          const periodicScreenshot = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}_${intervalCount * 5}s.png`);
          await this.page.screenshot({
            path: periodicScreenshot,
            fullPage: false
          });
          testResult.screenshots.push({ 
            type: 'periodic', 
            path: periodicScreenshot, 
            timestamp: Date.now(),
            secondsElapsed: intervalCount * 5
          });

          console.log(`   ⏱️  ${intervalCount * 5}s elapsed...`);

          // Check if target error was detected
          if (this.results.targetError && !testResult.errorDetected) {
            testResult.errorDetected = true;
            testResult.errorTime = this.results.targetError.detectedAt - startWait;
            console.log(`   🎯 ERROR DETECTED after ${testResult.errorTime}ms!`);
            
            // Take error screenshot
            const errorScreenshot = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}_error.png`);
            await this.page.screenshot({
              path: errorScreenshot,
              fullPage: true
            });
            testResult.screenshots.push({ type: 'error', path: errorScreenshot, timestamp: Date.now() });
            break;
          }
        }

        // Take final screenshot
        const finalScreenshot = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}_final.png`);
        await this.page.screenshot({
          path: finalScreenshot,
          fullPage: false
        });
        testResult.screenshots.push({ type: 'final', path: finalScreenshot, timestamp: Date.now() });

      } else {
        console.log(`   ❌ Status: ${testResult.statusCode} | Load Time: ${testResult.loadTime}ms`);
      }

    } catch (error) {
      console.log(`   💥 Error: ${error.message}`);
      testResult.errors.push({
        message: error.message,
        stack: error.stack
      });
    }

    testResult.endTime = Date.now();
    this.results.testRuns.push(testResult);
    console.log(''); // Empty line for readability

    return testResult;
  }

  async testMultipleBlogPosts() {
    console.log('📚 Testing Multiple Blog Posts...\n');

    // Test a few different blog posts to see if the issue is consistent
    const blogPosts = [
      '/blog/post-1',
      '/blog/adbe-fundamental-analysis-20250723',
      '/blog/amzn-fundamental-analysis-20250618',
    ];

    for (const blogPath of blogPosts) {
      await this.testBlogRoute(blogPath, 'Individual blog post', 20000);
      
      // Brief pause between tests
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  async analyzeResults() {
    console.log('📊 Analyzing Results...\n');

    const totalTests = this.results.testRuns.length;
    const errorDetections = this.results.testRuns.filter(t => t.errorDetected).length;
    const consoleErrors = this.results.console.filter(c => c.type === 'error').length;
    const pageErrors = this.results.errors.length;

    console.log(`📊 Test Summary:`);
    console.log(`   🧪 Total Tests: ${totalTests}`);
    console.log(`   🎯 Target Error Detected: ${errorDetections}/${totalTests} tests`);
    console.log(`   💥 Console Errors: ${consoleErrors}`);
    console.log(`   💥 Page Errors: ${pageErrors}`);

    if (this.results.targetError) {
      console.log(`\n🎯 Target Error Details:`);
      console.log(`   Time: ${new Date(this.results.targetError.timestamp).toLocaleTimeString()}`);
      console.log(`   Type: ${this.results.targetError.type}`);
      console.log(`   Message: ${this.results.targetError.message || this.results.targetError.text}`);
    }

    // Show all console errors for analysis
    const allErrors = this.results.console.filter(c => c.type === 'error');
    if (allErrors.length > 0) {
      console.log(`\n💥 All Console Errors:`);
      allErrors.forEach((error, index) => {
        console.log(`   ${index + 1}. [${new Date(error.timestamp).toLocaleTimeString()}] ${error.text}`);
      });
    }
  }

  async generateReport() {
    console.log('📝 Generating Debug Report...\n');

    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'blog-timing-debug-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

    console.log(`📄 Full report saved to: ${reportPath}`);
    
    // Show screenshot locations
    console.log('\n📸 Screenshots captured:');
    this.results.testRuns.forEach(test => {
      if (test.screenshots.length > 0) {
        console.log(`   Route: ${test.path}`);
        test.screenshots.forEach(screenshot => {
          console.log(`     ${screenshot.type}: ${screenshot.path}`);
        });
      }
    });

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

      // Test blog main page first
      await this.testBlogRoute('/blog', 'Blog index page', 15000);
      
      // Test individual blog posts
      await this.testMultipleBlogPosts();

      // Analyze results
      await this.analyzeResults();

      // Generate final report
      await this.generateReport();

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
  console.log('🔍 Blog Post Timing Issue Debugger');
  console.log('=====================================\n');

  // Check if dev server is running
  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  console.log(`✅ Dev server detected at ${DEV_SERVER_URL}\n`);

  const blogDebugger = new BlogTimingDebugger();
  await blogDebugger.run();

  console.log('\n🎉 Debug complete! Check the debug-output/ directory for screenshots and reports.');
  console.log('🔍 Look for blog-timing-debug-report.json for detailed analysis.');
}

// Run the debugger
main().catch(console.error);