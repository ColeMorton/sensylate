/**
 * Unified Chart Data Service
 *
 * Consolidates ChartDataService and EnhancedChartDataService into a single
 * service that uses chart-specific adapters for data fetching.
 *
 * Architecture:
 * - Registry-driven adapter resolution
 * - Colocated chart data logic
 * - Enhanced features (caching, dependency management)
 * - Backward compatibility with existing hooks
 */

import type {
  ChartType,
  DataServiceResponse,
  StockDataRow,
  PortfolioDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
} from "@/types/ChartTypes";

import type {
  DataSourceStatus,
  DataRefreshResult,
  ChartRefreshCapability,
} from "@/types/DataDependencyTypes";

import { chartRegistry } from "@/charts/chart-registry";
import { dataDependencyManager } from "@/services/DataDependencyManager";

// Generic data adapter interface
export interface ChartDataAdapter<T = any> {
  fetchData(signal?: AbortSignal, params?: any): Promise<T[]>;
}

// Enhanced response type
export interface EnhancedDataServiceResponse<T> extends DataServiceResponse<T> {
  dataStatus?: DataSourceStatus;
  refreshCapability?: ChartRefreshCapability;
  refresh?: () => Promise<DataRefreshResult>;
}

/**
 * Unified Chart Data Service
 */
class UnifiedChartDataService {
  private cache = new Map<string, { data: any[]; lastFetched: number }>();
  private readonly DEFAULT_CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
  private refreshCallbacks = new Map<ChartType, Set<() => void>>();

  constructor() {
    this.initializeRefreshNotifications();
  }

  /**
   * Generic data fetching method using chart registry adapters
   */
  async fetchChartData<T = any>(
    chartType: ChartType,
    signal?: AbortSignal,
    params?: any,
  ): Promise<T[]> {
    // Try to get adapter from chart registry
    const chartConfig = chartRegistry.getChartConfig(chartType);
    const adapter = chartConfig?.dataAdapter;

    if (adapter && typeof adapter.fetchData === "function") {
      // Use colocated adapter
      return await adapter.fetchData(signal, params);
    }

    // Fallback to legacy data fetching for unmigrated charts
    return await this.fetchLegacyData<T>(chartType, signal, params);
  }

  /**
   * Enhanced data fetching with dependency management
   */
  async fetchEnhancedChartData<T = any>(
    chartType: ChartType,
    signal?: AbortSignal,
    params?: any,
  ): Promise<EnhancedDataServiceResponse<T>> {
    try {
      const data = await this.fetchChartData<T>(chartType, signal, params);

      // Get data status from dependency manager
      const dataStatus = dataDependencyManager.getDataStatus(chartType);
      const refreshCapability =
        dataDependencyManager.getChartRefreshCapability(chartType);

      return {
        data,
        loading: false,
        error: null,
        dataStatus,
        refreshCapability,
        refresh: () => this.refreshChartData(chartType, params),
      };
    } catch (error) {
      return {
        data: [],
        loading: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Cached data fetching
   */
  async fetchCachedChartData<T = any>(
    chartType: ChartType,
    signal?: AbortSignal,
    params?: any,
    cacheDuration?: number,
  ): Promise<T[]> {
    const cacheKey = this.getCacheKey(chartType, params);
    const cached = this.cache.get(cacheKey);
    const duration = cacheDuration ?? this.DEFAULT_CACHE_DURATION;

    // Return cached data if valid
    if (cached && Date.now() - cached.lastFetched < duration) {
      return cached.data;
    }

    // Fetch fresh data
    const data = await this.fetchChartData<T>(chartType, signal, params);

    // Update cache
    this.cache.set(cacheKey, {
      data,
      lastFetched: Date.now(),
    });

    return data;
  }

  /**
   * Legacy data fetching for backward compatibility
   */
  private async fetchLegacyData<T = any>(
    chartType: ChartType,
    signal?: AbortSignal,
    params?: any,
  ): Promise<T[]> {
    // Legacy chart type mappings
    const legacyMethods: Record<string, () => Promise<any[]>> = {
      "apple-price": () => this.fetchAppleStockData(signal),
      "mstr-price": () => this.fetchMSTRStockData(signal),
      "btc-price": () => this.fetchBTCPriceData(signal),
      "portfolio-value-comparison": () => this.fetchPortfolioData(signal),
      "live-signals-equity-curve": () => this.fetchLiveSignalsData(signal),
      "trade-pnl-waterfall": () => this.fetchTradeHistoryData(signal),
      // Add more mappings as needed
    };

    const fetchMethod = legacyMethods[chartType];
    if (fetchMethod) {
      return await fetchMethod();
    }

    throw new Error(`No data adapter found for chart type: ${chartType}`);
  }

  // Legacy methods (kept for backward compatibility)
  async fetchAppleStockData(signal?: AbortSignal): Promise<StockDataRow[]> {
    const response = await fetch("/data/raw/stocks/AAPL/daily.csv", { signal });
    if (!response.ok) {
      throw new Error(`Failed to fetch Apple data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parseCSV(csvText);
  }

  async fetchMSTRStockData(signal?: AbortSignal): Promise<StockDataRow[]> {
    const response = await fetch("/data/raw/stocks/MSTR/daily.csv", { signal });
    if (!response.ok) {
      throw new Error(`Failed to fetch MSTR data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parseCSV(csvText);
  }

  async fetchBTCPriceData(signal?: AbortSignal): Promise<StockDataRow[]> {
    const response = await fetch("/data/raw/stocks/BITCOIN/daily.csv", {
      signal,
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch BTC data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parseCSV(csvText);
  }

  async fetchPortfolioData(signal?: AbortSignal): Promise<PortfolioDataRow[]> {
    const response = await fetch(
      "/data/outputs/multi_strategy_bitcoin_portfolio.csv",
      { signal },
    );
    if (!response.ok) {
      throw new Error(`Failed to fetch portfolio data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parsePortfolioCSV(csvText);
  }

  async fetchLiveSignalsData(
    signal?: AbortSignal,
  ): Promise<LiveSignalsDataRow[]> {
    const response = await fetch("/data/outputs/live_signals_portfolio.csv", {
      signal,
    });
    if (!response.ok) {
      throw new Error(`Failed to fetch live signals data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parseLiveSignalsCSV(csvText);
  }

  async fetchTradeHistoryData(
    signal?: AbortSignal,
  ): Promise<TradeHistoryDataRow[]> {
    const response = await fetch(
      "/data/outputs/live_signals_closed_positions.csv",
      { signal },
    );
    if (!response.ok) {
      throw new Error(`Failed to fetch trade history data: ${response.status}`);
    }
    const csvText = await response.text();
    return this.parseTradeHistoryCSV(csvText);
  }

  // CSV parsing utilities (reused from original service)
  private parseCSV(csvText: string): StockDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: StockDataRow = {} as StockDataRow;
      headers.forEach((header, index) => {
        row[header.trim()] = values[index]?.trim() || "";
      });
      return row;
    });
  }

  private parsePortfolioCSV(csvText: string): PortfolioDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: Partial<PortfolioDataRow> = {};
      headers.forEach((header, index) => {
        row[header.trim() as keyof PortfolioDataRow] =
          values[index]?.trim() || "";
      });
      return row as PortfolioDataRow;
    });
  }

  private parseLiveSignalsCSV(csvText: string): LiveSignalsDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: Partial<LiveSignalsDataRow> = {};
      headers.forEach((header, index) => {
        row[header.trim() as keyof LiveSignalsDataRow] =
          values[index]?.trim() || "";
      });
      return row as LiveSignalsDataRow;
    });
  }

