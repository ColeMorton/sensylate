/**
 * Multi-Stock Price Chart Data Requirements
 *
 * Colocated data requirements for multi-stock price comparison charts.
 * Supports dynamic symbol configuration and peer analysis.
 */

import type { 
  DataRequirements, 
  ExtendedChartDataRequirements,
  MultiSymbolConfig,
  DefaultDataRequirements 
} from "../data-requirements.schema";

/**
 * Default multi-symbol configuration for XPEV vs NIO comparison
 */
export const xpevNioMultiSymbolConfig: MultiSymbolConfig = {
  symbols: ["XPEV", "NIO"],
  displayName: "XPEV vs NIO Comparison",
  description: "Chinese EV stocks price comparison over 1 year",
  comparisonType: "peer_analysis",
  samePercentageScale: true,
};

/**
 * Pipeline data requirements for multi-stock price chart
 */
export const multiStockPriceDataRequirements: DataRequirements = {
  chartType: "multi-stock-price",
  chartStatus: "active",
  category: "raw",
  requiredServices: ["yahoo_finance"],
  
  primarySource: {
    type: "cli-api",
    location: "dynamic", // Location determined by selected symbols
    refreshMethod: "api-poll",
    frequency: "daily",
    cliService: "yahoo_finance",
    metadata: {
      description: "Multi-stock comparison data from Yahoo Finance API",
      format: "csv",
      lastUpdatedBy: "yahoo-finance-api",
    },
  },
  
  freshness: {
    ...DefaultDataRequirements.stockPrice.freshness,
  },
  
  refreshPolicy: {
    ...DefaultDataRequirements.stockPrice.refreshPolicy,
    refreshInterval: 24 * 60 * 60 * 1000, // 24 hours
  },
  
  multiSymbolConfig: xpevNioMultiSymbolConfig,
  
  serviceConfigs: [
    {
      name: "yahoo_finance",
      command: "history",
      args: [], // Args populated dynamically based on symbols
      options: {
        period: "1y",
        symbols: "dynamic", // Replaced at runtime
      },
      timeout: 120, // Longer timeout for multiple symbols
    },
  ],
  
  pipelineSettings: {
    enableFileWatching: true,
    maxConcurrency: 3, // Can fetch multiple symbols concurrently
    customProcessor: "multi_stock_processor.py",
  },
};

/**
 * Combined data requirements for multi-stock-price chart
 */
export const multiStockPriceExtendedDataRequirements: ExtendedChartDataRequirements = {
  basic: {
    dataSources: [], // Dynamic based on selected symbols
    cacheable: true,
    cacheDuration: 5 * 60 * 1000, // 5 minutes
  },
  pipeline: multiStockPriceDataRequirements,
};

/**
 * Data mapping for pipeline discovery
 */
export const multiStockPriceDataMapping = {
  "multi-stock-price": {
    data_source: "dynamic",
    category: "raw",
    services: ["yahoo_finance"],
    symbols: "dynamic",
    samePercentageScale: true,
  },
};

/**
 * Predefined symbol configurations
 */
export const PredefinedSymbolConfigs = {
  "xpev-nio": {
    symbols: ["XPEV", "NIO"],
    displayName: "Chinese EV Comparison",
    dataSources: ["raw/stocks/XPEV/daily.csv", "raw/stocks/NIO/daily.csv"],
  },
  "faang": {
    symbols: ["META", "AMZN", "AAPL", "NFLX", "GOOGL"],
    displayName: "FAANG Stocks",
    dataSources: [
      "raw/stocks/META/daily.csv",
      "raw/stocks/AMZN/daily.csv", 
      "raw/stocks/AAPL/daily.csv",
      "raw/stocks/NFLX/daily.csv",
      "raw/stocks/GOOGL/daily.csv",
    ],
  },
} as const;

export default multiStockPriceDataRequirements;