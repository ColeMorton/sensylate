/**
 * Bitcoin Price Chart Data Requirements
 *
 * Colocated data requirements for Bitcoin price chart.
 * Integrates with DevContentOps data pipeline for automated data management.
 */

import type { 
  DataRequirements, 
  ExtendedChartDataRequirements,
  DefaultDataRequirements 
} from "../data-requirements.schema";

/**
 * Pipeline data requirements for BTC price chart
 */
export const btcPriceDataRequirements: DataRequirements = {
  chartType: "btc-price",
  chartStatus: "active",
  category: "raw",
  requiredServices: ["yahoo_finance"],
  
  primarySource: {
    type: "cli-api",
    location: "raw/stocks/BITCOIN/daily.csv",
    refreshMethod: "api-poll",
    frequency: "daily",
    cliService: "yahoo_finance",
    metadata: {
      description: "Bitcoin (BITCOIN) price data for cycle intelligence analysis",
      format: "csv",
      lastUpdatedBy: "yahoo-finance-api",
    },
  },
  
  freshness: {
    ...DefaultDataRequirements.cryptoPrice.freshness,
    warningThreshold: 6,
    errorThreshold: 24,
  },
  
  refreshPolicy: {
    ...DefaultDataRequirements.cryptoPrice.refreshPolicy,
    // Override for more frequent updates during active periods
    refreshInterval: 24 * 60 * 60 * 1000, // 24 hours
  },
  
  symbolMetadata: {
    symbol: "BTC-USD",
    displayName: "Bitcoin Price",
    name: "Bitcoin",
    sector: "Cryptocurrency",
    dataYears: 1, // 1 year of Bitcoin price data
  },
  
  serviceConfigs: [
    {
      name: "yahoo_finance",
      command: "history",
      args: ["BTC-USD", "--period", "1y"],
      timeout: 60,
    },
  ],
  
  pipelineSettings: {
    enableFileWatching: true,
    maxConcurrency: 1,
  },
};

/**
 * Combined data requirements for btc-price chart
 */
export const btcPriceExtendedDataRequirements: ExtendedChartDataRequirements = {
  basic: {
    dataSources: ["/data/raw/stocks/BITCOIN/daily.csv"],
    cacheable: true,
    cacheDuration: 5 * 60 * 1000, // 5 minutes (matches data-adapter.ts)
  },
  pipeline: btcPriceDataRequirements,
};

/**
 * Data mapping for pipeline discovery
 */
export const btcPriceDataMapping = {
  "btc-price": {
    data_source: "raw/stocks/BITCOIN/daily.csv",
    category: "raw",
    services: ["yahoo_finance"],
  },
};

export default btcPriceDataRequirements;