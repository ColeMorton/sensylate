/**
 * Final Validation Script
 *
 * Comprehensive test to validate that the blog post timing issue has been resolved
 * with charts enabled and all functionality working properly.
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const DEBUG_OUTPUT_DIR = path.join(process.cwd(), 'debug-output');
const DEV_SERVER_URL = 'http://localhost:4321';

if (!fs.existsSync(DEBUG_OUTPUT_DIR)) {
  fs.mkdirSync(DEBUG_OUTPUT_DIR, { recursive: true });
}

class FinalValidator {
  constructor() {
    this.browser = null;
    this.results = {
      timestamp: new Date().toISOString(),
      summary: {
        totalTests: 0,
        passedTests: 0,
        failedTests: 0
      },
      tests: []
    };
  }

  async init() {
    console.log('🎯 Final Validation - Complete Fix Test\n');

    this.browser = await puppeteer.launch({
      headless: false,
      slowMo: 100,
      devtools: false
    });
  }

  async testRoute(route, description, expectedStatus = 200) {
    console.log(`📍 Testing: ${route} (${description})`);

    const page = await this.browser.newPage();
    const test = {
      route,
      description,
      expectedStatus,
      actualStatus: null,
      success: false,
      loadTime: null,
      hasContent: false,
      error: null,
      timestamp: Date.now()
    };

    try {
      const startTime = Date.now();
      const response = await page.goto(`${DEV_SERVER_URL}${route}`, {
        waitUntil: 'networkidle2',
        timeout: 15000
      });

      test.actualStatus = response.status();
      test.loadTime = Date.now() - startTime;
      test.success = test.actualStatus === expectedStatus;

      if (test.success) {
        // Check for content
        const hasTitle = await page.$('h1, h2, .h2, title');
        const hasContent = await page.$('.content, article, main, .chart-container');
        test.hasContent = !!(hasTitle && hasContent);

        console.log(`   ✅ ${test.actualStatus} (${test.loadTime}ms) - Content: ${test.hasContent}`);
      } else {
        console.log(`   ❌ ${test.actualStatus} (expected ${expectedStatus}) (${test.loadTime}ms)`);
      }

    } catch (error) {
      test.error = error.message;
      test.success = false;
      console.log(`   💥 Error: ${error.message}`);
    } finally {
      await page.close();
    }

    this.results.tests.push(test);
    this.results.summary.totalTests++;
    if (test.success) {
      this.results.summary.passedTests++;
    } else {
      this.results.summary.failedTests++;
    }

    return test;
  }

  async testConcurrentBlogAccess() {
    console.log('🔄 Testing Concurrent Blog Access (Stress Test)...');

    const blogRoutes = [
      '/blog/post-1',
      '/blog/adbe-fundamental-analysis-20250723',
      '/blog/amzn-fundamental-analysis-20250618',
      '/blog/post-1', // Duplicate to test caching
      '/blog/adbe-fundamental-analysis-20250723' // Duplicate
    ];

    const pages = [];
    const promises = [];

    try {
      // Create multiple pages
      for (let i = 0; i < blogRoutes.length; i++) {
        pages.push(await this.browser.newPage());
      }

      const startTime = Date.now();

      // Launch concurrent requests
      promises.push(...pages.map((page, index) =>
        page.goto(`${DEV_SERVER_URL}${blogRoutes[index]}`, {
          waitUntil: 'networkidle2',
          timeout: 20000
        }).then(response => ({
          index: index + 1,
          route: blogRoutes[index],
          status: response.status(),
          success: response.status() === 200
        })).catch(error => ({
          index: index + 1,
          route: blogRoutes[index],
          error: error.message,
          success: false
        }))
      ));

      const results = await Promise.all(promises);
      const totalTime = Date.now() - startTime;

      console.log(`   📊 Concurrent Test Results (${totalTime}ms total):`);
      results.forEach(result => {
        if (result.success) {
          console.log(`   ✅ ${result.index}. ${result.route}: ${result.status}`);
        } else {
          console.log(`   ❌ ${result.index}. ${result.route}: ${result.error || 'Failed'}`);
        }
      });

      const successCount = results.filter(r => r.success).length;
      console.log(`   📈 Success Rate: ${successCount}/${results.length} (${((successCount/results.length)*100).toFixed(1)}%)`);

      return {
        totalTests: results.length,
        successCount,
        totalTime,
        results
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

  generateReport() {
    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'final-validation-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

    console.log('\n📊 FINAL VALIDATION SUMMARY:');
    console.log(`   Total Tests: ${this.results.summary.totalTests}`);
    console.log(`   Passed: ${this.results.summary.passedTests}`);
    console.log(`   Failed: ${this.results.summary.failedTests}`);
    console.log(`   Success Rate: ${((this.results.summary.passedTests / this.results.summary.totalTests) * 100).toFixed(1)}%`);

    const avgLoadTime = this.results.tests
      .filter(t => t.loadTime)
      .reduce((sum, t) => sum + t.loadTime, 0) / this.results.tests.filter(t => t.loadTime).length;

    console.log(`   Average Load Time: ${avgLoadTime.toFixed(0)}ms`);

    console.log(`\n📄 Full report: ${reportPath}`);

    if (this.results.summary.failedTests === 0) {
      console.log('\n🎉 ALL TESTS PASSED - Blog timing issue has been RESOLVED!');
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

      // Test core functionality
      await this.testRoute('/', 'Homepage');
      await this.testRoute('/blog', 'Blog index page');
      await this.testRoute('/charts', 'Charts page (with ChartDisplay components)');

      // Test individual blog posts that were previously failing
      await this.testRoute('/blog/post-1', 'Blog post 1');
      await this.testRoute('/blog/adbe-fundamental-analysis-20250723', 'Recent analysis post');
      await this.testRoute('/blog/amzn-fundamental-analysis-20250618', 'Historical analysis post');

      // Test other routes for regression
      await this.testRoute('/about', 'About page');
      await this.testRoute('/contact', 'Contact page');

      // Stress test concurrent blog access
      const concurrentResults = await this.testConcurrentBlogAccess();

      // Add concurrent test to summary
      this.results.concurrentTest = concurrentResults;

      // Generate final report
      this.generateReport();

    } catch (error) {
      console.error('💥 Validation failed:', error);
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
  console.log('🎯 Final Validation Test');
  console.log('='.repeat(50));

  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  console.log(`✅ Dev server detected at ${DEV_SERVER_URL}\n`);

  const validator = new FinalValidator();
  await validator.run();

  console.log('\n🎯 Final validation complete!');
}

main().catch(console.error);
