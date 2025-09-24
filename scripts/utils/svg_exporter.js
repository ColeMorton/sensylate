#!/usr/bin/env node

/**
 * SVG Export Utility for Photo Booth
 *
 * This module provides vector-based image export using SVG format for:
 * - Infinite scalability without quality loss
 * - Small file sizes with embedded chart data
 * - Professional vector graphics for presentations
 * - Text remains selectable and searchable
 */

let puppeteer;
try {
  // Try to require from frontend node_modules first
  const path = require('path');
  const frontendPath = path.join(__dirname, '../../frontend/node_modules/puppeteer');
  puppeteer = require(frontendPath);
} catch (error) {
  try {
    // Fallback to standard require
    puppeteer = require('puppeteer');
  } catch (fallbackError) {
    console.error('❌ Puppeteer not found. Please install puppeteer in the frontend directory:');
    console.error('   cd frontend && npm install puppeteer');
    process.exit(1);
  }
}
const fs = require('fs').promises;
const path = require('path');

class SVGExporter {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.timeout = options.timeout || 30000;
    this.waitForSelector = options.waitForSelector || '.photo-booth-ready';
  }

  /**
   * Export dashboard as SVG
   * @param {string} url - URL to capture
   * @param {string} outputPath - Path for output SVG file
   * @param {Object} options - Export options
   * @returns {Promise<Object>} Export result with metadata
   */
  async exportSVG(url, outputPath, options = {}) {
    const {
      width = 1920,
      height = 1080,
      backgroundColor = '#ffffff',
      includeCSS = true,
      optimizeText = true
    } = options;

    let browser;
    try {
      if (this.verbose) {
        console.log(`📊 Exporting SVG from: ${url}`);
        console.log(`   Dimensions: ${width}x${height}`);
        console.log(`   Output: ${path.basename(outputPath)}`);
      }

      browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
      });

      const page = await browser.newPage();

      // Set viewport
      await page.setViewport({ width, height, deviceScaleFactor: 1 });

      // Navigate to page
      await page.goto(url, { waitUntil: 'networkidle0', timeout: this.timeout });

      // Wait for dashboard to be ready
      await page.waitForSelector(this.waitForSelector, { timeout: this.timeout });

      // Additional wait for charts to render
      await new Promise(resolve => setTimeout(resolve, 3000));

      // Hide UI elements for clean export
      await this._hideUIElements(page);

      // Extract SVG data from charts
      const svgData = await this._extractChartSVGs(page);

      // Extract text elements (for logos and other non-chart content)
      const textData = await this._extractTextElements(page);

      // Get dashboard layout and styling
      const layoutData = await this._extractLayoutData(page, { width, height });

      // Compose final SVG
      const finalSVG = await this._composeSVG(svgData, textData, layoutData, {
        width,
        height,
        backgroundColor,
        includeCSS,
        optimizeText
      });

      // Write SVG file
      await fs.writeFile(outputPath, finalSVG, 'utf8');

      // Get file stats
      const stats = await fs.stat(outputPath);

      const result = {
        success: true,
        outputPath,
        dimensions: { width, height },
        fileSize: stats.size,
        fileSizeKB: (stats.size / 1024).toFixed(2),
        chartCount: svgData.charts.length,
        textElementCount: textData.textElements.length,
        hasBrandText: textData.hasBrandText,
        hasEmbeddedCSS: includeCSS,
        exportTime: Date.now()
      };

      if (this.verbose) {
        console.log(`✅ SVG exported: ${width}x${height}`);
        console.log(`   File size: ${result.fileSizeKB} KB`);
        console.log(`   Charts included: ${result.chartCount}`);
        console.log(`   Text elements: ${result.textElementCount}`);
        if (result.hasBrandText) {
          console.log(`   ✓ Brand text detected and included`);
        }
      }

      return result;

    } catch (error) {
      const result = {
        success: false,
        error: error.message,
        url,
        outputPath
      };

      if (this.verbose) {
        console.error(`❌ SVG export failed: ${error.message}`);
      }

      throw error;

    } finally {
      if (browser) {
        await browser.close();
      }
    }
  }

  /**
   * Hide UI elements for clean export
   * @private
   */
  async _hideUIElements(page) {
    await page.evaluate(() => {
      // Hide photo booth controls
      const controls = document.querySelectorAll('.photo-booth-controls');
      controls.forEach(element => {
        element.style.display = 'none';
        element.style.visibility = 'hidden';
      });

      // Hide Astro dev toolbar
      const devToolbarSelectors = [
        'astro-dev-toolbar',
        '#dev-toolbar-root',
        '[data-astro-dev-toolbar]',
        '.astro-dev-toolbar',
        '#astro-dev-toolbar'
      ];

      devToolbarSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
          element.style.display = 'none';
          element.style.visibility = 'hidden';
        });
      });

      // Hide any loading spinners or placeholder content
      const hideSelectors = ['.loading', '.spinner', '.placeholder'];
      hideSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
          element.style.display = 'none';
        });
      });
    });
  }

  /**
   * Extract SVG data from Plotly.js charts
   * @private
   */
  async _extractChartSVGs(page) {
    return await page.evaluate(() => {
      const charts = [];
      const plotlyDivs = document.querySelectorAll('.js-plotly-plot');

      plotlyDivs.forEach((plotDiv, index) => {
        try {
          if (plotDiv._fullLayout && plotDiv._fullData) {
            // Get chart position and dimensions
            const rect = plotDiv.getBoundingClientRect();

            // Extract Plotly chart as SVG
            const gd = plotDiv;

            // Create a temporary div for SVG generation
            const tempDiv = document.createElement('div');
            tempDiv.style.position = 'absolute';
            tempDiv.style.left = '-9999px';
            tempDiv.style.width = rect.width + 'px';
            tempDiv.style.height = rect.height + 'px';
            document.body.appendChild(tempDiv);

            // Try to get SVG from Plotly
            let svgString = '';
            if (window.Plotly && window.Plotly.toImage) {
              // This is async, but we'll handle it differently
              svgString = `<!-- Plotly chart ${index} - ${rect.width}x${rect.height} -->`;
            }

            // Fallback: extract the SVG element directly if it exists
            const svgElement = plotDiv.querySelector('svg.main-svg');
            if (svgElement) {
              svgString = svgElement.outerHTML;
            }

            document.body.removeChild(tempDiv);

            charts.push({
              id: `chart-${index}`,
              position: { x: rect.left, y: rect.top },
              dimensions: { width: rect.width, height: rect.height },
              svg: svgString,
              title: plotDiv.getAttribute('data-title') || `Chart ${index + 1}`
            });
          }
        } catch (error) {
          console.warn(`Failed to extract SVG from chart ${index}:`, error);
        }
      });

      return { charts, totalCharts: plotlyDivs.length };
    });
  }

  /**
   * Extract text elements from dashboard (especially for logos)
   * @private
   */
  async _extractTextElements(page) {
    return await page.evaluate(() => {
      const textElements = [];

      // Look for brand text elements (logos)
      const brandElements = document.querySelectorAll('.brand-text');
      brandElements.forEach((element, index) => {
        try {
          const rect = element.getBoundingClientRect();
          const computedStyle = window.getComputedStyle(element);

          // Get the effective text color based on theme
          const isDarkMode = document.documentElement.classList.contains('dark');
          const textColor = isDarkMode ? '#ffffff' : '#000000'; // Black for light theme, white for dark

          textElements.push({
            id: `brand-text-${index}`,
            type: 'brand-text',
            content: element.textContent?.trim() || '',
            position: { x: rect.left, y: rect.top },
            dimensions: { width: rect.width, height: rect.height },
            styles: {
              fontSize: computedStyle.fontSize,
              fontFamily: computedStyle.fontFamily,
              fontWeight: computedStyle.fontWeight,
              color: textColor, // Use theme-appropriate color
              textAlign: computedStyle.textAlign || 'center'
            },
            className: element.className
          });
        } catch (error) {
          console.warn(`Failed to extract text element ${index}:`, error);
        }
      });

      // Look for other important text elements
      const headingElements = document.querySelectorAll('h1, h2, h3');
      headingElements.forEach((element, index) => {
        // Skip if already captured as brand-text
        if (element.classList.contains('brand-text')) return;

        try {
          const rect = element.getBoundingClientRect();
          const computedStyle = window.getComputedStyle(element);

          // Only capture visible elements with meaningful content
          if (rect.width > 0 && rect.height > 0 && element.textContent?.trim()) {
            const isDarkMode = document.documentElement.classList.contains('dark');
            const textColor = isDarkMode ? '#ffffff' : '#000000';

            textElements.push({
              id: `heading-${index}`,
              type: 'heading',
              content: element.textContent.trim(),
              position: { x: rect.left, y: rect.top },
              dimensions: { width: rect.width, height: rect.height },
              styles: {
                fontSize: computedStyle.fontSize,
                fontFamily: computedStyle.fontFamily,
                fontWeight: computedStyle.fontWeight,
                color: textColor,
                textAlign: computedStyle.textAlign || 'left'
              },
              tagName: element.tagName.toLowerCase()
            });
          }
        } catch (error) {
          console.warn(`Failed to extract heading element ${index}:`, error);
        }
      });

      return {
        textElements,
        totalElements: textElements.length,
        hasBrandText: brandElements.length > 0
      };
    });
  }

  /**
   * Extract layout and styling data from dashboard
   * @private
   */
  async _extractLayoutData(page, viewport) {
    return await page.evaluate((vp) => {
      const dashboard = document.querySelector('.photo-booth-dashboard') ||
                      document.querySelector('.dashboard-content') ||
                      document.body;

      const rect = dashboard.getBoundingClientRect();

      // Extract relevant CSS styles
      const computedStyle = window.getComputedStyle(dashboard);

      // Get grid layout information
      const gridInfo = {
        display: computedStyle.display,
        gridTemplateColumns: computedStyle.gridTemplateColumns,
        gridTemplateRows: computedStyle.gridTemplateRows,
        gap: computedStyle.gap,
        padding: computedStyle.padding,
        margin: computedStyle.margin
      };

      // Extract background and theme information
      const themeInfo = {
        backgroundColor: computedStyle.backgroundColor,
        color: computedStyle.color,
        fontFamily: computedStyle.fontFamily,
        fontSize: computedStyle.fontSize
      };

      return {
        viewport: vp,
        dashboard: {
          position: { x: rect.left, y: rect.top },
          dimensions: { width: rect.width, height: rect.height }
        },
        grid: gridInfo,
        theme: themeInfo,
        isDarkMode: document.documentElement.classList.contains('dark') ||
                   document.body.classList.contains('dark-mode')
      };
    }, viewport);
  }

  /**
   * Compose final SVG from extracted data
   * @private
   */
  async _composeSVG(svgData, textData, layoutData, options) {
    const { width, height, backgroundColor, includeCSS, optimizeText } = options;
    const { charts } = svgData;
    const { textElements } = textData;
    const { theme, isDarkMode } = layoutData;

    // SVG header with proper namespaces and viewport
    let svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="${width}"
     height="${height}"
     viewBox="0 0 ${width} ${height}"
     style="background-color: ${backgroundColor};">
`;

    // Add CSS styles if requested
    if (includeCSS) {
      svg += this._generateEmbeddedCSS(theme, isDarkMode);
    }

    // Add background
    svg += `  <rect width="100%" height="100%" fill="${backgroundColor}"/>\n`;

    // Add title and metadata
    svg += `  <title>Dashboard Export - ${new Date().toISOString()}</title>
  <desc>Vector dashboard export with ${charts.length} charts and ${textElements.length} text elements</desc>\n`;

    // Add each chart as a group
    charts.forEach((chart, index) => {
      if (chart.svg && chart.svg.includes('<svg')) {
        // Clean up the individual chart SVG
        let cleanSVG = this._cleanChartSVG(chart.svg, chart, optimizeText);

        svg += `  <!-- Chart ${index + 1}: ${chart.title} -->\n`;
        svg += `  <g id="${chart.id}" transform="translate(${chart.position.x}, ${chart.position.y})">\n`;
        svg += `    ${cleanSVG}\n`;
        svg += `  </g>\n`;
      }
    });

    // Add text elements (logos, headings, etc.)
    textElements.forEach((textElement, index) => {
      svg += `  <!-- Text Element ${index + 1}: ${textElement.type} -->\n`;
      svg += `  <g id="${textElement.id}">\n`;

      // Convert font size from pixels to SVG units
      const fontSize = parseFloat(textElement.styles.fontSize) || 16;
      const fontFamily = this._escapeXMLAttribute(textElement.styles.fontFamily || 'Arial, sans-serif');
      const fontWeight = textElement.styles.fontWeight || 'normal';
      const textColor = textElement.styles.color || (isDarkMode ? '#ffffff' : '#000000');
      const textAnchor = textElement.styles.textAlign === 'center' ? 'middle' :
                        textElement.styles.textAlign === 'right' ? 'end' : 'start';

      // Position text at center of element bounds for center alignment
      const textX = textElement.styles.textAlign === 'center' ?
                   textElement.position.x + (textElement.dimensions.width / 2) :
                   textElement.position.x;
      const textY = textElement.position.y + (textElement.dimensions.height / 2) + (fontSize / 3);

      svg += `    <text x="${textX}" y="${textY}"\n`;
      svg += `          font-family="${fontFamily}"\n`;
      svg += `          font-size="${fontSize}"\n`;
      svg += `          font-weight="${fontWeight}"\n`;
      svg += `          fill="${textColor}"\n`;
      svg += `          text-anchor="${textAnchor}"\n`;
      svg += `          dominant-baseline="middle">\n`;
      svg += `      ${textElement.content}\n`;
      svg += `    </text>\n`;
      svg += `  </g>\n`;
    });

    // Add footer with export info
    svg += `  <g id="export-info" opacity="0.1">
    <text x="${width - 10}" y="${height - 10}"
          text-anchor="end" font-size="10" fill="${isDarkMode ? '#ffffff' : '#000000'}">
      Exported: ${new Date().toLocaleString()}
    </text>
  </g>\n`;

    svg += '</svg>';

    return svg;
  }

  /**
   * Generate embedded CSS for SVG
   * @private
   */
  _generateEmbeddedCSS(theme, isDarkMode) {
    const textColor = isDarkMode ? '#ffffff' : '#000000';
    const gridColor = isDarkMode ? '#374151' : '#e5e7eb';

    return `  <defs>
    <style type="text/css"><![CDATA[
      .chart-title {
        font-family: ${theme.fontFamily || 'Arial, sans-serif'};
        font-size: 16px;
        font-weight: bold;
        fill: ${textColor};
      }
      .chart-text {
        font-family: ${theme.fontFamily || 'Arial, sans-serif'};
        font-size: 12px;
        fill: ${textColor};
      }
      .grid-line {
        stroke: ${gridColor};
        stroke-width: 1;
      }
    ]]></style>
  </defs>\n`;
  }

  /**
   * Escape XML attribute values to prevent syntax errors
   * @private
   */
  _escapeXMLAttribute(value) {
    if (!value) return '';

    return value
      .replace(/&/g, '&amp;')    // Must be first
      .replace(/"/g, '&quot;')   // Escape double quotes
      .replace(/'/g, '&apos;')   // Escape single quotes
      .replace(/</g, '&lt;')     // Escape less than
      .replace(/>/g, '&gt;');    // Escape greater than
  }

  /**
   * Clean and optimize individual chart SVG
   * @private
   */
  _cleanChartSVG(svgString, chart, optimizeText) {
    // Remove SVG wrapper and keep inner content
    let cleaned = svgString.replace(/<svg[^>]*>/, '').replace(/<\/svg>$/, '');

    // Remove any absolute positioning that might conflict
    cleaned = cleaned.replace(/style="[^"]*position:\s*absolute[^"]*"/g, '');

    // Optimize text elements if requested
    if (optimizeText) {
      // Convert text to more readable format
      cleaned = cleaned.replace(/<text([^>]*)>/g, '<text$1 class="chart-text">');
    }

    // Ensure proper scaling within the chart bounds
    if (chart.dimensions.width && chart.dimensions.height) {
      cleaned = `<svg viewBox="0 0 ${chart.dimensions.width} ${chart.dimensions.height}"
                      width="${chart.dimensions.width}"
                      height="${chart.dimensions.height}">
        ${cleaned}
      </svg>`;
    }

    return cleaned;
  }

  /**
   * Batch export multiple dashboards as SVG
   * @param {Array} exportList - Array of {url, output, options} objects
   * @returns {Promise<Array>} Array of export results
   */
  async batchExportSVG(exportList) {
    const results = [];

    if (this.verbose) {
      console.log(`🔄 Batch SVG export: ${exportList.length} dashboards...`);
    }

    for (const { url, output, options = {} } of exportList) {
      try {
        const result = await this.exportSVG(url, output, options);
        results.push(result);
      } catch (error) {
        results.push({
          success: false,
          error: error.message,
          url,
          outputPath: output
        });
      }
    }

    const successful = results.filter(r => r.success).length;
    if (this.verbose) {
      console.log(`✅ Batch SVG export complete: ${successful}/${exportList.length} successful`);
    }

    return results;
  }
}

// CLI interface
if (require.main === module) {
  const [,, command, ...args] = process.argv;

  const exporter = new SVGExporter({ verbose: true });

  async function main() {
    try {
      switch (command) {
        case 'export':
          if (args.length < 2) {
            console.error('Usage: node svg_exporter.js export <url> <output.svg> [width] [height]');
            process.exit(1);
          }
          const [url, output, width = 1920, height = 1080] = args;
          const result = await exporter.exportSVG(url, output, {
            width: parseInt(width),
            height: parseInt(height)
          });
          console.log('✅ SVG export complete:', result);
          break;

        default:
          console.log(`
SVG Exporter for Photo Booth

Usage:
  node svg_exporter.js export <url> <output.svg> [width] [height]

Examples:
  node svg_exporter.js export "http://localhost:4321/photo-booth?dashboard=trading" output.svg
  node svg_exporter.js export "http://localhost:4321/photo-booth?dashboard=portfolio" portfolio.svg 1440 1080
          `);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  }

  main();
}

module.exports = SVGExporter;
