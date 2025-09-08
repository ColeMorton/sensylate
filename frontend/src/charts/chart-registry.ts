/**
 * Chart Registry
 * 
 * Auto-discovery and registration system for chart components.
 * Replaces hardcoded chart type arrays and routing logic.
 */

import type { ChartRegistryEntry, ChartConfig } from './chart-config.schema';
import type { ChartDataAdapter } from '@/services/UnifiedChartDataService';

// Import chart configurations (will be auto-generated in future)
import btcPriceChartConfig from './btc-price/chart.config';
import { btcPriceDataAdapter } from './btc-price/data-adapter';

/**
 * Chart Registry - maintains all available chart configurations
 */
class ChartRegistry {
  private registry = new Map<string, ChartRegistryEntry>();
  private legacyChartTypes = new Set<string>();

  constructor() {
    this.initialize();
  }

  private initialize() {
    // Register BTC Price Chart (colocated)
    this.registry.set('btc-price', {
      ...btcPriceChartConfig,
      component: null, // Will be loaded lazily via PortfolioChart
      dataAdapter: btcPriceDataAdapter
    });

    // Legacy chart types (handled by existing PortfolioChart component)
    const legacyTypes = [
      "apple-price",
      "mstr-price", 
      "portfolio-value-comparison",
      "returns-comparison",
      "portfolio-drawdowns",
      "live-signals-equity-curve",
      "live-signals-benchmark-comparison", 
      "live-signals-drawdowns",
      "live-signals-weekly-candlestick",
      "trade-pnl-waterfall",
      "open-positions-pnl-timeseries",
      "closed-positions-pnl-timeseries",
      "multi-stock-price",
      "xpev-nio-stock-price"
    ];

    legacyTypes.forEach(type => {
      this.legacyChartTypes.add(type);
      this.registry.set(type, {
        metadata: {
          title: this.generateLegacyTitle(type),
          category: "Legacy Chart",
          description: `Legacy chart implementation for ${type}`,
          chartType: type
        },
        dataRequirements: {
          dataSources: [],
          cacheable: true
        },
        productionReady: true,
        component: null, // Uses PortfolioChart
        dataAdapter: null // Uses ChartDataService
      });
    });

    // Fundamental chart types (development only)
    const fundamentalTypes = [
      "fundamental-revenue-fcf",
      "fundamental-revenue-source", 
      "fundamental-geography",
      "fundamental-key-metrics",
      "fundamental-quality-rating",
      "fundamental-financial-health",
      "fundamental-pros-cons",
      "fundamental-valuation",
      "fundamental-balance-sheet"
    ];

    fundamentalTypes.forEach(type => {
      this.registry.set(type, {
        metadata: {
          title: this.generateFundamentalTitle(type),
          category: "Fundamental Analysis",
          description: `Fundamental analysis chart for ${type.replace('fundamental-', '')}`,
          chartType: type
        },
        dataRequirements: {
          dataSources: [],
          cacheable: false
        },
        productionReady: false, // Development only
        component: null, // Uses FundamentalChart
        dataAdapter: null
      });
    });
  }

  private generateLegacyTitle(type: string): string {
    return type
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  private generateFundamentalTitle(type: string): string {
    return type
      .replace('fundamental-', '')
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' & ');
  }

  /**
   * Get chart configuration by type
   */
  getChartConfig(chartType: string): ChartConfig | undefined {
    return this.registry.get(chartType);
  }

  /**
   * Get all registered chart types
   */
  getChartTypes(): string[] {
    return Array.from(this.registry.keys());
  }

  /**
   * Check if a chart type is supported
   */
  isSupported(chartType: string): boolean {
    return this.registry.has(chartType);
  }

  /**
   * Check if a chart type is ready for production
   */
  isProductionReady(chartType: string): boolean {
    const entry = this.registry.get(chartType);
    return entry?.productionReady ?? false;
  }

  /**
   * Check if a chart is a fundamental analysis chart
   */
  isFundamentalChart(chartType: string): boolean {
    return chartType.startsWith('fundamental-');
  }

  /**
   * Check if a chart is a legacy chart (uses PortfolioChart)
   */
  isLegacyChart(chartType: string): boolean {
    return this.legacyChartTypes.has(chartType);
  }

  /**
   * Get all chart configurations (for dashboard generation)
   */
  getAllChartConfigs(): Record<string, ChartConfig> {
    const configs: Record<string, ChartConfig> = {};
    for (const [type, entry] of this.registry.entries()) {
      configs[type] = {
        metadata: entry.metadata,
        dataRequirements: entry.dataRequirements,
        displayOptions: entry.displayOptions,
        productionReady: entry.productionReady
      };
    }
    return configs;
  }

  /**
   * Get chart configurations for a specific dashboard
   * This replaces hardcoded configurations in Python script
   */
  getChartsForDashboard(dashboardId: string): ChartConfig[] {
    // Dashboard-specific chart mappings
    // TODO: Move this to dashboard configuration files
    const dashboardCharts: Record<string, string[]> = {
      'bitcoin_cycle_intelligence': ['btc-price'],
      // Add other dashboard mappings as we migrate them
    };

    const chartTypes = dashboardCharts[dashboardId] || [];
    return chartTypes
      .map(type => this.getChartConfig(type))
      .filter((config): config is ChartConfig => config !== undefined);
  }
}

// Export singleton instance
export const chartRegistry = new ChartRegistry();

// Export types for external use
export type { ChartRegistryEntry };
export { type ChartConfig } from './chart-config.schema';