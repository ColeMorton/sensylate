/**
 * Enhanced Portfolio Data Hooks
 *
 * React hooks that provide data dependency management, refresh capabilities,
 * and data status information for chart components.
 */

import { useState, useEffect, useCallback, useRef } from "react";
import type {
  ChartType,
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  ClosedPositionPnLDataRow,
  OpenPositionPnLDataRow,
  LiveSignalsBenchmarkDataRow,
} from "@/types/ChartTypes";

import type {
  DataSourceStatus,
  DataRefreshResult,
  ChartRefreshCapability,
} from "@/types/DataDependencyTypes";

import {
  enhancedChartDataService,
  type EnhancedDataServiceResponse,
} from "@/services/EnhancedChartDataService";

/**
 * Enhanced data service response with refresh capabilities
 */
export interface UseEnhancedDataResponse<T> {
  data: T;
  loading: boolean;
  error: string | null;
  dataStatus?: DataSourceStatus;
  refreshCapability?: ChartRefreshCapability;
  refresh?: () => Promise<DataRefreshResult>;
  canRefresh: boolean;
  isRefreshing: boolean;
  lastRefreshed?: number;
}

/**
 * Base hook for enhanced data with dependency management
 */
function useEnhancedData<T>(
  chartType: ChartType,
  dataFetcher: () => EnhancedDataServiceResponse<T>,
  dependencies: any[] = [],
): UseEnhancedDataResponse<T> {
  const [data, setData] = useState<T>({} as T);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dataStatus, setDataStatus] = useState<DataSourceStatus>();
  const [refreshCapability, setRefreshCapability] =
    useState<ChartRefreshCapability>();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState<number>();

  const refreshFunctionRef = useRef<
    (() => Promise<DataRefreshResult>) | undefined
  >(undefined);
  const unsubscribeRef = useRef<(() => void) | undefined>(undefined);

  // Enhanced refresh function with loading state management
  const refresh = useCallback(async (): Promise<DataRefreshResult> => {
    if (!refreshFunctionRef.current) {
      return {
        success: false,
        status: dataStatus || {
          status: "error",
          ageHours: 0,
          retryCount: 0,
          refreshing: false,
          error: "Refresh function not available",
        },
        duration: 0,
        error: {
          message: "Refresh function not available",
          code: "REFRESH_NOT_AVAILABLE",
          retryable: false,
        },
        source: {
          type: "manual",
          location: "unknown",
          refreshMethod: "never",
          frequency: "never",
        },
      };
    }

    setIsRefreshing(true);
    setError(null);

    try {
      const result = await refreshFunctionRef.current();

      if (result.success) {
        setLastRefreshed(Date.now());
        setDataStatus(result.status);

        // Trigger data reload
        const response = dataFetcher();
        setData(response.data);
        setError(response.error);
      } else {
        setError(result.error?.message || "Refresh failed");
        setDataStatus(result.status);
      }

      return result;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Unknown refresh error";
      setError(errorMessage);

      return {
        success: false,
        status: dataStatus || {
          status: "error",
          ageHours: 0,
          retryCount: 0,
          refreshing: false,
          error: errorMessage,
        },
        duration: 0,
        error: {
          message: errorMessage,
          code: "REFRESH_ERROR",
          retryable: true,
        },
        source: {
          type: "manual",
          location: "unknown",
          refreshMethod: "never",
          frequency: "never",
        },
      };
    } finally {
      setIsRefreshing(false);
    }
  }, [dataFetcher, dataStatus]);

  // Subscribe to refresh notifications
  useEffect(() => {
    const unsubscribe = enhancedChartDataService.subscribeToRefresh(
      chartType,
      () => {
        // Data was refreshed externally, reload
        const response = dataFetcher();
        setData(response.data);
        setError(response.error);
        setDataStatus(response.dataStatus);
        setRefreshCapability(response.refreshCapability);
        refreshFunctionRef.current = response.refresh;
        setLastRefreshed(Date.now());
      },
    );

    unsubscribeRef.current = unsubscribe;
    return unsubscribe;
  }, [chartType, dataFetcher]);

  // Initial data load and dependency updates
  useEffect(() => {
    setLoading(true);
    setError(null);

    try {
      const response = dataFetcher();
      setData(response.data);
      setLoading(response.loading);
      setError(response.error);
      setDataStatus(response.dataStatus);
      setRefreshCapability(response.refreshCapability);
      refreshFunctionRef.current = response.refresh;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
      setLoading(false);
    }
  }, [dataFetcher, ...dependencies]);

  return {
    data,
    loading,
    error,
    dataStatus,
    refreshCapability,
    refresh,
    canRefresh: Boolean(refreshCapability?.canRefresh),
    isRefreshing,
    lastRefreshed,
  };
}

/**
 * Enhanced Apple stock data hook with dependency management
 */
export function useEnhancedAppleStockData(): UseEnhancedDataResponse<
  StockDataRow[]
> {
  return useEnhancedData(
    "apple-price",
    () => enhancedChartDataService.useAppleStockData(),
    [],
  );
}

/**
 * Enhanced portfolio data hook with dependency management
 */
