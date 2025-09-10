/**
 * Multi-Stock Price Chart Configuration
 *
 * Colocated configuration for multi-stock price comparison charts.
 * Supports dynamic symbol comparison and peer analysis.
 */

import type { ChartConfig } from "../chart-config.schema";

export const multiStockPriceChartConfig: ChartConfig = {
  metadata: {
    title: "Multi-Stock Price Comparison",
    category: "Stock Analysis",
    description:
      "Multi-stock comparison chart supporting dynamic symbol selection for peer analysis, sector comparisons, and relative performance tracking.",
    chartType: "multi-stock-price",
  },
  dataRequirements: {
    dataSources: [], // Dynamic based on selected symbols
    cacheable: true,
    cacheDuration: 5 * 60 * 1000, // 5 minutes
  },
  displayOptions: {
    defaultTimeframe: "1y",
    supportsIndexed: true,
    supportsPositionType: false,
    supportsSamePercentageScale: true,
  },
  productionReady: true,
};

export default multiStockPriceChartConfig;