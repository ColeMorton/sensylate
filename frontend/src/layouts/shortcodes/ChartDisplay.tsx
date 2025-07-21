import React, { useState, useEffect, useMemo, lazy, Suspense } from "react";
import type { Data, Layout } from "plotly.js";

// Lazy load the plot component to avoid SSR issues
const Plot = lazy(() => {
  if (typeof window === "undefined") {
    // Return a mock component for SSR
    return Promise.resolve({
      default: () =>
        React.createElement("div", {
          className: "plotly-loading",
          children: "Loading chart...",
        }),
    });
  }

  return import("react-plotly.js/factory").then(async (factory) => {
    const Plotly = await import("plotly.js-basic-dist-min");
    return { default: factory.default(Plotly) };
  });
});

interface StockDataRow {
  Date: string;
  "AAPL.High": string;
  "AAPL.Low": string;
  [key: string]: string;
}

interface PortfolioDataRow {
  Date: string;
  Portfolio_Value?: string;
  Normalized_Value?: string;
  Cumulative_Returns?: string;
  Cumulative_Returns_Pct?: string;
  Drawdown?: string;
  Drawdown_Pct?: string;
  Peak_Value?: string;
  Current_Value?: string;
  Returns?: string;
  Returns_Pct?: string;
  [key: string]: string | undefined;
}

interface ChartDisplayProps {
  title: string;
  category?: string;
  description?: string;
  chartType?: string;
  className?: string;
}