export function useEnhancedPortfolioData(
  chartType: ChartType,
): UseEnhancedDataResponse<{
  multiStrategy?: PortfolioDataRow[];
  buyHold?: PortfolioDataRow[];
  drawdowns?: PortfolioDataRow[];
}> {
  return useEnhancedData(
    chartType,
    () => enhancedChartDataService.usePortfolioData(chartType),
    [chartType],
  );
}

/**
 * Enhanced live signals data hook with dependency management
 */
export function useEnhancedLiveSignalsData(): UseEnhancedDataResponse<
  LiveSignalsDataRow[]
> {
  return useEnhancedData(
    "live-signals-equity-curve",
    () => enhancedChartDataService.useLiveSignalsData(),
    [],
  );
}

/**
 * Enhanced trade history data hook with dependency management
 */
export function useEnhancedTradeHistoryData(): UseEnhancedDataResponse<
  TradeHistoryDataRow[]
> {
  return useEnhancedData(
    "trade-pnl-waterfall",
    () => enhancedChartDataService.useTradeHistoryData(),
    [],
  );
}

/**
 * Enhanced open positions PnL data hook with dependency management
 */
export function useEnhancedOpenPositionsPnLData(): UseEnhancedDataResponse<
  OpenPositionPnLDataRow[]
> {
  return useEnhancedData(
    "open-positions-pnl-timeseries",
    () => enhancedChartDataService.useOpenPositionsPnLData(),
    [],
  );
}

/**
 * Enhanced closed positions PnL data hook with dependency management
 */
export function useEnhancedClosedPositionsPnLData(): UseEnhancedDataResponse<
  ClosedPositionPnLDataRow[]
> {
  return useEnhancedData(
    "closed-positions-pnl-timeseries",
    () => enhancedChartDataService.useClosedPositionsPnLData(),
    [],
  );
}

/**
 * Enhanced live signals benchmark data hook with dependency management
 */
export function useEnhancedLiveSignalsBenchmarkData(): UseEnhancedDataResponse<
  LiveSignalsBenchmarkDataRow[]
> {
  return useEnhancedData(
    "live-signals-benchmark-comparison",
    () => enhancedChartDataService.useLiveSignalsBenchmarkData(),
    [],
  );
}

/**
 * Hook for managing data status across multiple chart types
 */
export function useDataStatusManager() {
  const [allStatuses, setAllStatuses] = useState<
    Map<ChartType, DataSourceStatus>
  >(new Map());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const updateStatuses = () => {
      const statuses = enhancedChartDataService.getAllDataStatuses();
      setAllStatuses(new Map(statuses));
      setLoading(false);
    };

    // Initial load
    updateStatuses();

    // Update periodically
    const interval = setInterval(updateStatuses, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusSummary = useCallback(() => {
    const summary = {
      total: allStatuses.size,
      available: 0,
      stale: 0,
      missing: 0,
      error: 0,
    };

    allStatuses.forEach((status) => {
      summary[status.status]++;
    });

    return summary;
  }, [allStatuses]);

  const getStaleCharts = useCallback(() => {
    const staleCharts: ChartType[] = [];
    allStatuses.forEach((status, chartType) => {
      if (status.status === "stale" || status.status === "error") {
        staleCharts.push(chartType);
      }
    });
    return staleCharts;
  }, [allStatuses]);

  const refreshAll = useCallback(
    async (priority: "low" | "normal" | "high" = "normal") => {
      const refreshPromises: Promise<DataRefreshResult>[] = [];

      allStatuses.forEach((status, chartType) => {
        if (enhancedChartDataService.canRefreshChart(chartType)) {
          refreshPromises.push(
            enhancedChartDataService.refreshChartData(chartType, { priority }),
          );
        }
      });

      return Promise.allSettled(refreshPromises);
    },
    [allStatuses],
  );

  return {
    allStatuses,
    loading,
    getStatusSummary,
    getStaleCharts,
    refreshAll,
  };
}

/**
 * Hook for chart-specific data management
 */
export function useChartDataManager(chartType: ChartType) {
  const [dataStatus, setDataStatus] = useState<DataSourceStatus>();
  const [refreshCapability, setRefreshCapability] =
    useState<ChartRefreshCapability>();
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    const updateStatus = () => {
      setDataStatus(enhancedChartDataService.getDataStatus(chartType));
      setRefreshCapability(
        enhancedChartDataService.getRefreshCapability(chartType),
      );
    };

    updateStatus();

    // Subscribe to refresh notifications
    const unsubscribe = enhancedChartDataService.subscribeToRefresh(
      chartType,
      updateStatus,
    );

    return unsubscribe;
  }, [chartType]);

  const refresh = useCallback(
    async (options?: {
      force?: boolean;
      priority?: "low" | "normal" | "high";
    }) => {
      setIsRefreshing(true);

      try {
        const result = await enhancedChartDataService.refreshChartData(
          chartType,
          options,
        );
        setDataStatus(result.status);
        return result;
      } finally {
        setIsRefreshing(false);
      }
    },
    [chartType],
  );

  const getDependencyInfo = useCallback(() => {
    return enhancedChartDataService.getDependencyInfo(chartType);
  }, [chartType]);

  return {
    dataStatus,
    refreshCapability,
    isRefreshing,
    canRefresh: Boolean(refreshCapability?.canRefresh),
    refresh,
    getDependencyInfo,
  };
}
