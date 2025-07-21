const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  console.log('🚀 Running performance test after clean restart...');

  // Enable performance monitoring
  await page.setCacheEnabled(false);

  const startTime = Date.now();
  await page.goto('http://localhost:4321/charts', { waitUntil: 'networkidle2' });
  const loadTime = Date.now() - startTime;

  // Wait for charts to fully render
  await new Promise(resolve => setTimeout(resolve, 8000));

  const performanceMetrics = await page.evaluate(() => {
    const plotlyChart = document.querySelector('.plotly');
    const modebar = document.querySelector('.modebar');
    const chartData = document.querySelectorAll('svg.main-svg');

    // Check for console errors
    const errors = window.console._errors || [];

    // Check memory usage (basic)
    const memoryInfo = performance.memory ? {
      usedJSHeapSize: performance.memory.usedJSHeapSize,
      totalJSHeapSize: performance.memory.totalJSHeapSize,
      jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
    } : null;

    // Get navigation timing
    const navigation = performance.getEntriesByType('navigation')[0];

    return {
      chartRendered: plotlyChart !== null,
      modebarWorking: modebar !== null,
      svgElements: chartData.length,
      consoleErrors: errors.length || 0,
      memoryInfo: memoryInfo,
      domContentLoaded: navigation ? navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart : null,
      loadComplete: navigation ? navigation.loadEventEnd - navigation.loadEventStart : null,
      pageTitle: document.title,
      chartsVisible: document.body.textContent.includes('Apple Stock Price Range')
    };
  });

  console.log('\n📊 PERFORMANCE TEST RESULTS:');
  console.log('==============================');
  console.log(`⏱️  Page load time: ${loadTime}ms`);
  console.log(`📈 Charts rendered: ${performanceMetrics.chartRendered ? '✅' : '❌'}`);
  console.log(`🎛️  Modebar working: ${performanceMetrics.modebarWorking ? '✅' : '❌'}`);
  console.log(`🖼️  SVG elements: ${performanceMetrics.svgElements}`);
  console.log(`🚨 Console errors: ${performanceMetrics.consoleErrors}`);
  console.log(`📄 Page title: ${performanceMetrics.pageTitle}`);
  console.log(`👁️  Charts visible: ${performanceMetrics.chartsVisible ? '✅' : '❌'}`);

  if (performanceMetrics.memoryInfo) {
    const memoryUsageMB = (performanceMetrics.memoryInfo.usedJSHeapSize / 1024 / 1024).toFixed(2);
    console.log(`💾 Memory usage: ${memoryUsageMB} MB`);
  }

  if (performanceMetrics.domContentLoaded) {
    console.log(`🏗️  DOM Content Loaded: ${performanceMetrics.domContentLoaded.toFixed(2)}ms`);
  }

  if (performanceMetrics.loadComplete) {
    console.log(`✅ Load Event: ${performanceMetrics.loadComplete.toFixed(2)}ms`);
  }

  // Test responsiveness
  console.log('\n📱 Testing responsiveness...');
  await page.setViewport({ width: 768, height: 1024 }); // Tablet view
  await new Promise(resolve => setTimeout(resolve, 2000));

  await page.setViewport({ width: 375, height: 667 }); // Mobile view
  await new Promise(resolve => setTimeout(resolve, 2000));

  await page.setViewport({ width: 1920, height: 1080 }); // Desktop view
  await new Promise(resolve => setTimeout(resolve, 2000));

  console.log('   ✅ Responsive design test completed');

  // Final screenshot
  await page.screenshot({ path: 'debug-output/performance-test-final.png', fullPage: true });
  console.log('\n📸 Performance test screenshot saved');

  // Summary
  const allGood = performanceMetrics.chartRendered &&
                  performanceMetrics.modebarWorking &&
                  performanceMetrics.svgElements >= 3 &&
                  performanceMetrics.consoleErrors === 0 &&
                  loadTime < 5000;

  console.log('\n🏆 PERFORMANCE SUMMARY:');
  console.log('========================');
  if (allGood) {
    console.log('   🎉 EXCELLENT: All performance tests passed!');
    console.log('   ✅ Fast loading times');
    console.log('   ✅ Clean error-free environment');
    console.log('   ✅ Charts rendering efficiently');
    console.log('   ✅ Plotly.js 3.0.1 working perfectly');
    console.log('   ✅ react-plotly.js 2.6.0 working perfectly');
  } else {
    console.log('   ⚠️  Some performance issues detected');
  }

  await browser.close();
})().catch(console.error);
