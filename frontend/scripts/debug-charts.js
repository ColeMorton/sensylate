/**
 * Puppeteer Debug Script for Charts Page
 *
 * Systematically debugs the /charts route issue by:
 * 1. Testing route accessibility
 * 2. Analyzing HTTP responses
 * 3. Checking content rendering
 * 4. Comparing with working routes
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

class ChartsDebugger {
  constructor() {
    this.browser = null;
    this.page = null;
    this.results = {
      timestamp: new Date().toISOString(),
      routes: {},
      errors: [],
      network: [],
      console: []
    };
  }

  async init() {
    console.log('🚀 Starting Charts Page Debug...\n');

    this.browser = await puppeteer.launch({
      headless: false, // Show browser for debugging
      slowMo: 100,
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

    // Listen for console logs
    this.page.on('console', (msg) => {
      this.results.console.push({
        type: msg.type(),
        text: msg.text(),
        timestamp: Date.now()
      });
    });

    // Listen for page errors
    this.page.on('pageerror', (error) => {
      this.results.errors.push({
        type: 'pageerror',
        message: error.message,
        stack: error.stack,
        timestamp: Date.now()
      });
    });
  }

  async testRoute(routePath, description) {
    console.log(`📍 Testing: ${routePath} (${description})`);

    const routeResult = {
      path: routePath,
      description,
      timestamp: Date.now(),
      accessible: false,
      statusCode: null,
      title: null,
      content: null,
      screenshot: null,
      loadTime: null,
      errors: []
    };

    try {
      const startTime = Date.now();

      // Navigate to the route
      const response = await this.page.goto(`${DEV_SERVER_URL}${routePath}`, {
        waitUntil: 'networkidle2',
        timeout: 10000
      });

      routeResult.loadTime = Date.now() - startTime;
      routeResult.statusCode = response.status();
      routeResult.accessible = response.status() === 200;

      if (routeResult.accessible) {
        // Get page title
        routeResult.title = await this.page.title();

        // Get main content
        const contentElement = await this.page.$('main, body, .content');
        if (contentElement) {
          routeResult.content = await this.page.evaluate(el => el.textContent?.slice(0, 500), contentElement);
        }

        // Take screenshot
        const screenshotPath = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}.png`);
        await this.page.screenshot({
          path: screenshotPath,
          fullPage: true
        });
        routeResult.screenshot = screenshotPath;

        console.log(`   ✅ Status: ${routeResult.statusCode} | Load Time: ${routeResult.loadTime}ms`);
        if (routeResult.title) {
          console.log(`   📄 Title: "${routeResult.title}"`);
        }
      } else {
        console.log(`   ❌ Status: ${routeResult.statusCode} | Load Time: ${routeResult.loadTime}ms`);

        // Take screenshot of error page
        const screenshotPath = path.join(DEBUG_OUTPUT_DIR, `${routePath.replace(/\//g, '_')}_error.png`);
        await this.page.screenshot({
          path: screenshotPath,
          fullPage: true
        });
        routeResult.screenshot = screenshotPath;
      }

    } catch (error) {
      console.log(`   💥 Error: ${error.message}`);
      routeResult.errors.push({
        message: error.message,
        stack: error.stack
      });
    }

    this.results.routes[routePath] = routeResult;
    console.log(''); // Empty line for readability

    return routeResult;
  }

  async debugContentCollection() {
    console.log('🔍 Debugging Content Collection...\n');

    try {
      // Navigate to a working page first
      await this.page.goto(`${DEV_SERVER_URL}/about`, { waitUntil: 'networkidle2' });

      // Check if we can access Astro dev tools or debug info
      const astroDebugInfo = await this.page.evaluate(() => {
        // Look for any Astro-specific debugging information
        return {
          hasAstroDevTools: !!window.__astro,
          userAgent: navigator.userAgent,
          currentUrl: location.href,
          hasViteClient: !!window.__vite_is_modern_browser
        };
      });

      console.log('🔧 Astro Debug Info:', astroDebugInfo);

    } catch (error) {
      console.log('❌ Content Collection Debug Error:', error.message);
    }
  }

  async analyzeNetworkTraffic() {
    console.log('🌐 Analyzing Network Traffic...\n');

    const requests = this.results.network.filter(n => n.type === 'request');
    const responses = this.results.network.filter(n => n.type === 'response');

    console.log(`📊 Total Requests: ${requests.length}`);
    console.log(`📊 Total Responses: ${responses.length}`);

    // Find failed requests
    const failedResponses = responses.filter(r => r.status >= 400);
    if (failedResponses.length > 0) {
      console.log(`❌ Failed Requests (${failedResponses.length}):`);
      failedResponses.forEach(r => {
        console.log(`   ${r.status} - ${r.url}`);
      });
    }

    // Check for specific routes
    const chartsRequests = requests.filter(r => r.url.includes('/charts'));
    if (chartsRequests.length > 0) {
      console.log(`📍 Charts Route Requests (${chartsRequests.length}):`);
      chartsRequests.forEach(r => {
        console.log(`   ${r.method} ${r.url}`);
      });
    }
  }

  async generateReport() {
    console.log('📝 Generating Debug Report...\n');

    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'debug-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));

    console.log(`📄 Full report saved to: ${reportPath}`);

    // Generate summary
    const summary = {
      totalRoutesTested: Object.keys(this.results.routes).length,
      accessibleRoutes: Object.values(this.results.routes).filter(r => r.accessible).length,
      failedRoutes: Object.values(this.results.routes).filter(r => !r.accessible).length,
      totalErrors: this.results.errors.length,
      totalNetworkRequests: this.results.network.filter(n => n.type === 'request').length
    };

    console.log('📊 Debug Summary:');
    console.log(`   ✅ Accessible Routes: ${summary.accessibleRoutes}/${summary.totalRoutesTested}`);
    console.log(`   ❌ Failed Routes: ${summary.failedRoutes}/${summary.totalRoutesTested}`);
    console.log(`   💥 Page Errors: ${summary.totalErrors}`);
    console.log(`   🌐 Network Requests: ${summary.totalNetworkRequests}`);

    return summary;
  }

  async cleanup() {
    if (this.browser) {
      await this.browser.close();
    }
  }

  async run() {
    try {
      await this.init();

      // Test various routes to compare behavior
      await this.testRoute('/', 'Homepage');
      await this.testRoute('/about', 'Working static page');
      await this.testRoute('/blog', 'Working collection page');
      await this.testRoute('/charts', 'Target charts page (problematic)');
      await this.testRoute('/elements', 'Elements page via [regular].astro');
      await this.testRoute('/nonexistent', 'Non-existent page (should 404)');

      // Additional debugging
      await this.debugContentCollection();
      await this.analyzeNetworkTraffic();

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
  console.log('🔍 Charts Page Puppeteer Debugger');
  console.log('=====================================\n');

  // Check if dev server is running
  const serverRunning = await checkDevServer();
  if (!serverRunning) {
    console.error(`❌ Dev server not running at ${DEV_SERVER_URL}`);
    console.log('   Please start the dev server with: yarn dev');
    process.exit(1);
  }

  console.log(`✅ Dev server detected at ${DEV_SERVER_URL}\n`);

  const chartsDebugger = new ChartsDebugger();
  await chartsDebugger.run();

  console.log('\n🎉 Debug complete! Check the debug-output/ directory for screenshots and reports.');
}

// Run the debugger
main().catch(console.error);
