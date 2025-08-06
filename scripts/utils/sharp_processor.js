#!/usr/bin/env node

/**
 * Sharp.js Image Processing Module for Photo Booth
 *
 * This module provides high-performance image processing using Sharp.js for:
 * - High-DPI PNG optimization with proper metadata
 * - DPI setting and metadata injection
 * - Format conversion and optimization
 * - Professional-grade image output
 */

let sharp;
try {
  // Try to require from frontend node_modules first
  const path = require('path');
  const frontendPath = path.join(__dirname, '../../frontend/node_modules/sharp');
  sharp = require(frontendPath);
} catch (error) {
  try {
    // Fallback to standard require
    sharp = require('sharp');
  } catch (fallbackError) {
    console.error('❌ Sharp.js not found. Please install sharp in the frontend directory:');
    console.error('   cd frontend && npm install sharp');
    process.exit(1);
  }
}
const path = require('path');
const fs = require('fs').promises;

class SharpProcessor {
  constructor(options = {}) {
    this.defaultDPI = options.defaultDPI || 300;
    this.defaultQuality = options.defaultQuality || 95;
    this.verbose = options.verbose || false;
  }

  /**
   * Process PNG image with high-DPI metadata and optimization
   * @param {string} inputPath - Path to input PNG file
   * @param {string} outputPath - Path for output PNG file
   * @param {Object} options - Processing options
   * @returns {Promise<Object>} Processing result with metadata
   */
  async processPNG(inputPath, outputPath, options = {}) {
    const {
      dpi = this.defaultDPI,
      quality = this.defaultQuality,
      scaleFactor = 1,
      optimize = true
    } = options;

    try {
      if (this.verbose) {
        console.log(`📷 Processing PNG: ${path.basename(inputPath)}`);
        console.log(`   DPI: ${dpi}, Scale: ${scaleFactor}x, Quality: ${quality}%`);
      }

      let processor = sharp(inputPath);

      // Get input metadata
      const metadata = await processor.metadata();
      const originalWidth = metadata.width;
      const originalHeight = metadata.height;

      // Apply scaling if needed
      if (scaleFactor !== 1) {
        const newWidth = Math.round(originalWidth * scaleFactor);
        const newHeight = Math.round(originalHeight * scaleFactor);
        processor = processor.resize(newWidth, newHeight, {
          kernel: sharp.kernel.lanczos3,
          withoutEnlargement: false
        });
      }

      // Configure PNG output with optimization and metadata
      processor = processor.png({
        quality: quality,
        compressionLevel: optimize ? 9 : 6,
        adaptiveFiltering: optimize,
        palette: false, // Ensure full color depth
        progressive: false
      });

      // Add DPI metadata
      processor = processor.withMetadata({
        density: dpi,
        exif: {},
        icc: metadata.icc, // Preserve color profile
        iptc: {},
        xmp: {}
      });

      // Write processed image
      await processor.toFile(outputPath);

      // Get final metadata for verification
      const finalMetadata = await sharp(outputPath).metadata();

      const result = {
        success: true,
        inputPath,
        outputPath,
        originalDimensions: { width: originalWidth, height: originalHeight },
        finalDimensions: { width: finalMetadata.width, height: finalMetadata.height },
        dpi: finalMetadata.density || dpi,
        format: finalMetadata.format,
        fileSize: (await fs.stat(outputPath)).size,
        scaleFactor,
        processingTime: Date.now()
      };

      if (this.verbose) {
        console.log(`✅ PNG processed: ${finalMetadata.width}x${finalMetadata.height} @ ${result.dpi} DPI`);
        console.log(`   File size: ${(result.fileSize / 1024 / 1024).toFixed(2)} MB`);
      }

      return result;

    } catch (error) {
      const result = {
        success: false,
        error: error.message,
        inputPath,
        outputPath
      };

      if (this.verbose) {
        console.error(`❌ PNG processing failed: ${error.message}`);
      }

      throw error;
    }
  }

  /**
   * Create multiple DPI versions of a PNG
   * @param {string} inputPath - Input PNG file
   * @param {string} baseOutputPath - Base output path (without extension)
   * @param {Array<number>} dpiList - List of DPI values to generate
   * @param {Object} options - Processing options
   * @returns {Promise<Array>} Array of processing results
   */
  async createMultiDPIVersions(inputPath, baseOutputPath, dpiList = [150, 300, 600], options = {}) {
    const results = [];

    if (this.verbose) {
      console.log(`🎯 Creating multi-DPI versions: ${dpiList.join(', ')} DPI`);
    }

    for (const dpi of dpiList) {
      const outputPath = `${baseOutputPath}_${dpi}dpi.png`;

      // Calculate scale factor for higher DPI (assuming 150 DPI as base)
      const baseDPI = 150;
      const scaleFactor = dpi / baseDPI;

      try {
        const result = await this.processPNG(inputPath, outputPath, {
          ...options,
          dpi,
          scaleFactor
        });
        results.push(result);
      } catch (error) {
        results.push({
          success: false,
          error: error.message,
          dpi,
          outputPath
        });
      }
    }

    return results;
  }

