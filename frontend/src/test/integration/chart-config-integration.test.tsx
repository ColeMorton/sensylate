/**
 * Integration test for chart configuration consolidation.
 * Verifies that React components can load and use the consolidated config.
 */

import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render } from "@testing-library/react";

// Import the consolidated config directly
import chartDependencyConfig from "@/config/chart-data-dependencies.json";

// Mock the PortfolioChart component imports
vi.mock("@/hooks/usePortfolioData", () => ({
  useStockData: vi.fn(() => ({
    data: [
      { date: "2024-01-01", close: "150.00" },
      { date: "2024-01-02", close: "152.00" },
    ],
    loading: false,
    error: null,
  })),
}));

vi.mock("@/utils/chartTheme", () => ({
  getChartColors: vi.fn(() => ({
    tertiary: "#4285F4",
    multiStrategy: "#00BCD4",
    buyHold: "#9575CD",
    drawdown: "#FF7043",
    neutral: "#90A4AE",
  })),
  getPlotlyThemeColors: vi.fn(() => ({
    paper_bgcolor: "white",
    plot_bgcolor: "white",
    font: { color: "black" },
    titleFont: { color: "black", size: 16 },
    gridColor: "#e0e0e0",
    tickColor: "#666",
    legendBgColor: "rgba(255,255,255,0.8)",
    legendBorderColor: "#ccc",
  })),
}));

vi.mock("./ChartRenderer", () => ({
  default: ({ data, _layout, _config, loading, error }: any) => (
    <div data-testid="chart-renderer">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      <div data-testid="chart-loading">{loading ? "loading" : "ready"}</div>
      <div data-testid="chart-error">{error ? error.message : "no-error"}</div>
    </div>
  ),
}));

// Import after mocking
import PortfolioChart from "@/layouts/components/charts/PortfolioChart";

