import type {
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  TradeHistoryDataRow,
  OpenPositionPnLDataRow,
  PortfolioDataCache,
} from "@/types/ChartTypes";

class ChartDataService {
  private cache: Partial<PortfolioDataCache> = {};
  private liveSignalsCache: {
    data?: LiveSignalsDataRow[];
    lastFetched?: number;
  } = {};
  private tradeHistoryCache: {
    data?: TradeHistoryDataRow[];
    lastFetched?: number;
  } = {};
  private openPositionsPnLCache: {
    data?: OpenPositionPnLDataRow[];
    lastFetched?: number;
  } = {};
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  // CSV parsing utilities
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

  private parseOpenPositionsPnLCSV(csvText: string): OpenPositionPnLDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: Partial<OpenPositionPnLDataRow> = {};
      headers.forEach((header, index) => {
        row[header.trim() as keyof OpenPositionPnLDataRow] =
          values[index]?.trim() || "";
      });
      return row as OpenPositionPnLDataRow;
    });
  }

  // Cache management
  private isCacheValid(): boolean {
    return (
      this.cache.lastFetched !== undefined &&
      Date.now() - this.cache.lastFetched < this.CACHE_DURATION
    );
  }

  private setCacheTimestamp(): void {
    this.cache.lastFetched = Date.now();
  }

  private isLiveSignalsCacheValid(): boolean {
    return (
      this.liveSignalsCache.lastFetched !== undefined &&
      Date.now() - this.liveSignalsCache.lastFetched < this.CACHE_DURATION
    );
  }

  private isTradeHistoryCacheValid(): boolean {
    return (
      this.tradeHistoryCache.lastFetched !== undefined &&
      Date.now() - this.tradeHistoryCache.lastFetched < this.CACHE_DURATION
    );
  }

  private isOpenPositionsPnLCacheValid(): boolean {
    return (
      this.openPositionsPnLCache.lastFetched !== undefined &&
      Date.now() - this.openPositionsPnLCache.lastFetched < this.CACHE_DURATION
    );
  }

  // Data fetching methods
  async fetchAppleStockData(signal?: AbortSignal): Promise<StockDataRow[]> {
    try {
      const response = await fetch(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv",
        { signal }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      return this.parseCSV(csvText);
    } catch (error) {
      // Re-throw AbortError without wrapping to preserve abort handling
      if (error instanceof Error && error.name === 'AbortError') {
        throw error;
      }
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to fetch Apple stock data",
      );
    }
  }

  async fetchPortfolioData(signal?: AbortSignal): Promise<PortfolioDataCache> {
    // Return cached data if valid
    if (this.isCacheValid() && this.isPortfolioCacheComplete()) {
      return this.cache as PortfolioDataCache;
    }

    try {
      // Fetch all portfolio data files in parallel
      const [
        multiStrategyValueResponse,
        buyHoldValueResponse,
        multiStrategyCumulativeResponse,
        multiStrategyReturnsResponse,
        buyHoldReturnsResponse,
        multiStrategyDrawdownsResponse,
      ] = await Promise.all([
        fetch("/data/portfolio/multi_strategy_portfolio_portfolio_value.csv", { signal }),
        fetch("/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv", { signal }),
        fetch(
          "/data/portfolio/multi_strategy_portfolio_cumulative_returns.csv",
          { signal }
        ),
        fetch("/data/portfolio/multi_strategy_portfolio_returns.csv", { signal }),
        fetch("/data/portfolio/portfolio_buy_and_hold_returns.csv", { signal }),
        fetch("/data/portfolio/multi_strategy_portfolio_drawdowns.csv", { signal }),
      ]);

      // Check all responses
      const responses = [
        multiStrategyValueResponse,
        buyHoldValueResponse,
        multiStrategyCumulativeResponse,
        multiStrategyReturnsResponse,
        buyHoldReturnsResponse,
        multiStrategyDrawdownsResponse,
      ];

      if (responses.some((response) => !response.ok)) {
        throw new Error("Failed to load one or more portfolio data files");
      }

      // Parse all CSV data in parallel
      const [
        multiStrategyValueCsv,
        buyHoldValueCsv,
        multiStrategyCumulativeCsv,
        multiStrategyReturnsCsv,
        buyHoldReturnsCsv,
        multiStrategyDrawdownsCsv,
      ] = await Promise.all(responses.map((response) => response.text()));

      // Create cache object
      const portfolioCache: PortfolioDataCache = {
        multiStrategyValue: this.parsePortfolioCSV(multiStrategyValueCsv),
        buyHoldValue: this.parsePortfolioCSV(buyHoldValueCsv),
        multiStrategyCumulative: this.parsePortfolioCSV(
          multiStrategyCumulativeCsv,
        ),
        multiStrategyReturns: this.parsePortfolioCSV(multiStrategyReturnsCsv),
        buyHoldReturns: this.parsePortfolioCSV(buyHoldReturnsCsv),
        multiStrategyDrawdowns: this.parsePortfolioCSV(
          multiStrategyDrawdownsCsv,
        ),
        lastFetched: Date.now(),
      };

      // Update cache
      this.cache = portfolioCache;
      this.setCacheTimestamp();

      return portfolioCache;
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to load portfolio data",
      );
    }
  }

  async fetchLiveSignalsData(): Promise<LiveSignalsDataRow[]> {
    // Return cached data if valid
    if (this.liveSignalsCache.data && this.isLiveSignalsCacheValid()) {
      return this.liveSignalsCache.data;
    }

    try {
      const response = await fetch(
        "/data/portfolio/live-signals/live_signals_equity.csv",
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      const data = this.parseLiveSignalsCSV(csvText);

      // Update cache
      this.liveSignalsCache = {
        data,
        lastFetched: Date.now(),
      };

      return data;
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to load live signals data",
      );
    }
  }

  async fetchTradeHistoryData(): Promise<TradeHistoryDataRow[]> {
    // Return cached data if valid
    if (this.tradeHistoryCache.data && this.isTradeHistoryCacheValid()) {
      return this.tradeHistoryCache.data;
    }

    try {
      const response = await fetch("/data/trade-history/live_signals.csv");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      const data = this.parseTradeHistoryCSV(csvText);

      // Update cache
      this.tradeHistoryCache = {
        data,
        lastFetched: Date.now(),
      };

      return data;
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to load trade history data",
      );
    }
  }

  // Specific data getters
  async getMultiStrategyValue(): Promise<PortfolioDataRow[]> {
    if (this.cache.multiStrategyValue && this.isCacheValid()) {
      return this.cache.multiStrategyValue;
    }
    const data = await this.fetchPortfolioData();
    return data.multiStrategyValue;
  }

  async getBuyHoldValue(): Promise<PortfolioDataRow[]> {
    if (this.cache.buyHoldValue && this.isCacheValid()) {
      return this.cache.buyHoldValue;
    }
    const data = await this.fetchPortfolioData();
    return data.buyHoldValue;
  }

  async getMultiStrategyCumulative(): Promise<PortfolioDataRow[]> {
    if (this.cache.multiStrategyCumulative && this.isCacheValid()) {
      return this.cache.multiStrategyCumulative;
    }
    const data = await this.fetchPortfolioData();
    return data.multiStrategyCumulative;
  }

  async getBuyHoldReturns(): Promise<PortfolioDataRow[]> {
    if (this.cache.buyHoldReturns && this.isCacheValid()) {
      return this.cache.buyHoldReturns;
    }
    const data = await this.fetchPortfolioData();
    return data.buyHoldReturns;
  }

  async getMultiStrategyReturns(): Promise<PortfolioDataRow[]> {
    if (this.cache.multiStrategyReturns && this.isCacheValid()) {
      return this.cache.multiStrategyReturns;
    }
    const data = await this.fetchPortfolioData();
    return data.multiStrategyReturns;
  }

  async getMultiStrategyDrawdowns(): Promise<PortfolioDataRow[]> {
    if (this.cache.multiStrategyDrawdowns && this.isCacheValid()) {
      return this.cache.multiStrategyDrawdowns;
    }
    const data = await this.fetchPortfolioData();
    return data.multiStrategyDrawdowns;
  }

  async getLiveSignalsData(): Promise<LiveSignalsDataRow[]> {
    return await this.fetchLiveSignalsData();
  }

  async getClosedTrades(): Promise<TradeHistoryDataRow[]> {
    const allTrades = await this.fetchTradeHistoryData();

    // Filter for closed trades only and sort by PnL (highest to lowest)
    const closedTrades = allTrades.filter((trade) => trade.Status === "Closed");
    return closedTrades.sort((a, b) => parseFloat(b.PnL) - parseFloat(a.PnL));
  }

  async fetchOpenPositionsPnLData(): Promise<OpenPositionPnLDataRow[]> {
    // Return cached data if valid
    if (
      this.openPositionsPnLCache.data &&
      this.isOpenPositionsPnLCacheValid()
    ) {
      return this.openPositionsPnLCache.data;
    }

    try {
      const response = await fetch(
        "/data/open-positions/live_signals_open_positions_pnl.csv",
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      const data = this.parseOpenPositionsPnLCSV(csvText);

      // Update cache
      this.openPositionsPnLCache = {
        data,
        lastFetched: Date.now(),
      };

      return data;
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to load open positions PnL data",
      );
    }
  }

  async getOpenPositionsPnLData(): Promise<OpenPositionPnLDataRow[]> {
    return await this.fetchOpenPositionsPnLData();
  }

  // Utility methods
  private isPortfolioCacheComplete(): boolean {
    return !!(
      this.cache.multiStrategyValue &&
      this.cache.buyHoldValue &&
      this.cache.multiStrategyCumulative &&
      this.cache.multiStrategyReturns &&
      this.cache.buyHoldReturns &&
      this.cache.multiStrategyDrawdowns
    );
  }

  // Clear cache (useful for development or forced refresh)
  clearCache(): void {
    this.cache = {};
    this.liveSignalsCache = {};
    this.tradeHistoryCache = {};
    this.openPositionsPnLCache = {};
  }

  // Get cache status
  getCacheStatus(): {
    isValid: boolean;
    lastFetched?: number;
    hasData: boolean;
  } {
    return {
      isValid: this.isCacheValid(),
      lastFetched: this.cache.lastFetched,
      hasData: this.isPortfolioCacheComplete(),
    };
  }
}

// Export singleton instance
export const chartDataService = new ChartDataService();
export default chartDataService;
