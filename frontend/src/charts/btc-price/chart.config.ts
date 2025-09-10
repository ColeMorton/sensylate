/**
 * Bitcoin Price Chart Configuration
 *
 * Colocated configuration for Bitcoin price chart.
 * This replaces hardcoded configuration in generate_dashboard_configs.py
 */

import type { ChartConfig } from "../chart-config.schema";

export const btcPriceChartConfig: ChartConfig = {
  metadata: {
    title: "Bitcoin Price - 1 Year History",
    category: "Bitcoin Analysis",
    description:
      "Interactive Bitcoin (BITCOIN) price chart showing the last 1 year of market data. Displays daily open, high, low, close prices with volume data for cycle intelligence analysis.",
    chartType: "btc-price",
  },
  dataRequirements: {
    dataSources: ["/data/raw/stocks/BTC-USD/daily.csv"],
    cacheable: true,
    cacheDuration: 5 * 60 * 1000, // 5 minutes
  },
  displayOptions: {
    defaultTimeframe: "daily",
    supportsIndexed: false,
    supportsPositionType: false,
    supportsSamePercentageScale: true,
  },
  productionReady: true,
};

export default btcPriceChartConfig;
