const puppeteer = require('puppeteer');

async function testPhotoBooth() {
  console.log('🚀 Testing PhotoBooth component loading...');

  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('📍 Navigating to PhotoBooth page...');
    await page.goto('http://localhost:4321/photo-booth', {
      waitUntil: 'networkidle0',
      timeout: 10000
    });

    console.log('📋 Checking page content...');
    const pageInfo = await page.evaluate(() => {
      return {
        title: document.title,
        url: window.location.href,
        bodyText: document.body ? document.body.textContent?.substring(0, 200) : 'No body',
        hasPhotoBoothContainer: !!document.querySelector('.photo-booth-container'),
        hasLoadingText: document.body && document.body.textContent && document.body.textContent.includes('Loading dashboards...'),
        hasDashboard: !!document.querySelector('.photo-booth-dashboard'),
        hasControls: !!document.querySelector('.photo-booth-controls'),
        allDivs: Array.from(document.querySelectorAll('div')).map(el => el.className).filter(c => c).slice(0, 10),
      };
    });

    console.log('✅ Page info:', JSON.stringify(pageInfo, null, 2));

    if (pageInfo.hasPhotoBoothContainer) {
      console.log('🎉 SUCCESS: PhotoBooth container found!');
    } else {
      console.log('❌ FAIL: PhotoBooth container not found');
    }

    // Wait a bit for any async loading
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Take a screenshot
    await page.screenshot({ path: 'photobooth-test.png', fullPage: true });
    console.log('📸 Screenshot saved as photobooth-test.png');

  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await browser.close();
  }
}

testPhotoBooth().catch(console.error);
