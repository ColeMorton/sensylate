import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function captureOGImage() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Set viewport to OG image dimensions
    await page.setViewport({
      width: 1200,
      height: 630,
      deviceScaleFactor: 2 // Higher quality
    });

    // Navigate to the homepage
    await page.goto('http://localhost:4321', {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // Wait for content to fully load
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Take screenshot
    const outputPath = path.join(__dirname, '../public/images/og-image.png');
    await page.screenshot({
      path: outputPath,
      type: 'png',
      clip: {
        x: 0,
        y: 0,
        width: 1200,
        height: 630
      }
    });

    console.log(`OG image captured successfully at: ${outputPath}`);
  } catch (error) {
    console.error('Error capturing OG image:', error);
  } finally {
    await browser.close();
  }
}

captureOGImage();
