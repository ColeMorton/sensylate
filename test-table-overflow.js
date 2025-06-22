const puppeteer = require('puppeteer');
const path = require('path');

async function testTableOverflow() {
  console.log('🚀 Testing table overflow on mobile...');

  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: { width: 375, height: 667 } // iPhone SE size
  });

  const page = await browser.newPage();

  // Set mobile viewport
  await page.setViewport({ width: 375, height: 667 });

  // Navigate to a page with tables (using the WELL analysis page from screenshot)
  const url = 'http://localhost:4321/blog/well-fundamental-analysis-20250620/';

  try {
    console.log(`📱 Navigating to: ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Take screenshot of current state
    const screenshotPath = path.join(__dirname, 'table-overflow-before.png');
    await page.screenshot({
      path: screenshotPath,
      fullPage: true
    });
    console.log(`📸 Screenshot saved: ${screenshotPath}`);

    // Check for horizontal scroll on the page
    const pageWidth = await page.evaluate(() => {
      return {
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        hasHorizontalScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth
      };
    });

    console.log('📊 Page width analysis:', pageWidth);

    // Find tables and analyze their overflow
    const tableInfo = await page.evaluate(() => {
      const tables = document.querySelectorAll('table');
      return Array.from(tables).map((table, index) => {
        const rect = table.getBoundingClientRect();
        const containerRect = table.closest('.content, .prose, main, body').getBoundingClientRect();
        return {
          index,
          width: rect.width,
          containerWidth: containerRect.width,
          overflows: rect.width > containerRect.width,
          className: table.className,
          parentClasses: table.parentElement?.className || ''
        };
      });
    });

    console.log('📋 Table analysis:', tableInfo);

    if (pageWidth.hasHorizontalScroll) {
      console.log('❌ ISSUE CONFIRMED: Page has horizontal scroll');
    } else {
      console.log('✅ No horizontal scroll detected');
    }

  } catch (error) {
    console.error('Error during test:', error);
  } finally {
    await browser.close();
  }
}

// Run the test
testTableOverflow().catch(console.error);