describe("Chart Configuration Integration", () => {
  describe("Consolidated Configuration Structure", () => {
    it("should have the expected structure", () => {
      expect(chartDependencyConfig).toHaveProperty("symbolMetadata");
      expect(chartDependencyConfig).toHaveProperty("chartTypeMapping");
      expect(chartDependencyConfig).toHaveProperty("defaults");
      expect(chartDependencyConfig).toHaveProperty("dependencies");
    });

    it("should contain symbol metadata for AAPL and MSTR", () => {
      const { symbolMetadata } = chartDependencyConfig;

      expect(symbolMetadata).toHaveProperty("AAPL");
      expect(symbolMetadata).toHaveProperty("MSTR");

      expect(symbolMetadata.AAPL.displayName).toBe("Apple Price");
      expect(symbolMetadata.AAPL.chartType).toBe("apple-price");
      expect(symbolMetadata.AAPL.dataYears).toBe(15);

      expect(symbolMetadata.MSTR.displayName).toBe("Strategy Price");
      expect(symbolMetadata.MSTR.chartType).toBe("mstr-price");
      expect(symbolMetadata.MSTR.dataYears).toBe(6);
    });

    it("should have chart type mappings", () => {
      const { chartTypeMapping } = chartDependencyConfig;

      expect(chartTypeMapping["apple-price"]).toBe("AAPL");
      expect(chartTypeMapping["mstr-price"]).toBe("MSTR");
    });

    it("should have default configuration values", () => {
      const { defaults } = chartDependencyConfig;

      expect(defaults.yAxisLabel).toBe("Price ($)");
      expect(defaults.period).toBe("1y");
      expect(defaults.dataFormat).toBe("csv");
      expect(defaults.refreshInterval).toBe(86400000);
    });
  });

  describe("PortfolioChart Component Integration", () => {
    it("should render apple-price chart correctly", () => {
      const { getByTestId } = render(
        <PortfolioChart chartType="apple-price" title="Apple Stock Price" />,
      );

      expect(getByTestId("chart-renderer")).toBeInTheDocument();
      expect(getByTestId("chart-loading")).toHaveTextContent("ready");
      expect(getByTestId("chart-error")).toHaveTextContent("no-error");
    });

    it("should render mstr-price chart correctly", () => {
      const { getByTestId } = render(
        <PortfolioChart
          chartType="mstr-price"
          title="MicroStrategy Stock Price"
        />,
      );

      expect(getByTestId("chart-renderer")).toBeInTheDocument();
      expect(getByTestId("chart-loading")).toHaveTextContent("ready");
      expect(getByTestId("chart-error")).toHaveTextContent("no-error");
    });

    it("should handle non-stock chart types", () => {
      const { getByTestId } = render(
        <PortfolioChart
          chartType="portfolio-value-comparison"
          title="Portfolio Comparison"
        />,
      );

      expect(getByTestId("chart-renderer")).toBeInTheDocument();
      expect(getByTestId("chart-loading")).toHaveTextContent("ready");
      expect(getByTestId("chart-error")).toHaveTextContent("no-error");
    });
  });

  describe("Configuration Access Methods", () => {
    it("should provide helper functions for accessing symbol data", () => {
      // These are the helper functions from PortfolioChart.tsx
      const isDailyPriceChart = (chartType: string): boolean => {
        return chartType.endsWith("-price");
      };

      const getSymbolFromChartType = (chartType: string): string | null => {
        if (!isDailyPriceChart(chartType)) {
          return null;
        }
        const mapping = chartDependencyConfig.chartTypeMapping;
        return mapping[chartType as keyof typeof mapping] || null;
      };

      const getSymbolDisplayName = (chartType: string): string => {
        const symbol = getSymbolFromChartType(chartType);
        if (!symbol) {
          return "Chart";
        }
        const metadata =
          chartDependencyConfig.symbolMetadata[
            symbol as keyof typeof chartDependencyConfig.symbolMetadata
          ];
        return metadata?.displayName || `${symbol} Price`;
      };

      // Test the helper functions
      expect(isDailyPriceChart("apple-price")).toBe(true);
      expect(isDailyPriceChart("portfolio-value-comparison")).toBe(false);

      expect(getSymbolFromChartType("apple-price")).toBe("AAPL");
      expect(getSymbolFromChartType("mstr-price")).toBe("MSTR");
      expect(getSymbolFromChartType("portfolio-value-comparison")).toBe(null);

      expect(getSymbolDisplayName("apple-price")).toBe("Apple Price");
      expect(getSymbolDisplayName("mstr-price")).toBe("Strategy Price");
      expect(getSymbolDisplayName("portfolio-value-comparison")).toBe("Chart");
    });

    it("should maintain consistency between symbol metadata and dependencies", () => {
      const { symbolMetadata, dependencies, chartTypeMapping } =
        chartDependencyConfig;

      Object.keys(symbolMetadata).forEach((symbol) => {
        const symbolData =
          symbolMetadata[symbol as keyof typeof symbolMetadata];
        const chartType = symbolData.chartType;

        // Chart type should be in mapping
        expect(chartTypeMapping).toHaveProperty(chartType);
        expect(
          chartTypeMapping[chartType as keyof typeof chartTypeMapping],
        ).toBe(symbol);

        // Chart type should have a dependency
        expect(dependencies).toHaveProperty(chartType);
        expect(
          dependencies[chartType as keyof typeof dependencies].chartType,
        ).toBe(chartType);
      });
    });
  });

  describe("Backwards Compatibility", () => {
    it("should maintain all existing chart types in dependencies", () => {
      const { dependencies } = chartDependencyConfig;

      // Should still have the original chart types
      const expectedChartTypes = [
        "apple-price",
        "mstr-price",
        "portfolio-value-comparison",
        "returns-comparison",
        "portfolio-drawdowns",
        "live-signals-equity-curve",
        "live-signals-benchmark-comparison",
        "live-signals-drawdowns",
        "live-signals-weekly-candlestick",
        "trade-pnl-waterfall",
        "closed-positions-pnl-timeseries",
        "open-positions-pnl-timeseries",
      ];

      expectedChartTypes.forEach((chartType) => {
        expect(dependencies).toHaveProperty(chartType);
        expect(
          dependencies[chartType as keyof typeof dependencies].chartType,
        ).toBe(chartType);
      });
    });

    it("should maintain the original dependency structure", () => {
      const { dependencies } = chartDependencyConfig;
      const applePriceDep = dependencies["apple-price"];

      expect(applePriceDep).toHaveProperty("chartType");
      expect(applePriceDep).toHaveProperty("chartStatus");
      expect(applePriceDep).toHaveProperty("primarySource");
      expect(applePriceDep).toHaveProperty("freshness");
      expect(applePriceDep).toHaveProperty("refreshPolicy");

      expect(applePriceDep.primarySource).toHaveProperty("type");
      expect(applePriceDep.primarySource).toHaveProperty("location");
      expect(applePriceDep.primarySource).toHaveProperty("refreshMethod");
    });
  });
});
