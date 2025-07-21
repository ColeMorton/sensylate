import type {
  PortfolioDataRow,
  StockDataRow,
  PortfolioDataCache,
} from "@/types/ChartTypes";

class ChartDataService {
  private cache: Partial<PortfolioDataCache> = {};
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
      const row: PortfolioDataRow = {};
      headers.forEach((header, index) => {
        row[header.trim()] = values[index]?.trim() || "";
      });
      return row;
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

  // Data fetching methods
  async fetchAppleStockData(): Promise<StockDataRow[]> {
    try {
      const response = await fetch(
        "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv",
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const csvText = await response.text();
      return this.parseCSV(csvText);
    } catch (error) {
      throw new Error(
        error instanceof Error
          ? error.message
          : "Failed to fetch Apple stock data",
      );
    }
  }

  async fetchPortfolioData(): Promise<PortfolioDataCache> {
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
        buyHoldReturnsResponse,
        multiStrategyDrawdownsResponse,
      ] = await Promise.all([
        fetch("/data/portfolio/multi_strategy_portfolio_portfolio_value.csv"),
        fetch("/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv"),
        fetch(
          "/data/portfolio/multi_strategy_portfolio_cumulative_returns.csv",
        ),
        fetch("/data/portfolio/portfolio_buy_and_hold_returns.csv"),
        fetch("/data/portfolio/multi_strategy_portfolio_drawdowns.csv"),
      ]);

      // Check all responses
      const responses = [
        multiStrategyValueResponse,
        buyHoldValueResponse,
        multiStrategyCumulativeResponse,
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

  async getMultiStrategyDrawdowns(): Promise<PortfolioDataRow[]> {
    if (this.cache.multiStrategyDrawdowns && this.isCacheValid()) {
      return this.cache.multiStrategyDrawdowns;
    }
    const data = await this.fetchPortfolioData();
    return data.multiStrategyDrawdowns;
  }

  // Utility methods
  private isPortfolioCacheComplete(): boolean {
    return !!(
      this.cache.multiStrategyValue &&
      this.cache.buyHoldValue &&
      this.cache.multiStrategyCumulative &&
      this.cache.buyHoldReturns &&
      this.cache.multiStrategyDrawdowns
    );
  }

  // Clear cache (useful for development or forced refresh)
  clearCache(): void {
    this.cache = {};
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
