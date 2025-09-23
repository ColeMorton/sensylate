const puppeteer = require('puppeteer');

(async () => {
  console.log('🔧 Testing light theme implementation...');

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Navigate to the photo booth with light mode
    const url = 'http://localhost:4321/photo-booth?dashboard=logo_generation&mode=light&brand=personal&aspect_ratio=16:9';
    console.log(`🌐 Navigating to: ${url}`);

    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for the dashboard to be ready
    await page.waitForSelector('.photo-booth-ready', { timeout: 15000 });

    // Give additional time for theme to apply
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Get theme state
    const themeState = await page.evaluate(() => {
      const html = document.documentElement;
      const logoElement = document.querySelector('.brand-text');

      if (!logoElement) {
        return { error: 'Logo element not found' };
      }

      const logoStyles = window.getComputedStyle(logoElement);
      const rootStyles = window.getComputedStyle(html);

      return {
        hasDarkClass: html.classList.contains('dark'),
        logoTextColor: logoStyles.color,
        textColorVar: rootStyles.getPropertyValue('--color-text-dark').trim(),
        darkTextColorVar: rootStyles.getPropertyValue('--color-darkmode-text-dark').trim(),
        brandText: logoElement.textContent?.trim(),
      };
    });

    console.log('🎨 Theme state:', JSON.stringify(themeState, null, 2));

    // Check if light theme is working correctly
    if (themeState.error) {
      console.error('❌ Error:', themeState.error);
    } else if (themeState.hasDarkClass) {
      console.error('❌ Light theme test FAILED: Dark class is present');
      console.error(`   Expected: hasDarkClass = false`);
      console.error(`   Actual: hasDarkClass = ${themeState.hasDarkClass}`);
    } else if (themeState.logoTextColor === 'rgb(249, 250, 251)') {
      console.error('❌ Light theme test FAILED: Text color is still white (dark theme color)');
      console.error(`   Expected: rgb(26, 26, 26) (black)`);
      console.error(`   Actual: ${themeState.logoTextColor} (white)`);
    } else if (themeState.logoTextColor === 'rgb(26, 26, 26)') {
      console.log('✅ Light theme test PASSED: Text color is black as expected');
      console.log(`   hasDarkClass: ${themeState.hasDarkClass}`);
      console.log(`   logoTextColor: ${themeState.logoTextColor}`);
      console.log(`   brandText: ${themeState.brandText}`);
    } else {
      console.warn('⚠️  Light theme test UNKNOWN: Unexpected text color');
      console.warn(`   logoTextColor: ${themeState.logoTextColor}`);
      console.warn(`   Expected: rgb(26, 26, 26) (black)`);
    }

  } catch (error) {
    console.error('❌ Test failed with error:', error.message);
  } finally {
    await browser.close();
  }
})();