  private parseTradeHistoryCSV(csvText: string): TradeHistoryDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: Partial<TradeHistoryDataRow> = {};
      headers.forEach((header, index) => {
        row[header.trim() as keyof TradeHistoryDataRow] =
          values[index]?.trim() || "";
      });
      return row as TradeHistoryDataRow;
    });
  }

  // Enhanced features
  private initializeRefreshNotifications(): void {
    setInterval(() => {
      this.checkForDataUpdates();
    }, 30000); // Check every 30 seconds
  }

  private checkForDataUpdates(): void {
    const allStatuses = dataDependencyManager.getAllDataStatuses();

    allStatuses.forEach((status, chartType) => {
      if (status.lastUpdateSource && status.lastUpdated) {
        const timeSinceUpdate = Date.now() - status.lastUpdated;
        if (timeSinceUpdate < 60000) {
          this.notifyRefreshSubscribers(chartType);
        }
      }
    });
  }

  private notifyRefreshSubscribers(chartType: ChartType): void {
    const subscribers = this.refreshCallbacks.get(chartType);
    if (subscribers) {
      subscribers.forEach((callback) => callback());
    }
  }

  private async refreshChartData(
    chartType: ChartType,
    params?: any,
  ): Promise<DataRefreshResult> {
    try {
      // Clear cache for this chart
      const cacheKey = this.getCacheKey(chartType, params);
      this.cache.delete(cacheKey);

      // Fetch fresh data
      await this.fetchChartData(chartType, undefined, params);

      return { success: true, timestamp: Date.now() };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
        timestamp: Date.now(),
      };
    }
  }

  private getCacheKey(chartType: ChartType, params?: any): string {
    return params ? `${chartType}:${JSON.stringify(params)}` : chartType;
  }

  // Subscribe to refresh notifications
  subscribeToRefresh(chartType: ChartType, callback: () => void): () => void {
    if (!this.refreshCallbacks.has(chartType)) {
      this.refreshCallbacks.set(chartType, new Set());
    }

    const subscribers = this.refreshCallbacks.get(chartType)!;
    subscribers.add(callback);

    // Return unsubscribe function
    return () => {
      subscribers.delete(callback);
      if (subscribers.size === 0) {
        this.refreshCallbacks.delete(chartType);
      }
    };
  }
}

// Export singleton instance
export const unifiedChartDataService = new UnifiedChartDataService();
export default unifiedChartDataService;
