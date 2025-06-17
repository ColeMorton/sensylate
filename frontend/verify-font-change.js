import puppeteer from 'puppeteer';

async function verifyFontChange() {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  try {
    // Set viewport
    await page.setViewport({ width: 1200, height: 800 });

    // Navigate to local dev server
    console.log('Navigating to local development server...');
    await page.goto('http://localhost:4321', { waitUntil: 'networkidle2' });

    // Wait for page to load
    await page.waitForSelector('h1, h2, h3, h4, h5, h6', { timeout: 10000 });

    // Check if Paytone One font is loaded
    const fontFaceRules = await page.evaluate(() => {
      const styles = Array.from(document.styleSheets);
      const fontFaces = [];

      styles.forEach(sheet => {
        try {
          const rules = Array.from(sheet.cssRules || sheet.rules || []);
          rules.forEach(rule => {
            if (rule instanceof CSSFontFaceRule) {
              const family = rule.style.fontFamily;
              if (family && family.includes('Paytone')) {
                fontFaces.push({
                  family: family,
                  src: rule.style.src
                });
              }
            }
          });
        } catch (e) {
          // Skip cross-origin stylesheets
        }
      });

      return fontFaces;
    });

    console.log('Paytone One font faces found:', fontFaceRules.length);

    // Check computed styles on headings
    const headingFonts = await page.evaluate(() => {
      const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
      return headings.map(h => {
        const computed = window.getComputedStyle(h);
        return {
          tag: h.tagName,
          text: h.textContent.trim().substring(0, 50),
          fontFamily: computed.fontFamily
        };
      });
    });

    console.log('\nHeading font families:');
    headingFonts.forEach(h => {
      const hasPaytone = h.fontFamily.toLowerCase().includes('paytone');
      console.log(`${h.tag}: ${hasPaytone ? '✅' : '❌'} ${h.fontFamily}`);
      if (h.text) console.log(`   Text: "${h.text}..."`);
    });

    // Check CSS variables
    const cssVars = await page.evaluate(() => {
      const root = document.documentElement;
      const computed = window.getComputedStyle(root);
      return {
        fontPrimary: computed.getPropertyValue('--font-primary'),
        fontSecondary: computed.getPropertyValue('--font-secondary')
      };
    });

    console.log('\nCSS Variables:');
    console.log('--font-primary:', cssVars.fontPrimary);
    console.log('--font-secondary:', cssVars.fontSecondary);

    // Take screenshots
    console.log('\nTaking screenshots...');

    // Find a page with headings
    await page.goto('http://localhost:4321/blog', { waitUntil: 'networkidle2' });
    await page.waitForSelector('h1, h2', { timeout: 5000 });

    await page.screenshot({
      path: 'font-verification-blog.png',
      fullPage: true,
      type: 'png'
    });

    // Go to homepage
    await page.goto('http://localhost:4321', { waitUntil: 'networkidle2' });
    await page.screenshot({
      path: 'font-verification-home.png',
      fullPage: true,
      type: 'png'
    });

    // Verify results
    const paytoneFound = fontFaceRules.length > 0 ||
                        cssVars.fontSecondary.toLowerCase().includes('paytone') ||
                        headingFonts.some(h => h.fontFamily.toLowerCase().includes('paytone'));

    if (paytoneFound) {
      console.log('\n✅ Paytone One font successfully implemented!');
    } else {
      console.log('\n❌ Paytone One font not detected. Please check the configuration.');
    }

    console.log('\nScreenshots saved:');
    console.log('- font-verification-blog.png');
    console.log('- font-verification-home.png');

  } catch (error) {
    console.error('Error during font verification:', error);
  } finally {
    await browser.close();
  }
}

// Run the verification
verifyFontChange().catch(console.error);
