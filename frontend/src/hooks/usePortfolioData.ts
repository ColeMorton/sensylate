import { useState, useEffect, useCallback } from "react";
import type {
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  ChartType,
  DataServiceResponse,
} from "@/types/ChartTypes";
import { chartDataService } from "@/services/ChartDataService";

// Hook for Apple stock data
export function useAppleStockData(): DataServiceResponse<StockDataRow[]> {
  const [data, setData] = useState<StockDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const stockData = await chartDataService.fetchAppleStockData();
        setData(stockData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load Apple stock data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for portfolio data based on chart type
export function usePortfolioData(chartType: ChartType): DataServiceResponse<{
  multiStrategy?: PortfolioDataRow[];
  buyHold?: PortfolioDataRow[];
  drawdowns?: PortfolioDataRow[];
}> {
  const [data, setData] = useState<{
    multiStrategy?: PortfolioDataRow[];
    buyHold?: PortfolioDataRow[];
    drawdowns?: PortfolioDataRow[];
  }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDataForChartType = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      switch (chartType) {
        case "portfolio-value-comparison":
        case "normalized-performance": {
          const [multiStrategy, buyHold] = await Promise.all([
            chartDataService.getMultiStrategyValue(),
            chartDataService.getBuyHoldValue(),
          ]);
          setData({ multiStrategy, buyHold });
          break;
        }

        case "returns-comparison": {
          const [multiStrategy, buyHold] = await Promise.all([
            chartDataService.getMultiStrategyCumulative(),
            chartDataService.getBuyHoldReturns(),
          ]);
          setData({ multiStrategy, buyHold });
          break;
        }

        case "portfolio-drawdowns": {
          const drawdowns = await chartDataService.getMultiStrategyDrawdowns();
          setData({ drawdowns });
          break;
        }

        case "live-signals-equity-curve":
        case "live-signals-drawdowns":
        case "live-signals-performance-metrics":
        case "live-signals-weekly-candlestick": {
          // Live signals charts are handled by useLiveSignalsData hook
          setData({});
          break;
        }

        case "trade-pnl-waterfall": {
          // Trade history charts are handled by useTradeHistoryData hook
          setData({});
          break;
        }

        default:
          setData({});
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load portfolio data",
      );
    } finally {
      setLoading(false);
    }
  }, [chartType]);

  useEffect(() => {
    if (
      chartType !== "apple-stock" &&
      !chartType.startsWith("live-signals-") &&
      chartType !== "trade-pnl-waterfall"
    ) {
      fetchDataForChartType();
    } else {
      setLoading(false);
    }
  }, [chartType, fetchDataForChartType]);

  return { data, loading, error };
}

// Hook for preloading all portfolio data (useful for charts page)
export function usePreloadPortfolioData(): DataServiceResponse<boolean> {
  const [data, setData] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const preloadData = async () => {
      try {
        setLoading(true);
        setError(null);
        await chartDataService.fetchPortfolioData();
        setData(true);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to preload portfolio data",
        );
      } finally {
        setLoading(false);
      }
    };

    preloadData();
  }, []);

  return { data, loading, error };
}

// Hook for specific portfolio datasets
export function useMultiStrategyValue(): DataServiceResponse<
  PortfolioDataRow[]
> {
  const [data, setData] = useState<PortfolioDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getMultiStrategyValue();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load multi-strategy data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

export function useBuyHoldValue(): DataServiceResponse<PortfolioDataRow[]> {
  const [data, setData] = useState<PortfolioDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getBuyHoldValue();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load buy-hold data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for live signals data
export function useLiveSignalsData(): DataServiceResponse<
  LiveSignalsDataRow[]
> {
  const [data, setData] = useState<LiveSignalsDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getLiveSignalsData();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load live signals data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for trade history data
export function useTradeHistoryData(): DataServiceResponse<
  TradeHistoryDataRow[]
> {
  const [data, setData] = useState<TradeHistoryDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getClosedTrades();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load trade history data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Utility hook for data service status
export function useDataServiceStatus() {
  const [status, setStatus] = useState(chartDataService.getCacheStatus());

  const refreshStatus = useCallback(() => {
    setStatus(chartDataService.getCacheStatus());
  }, []);

  const clearCache = useCallback(() => {
    chartDataService.clearCache();
    refreshStatus();
  }, [refreshStatus]);

  return {
    ...status,
    refreshStatus,
    clearCache,
  };
}
