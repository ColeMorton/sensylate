#!/usr/bin/env node
/**
 * Data Mappings Auto-Discovery Script
 *
 * Extracts data requirements from colocated chart directories to integrate
 * with the DevContentOps data pipeline. This bridges the gap between frontend
 * chart colocation and backend data pipeline discovery.
 */

const fs = require('fs').promises;
const path = require('path');

/**
 * Data mapping discovery configuration
 */
const CONFIG = {
  // Chart directories to scan
  chartsDir: path.resolve(__dirname, '../frontend/src/charts'),
  
  // Output file for data mappings
  outputFile: path.resolve(__dirname, 'data-mappings.json'),
  
  // Pipeline mappings output (for integration with active_chart_requirements.py)
  pipelineOutputFile: path.resolve(__dirname, 'pipeline-data-mappings.json'),
  
  // Data requirements file pattern
  dataRequirementsPattern: 'data-requirements.ts',
};

/**
 * Extract data mapping from data-requirements.ts content
 */
function extractDataMappingFromContent(content, chartType) {
  try {
    // Extract the data mapping export
    const dataMappingMatch = content.match(/export const \w+DataMapping\s*=\s*({[\s\S]*?});/);
    if (dataMappingMatch) {
      // Parse the mapping object (basic extraction)
      const mappingStr = dataMappingMatch[1];
      
      // Extract key properties using regex (more robust than eval)
      const dataSourceMatch = mappingStr.match(/data_source:\s*["']([^"']+)["']/);
      const categoryMatch = mappingStr.match(/category:\s*["']([^"']+)["']/);
      const servicesMatch = mappingStr.match(/services:\s*\[([^\]]+)\]/);
      
      if (dataSourceMatch && categoryMatch) {
        const mapping = {
          data_source: dataSourceMatch[1],
          category: categoryMatch[1],
          services: [],
        };
        
        if (servicesMatch) {
          // Extract services array
          const servicesStr = servicesMatch[1];
          const services = servicesStr.split(',').map(s => s.trim().replace(/["']/g, ''));
          mapping.services = services;
        }
        
        return { [chartType]: mapping };
      }
    }
    
    return null;
  } catch (error) {
    console.warn(`Warning: Could not extract data mapping for ${chartType}:`, error.message);
    return null;
  }
}

/**
 * Extract comprehensive data requirements for pipeline integration
 */
function extractDataRequirementsFromContent(content, chartType) {
  try {
    // Extract symbol metadata
    const symbolMetadataMatch = content.match(/symbolMetadata:\s*{([\s\S]*?)}/);
    let symbolMetadata = null;
    
    if (symbolMetadataMatch) {
      const metadataStr = symbolMetadataMatch[1];
      const symbolMatch = metadataStr.match(/symbol:\s*["']([^"']+)["']/);
      const nameMatch = metadataStr.match(/name:\s*["']([^"']+)["']/);
      const dataYearsMatch = metadataStr.match(/dataYears:\s*(\d+)/);
      
      if (symbolMatch) {
        symbolMetadata = {
          symbol: symbolMatch[1],
          name: nameMatch ? nameMatch[1] : null,
          dataYears: dataYearsMatch ? parseInt(dataYearsMatch[1]) : null,
        };
      }
    }
    
    // Extract multi-symbol config
    const multiSymbolMatch = content.match(/symbols:\s*\[([^\]]+)\]/);
    let multiSymbolConfig = null;
    
    if (multiSymbolMatch) {
      const symbolsStr = multiSymbolMatch[1];
      const symbols = symbolsStr.split(',').map(s => s.trim().replace(/["']/g, ''));
      multiSymbolConfig = { symbols };
    }
    
    return {
      chartType,
      symbolMetadata,
      multiSymbolConfig,
    };
  } catch (error) {
    console.warn(`Warning: Could not extract data requirements for ${chartType}:`, error.message);
    return null;
  }
}

/**
 * Discover data mappings from a single chart directory
 */
async function discoverChartDataMapping(chartDir) {
  try {
    const chartType = path.basename(chartDir);
    const dataRequirementsFile = path.join(chartDir, CONFIG.dataRequirementsPattern);
    
    // Check if data-requirements.ts exists
    try {
      await fs.access(dataRequirementsFile);
    } catch {
      // No data requirements file found
      return null;
    }
    
    // Read and extract data mapping
    const content = await fs.readFile(dataRequirementsFile, 'utf8');
    const dataMapping = extractDataMappingFromContent(content, chartType);
    const dataRequirements = extractDataRequirementsFromContent(content, chartType);
    
    if (dataMapping) {
      console.log(`✅ Extracted data mapping for: ${chartType}`);
      return {
        mapping: dataMapping,
        requirements: dataRequirements,
      };
    }
    
    return null;
  } catch (error) {
    console.warn(`⚠️  Error processing chart directory ${chartDir}:`, error.message);
    return null;
  }
}

/**
 * Main discovery function
 */
async function discoverAllDataMappings() {
  try {
    console.log('🔍 Starting data mappings auto-discovery...');
    console.log(`📁 Scanning charts directory: ${CONFIG.chartsDir}`);
    
    // Get all chart directories
    const entries = await fs.readdir(CONFIG.chartsDir, { withFileTypes: true });
    const chartDirectories = entries
      .filter(entry => entry.isDirectory())
      .map(entry => path.join(CONFIG.chartsDir, entry.name));
    
    console.log(`📊 Found ${chartDirectories.length} chart directories`);
    
    // Discover data mappings from each chart
    const discoveries = await Promise.all(
      chartDirectories.map(discoverChartDataMapping)
    );
    
    // Filter successful discoveries
    const successfulDiscoveries = discoveries.filter(Boolean);
    
    // Combine all data mappings
    const allDataMappings = {};
    const allDataRequirements = [];
    
    successfulDiscoveries.forEach(discovery => {
      Object.assign(allDataMappings, discovery.mapping);
      if (discovery.requirements) {
        allDataRequirements.push(discovery.requirements);
      }
    });
    
    // Create output objects
    const output = {
      version: '1.0.0',
      description: 'Auto-discovered data mappings from colocated chart directories',
      discoveredAt: new Date().toISOString(),
      totalCharts: chartDirectories.length,
      chartsWithDataMappings: successfulDiscoveries.length,
      dataMappings: allDataMappings,
      dataRequirements: allDataRequirements,
    };
    
    // Pipeline-specific format (matches active_chart_requirements.py expectations)
    const pipelineOutput = {
      version: '1.0.0',
      chartDataMapping: allDataMappings,
      discoveredAt: new Date().toISOString(),
      source: 'colocated-charts-auto-discovery',
    };
    
    // Write output files
    await fs.writeFile(CONFIG.outputFile, JSON.stringify(output, null, 2));
    await fs.writeFile(CONFIG.pipelineOutputFile, JSON.stringify(pipelineOutput, null, 2));
    
    console.log('✅ Data mappings discovery completed successfully');
    console.log(`📄 Generated mappings file: ${CONFIG.outputFile}`);
    console.log(`🔗 Generated pipeline mappings: ${CONFIG.pipelineOutputFile}`);
    console.log(`📊 Discovered ${successfulDiscoveries.length}/${chartDirectories.length} data mappings`);
    
    // Log discovered mappings
    Object.keys(allDataMappings).forEach(chartType => {
      const mapping = allDataMappings[chartType];
      console.log(`   - ${chartType}: ${mapping.data_source} (${mapping.category})`);
    });
    
    return output;
    
  } catch (error) {
    console.error('❌ Data mappings discovery failed:', error);
    process.exit(1);
  }
}

// Run discovery if called directly
if (require.main === module) {
  discoverAllDataMappings().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = {
  discoverAllDataMappings,
  CONFIG,
};