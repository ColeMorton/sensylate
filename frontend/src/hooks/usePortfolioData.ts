import { useState, useEffect, useCallback } from "react";
import type {
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  ClosedPositionPnLDataRow,
  OpenPositionPnLDataRow,
  BenchmarkDataRow,
  LiveSignalsBenchmarkDataRow,
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
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const stockData = await chartDataService.fetchAppleStockData(
          abortController.signal,
        );
        setData(stockData);
      } catch (err) {
        // Don't set error if request was aborted (component unmounting)
        if (err instanceof Error && err.name !== "AbortError") {
          // Apple stock data loading error
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load Apple stock data",
          );
        }
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    // Cleanup function to abort fetch requests
    return () => {
      abortController.abort();
    };
  }, []);

  return { data, loading, error };
}

// Hook for generic stock data based on symbol
export function useStockData(
  symbol: string,
): DataServiceResponse<StockDataRow[]> {
  const [data, setData] = useState<StockDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const stockData = await chartDataService.fetchStockData(
          symbol,
          abortController.signal,
        );
        setData(stockData);
      } catch (err) {
        // Don't set error if request was aborted (component unmounting)
        if (err instanceof Error && err.name !== "AbortError") {
          // Generic stock data loading error
          setError(
            err instanceof Error
              ? err.message
              : `Failed to load ${symbol} stock data`,
          );
        }
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false);
        }
      }
    };

    // Only fetch if symbol is provided
    if (symbol) {
      fetchData();
    } else {
      setLoading(false);
      setError("No symbol provided");
    }

    // Cleanup function to abort fetch requests
    return () => {
      abortController.abort();
    };
  }, [symbol]);

  return { data, loading, error };
}

// Hook for multi-stock data based on symbol array
export function useMultiStockData(
  symbols: string[],
): DataServiceResponse<{ [symbol: string]: StockDataRow[] }> {
  const [data, setData] = useState<{ [symbol: string]: StockDataRow[] }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch data for all symbols concurrently
        const stockDataPromises = symbols.map(async (symbol) => {
          const stockData = await chartDataService.fetchStockData(
            symbol,
            abortController.signal,
          );
          return { symbol, data: stockData };
        });

        const results = await Promise.all(stockDataPromises);

        // Convert array to object keyed by symbol
        const stockDataMap = results.reduce(
          (acc, { symbol, data }) => {
            acc[symbol] = data;
            return acc;
          },
          {} as { [symbol: string]: StockDataRow[] },
        );

        setData(stockDataMap);
      } catch (err) {
        // Don't set error if request was aborted (component unmounting)
        if (err instanceof Error && err.name !== "AbortError") {
          setError(
            err instanceof Error
              ? err.message
              : `Failed to load multi-stock data for ${symbols.join(", ")}`,
          );
        }
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false);
        }
      }
    };

    if (symbols.length > 0) {
      fetchData();
    } else {
      setLoading(false);
    }

    // Cleanup function to abort fetch requests
    return () => {
      abortController.abort();
    };
  }, [symbols]); // Dependencies on symbols array

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

  const fetchDataForChartType = useCallback(
    async (signal?: AbortSignal) => {
      try {
        setLoading(true);
        setError(null);

        switch (chartType) {
          case "portfolio-value-comparison": {
            const [multiStrategy, buyHold] = await Promise.all([
              chartDataService.getMultiStrategyValue(),
              chartDataService.getBuyHoldValue(),
            ]);
            if (signal?.aborted) {
              return;
            }
            setData({ multiStrategy, buyHold });
            break;
          }

          case "returns-comparison": {
            const [multiStrategy, buyHold] = await Promise.all([
              chartDataService.getMultiStrategyReturns(),
              chartDataService.getBuyHoldReturns(),
            ]);
            if (signal?.aborted) {
              return;
            }
            setData({ multiStrategy, buyHold });
            break;
          }

          case "portfolio-drawdowns": {
            const drawdowns =
              await chartDataService.getMultiStrategyDrawdowns();
            if (signal?.aborted) {
              return;
            }
            setData({ drawdowns });
            break;
          }

          case "live-signals-equity-curve":
          case "live-signals-benchmark-comparison":
          case "live-signals-drawdowns":
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

          case "closed-positions-pnl-timeseries": {
            // Closed positions PnL charts are handled by useTradeHistoryData hook
            setData({});
            break;
          }

          case "open-positions-pnl-timeseries": {
            // Open positions PnL charts are handled by useOpenPositionsPnLData hook
            setData({});
            break;
          }

          default:
            setData({});
        }
      } catch (err) {
        // Don't set error if request was aborted (component unmounting)
        if (err instanceof Error && err.name !== "AbortError") {
          // Portfolio data loading error
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load portfolio data",
          );
        }
      } finally {
        if (!signal?.aborted) {
          setLoading(false);
        }
      }
    },
    [chartType],
  );

  useEffect(() => {
    const abortController = new AbortController();

    if (
      !chartType.endsWith("-price") &&
      !chartType.includes("multi-stock") &&
      !chartType.endsWith("-stock-price") &&
      !chartType.startsWith("live-signals-") &&
      chartType !== "trade-pnl-waterfall" &&
      chartType !== "closed-positions-pnl-timeseries" &&
      chartType !== "open-positions-pnl-timeseries"
    ) {
      fetchDataForChartType(abortController.signal);
    } else {
      setLoading(false);
    }

    // Cleanup function to abort fetch requests
    return () => {
      abortController.abort();
    };
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

// Hook for open positions PnL data
export function useOpenPositionsPnLData(): DataServiceResponse<
  OpenPositionPnLDataRow[]
> {
  const [data, setData] = useState<OpenPositionPnLDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getOpenPositionsPnLData();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load open positions PnL data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for waterfall chart data (uses pre-sorted backend data)
export function useWaterfallTradeData(): DataServiceResponse<
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
        const result = await chartDataService.getWaterfallTradeData();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load waterfall trade data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for closed positions with real price history
export function useClosedPositionsPnLData(): DataServiceResponse<
  ClosedPositionPnLDataRow[]
> {
  const [data, setData] = useState<ClosedPositionPnLDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getClosedTradesWithPriceHistory();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load closed positions PnL data with price history",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}

// Hook for benchmark data (SPY, QQQ, BTC-USD)
export function useBenchmarkData(): DataServiceResponse<BenchmarkDataRow[]> {
  const [data, setData] = useState<BenchmarkDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getBenchmarkData();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load benchmark data",
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

// Hook for live signals benchmark comparison data
export function useLiveSignalsBenchmarkData(): DataServiceResponse<
  LiveSignalsBenchmarkDataRow[]
> {
  const [data, setData] = useState<LiveSignalsBenchmarkDataRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await chartDataService.getLiveSignalsBenchmarkData();
        setData(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load live signals benchmark comparison data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}
