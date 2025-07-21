import React, { useMemo, useState, useEffect } from "react";
import type { Data, Layout } from "plotly.js";
import type {
  ChartType,
  PortfolioDataRow,
  StockDataRow,
} from "@/types/ChartTypes";
import { usePortfolioData, useAppleStockData } from "@/hooks/usePortfolioData";
import { getChartColors, getPlotlyThemeColors } from "@/utils/chartTheme";
import ChartRenderer from "./ChartRenderer";

interface PortfolioChartProps {
  chartType: ChartType;
  title?: string;
}

const PortfolioChart: React.FC<PortfolioChartProps> = ({
  chartType,
  title,
}) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Data hooks
  const portfolioData = usePortfolioData(chartType);
  const appleData = useAppleStockData();

  // Use appropriate data source based on chart type
  const { data, loading, error } =
    chartType === "apple-stock" ? appleData : portfolioData;

  // Dark mode detection
  useEffect(() => {
    const checkDarkMode = () => {
      if (typeof window !== "undefined") {
        const darkMode =
          document.documentElement.classList.contains("dark") ||
          window.matchMedia("(prefers-color-scheme: dark)").matches;
        setIsDarkMode(darkMode);
      }
    };

    checkDarkMode();

    const observer = new MutationObserver(checkDarkMode);
    if (typeof window !== "undefined") {
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", checkDarkMode);

    return () => {
      observer.disconnect();
      mediaQuery.removeEventListener("change", checkDarkMode);
    };
  }, []);

  // Data unpacking utilities
  const unpack = (rows: StockDataRow[], key: keyof StockDataRow): string[] => {
    return rows.map((row) => row[key]);
  };

  const unpackPortfolio = (
    rows: PortfolioDataRow[],
    key: keyof PortfolioDataRow,
  ): (string | number)[] => {
    return rows.map((row) => {
      const value = row[key];
      return value !== undefined ? value : "";
    });
  };

  // Chart data generation
  const chartData: Data[] = useMemo(() => {
    const colors = getChartColors(isDarkMode);

    if (loading || error) {
      return [];
    }

    switch (chartType) {
      case "apple-stock": {
        const stockRows = data as StockDataRow[];
        if (!stockRows || stockRows.length === 0) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpack(stockRows, "Date"),
            y: unpack(stockRows, "AAPL.High"),
            line: { color: colors.tertiary, width: 2 },
            name: "AAPL High",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpack(stockRows, "Date"),
            y: unpack(stockRows, "AAPL.Low"),
            line: { color: colors.neutral, width: 2 },
            name: "AAPL Low",
          },
        ];
      }

      case "portfolio-value-comparison": {
        const portfolioRows = data as {
          multiStrategy?: PortfolioDataRow[];
          buyHold?: PortfolioDataRow[];
        };
        if (!portfolioRows.multiStrategy || !portfolioRows.buyHold) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.multiStrategy, "Date"),
            y: unpackPortfolio(portfolioRows.multiStrategy, "Portfolio_Value"),
            line: { color: colors.multiStrategy, width: 2 },
            name: "Multi-Strategy Portfolio",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.buyHold, "Date"),
            y: unpackPortfolio(portfolioRows.buyHold, "Portfolio_Value"),
            line: { color: colors.buyHold, width: 2 },
            name: "Buy & Hold Portfolio",
          },
        ];
      }

      case "returns-comparison": {
        const portfolioRows = data as {
          multiStrategy?: PortfolioDataRow[];
          buyHold?: PortfolioDataRow[];
        };
        if (!portfolioRows.multiStrategy || !portfolioRows.buyHold) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.multiStrategy, "Date"),
            y: unpackPortfolio(
              portfolioRows.multiStrategy,
              "Cumulative_Returns_Pct",
            ),
            line: { color: colors.multiStrategy, width: 2 },
            name: "Multi-Strategy Returns (%)",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.buyHold, "Date"),
            y: unpackPortfolio(portfolioRows.buyHold, "Returns_Pct"),
            line: { color: colors.buyHold, width: 2 },
            name: "Buy & Hold Returns (%)",
          },
        ];
      }

      case "portfolio-drawdowns": {
        const portfolioRows = data as { drawdowns?: PortfolioDataRow[] };
        if (!portfolioRows.drawdowns) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.drawdowns, "Date"),
            y: unpackPortfolio(portfolioRows.drawdowns, "Drawdown_Pct"),
            line: { color: colors.drawdown, width: 2 },
            fill: "tozeroy",
            fillcolor: `rgba(255, 112, 67, 0.1)`,
            name: "Drawdown (%)",
          },
        ];
      }

      case "normalized-performance": {
        const portfolioRows = data as {
          multiStrategy?: PortfolioDataRow[];
          buyHold?: PortfolioDataRow[];
        };
        if (!portfolioRows.multiStrategy || !portfolioRows.buyHold) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.multiStrategy, "Date"),
            y: unpackPortfolio(portfolioRows.multiStrategy, "Normalized_Value"),
            line: { color: colors.multiStrategy, width: 2 },
            name: "Multi-Strategy (Normalized)",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(portfolioRows.buyHold, "Date"),
            y: unpackPortfolio(portfolioRows.buyHold, "Normalized_Value"),
            line: { color: colors.buyHold, width: 2 },
            name: "Buy & Hold (Normalized)",
          },
        ];
      }

      default:
        return [];
    }
  }, [chartType, data, isDarkMode, loading, error]);

  // Chart layout
  const layout: Partial<Layout> = useMemo(() => {
    const themeColors = getPlotlyThemeColors(isDarkMode);

    const getChartTitle = () => {
      if (title) {
        return title;
      }

      switch (chartType) {
        case "apple-stock":
          return "Apple Stock Price Range (Custom Range)";
        case "portfolio-value-comparison":
          return "Portfolio Value Comparison";
        case "returns-comparison":
          return "Cumulative Returns Comparison";
        case "portfolio-drawdowns":
          return "Portfolio Drawdown Analysis";
        case "normalized-performance":
          return "Normalized Performance Comparison";
        default:
          return "Chart";
      }
    };

    const getYAxisTitle = () => {
      switch (chartType) {
        case "apple-stock":
          return "Price ($)";
        case "portfolio-value-comparison":
          return "Portfolio Value ($)";
        case "returns-comparison":
          return "Returns (%)";
        case "portfolio-drawdowns":
          return "Drawdown (%)";
        case "normalized-performance":
          return "Normalized Value";
        default:
          return "Value";
      }
    };

    return {
      autosize: true,
      responsive: true,
      margin: { l: 50, r: 50, t: 50, b: 50 },
      paper_bgcolor: themeColors.paper_bgcolor,
      plot_bgcolor: themeColors.plot_bgcolor,
      font: themeColors.font,
      title: {
        text: getChartTitle(),
        font: themeColors.titleFont,
      },
      modebar: {
        orientation: "h",
      },
      showlegend: true,
      legend: {
        x: 0,
        xanchor: "left",
        y: 1,
        yanchor: "top",
        bgcolor: themeColors.legendBgColor,
        bordercolor: themeColors.legendBorderColor,
        borderwidth: 1,
        font: themeColors.font,
      },
      xaxis: {
        range:
          chartType === "apple-stock"
            ? ["2016-07-01", "2016-12-31"]
            : undefined,
        type: "date",
        title: {
          text: "Date",
          font: themeColors.font,
        },
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: themeColors.font,
      },
      yaxis: {
        autorange: true,
        range:
          chartType === "apple-stock"
            ? [86.8700008333, 138.870004167]
            : undefined,
        type: "linear",
        title: {
          text: getYAxisTitle(),
          font: themeColors.font,
        },
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: themeColors.font,
      },
      hovermode: "x unified",
    };
  }, [isDarkMode, chartType, title]);

  // Chart config
  const config = useMemo(
    () => ({
      responsive: true,
      displayModeBar: false,
      displaylogo: false,
      toImageButtonOptions: {
        format: "png",
        filename: `${chartType}-chart`,
        height: 500,
        width: 700,
        scale: 1,
      },
      autosizable: true,
    }),
    [chartType],
  );

  return (
    <ChartRenderer
      data={chartData}
      layout={layout}
      config={config}
      loading={loading}
      error={error}
    />
  );
};

export default PortfolioChart;
