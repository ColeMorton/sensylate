/**
 * Enhanced Chart Data Service
 *
 * Extends the existing ChartDataService with data dependency management,
 * intelligent refresh policies, and data source status tracking.
 */

import type {
  ChartType,
  DataServiceResponse,
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  ClosedPositionPnLDataRow,
  OpenPositionPnLDataRow,
  BenchmarkDataRow,
  LiveSignalsBenchmarkDataRow,
  PortfolioDataCache,
} from "@/types/ChartTypes";

import type {
  DataSourceStatus,
  DataRefreshRequest,
  DataRefreshResult,
  ChartRefreshCapability,
} from "@/types/DataDependencyTypes";

import { chartDataService } from "@/services/ChartDataService";
import { dataDependencyManager } from "@/services/DataDependencyManager";

/**
 * Enhanced response type that includes data dependency information
 */
export interface EnhancedDataServiceResponse<T> extends DataServiceResponse<T> {
  /** Data source status and freshness information */
  dataStatus?: DataSourceStatus;
  /** Refresh capability for this chart type */
  refreshCapability?: ChartRefreshCapability;
  /** Function to trigger manual refresh */
  refresh?: () => Promise<DataRefreshResult>;
}

/**
 * Enhanced Chart Data Service with dependency management
 */
class EnhancedChartDataService {
  private refreshCallbacks: Map<ChartType, Set<() => void>> = new Map();

  constructor() {
    // Set up refresh notifications
    this.initializeRefreshNotifications();
  }

  /**
   * Initialize refresh notification system
   */
  private initializeRefreshNotifications(): void {
    // Monitor data status changes and notify subscribers
    setInterval(() => {
      this.checkForDataUpdates();
    }, 30000); // Check every 30 seconds
  }

  /**
   * Check for data updates and notify subscribers
   */
  private checkForDataUpdates(): void {
    const allStatuses = dataDependencyManager.getAllDataStatuses();

    allStatuses.forEach((status, chartType) => {
      if (status.lastUpdateSource && status.lastUpdated) {
        // If data was recently updated, notify subscribers
        const timeSinceUpdate = Date.now() - status.lastUpdated;
        if (timeSinceUpdate < 60000) {
          // Updated in last minute
          this.notifyRefreshSubscribers(chartType);
        }
      }
    });
  }

  /**
   * Notify subscribers of data refresh for a chart type
   */
  private notifyRefreshSubscribers(chartType: ChartType): void {
    const callbacks = this.refreshCallbacks.get(chartType);
    if (callbacks) {
      callbacks.forEach((callback) => callback());
    }
  }

  /**
   * Subscribe to refresh notifications for a chart type
   */
  public subscribeToRefresh(
    chartType: ChartType,
    callback: () => void,
  ): () => void {
    if (!this.refreshCallbacks.has(chartType)) {
      this.refreshCallbacks.set(chartType, new Set());
    }

    this.refreshCallbacks.get(chartType)!.add(callback);

    // Return unsubscribe function
    return () => {
      this.refreshCallbacks.get(chartType)?.delete(callback);
    };
  }

  /**
   * Create enhanced response with dependency information
   */
  private createEnhancedResponse<T>(
    chartType: ChartType,
    baseResponse: DataServiceResponse<T>,
  ): EnhancedDataServiceResponse<T> {
    const dataStatus = dataDependencyManager.getDataStatus(chartType);
    const refreshCapability =
      dataDependencyManager.getRefreshCapability(chartType);

    const refresh = refreshCapability?.canRefresh
      ? async () => {
          const request: DataRefreshRequest = {
            chartType,
            priority: "normal",
          };
          return dataDependencyManager.requestRefresh(request);
        }
      : undefined;

    return {
      ...baseResponse,
      dataStatus,
      refreshCapability,
      refresh,
    };
  }

  // Enhanced data fetching methods that include dependency information

  /**
   * Enhanced Apple stock data with dependency management
   */
  public useAppleStockData(): EnhancedDataServiceResponse<StockDataRow[]> {
    // Get base data from original service
    const baseResponse = this.getBaseAppleStockData();
    return this.createEnhancedResponse("apple-stock", baseResponse);
  }

  /**
   * Enhanced portfolio data with dependency management
   */
  public usePortfolioData(chartType: ChartType): EnhancedDataServiceResponse<{
    multiStrategy?: PortfolioDataRow[];
    buyHold?: PortfolioDataRow[];
    drawdowns?: PortfolioDataRow[];
  }> {
    const baseResponse = this.getBasePortfolioData(chartType);
    return this.createEnhancedResponse(chartType, baseResponse);
  }

  /**
   * Enhanced live signals data with dependency management
   */
  public useLiveSignalsData(): EnhancedDataServiceResponse<
    LiveSignalsDataRow[]
  > {
    const baseResponse = this.getBaseLiveSignalsData();
    return this.createEnhancedResponse(
      "live-signals-equity-curve",
      baseResponse,
    );
  }