const ChartDisplay: React.FC<ChartDisplayProps> = ({
  title,
  category,
  description,
  chartType = "apple-stock",
  className = "",
}) => {
  const [chartData, setChartData] = useState<Data[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Detect dark mode
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

    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    if (typeof window !== "undefined") {
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }

    // Listen for system theme changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", checkDarkMode);

    return () => {
      observer.disconnect();
      mediaQuery.removeEventListener("change", checkDarkMode);
    };
  }, []);

  // Helper function to parse CSV data
  const parseCSV = (csvText: string): StockDataRow[] => {
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
  };

  // Helper function to unpack data
  const unpack = (rows: StockDataRow[], key: keyof StockDataRow): string[] => {
    return rows.map((row) => row[key]);
  };

  // Helper function to unpack portfolio data
  const unpackPortfolio = (
    rows: PortfolioDataRow[],
    key: keyof PortfolioDataRow,
  ): (string | number)[] => {
    return rows.map((row) => {
      const value = row[key];
      return value !== undefined ? value : "";
    });
  };

  // Helper function to parse portfolio CSV
  const parsePortfolioCSV = (csvText: string): PortfolioDataRow[] => {
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
  };

  // Load chart data based on chart type
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        if (chartType === "apple-stock") {
          const response = await fetch(
            "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv",
          );

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const csvText = await response.text();
          const rows = parseCSV(csvText);

          const trace1: Data = {
            type: "scatter",
            mode: "lines",
            x: unpack(rows, "Date"),
            y: unpack(rows, "AAPL.High"),
            line: { color: "#17BECF" },
            name: "AAPL High",
          };

          const trace2: Data = {
            type: "scatter",
            mode: "lines",
            x: unpack(rows, "Date"),
            y: unpack(rows, "AAPL.Low"),
            line: { color: "#7F7F7F" },
            name: "AAPL Low",
          };

          setChartData([trace1, trace2]);
        } else if (chartType === "portfolio-value-comparison") {
          const [multiStrategyResponse, buyHoldResponse] = await Promise.all([
            fetch(
              "/data/portfolio/multi_strategy_portfolio_portfolio_value.csv",
            ),
            fetch("/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv"),
          ]);

          if (!multiStrategyResponse.ok || !buyHoldResponse.ok) {
            throw new Error("Failed to load portfolio data");
          }

          const [multiStrategyCsv, buyHoldCsv] = await Promise.all([
            multiStrategyResponse.text(),
            buyHoldResponse.text(),
          ]);

          const multiStrategyRows = parsePortfolioCSV(multiStrategyCsv);
          const buyHoldRows = parsePortfolioCSV(buyHoldCsv);

          const trace1: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(multiStrategyRows, "Date"),
            y: unpackPortfolio(multiStrategyRows, "Portfolio_Value"),
            line: { color: "#00BCD4", width: 2 },
            name: "Multi-Strategy Portfolio",
          };

          const trace2: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(buyHoldRows, "Date"),
            y: unpackPortfolio(buyHoldRows, "Portfolio_Value"),
            line: { color: "#9575CD", width: 2 },
            name: "Buy & Hold Portfolio",
          };

          setChartData([trace1, trace2]);
        } else if (chartType === "returns-comparison") {
          const [cumulativeReturnsResponse, buyHoldReturnsResponse] =
            await Promise.all([
              fetch(
                "/data/portfolio/multi_strategy_portfolio_cumulative_returns.csv",
              ),
              fetch("/data/portfolio/portfolio_buy_and_hold_returns.csv"),
            ]);

          if (!cumulativeReturnsResponse.ok || !buyHoldReturnsResponse.ok) {
            throw new Error("Failed to load returns data");
          }

          const [cumulativeReturnsCsv, buyHoldReturnsCsv] = await Promise.all([
            cumulativeReturnsResponse.text(),
            buyHoldReturnsResponse.text(),
          ]);

          const cumulativeReturnsRows = parsePortfolioCSV(cumulativeReturnsCsv);
          const buyHoldReturnsRows = parsePortfolioCSV(buyHoldReturnsCsv);

          const trace1: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(cumulativeReturnsRows, "Date"),
            y: unpackPortfolio(cumulativeReturnsRows, "Cumulative_Returns_Pct"),
            line: { color: "#00BCD4", width: 2 },
            name: "Multi-Strategy Returns (%)",
          };

          const trace2: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(buyHoldReturnsRows, "Date"),
            y: unpackPortfolio(buyHoldReturnsRows, "Returns_Pct"),
            line: { color: "#9575CD", width: 2 },
            name: "Buy & Hold Returns (%)",
          };

          setChartData([trace1, trace2]);
        } else if (chartType === "portfolio-drawdowns") {
          const response = await fetch(
            "/data/portfolio/multi_strategy_portfolio_drawdowns.csv",
          );

          if (!response.ok) {
            throw new Error("Failed to load drawdown data");
          }

          const csvText = await response.text();
          const rows = parsePortfolioCSV(csvText);

          const trace1: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(rows, "Date"),
            y: unpackPortfolio(rows, "Drawdown_Pct"),
            line: { color: "#FF7043", width: 2 },
            fill: "tozeroy",
            fillcolor: "rgba(255, 112, 67, 0.1)",
            name: "Drawdown (%)",
          };

          setChartData([trace1]);
        } else if (chartType === "normalized-performance") {
          const [multiStrategyResponse, buyHoldResponse] = await Promise.all([
            fetch(
              "/data/portfolio/multi_strategy_portfolio_portfolio_value.csv",
            ),
            fetch("/data/portfolio/portfolio_buy_and_hold_portfolio_value.csv"),
          ]);

          if (!multiStrategyResponse.ok || !buyHoldResponse.ok) {
            throw new Error("Failed to load normalized data");
          }

          const [multiStrategyCsv, buyHoldCsv] = await Promise.all([
            multiStrategyResponse.text(),
            buyHoldResponse.text(),
          ]);

          const multiStrategyRows = parsePortfolioCSV(multiStrategyCsv);
          const buyHoldRows = parsePortfolioCSV(buyHoldCsv);

          const trace1: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(multiStrategyRows, "Date"),
            y: unpackPortfolio(multiStrategyRows, "Normalized_Value"),
            line: { color: "#00BCD4", width: 2 },
            name: "Multi-Strategy (Normalized)",
          };

          const trace2: Data = {
            type: "scatter",
            mode: "lines",
            x: unpackPortfolio(buyHoldRows, "Date"),
            y: unpackPortfolio(buyHoldRows, "Normalized_Value"),
            line: { color: "#9575CD", width: 2 },
            name: "Buy & Hold (Normalized)",
          };

          setChartData([trace1, trace2]);
        } else {
          setLoading(false);
          return;
        }
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load chart data",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [chartType]);

  // Helper function to get chart title
  const getChartTitle = () => {
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
        return title;
    }
  };

  // Helper function to get Y-axis title
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

  // Layout configuration with dark mode support
  const layout: Partial<Layout> = useMemo(
    () => ({
      autosize: true,
      responsive: true,
      margin: { l: 50, r: 50, t: 50, b: 50 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: {
        family: '"Inter", ui-sans-serif, system-ui, -apple-system, sans-serif',
        size: 12,
        color: isDarkMode ? "#E5E7EB" : "#374151",
      },
      title: {
        text: getChartTitle(),
        font: { size: 16, color: isDarkMode ? "#E5E7EB" : "#374151" },
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
        bgcolor: isDarkMode
          ? "rgba(31, 41, 55, 0.8)"
          : "rgba(255, 255, 255, 0.8)",
        bordercolor: isDarkMode
          ? "rgba(156, 163, 175, 0.3)"
          : "rgba(0, 0, 0, 0.2)",
        borderwidth: 1,
        font: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
      },
      xaxis: {
        range:
          chartType === "apple-stock"
            ? ["2016-07-01", "2016-12-31"]
            : undefined,
        type: "date",
        title: {
          text: "Date",
          font: {
            color: isDarkMode ? "#E5E7EB" : "#374151",
          },
        },
        gridcolor: isDarkMode
          ? "rgba(156, 163, 175, 0.2)"
          : "rgba(0, 0, 0, 0.1)",
        tickcolor: isDarkMode ? "#9CA3AF" : "#6B7280",
        tickfont: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
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
          font: {
            color: isDarkMode ? "#E5E7EB" : "#374151",
          },
        },
        gridcolor: isDarkMode
          ? "rgba(156, 163, 175, 0.2)"
          : "rgba(0, 0, 0, 0.1)",
        tickcolor: isDarkMode ? "#9CA3AF" : "#6B7280",
        tickfont: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
      },
      hovermode: "x unified",
    }),
    [isDarkMode, chartType, title, getChartTitle, getYAxisTitle],
  );

  // Config for better user experience
  const config = useMemo(
    () => ({
      responsive: true,
      displayModeBar: false,
      displaylogo: false,
      toImageButtonOptions: {
        format: "png",
        filename: `${title.toLowerCase().replace(/\s+/g, "-")}-chart`,
        height: 500,
        width: 700,
        scale: 1,
      },
      autosizable: true,
    }),
    [title],
  );

  return (
    <div
      className={`bg-body dark:bg-darkmode-body rounded-lg p-6 shadow-sm transition-all duration-300 hover:shadow-lg ${className}`}
    >
      {category && (
        <div className="mb-4">
          <span className="text-text/80 text-xs font-medium tracking-wider uppercase dark:text-gray-400">
            {category}
          </span>
        </div>
      )}

      <h3 className="text-dark mb-3 text-xl font-semibold dark:text-white">
        {title}
      </h3>

      {description && (
        <p className="text-text mb-6 dark:text-gray-300">{description}</p>
      )}

      <div className="chart-container min-h-[400px] w-full">
        {loading ? (
          <div className="flex h-full min-h-[400px] items-center justify-center">
            <div className="text-center">
              <div className="border-primary mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-b-2"></div>
              <p className="text-text/60 dark:text-gray-500">
                Loading chart data...
              </p>
            </div>
          </div>
        ) : error ? (
          <div className="flex h-full min-h-[400px] items-center justify-center">
            <div className="text-center">
              <p className="mb-2 text-red-500">Error loading chart:</p>
              <p className="text-text/60 text-sm dark:text-gray-500">{error}</p>
            </div>
          </div>
        ) : [
            "apple-stock",
            "portfolio-value-comparison",
            "returns-comparison",
            "portfolio-drawdowns",
            "normalized-performance",
          ].includes(chartType) ? (
          <div className="h-full min-h-[400px] w-full">
            <Suspense
              fallback={
                <div className="flex h-full min-h-[400px] items-center justify-center">
                  <div className="text-center">
                    <div className="border-primary mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-b-2"></div>
                    <p className="text-text/60 dark:text-gray-500">
                      Loading chart...
                    </p>
                  </div>
                </div>
              }
            >
              <Plot
                data={chartData}
                layout={layout}
                config={config}
                useResizeHandler={true}
                style={{ width: "100%", height: "100%" }}
                className="plotly-chart"
              />
            </Suspense>
          </div>
        ) : (
          <div className="flex min-h-[400px] items-center justify-center rounded-lg bg-blue-100 p-8 text-center dark:bg-blue-900">
            <div>
              <p className="font-semibold text-blue-700 dark:text-blue-300">
                📊 Charts Foundation Ready
              </p>
              <p className="mt-2 text-sm text-blue-600 dark:text-blue-400">
                More visualizations coming soon
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartDisplay;
