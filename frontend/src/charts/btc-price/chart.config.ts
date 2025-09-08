/**
 * Bitcoin Price Chart Configuration
 * 
 * Colocated configuration for BTC-USD price chart.
 * This replaces hardcoded configuration in generate_dashboard_configs.py
 */

import type { ChartConfig } from '../chart-config.schema';

export const btcPriceChartConfig: ChartConfig = {
  metadata: {
    title: "Bitcoin Price - 210 Day History",
    category: "Bitcoin Analysis", 
    description: "Interactive Bitcoin (BTC-USD) price chart showing the last 210 days of market data. Displays daily open, high, low, close prices with volume data for cycle intelligence analysis.",
    chartType: "btc-price"
  },
  dataRequirements: {
    dataSources: ["/data/raw/stocks/BTC-USD/daily.csv"],
    cacheable: true,
    cacheDuration: 5 * 60 * 1000 // 5 minutes
  },
  displayOptions: {
    defaultTimeframe: "daily",
    supportsIndexed: false,
    supportsPositionType: false,
    supportsSamePercentageScale: true
  },
  productionReady: true
};

export default btcPriceChartConfig;