  /**
   * Optimize existing PNG without changing dimensions
   * @param {string} inputPath - Input PNG file
   * @param {string} outputPath - Output PNG file
   * @param {Object} options - Optimization options
   * @returns {Promise<Object>} Processing result
   */
  async optimizePNG(inputPath, outputPath, options = {}) {
    const { dpi = this.defaultDPI, lossless = true } = options;

    return this.processPNG(inputPath, outputPath, {
      dpi,
      quality: lossless ? 100 : this.defaultQuality,
      scaleFactor: 1,
      optimize: true
    });
  }

  /**
   * Get image metadata and statistics
   * @param {string} imagePath - Path to image file
   * @returns {Promise<Object>} Image metadata
   */
  async getImageInfo(imagePath) {
    try {
      const metadata = await sharp(imagePath).metadata();
      const stats = await fs.stat(imagePath);

      return {
        success: true,
        path: imagePath,
        format: metadata.format,
        width: metadata.width,
        height: metadata.height,
        channels: metadata.channels,
        depth: metadata.depth,
        density: metadata.density,
        hasAlpha: metadata.hasAlpha,
        fileSize: stats.size,
        fileSizeMB: (stats.size / 1024 / 1024).toFixed(2),
        aspectRatio: (metadata.width / metadata.height).toFixed(3)
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        path: imagePath
      };
    }
  }

  /**
   * Batch process multiple images
   * @param {Array} imageList - Array of {input, output, options} objects
   * @returns {Promise<Array>} Array of processing results
   */
  async batchProcess(imageList) {
    const results = [];

    if (this.verbose) {
      console.log(`🔄 Batch processing ${imageList.length} images...`);
    }

    for (const { input, output, options = {} } of imageList) {
      try {
        const result = await this.processPNG(input, output, options);
        results.push(result);
      } catch (error) {
        results.push({
          success: false,
          error: error.message,
          inputPath: input,
          outputPath: output
        });
      }
    }

    const successful = results.filter(r => r.success).length;
    if (this.verbose) {
      console.log(`✅ Batch processing complete: ${successful}/${imageList.length} successful`);
    }

    return results;
  }
}

// CLI interface
if (require.main === module) {
  const [,, command, ...args] = process.argv;

  const processor = new SharpProcessor({ verbose: true });

  async function main() {
    try {
      switch (command) {
        case 'process':
          if (args.length < 2) {
            console.error('Usage: node sharp_processor.js process <input> <output> [dpi] [scale]');
            process.exit(1);
          }
          const [input, output, dpi = 300, scale = 1] = args;
          const result = await processor.processPNG(input, output, {
            dpi: parseInt(dpi),
            scaleFactor: parseFloat(scale)
          });
          console.log('✅ Processing complete:', result);
          break;

        case 'info':
          if (args.length < 1) {
            console.error('Usage: node sharp_processor.js info <image_path>');
            process.exit(1);
          }
          const info = await processor.getImageInfo(args[0]);
          console.log('📊 Image Information:', JSON.stringify(info, null, 2));
          break;

        case 'multi-dpi':
          if (args.length < 2) {
            console.error('Usage: node sharp_processor.js multi-dpi <input> <base_output> [dpi_list]');
            process.exit(1);
          }
          const [inputImg, baseOutput, dpiString = '150,300,600'] = args;
          const dpiList = dpiString.split(',').map(d => parseInt(d.trim()));
          const multiResults = await processor.createMultiDPIVersions(inputImg, baseOutput, dpiList);
          console.log('✅ Multi-DPI processing complete:', multiResults);
          break;

        default:
          console.log(`
Sharp.js Image Processor for Photo Booth

Usage:
  node sharp_processor.js process <input> <output> [dpi] [scale]
  node sharp_processor.js info <image_path>
  node sharp_processor.js multi-dpi <input> <base_output> [dpi_list]

Examples:
  node sharp_processor.js process input.png output.png 300 2
  node sharp_processor.js info dashboard.png
  node sharp_processor.js multi-dpi raw.png processed 150,300,600
          `);
      }
    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  }

  main();
}

module.exports = SharpProcessor;
