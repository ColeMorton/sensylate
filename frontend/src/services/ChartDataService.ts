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
        { signal },
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      return this.parseCSV(csvText);
    } catch (error) {
      // Re-throw AbortError without wrapping to preserve abort handling
      if (error instanceof Error && error.name === "AbortError") {
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
        fetch("/data/portfolio/multi_strategy_portfolio_portfolio_value.csv", {
          signal,
        }),
        fetch("/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv", {
          signal,
        }),
        fetch(
          "/data/portfolio/multi_strategy_portfolio_cumulative_returns.csv",
          { signal },
        ),
        fetch("/data/portfolio/multi_strategy_portfolio_returns.csv", {
          signal,
        }),
        fetch("/data/portfolio/portfolio_buy_and_hold_returns.csv", { signal }),
        fetch("/data/portfolio/multi_strategy_portfolio_drawdowns.csv", {
          signal,
        }),
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

  // Data validation methods
  private validateCSVData(data: any[], dataType: string): {
    isValid: boolean;
    issues: string[];
    recordCount: number;
  } {
    const issues = [];
    
    if (!Array.isArray(data)) {
      issues.push(`${dataType} data is not an array`);
      return { isValid: false, issues, recordCount: 0 };
    }
    
    if (data.length === 0) {
      issues.push(`${dataType} data is empty`);
      return { isValid: false, issues, recordCount: 0 };
    }
    
    // Validate data structure based on type
    if (dataType === "live_signals") {
      const requiredFields = ["timestamp", "equity", "drawdown", "mfe", "mae"];
      const sampleRecord = data[0];
      
      for (const field of requiredFields) {
        if (!(field in sampleRecord)) {
          issues.push(`Missing required field: ${field}`);
        }
      }
      
      // Check for reasonable data ranges
      const equityValues = data.map(d => parseFloat(d.equity)).filter(v => !isNaN(v));
      if (equityValues.length === 0) {
        issues.push("No valid equity values found");
      }
    }
    
    if (dataType === "portfolio") {
      const requiredFields = ["Date"];
      const sampleRecord = data[0];
      
      for (const field of requiredFields) {
        if (!(field in sampleRecord)) {
          issues.push(`Missing required field: ${field}`);
        }
      }
    }
    
    if (dataType === "trade_history") {
      const requiredFields = ["Ticker", "PnL", "Status"];
      const sampleRecord = data[0];
      
      for (const field of requiredFields) {
        if (!(field in sampleRecord)) {
          issues.push(`Missing required field: ${field}`);
        }
      }
    }
    
    return {
      isValid: issues.length === 0,
      issues,
      recordCount: data.length
    };
  }

  private async checkDataFreshness(endpoint: string): Promise<{
    isFresh: boolean;
    ageHours: number;
    lastModified?: string;
  }> {
    try {
      const response = await fetch(endpoint, { method: 'HEAD' });
      
      if (!response.ok) {
        return { isFresh: false, ageHours: Infinity };
      }
      
      const lastModified = response.headers.get('last-modified');
      if (lastModified) {
        const modifiedDate = new Date(lastModified);
        const ageMs = Date.now() - modifiedDate.getTime();
        const ageHours = ageMs / (1000 * 60 * 60);
        
        return {
          isFresh: ageHours <= 24, // Consider fresh if less than 24 hours old
          ageHours,
          lastModified
        };
      }
      
      return { isFresh: true, ageHours: 0 }; // Assume fresh if no timestamp
    } catch {
      return { isFresh: false, ageHours: Infinity };
    }
  }

  // Enhanced data fetching with validation
  async fetchLiveSignalsDataWithValidation(): Promise<{
    data: LiveSignalsDataRow[];
    validation: {
      isValid: boolean;
      issues: string[];
      recordCount: number;
    };
    freshness: {
      isFresh: boolean;
      ageHours: number;
      lastModified?: string;
    };
  }> {
    try {
      // Check data freshness first
      const freshness = await this.checkDataFreshness(
        "/data/portfolio/live-signals/live_signals_equity.csv"
      );
      
      // Fetch the data
      const data = await this.fetchLiveSignalsData();
      
      // Validate the data
      const validation = this.validateCSVData(data, "live_signals");
      
      return { data, validation, freshness };
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to fetch and validate live signals data"
      );
    }
  }

  async fetchTradeHistoryDataWithValidation(): Promise<{
    data: TradeHistoryDataRow[];
    validation: {
      isValid: boolean;
      issues: string[];
      recordCount: number;
    };
    freshness: {
      isFresh: boolean;
      ageHours: number;
      lastModified?: string;
    };
  }> {
    try {
      // Check data freshness first
      const freshness = await this.checkDataFreshness(
        "/data/trade-history/live_signals.csv"
      );
      
      // Fetch the data
      const data = await this.fetchTradeHistoryData();
      
      // Validate the data
      const validation = this.validateCSVData(data, "trade_history");
      
      return { data, validation, freshness };
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to fetch and validate trade history data"
      );
    }
  }

  async getDataQualityReport(): Promise<{
    overall: "healthy" | "warning" | "error";
    categories: {
      [key: string]: {
        status: "healthy" | "warning" | "error";
        recordCount: number;
        issues: string[];
        freshness: {
          isFresh: boolean;
          ageHours: number;
        };
      };
    };
    generatedAt: string;
  }> {
    const categories: any = {};
    let overallStatus: "healthy" | "warning" | "error" = "healthy";
    
    // Check live signals data
    try {
      const liveSignalsResult = await this.fetchLiveSignalsDataWithValidation();
      categories.live_signals = {
        status: liveSignalsResult.validation.isValid ? 
          (liveSignalsResult.freshness.isFresh ? "healthy" : "warning") : "error",
        recordCount: liveSignalsResult.validation.recordCount,
        issues: liveSignalsResult.validation.issues,
        freshness: {
          isFresh: liveSignalsResult.freshness.isFresh,
          ageHours: liveSignalsResult.freshness.ageHours
        }
      };
      
      if (categories.live_signals.status === "error") {
        overallStatus = "error";
      } else if (categories.live_signals.status === "warning" && overallStatus === "healthy") {
        overallStatus = "warning";
      }
    } catch (error) {
      categories.live_signals = {
        status: "error",
        recordCount: 0,
        issues: [`Failed to fetch: ${error}`],
        freshness: { isFresh: false, ageHours: Infinity }
      };
      overallStatus = "error";
    }
    
    // Check trade history data
    try {
      const tradeHistoryResult = await this.fetchTradeHistoryDataWithValidation();
      categories.trade_history = {
        status: tradeHistoryResult.validation.isValid ? 
          (tradeHistoryResult.freshness.isFresh ? "healthy" : "warning") : "error",
        recordCount: tradeHistoryResult.validation.recordCount,
        issues: tradeHistoryResult.validation.issues,
        freshness: {
          isFresh: tradeHistoryResult.freshness.isFresh,
          ageHours: tradeHistoryResult.freshness.ageHours
        }
      };
      
      if (categories.trade_history.status === "error") {
        overallStatus = "error";
      } else if (categories.trade_history.status === "warning" && overallStatus === "healthy") {
        overallStatus = "warning";
      }
    } catch (error) {
      categories.trade_history = {
        status: "error",
        recordCount: 0,
        issues: [`Failed to fetch: ${error}`],
        freshness: { isFresh: false, ageHours: Infinity }
      };
      overallStatus = "error";
    }
    
    // Check portfolio data
    try {
      const portfolioData = await this.fetchPortfolioData();
      const hasAllData = this.isPortfolioCacheComplete();
      
      categories.portfolio = {
        status: hasAllData ? "healthy" : "warning",
        recordCount: portfolioData.multiStrategyValue?.length || 0,
        issues: hasAllData ? [] : ["Some portfolio data files missing"],
        freshness: { isFresh: true, ageHours: 0 } // Portfolio data freshness check would need file-specific logic
      };
      
      if (categories.portfolio.status === "warning" && overallStatus === "healthy") {
        overallStatus = "warning";
      }
    } catch (error) {
      categories.portfolio = {
        status: "error",
        recordCount: 0,
        issues: [`Failed to fetch: ${error}`],
        freshness: { isFresh: false, ageHours: Infinity }
      };
      overallStatus = "error";
    }
    
    return {
      overall: overallStatus,
      categories,
      generatedAt: new Date().toISOString()
    };
  }

  // Clear cache (useful for development or forced refresh)
  clearCache(): void {
    this.cache = {};
    this.liveSignalsCache = {};
    this.tradeHistoryCache = {};
    this.openPositionsPnLCache = {};
  }

  // Enhanced cache status with data quality info
  getCacheStatus(): {
    isValid: boolean;
    lastFetched?: number;
    hasData: boolean;
    dataQuality?: "unknown" | "healthy" | "warning" | "error";
  } {
    return {
      isValid: this.isCacheValid(),
      lastFetched: this.cache.lastFetched,
      hasData: this.isPortfolioCacheComplete(),
      dataQuality: "unknown" // Would be set by validation methods
    };
  }
}

// Export singleton instance
export const chartDataService = new ChartDataService();
export default chartDataService;
