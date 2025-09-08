/**
 * Legacy Chart Data Service Compatibility Layer
 *
 * Provides backward compatibility for existing components while
 * gradually migrating to the UnifiedChartDataService.
 *
 * This allows us to:
 * 1. Keep existing hooks and components working
 * 2. Gradually migrate chart-by-chart
 * 3. Test unified service integration
 * 4. Eventually deprecate and remove this file
 */

import { unifiedChartDataService } from "./UnifiedChartDataService";
import type {
  StockDataRow,
  PortfolioDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  ClosedPositionPnLDataRow,
  OpenPositionPnLDataRow,
  BenchmarkDataRow,
  LiveSignalsBenchmarkDataRow,
} from "@/types/ChartTypes";

/**
 * Legacy ChartDataService wrapper
 * Routes calls to UnifiedChartDataService for gradual migration
 */
class LegacyChartDataService {
  // Legacy method signatures maintained for compatibility

  async fetchAppleStockData(signal?: AbortSignal): Promise<StockDataRow[]> {
    return unifiedChartDataService.fetchChartData("apple-price", signal);
  }

  async fetchMSTRStockData(signal?: AbortSignal): Promise<StockDataRow[]> {
    return unifiedChartDataService.fetchChartData("mstr-price", signal);
  }

  async fetchBTCPriceData(signal?: AbortSignal): Promise<StockDataRow[]> {
    return unifiedChartDataService.fetchChartData("btc-price", signal);
  }

  async fetchPortfolioData(signal?: AbortSignal): Promise<PortfolioDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "portfolio-value-comparison",
      signal,
    );
  }

  async fetchLiveSignalsData(
    signal?: AbortSignal,
  ): Promise<LiveSignalsDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "live-signals-equity-curve",
      signal,
    );
  }

  async fetchTradeHistoryData(
    signal?: AbortSignal,
  ): Promise<TradeHistoryDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "trade-pnl-waterfall",
      signal,
    );
  }

  async fetchClosedPositionsPnLData(
    signal?: AbortSignal,
  ): Promise<ClosedPositionPnLDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "closed-positions-pnl-timeseries",
      signal,
    );
  }

  async fetchOpenPositionsPnLData(
    signal?: AbortSignal,
  ): Promise<OpenPositionPnLDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "open-positions-pnl-timeseries",
      signal,
    );
  }

  async fetchBenchmarkData(signal?: AbortSignal): Promise<BenchmarkDataRow[]> {
    return unifiedChartDataService.fetchChartData("returns-comparison", signal);
  }

  async fetchLiveSignalsBenchmarkData(
    signal?: AbortSignal,
  ): Promise<LiveSignalsBenchmarkDataRow[]> {
    return unifiedChartDataService.fetchChartData(
      "live-signals-benchmark-comparison",
      signal,
    );
  }

  // Additional methods can be added as needed for compatibility
}

// Export instance for backward compatibility
export const chartDataService = new LegacyChartDataService();
export default chartDataService;
