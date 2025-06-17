import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

async function verifyLogo() {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  try {
    // Set viewport for consistent screenshots
    await page.setViewport({ width: 1200, height: 800 });

    // Navigate to local dev server
    console.log('Navigating to local development server...');
    await page.goto('http://localhost:4321', { waitUntil: 'networkidle2' });

    // Wait for the logo to load
    await page.waitForSelector('.navbar-brand', { timeout: 10000 });

    // Take screenshot of the header area
    console.log('Taking screenshot of header with logo...');
    const headerElement = await page.$('header, .navbar, nav');
    if (headerElement) {
      await headerElement.screenshot({
        path: 'logo-verification-header.png',
        type: 'png'
      });
    }

    // Take full page screenshot
    console.log('Taking full page screenshot...');
    await page.screenshot({
      path: 'logo-verification-full.png',
      fullPage: true,
      type: 'png'
    });

    // Check if logo text is present
    const logoText = await page.evaluate(() => {
      const logoElement = document.querySelector('.navbar-brand');
      return logoElement ? logoElement.textContent.trim() : null;
    });

    console.log('Logo text found:', logoText);

    // Test both light and dark themes if theme switcher is enabled
    const themeSwitcher = await page.$('[class*="theme"]');
    if (themeSwitcher) {
      console.log('Testing dark theme...');
      await themeSwitcher.click();
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for theme transition

      await page.screenshot({
        path: 'logo-verification-dark.png',
        fullPage: true,
        type: 'png'
      });
    }

    // Verify logo consistency across different page sizes
    console.log('Testing mobile view...');
    await page.setViewport({ width: 375, height: 667 });
    await new Promise(resolve => setTimeout(resolve, 500));

    await page.screenshot({
      path: 'logo-verification-mobile.png',
      fullPage: true,
      type: 'png'
    });

    console.log('✅ Logo verification complete!');
    console.log('Screenshots saved:');
    console.log('- logo-verification-header.png (header area)');
    console.log('- logo-verification-full.png (full page desktop)');
    console.log('- logo-verification-dark.png (dark theme)');
    console.log('- logo-verification-mobile.png (mobile view)');

    if (logoText === 'Cole Morton') {
      console.log('✅ Logo text correctly displays: "Cole Morton"');
    } else {
      console.log('❌ Logo text mismatch. Expected: "Cole Morton", Found:', logoText);
    }

  } catch (error) {
    console.error('Error during logo verification:', error);
  } finally {
    await browser.close();
  }
}

// Run the verification
verifyLogo().catch(console.error);
