/**
 * Unified Chart Data Hook
 *
 * Modern hook that uses the UnifiedChartDataService with chart registry integration.
 * Replaces chart-specific hooks with a single, type-safe hook.
 */

import { useState, useEffect, useCallback } from "react";
import { unifiedChartDataService } from "@/services/UnifiedChartDataService";
import type {
  ChartType,
  DataServiceResponse,
} from "@/types/ChartTypes";

interface UseChartDataOptions {
  /** Enable enhanced features (data status, refresh capability) */
  enhanced?: boolean;
  /** Custom cache duration in milliseconds */
  cacheDuration?: number;
  /** Additional parameters for data fetching */
  params?: unknown;
}

/**
 * Generic chart data hook that works with any chart type
 */
export function useUnifiedChartData<T = unknown>(
  chartType: ChartType,
  options: UseChartDataOptions = {},
): DataServiceResponse<T> & {
  refresh?: () => Promise<void>;
  dataStatus?: unknown;
} {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dataStatus, setDataStatus] = useState<unknown>(null);

  const { enhanced = false, cacheDuration, params } = options;

  const fetchData = useCallback(
    async (signal?: AbortSignal) => {
      try {
        setLoading(true);
        setError(null);

        let result: T[];
        if (enhanced) {
          const response =
            await unifiedChartDataService.fetchEnhancedChartData<T>(
              chartType,
              signal,
              params,
            );
          result = response.data;
          setDataStatus(response.dataStatus);
        } else if (cacheDuration) {
          result = await unifiedChartDataService.fetchCachedChartData<T>(
            chartType,
            signal,
            params,
            cacheDuration,
          );
        } else {
          result = await unifiedChartDataService.fetchChartData<T>(
            chartType,
            signal,
            params,
          );
        }

        setData(result);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err.message);
        }
      } finally {
        if (signal && !signal.aborted) {
          setLoading(false);
        }
      }
    },
    [chartType, enhanced, cacheDuration, params],
  );

  useEffect(() => {
    const abortController = new AbortController();
    fetchData(abortController.signal);

    return () => {
      abortController.abort();
    };
  }, [fetchData]);

  // Manual refresh function
  const refresh = useCallback(async () => {
    await fetchData();
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    ...(enhanced && { dataStatus }),
    refresh,
  };
}

/**
 * Chart-specific hooks for backward compatibility
 */
export function useBTCPriceData(options?: UseChartDataOptions) {
  return useUnifiedChartData("btc-price", options);
}

export function useAppleStockData(options?: UseChartDataOptions) {
  return useUnifiedChartData("apple-price", options);
}

export function useMSTRStockData(options?: UseChartDataOptions) {
  return useUnifiedChartData("mstr-price", options);
}

export function usePortfolioData(options?: UseChartDataOptions) {
  return useUnifiedChartData("portfolio-value-comparison", options);
}

export function useLiveSignalsData(options?: UseChartDataOptions) {
  return useUnifiedChartData("live-signals-equity-curve", options);
}

export function useTradeHistoryData(options?: UseChartDataOptions) {
  return useUnifiedChartData("trade-pnl-waterfall", options);
}

/**
 * Enhanced versions with dependency management
 */
export function useEnhancedBTCPriceData() {
  return useUnifiedChartData("btc-price", { enhanced: true });
}

export function useEnhancedPortfolioData() {
  return useUnifiedChartData("portfolio-value-comparison", { enhanced: true });
}
