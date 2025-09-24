#!/usr/bin/env node
/**
 * Extract complete computed CSS styles for brand typography
 *
 * This script uses puppeteer to navigate to the PhotoBooth logo generation
 * dashboard and extract all computed CSS properties for both "Cole Morton"
 * and "colemorton.com" brand implementations.
 */

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

const PHOTOBOOTH_URL = 'http://localhost:4321/photo-booth?dashboard=logo_generation';
const OUTPUT_FILE = path.join(__dirname, '..', 'brand_styles_extracted.json');

async function extractBrandStyles() {
  console.log('🚀 Starting brand style extraction...');

  const browser = await puppeteer.launch({
    headless: false, // Keep visible for debugging
    defaultViewport: { width: 1920, height: 1080 }
  });

  try {
    const page = await browser.newPage();

    // Set up console logging from the page
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));

    const styles = {
      personal: null,
      attribution: null,
      metadata: {
        timestamp: new Date().toISOString(),
        viewport: { width: 1920, height: 1080 },
        url_base: PHOTOBOOTH_URL
      }
    };

    console.log('📊 Extracting Personal Brand styles ("Cole Morton")...');

    // Extract Personal Brand styles
    console.log(`🔍 Navigating to: ${PHOTOBOOTH_URL}&brand=personal&mode=light`);
    await page.goto(`${PHOTOBOOTH_URL}&brand=personal&mode=light`);

    // Wait for page to be interactive
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Debug: Check what's on the page
    const bodyContent = await page.evaluate(() => document.body.innerHTML);
    console.log('📄 Page loaded, checking for elements...');

    // Try different selectors
    const selectors = ['.brand-text', 'h1', '.logo-generation-container h1', '[class*="brand"]'];
    let foundElement = false;
    let actualSelector = null;

    for (const selector of selectors) {
      try {
        await page.waitForSelector(selector, { timeout: 2000 });
        actualSelector = selector;
        foundElement = true;
        console.log(`✅ Found element with selector: ${selector}`);
        break;
      } catch (e) {
        console.log(`❌ Selector ${selector} not found`);
      }
    }

    if (!foundElement) {
      console.log('🔍 Debugging page content...');

      // Check all elements on the page
      const pageInfo = await page.evaluate(() => {
        const allElements = Array.from(document.querySelectorAll('*'));
        const h1s = Array.from(document.querySelectorAll('h1'));
        const brandElements = Array.from(document.querySelectorAll('[class*="brand"]'));
        const logoContainers = Array.from(document.querySelectorAll('[class*="logo"]'));

        return {
          totalElements: allElements.length,
          h1Count: h1s.length,
          h1Elements: h1s.map(h1 => ({
            text: h1.innerText,
            classes: Array.from(h1.classList),
            html: h1.outerHTML.substring(0, 200)
          })),
          brandElements: brandElements.map(el => ({
            tagName: el.tagName,
            text: el.innerText?.substring(0, 50),
            classes: Array.from(el.classList)
          })),
          logoElements: logoContainers.map(el => ({
            tagName: el.tagName,
            text: el.innerText?.substring(0, 50),
            classes: Array.from(el.classList)
          })),
          bodyPreview: document.body.innerHTML.substring(0, 500),
          url: window.location.href
        };
      });

      console.log('Page Debug Info:', pageInfo);

      // Try waiting longer and checking again
      console.log('⏳ Waiting additional 5 seconds for React to render...');
      await new Promise(resolve => setTimeout(resolve, 5000));

      // Try again after longer wait
      const retryElements = await page.evaluate(() => {
        const h1s = Array.from(document.querySelectorAll('h1'));
        const allText = Array.from(document.querySelectorAll('*')).filter(el =>
          el.innerText && (el.innerText.includes('Cole Morton') || el.innerText.includes('colemorton.com'))
        );

        return {
          h1Elements: h1s.map(h1 => ({
            text: h1.innerText,
            classes: Array.from(h1.classList)
          })),
          textElements: allText.map(el => ({
            tagName: el.tagName,
            text: el.innerText,
            classes: Array.from(el.classList)
          }))
        };
      });

      console.log('Retry Results:', retryElements);

      if (retryElements.textElements.length > 0) {
        console.log('✅ Found brand text elements after longer wait!');
        actualSelector = retryElements.textElements[0].tagName.toLowerCase();
        foundElement = true;
      } else {
        throw new Error('No brand text element found after extended wait');
      }
    }

    // Wait for font to load
    await page.waitForFunction(() => {
      return document.fonts.ready;
    });

    styles.personal = await extractElementStyles(page, actualSelector || '.brand-text');

    console.log('🔗 Extracting Attribution Brand styles ("colemorton.com")...');

    // Extract Attribution Brand styles
    console.log(`🔍 Navigating to: ${PHOTOBOOTH_URL}&brand=attribution&mode=light`);
    await page.goto(`${PHOTOBOOTH_URL}&brand=attribution&mode=light`);

    // Wait for page to be interactive
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Use the same selector we found for personal brand
    await page.waitForSelector(actualSelector || '.brand-text', { timeout: 10000 });

    // Wait for font to load
    await page.waitForFunction(() => {
      return document.fonts.ready;
    });

    styles.attribution = await extractElementStyles(page, actualSelector || '.brand-text');

    // Save extracted styles
    await fs.writeFile(OUTPUT_FILE, JSON.stringify(styles, null, 2));
    console.log(`✅ Brand styles extracted and saved to: ${OUTPUT_FILE}`);

    // Generate CSS output
    const cssOutput = generateCompleteCSS(styles);
    const cssFile = path.join(__dirname, '..', 'brand_styles_complete.css');
    await fs.writeFile(cssFile, cssOutput);
    console.log(`📝 Complete CSS generated: ${cssFile}`);

    return styles;

  } catch (error) {
    console.error('❌ Error extracting brand styles:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

async function extractElementStyles(page, selector) {
  return await page.evaluate((sel) => {
    const element = document.querySelector(sel);
    if (!element) {
      throw new Error(`Element not found: ${sel}`);
    }

    const computedStyle = window.getComputedStyle(element);
    const styles = {};

    // Extract all computed style properties
    for (let i = 0; i < computedStyle.length; i++) {
      const prop = computedStyle[i];
      styles[prop] = computedStyle.getPropertyValue(prop);
    }

    // Add element-specific metadata
    const rect = element.getBoundingClientRect();
    const elementData = {
      computed_styles: styles,
      bounding_rect: {
        width: rect.width,
        height: rect.height,
        top: rect.top,
        left: rect.left
      },
      inner_text: element.innerText,
      tag_name: element.tagName.toLowerCase(),
      class_list: Array.from(element.classList),
      font_loading_status: document.fonts.check('400 48px "Paytone One"') ? 'loaded' : 'not-loaded'
    };

    return elementData;
  }, selector);
}

function generateCompleteCSS(styles) {
  let css = `/*
 * Complete Brand Typography CSS
 * Generated: ${styles.metadata.timestamp}
 *
 * This CSS contains ALL computed properties needed to recreate
 * both "Cole Morton" and "colemorton.com" brand typography
 * with pixel-perfect accuracy.
 */

`;

  // Personal Brand CSS
  css += `/* ===== PERSONAL BRAND: "Cole Morton" ===== */\n`;
  css += `.personal-brand-complete {\n`;
  css += generateCSSProperties(styles.personal.computed_styles, 'personal');
  css += `}\n\n`;

  // Attribution Brand CSS
  css += `/* ===== ATTRIBUTION BRAND: "colemorton.com" ===== */\n`;
  css += `.attribution-brand-complete {\n`;
  css += generateCSSProperties(styles.attribution.computed_styles, 'attribution');
  css += `}\n\n`;

  // Add usage examples
  css += generateUsageExamples(styles);

  return css;
}

function generateCSSProperties(computedStyles, brandType) {
  const important_properties = [
    'font-family',
    'font-size',
    'font-weight',
    'font-style',
    'line-height',
    'letter-spacing',
    'word-spacing',
    'color',
    'display',
    'align-items',
    'justify-content',
    'transform',
    'margin',
    'margin-top',
    'margin-right',
    'margin-bottom',
    'margin-left',
    'padding',
    'padding-top',
    'padding-right',
    'padding-bottom',
    'padding-left',
    'text-align',
    'vertical-align',
    'text-decoration',
    'text-transform',
    'text-shadow',
    'opacity',
    'z-index',
    'position',
    'box-sizing',
    'width',
    'height',
    'max-width',
    'max-height',
    'min-width',
    'min-height'
  ];

  let css = '';

  // Add critical properties first
  important_properties.forEach(prop => {
    if (computedStyles[prop] && computedStyles[prop] !== 'auto' && computedStyles[prop] !== 'normal') {
      css += `  ${prop}: ${computedStyles[prop]};\n`;
    }
  });

  // Add comment about computed values
  css += `  \n  /* Additional computed properties available in extracted JSON */\n`;

  return css;
}

function generateUsageExamples(styles) {
  return `/* ===== USAGE EXAMPLES ===== */

/* Personal Brand Implementation */
.personal-brand-nav {
  /* Use for navigation header */
  composes: personal-brand-complete;
}

.personal-brand-logo {
  /* Use for logo displays */
  composes: personal-brand-complete;
}

/* Attribution Brand Implementation */
.attribution-brand-footer {
  /* Use for chart export footers */
  composes: attribution-brand-complete;
}

/* ===== RESPONSIVE VARIATIONS ===== */
@media (max-width: 768px) {
  .personal-brand-complete {
    font-size: 2rem; /* Adjust for mobile */
  }

  .attribution-brand-complete {
    font-size: 1.5rem; /* Adjust for mobile */
  }
}

/* ===== DARK MODE VARIATIONS ===== */
.dark .personal-brand-complete,
.dark .attribution-brand-complete {
  color: #e0e0e0; /* Dark mode text color */
}

/* ===== VALIDATION TEST CLASS ===== */
.brand-test-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
  background: #f5f5f5;
}

.brand-test-item {
  padding: 1rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}
`;
}

// Run extraction if called directly
if (require.main === module) {
  extractBrandStyles()
    .then(() => {
      console.log('✅ Brand style extraction completed successfully');
      process.exit(0);
    })
    .catch((error) => {
      console.error('❌ Brand style extraction failed:', error);
      process.exit(1);
    });
}

module.exports = { extractBrandStyles };