  /**
   * Enhanced trade history data with dependency management
   */
  public useTradeHistoryData(): EnhancedDataServiceResponse<
    TradeHistoryDataRow[]
  > {
    const baseResponse = this.getBaseTradeHistoryData();
    return this.createEnhancedResponse("trade-pnl-waterfall", baseResponse);
  }

  /**
   * Enhanced open positions PnL data with dependency management
   */
  public useOpenPositionsPnLData(): EnhancedDataServiceResponse<
    OpenPositionPnLDataRow[]
  > {
    const baseResponse = this.getBaseOpenPositionsPnLData();
    return this.createEnhancedResponse(
      "open-positions-pnl-timeseries",
      baseResponse,
    );
  }

  /**
   * Enhanced closed positions PnL data with dependency management
   */
  public useClosedPositionsPnLData(): EnhancedDataServiceResponse<
    ClosedPositionPnLDataRow[]
  > {
    const baseResponse = this.getBaseClosedPositionsPnLData();
    return this.createEnhancedResponse(
      "closed-positions-pnl-timeseries",
      baseResponse,
    );
  }

  /**
   * Enhanced benchmark data with dependency management
   */
  public useLiveSignalsBenchmarkData(): EnhancedDataServiceResponse<
    LiveSignalsBenchmarkDataRow[]
  > {
    const baseResponse = this.getBaseLiveSignalsBenchmarkData();
    return this.createEnhancedResponse(
      "live-signals-benchmark-comparison",
      baseResponse,
    );
  }

  // Base data fetching methods (delegate to original service)
  // These simulate the current ChartDataService behavior

  private getBaseAppleStockData(): DataServiceResponse<StockDataRow[]> {
    // Simulate current service behavior
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  private getBasePortfolioData(chartType: ChartType): DataServiceResponse<{
    multiStrategy?: PortfolioDataRow[];
    buyHold?: PortfolioDataRow[];
    drawdowns?: PortfolioDataRow[];
  }> {
    return {
      data: {},
      loading: false,
      error: null,
    };
  }

  private getBaseLiveSignalsData(): DataServiceResponse<LiveSignalsDataRow[]> {
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  private getBaseTradeHistoryData(): DataServiceResponse<
    TradeHistoryDataRow[]
  > {
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  private getBaseOpenPositionsPnLData(): DataServiceResponse<
    OpenPositionPnLDataRow[]
  > {
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  private getBaseClosedPositionsPnLData(): DataServiceResponse<
    ClosedPositionPnLDataRow[]
  > {
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  private getBaseLiveSignalsBenchmarkData(): DataServiceResponse<
    LiveSignalsBenchmarkDataRow[]
  > {
    return {
      data: [],
      loading: false,
      error: null,
    };
  }

  /**
   * Manual refresh for specific chart types
   */
  public async refreshChartData(
    chartType: ChartType,
    options: {
      force?: boolean;
      priority?: "low" | "normal" | "high";
      onProgress?: (progress: any) => void;
    } = {},
  ): Promise<DataRefreshResult> {
    const request: DataRefreshRequest = {
      chartType,
      force: options.force,
      priority: options.priority || "normal",
      onProgress: options.onProgress,
    };

    const result = await dataDependencyManager.requestRefresh(request);

    // Notify subscribers if refresh was successful
    if (result.success) {
      this.notifyRefreshSubscribers(chartType);

      // Clear cache in original service to force reload
      chartDataService.clearCache();
    }

    return result;
  }

  /**
   * Get data status for all chart types
   */
  public getAllDataStatuses(): Map<ChartType, DataSourceStatus> {
    return dataDependencyManager.getAllDataStatuses();
  }

  /**
   * Get data status for a specific chart type
   */
  public getDataStatus(chartType: ChartType): DataSourceStatus {
    return dataDependencyManager.getDataStatus(chartType);
  }

  /**
   * Check if chart data can be refreshed
   */
  public canRefreshChart(chartType: ChartType): boolean {
    return dataDependencyManager.canRefreshChart(chartType);
  }

  /**
   * Get refresh capability information for a chart
   */
  public getRefreshCapability(
    chartType: ChartType,
  ): ChartRefreshCapability | undefined {
    return dataDependencyManager.getRefreshCapability(chartType);
  }

  /**
   * Get dependency information for a chart type
   */
  public getDependencyInfo(chartType: ChartType) {
    return dataDependencyManager.getDependencyInfo(chartType);
  }

  /**
   * Clear cache for all chart types
   */
  public clearAllCaches(): void {
    dataDependencyManager.clearAllCaches();
    chartDataService.clearCache();
  }

  /**
   * Clear cache for specific chart type
   */
  public clearCache(chartType: ChartType): void {
    dataDependencyManager.clearCache(chartType);
  }

  /**
   * Get cache status information
   */
  public getCacheStatus() {
    return chartDataService.getCacheStatus();
  }
}

// Export singleton instance
export const enhancedChartDataService = new EnhancedChartDataService();
export default enhancedChartDataService;
