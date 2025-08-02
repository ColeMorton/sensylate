import React, { useMemo, useState, useEffect, useCallback } from "react";
import type { Data, Layout } from "plotly.js";
import type {
  ChartType,
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  WeeklyOHLCDataRow,
  TradeHistoryDataRow,
  OpenPositionPnLDataRow,
} from "@/types/ChartTypes";
import {
  usePortfolioData,
  useAppleStockData,
  useLiveSignalsData,
  useTradeHistoryData,
  useOpenPositionsPnLData,
} from "@/hooks/usePortfolioData";
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
  const liveSignalsData = useLiveSignalsData();
  const tradeHistoryData = useTradeHistoryData();
  const openPositionsPnLData = useOpenPositionsPnLData();

  // Use appropriate data source based on chart type
  const { data, loading, error } =
    chartType === "apple-stock"
      ? appleData
      : chartType.startsWith("live-signals-")
        ? liveSignalsData
        : chartType === "trade-pnl-waterfall"
          ? tradeHistoryData
          : chartType === "open-positions-pnl-timeseries" ||
              chartType === "open-positions-pnl-timeseries-weekly"
            ? openPositionsPnLData
            : portfolioData;

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

  const unpackLiveSignals = (
    rows: LiveSignalsDataRow[],
    key: keyof LiveSignalsDataRow,
  ): (string | number)[] => {
    return rows.map((row) => {
      const value = row[key];
      return value !== undefined ? value : "";
    });
  };

  // Convert daily equity data to weekly OHLC for candlestick charts
  const convertToWeeklyOHLC = useCallback((
    rows: LiveSignalsDataRow[],
  ): WeeklyOHLCDataRow[] => {
    if (!rows || rows.length === 0) {
      return [];
    }

    const weeklyData: WeeklyOHLCDataRow[] = [];
    let currentWeek: LiveSignalsDataRow[] = [];
    let currentWeekStart: Date | null = null;

    for (const row of rows) {
      const date = new Date(row.timestamp);
      const equity = parseFloat(row.equity);

      // Skip invalid data
      if (isNaN(equity)) {
        continue;
      }

      // Start of week is Monday (getDay() returns 0 for Sunday, 1 for Monday, etc.)
      const monday = new Date(date);
      monday.setDate(date.getDate() - ((date.getDay() + 6) % 7));
      monday.setHours(0, 0, 0, 0);

      // If this is a new week, process the previous week
      if (currentWeekStart && monday.getTime() !== currentWeekStart.getTime()) {
        if (currentWeek.length > 0) {
          const weekOHLC = processWeekData(currentWeek, currentWeekStart);
          if (weekOHLC) {
            weeklyData.push(weekOHLC);
          }
        }
        currentWeek = [];
      }

      // Update current week
      currentWeekStart = monday;
      currentWeek.push(row);
    }

    // Process the final week
    if (currentWeek.length > 0 && currentWeekStart) {
      const weekOHLC = processWeekData(currentWeek, currentWeekStart);
      if (weekOHLC) {
        weeklyData.push(weekOHLC);
      }
    }

    return weeklyData;
  }, []);

  const processWeekData = (
    weekData: LiveSignalsDataRow[],
    weekStart: Date,
  ): WeeklyOHLCDataRow | null => {
    if (weekData.length === 0) {
      return null;
    }

    const equities = weekData
      .map((row) => parseFloat(row.equity))
      .filter((val) => !isNaN(val));

    if (equities.length === 0) {
      return null;
    }

    // Get the Friday of this week (or last available day)
    const friday = new Date(weekStart);
    friday.setDate(weekStart.getDate() + 4);

    return {
      date: friday.toISOString().split("T")[0], // YYYY-MM-DD format
      open: equities[0],
      high: Math.max(...equities),
      low: Math.min(...equities),
      close: equities[equities.length - 1],
    };
  };

  // Convert daily PnL data to weekly for open positions
  const convertOpenPositionsPnLToWeekly = useCallback((
    rows: OpenPositionPnLDataRow[],
  ): OpenPositionPnLDataRow[] => {
    if (!rows || rows.length === 0) {
      return [];
    }

    const weeklyData: OpenPositionPnLDataRow[] = [];
    const tickerWeeklyMap: {
      [ticker: string]: { [weekKey: string]: OpenPositionPnLDataRow[] };
    } = {};

    // Group data by ticker and week
    for (const row of rows) {
      const date = new Date(row.Date);
      const ticker = row.Ticker;

      // Skip invalid data
      if (isNaN(date.getTime())) {
        continue;
      }

      // Start of week is Monday (getDay() returns 0 for Sunday, 1 for Monday, etc.)
      const monday = new Date(date);
      monday.setDate(date.getDate() - ((date.getDay() + 6) % 7));
      monday.setHours(0, 0, 0, 0);

      // Create week key (YYYY-MM-DD format for Monday)
      const weekKey = monday.toISOString().split("T")[0];

      if (!tickerWeeklyMap[ticker]) {
        tickerWeeklyMap[ticker] = {};
      }

      if (!tickerWeeklyMap[ticker][weekKey]) {
        tickerWeeklyMap[ticker][weekKey] = [];
      }

      tickerWeeklyMap[ticker][weekKey].push(row);
    }

    // Process each ticker's weekly data
    Object.entries(tickerWeeklyMap).forEach(([_ticker, weeklyMap]) => {
      Object.entries(weeklyMap).forEach(([weekKey, weekData]) => {
        if (weekData.length > 0) {
          // Sort by date to get the last entry of the week
          const sortedWeekData = weekData.sort(
            (a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime(),
          );

          const lastEntry = sortedWeekData[sortedWeekData.length - 1];

          // Get the Friday of this week (or last available day)
          const monday = new Date(weekKey);
          const friday = new Date(monday);
          friday.setDate(monday.getDate() + 4);

          // Create weekly data point using the last PnL value of the week
          weeklyData.push({
            ...lastEntry,
            Date: friday.toISOString().split("T")[0], // Use Friday as the week ending date
          });
        }
      });
    });

    // Sort by date
    return weeklyData.sort(
      (a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime(),
    );
  }, []);

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
            y: unpackPortfolio(portfolioRows.multiStrategy, "Returns_Pct"),
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

      case "live-signals-equity-curve": {
        const liveSignalsRows = data as LiveSignalsDataRow[];
        if (!liveSignalsRows || liveSignalsRows.length === 0) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "equity"),
            line: { color: colors.tertiary, width: 2 },
            name: "Live Signals Equity",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "mfe"),
            line: { color: colors.multiStrategy, width: 2 },
            name: "MFE (Maximum Favorable Excursion)",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "mae"),
            line: { color: colors.buyHold, width: 2 },
            name: "MAE (Maximum Adverse Excursion)",
          },
        ];
      }

      case "live-signals-drawdowns": {
        const liveSignalsRows = data as LiveSignalsDataRow[];
        if (!liveSignalsRows || liveSignalsRows.length === 0) {
          return [];
        }

        return [
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "drawdown"),
            line: { color: colors.drawdown, width: 2 },
            fill: "tozeroy",
            fillcolor: `rgba(255, 112, 67, 0.1)`,
            name: "Drawdown ($)",
          },
        ];
      }

      case "live-signals-weekly-candlestick": {
        const liveSignalsRows = data as LiveSignalsDataRow[];
        if (!liveSignalsRows || liveSignalsRows.length === 0) {
          return [];
        }

        const weeklyOHLC = convertToWeeklyOHLC(liveSignalsRows);
        if (weeklyOHLC.length === 0) {
          return [];
        }

        return [
          {
            type: "candlestick",
            x: weeklyOHLC.map((row) => row.date),
            open: weeklyOHLC.map((row) => row.open),
            high: weeklyOHLC.map((row) => row.high),
            low: weeklyOHLC.map((row) => row.low),
            close: weeklyOHLC.map((row) => row.close),
            increasing: { line: { color: "#17BECF" } },
            decreasing: { line: { color: "#7F7F7F" } },
            name: "Weekly Equity",
          },
        ];
      }

      case "trade-pnl-waterfall": {
        const tradeHistoryRows = data as TradeHistoryDataRow[];
        if (!tradeHistoryRows || tradeHistoryRows.length === 0) {
          return [];
        }

        const pnlValues = tradeHistoryRows.map((trade) =>
          parseFloat(trade.PnL),
        );
        const tickers = tradeHistoryRows.map((trade) => trade.Ticker);

        const waterfallData = {
          type: "waterfall" as const,
          orientation: "v" as const,
          measure: tradeHistoryRows.map(() => "relative"),
          x: tickers,
          y: pnlValues,
          textposition: "outside" as const,
          text: pnlValues.map((pnl) =>
            pnl > 0 ? `+${pnl.toFixed(2)}` : `${pnl.toFixed(2)}`,
          ),
          increasing: { marker: { color: colors.multiStrategy } },
          decreasing: { marker: { color: colors.buyHold } },
          connector: {
            line: {
              color: colors.neutral,
              width: 0,
            },
          },
          name: "Trade PnL",
          hovertemplate: "<b>%{x}</b><br>PnL: $%{y}<br><extra></extra>",
        };

        return [waterfallData];
      }

      case "open-positions-pnl-timeseries": {
        const openPositionsPnLRows = data as OpenPositionPnLDataRow[];
        if (!openPositionsPnLRows || openPositionsPnLRows.length === 0) {
          return [];
        }

        // Group data by ticker to create separate time series for each position
        const positionMap: { [ticker: string]: OpenPositionPnLDataRow[] } = {};
        openPositionsPnLRows.forEach((row) => {
          if (!positionMap[row.Ticker]) {
            positionMap[row.Ticker] = [];
          }
          positionMap[row.Ticker].push(row);
        });

        // Create a line for each position using different colors
        const chartColors = [
          colors.multiStrategy, // #00BCD4 - Cyan
          colors.buyHold, // #9575CD - Purple
          colors.tertiary, // #4285F4 - Blue
          colors.drawdown, // #FF7043 - Orange
          colors.neutral, // #90A4AE - Gray
          "#FF6B6B", // Red
          "#4ECDC4", // Teal
          "#45B7D1", // Sky Blue
          "#96CEB4", // Mint Green
        ];

        const chartData: Data[] = [];
        let colorIndex = 0;

        Object.entries(positionMap).forEach(([ticker, rows]) => {
          // Sort rows by date
          const sortedRows = rows.sort(
            (a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime(),
          );

          const dates = sortedRows.map((row) => row.Date);
          const pnlValues = sortedRows.map((row) => parseFloat(row.PnL));

          chartData.push({
            type: "scatter",
            mode: "lines+markers",
            x: dates,
            y: pnlValues,
            name: ticker,
            line: {
              color: chartColors[colorIndex % chartColors.length],
              width: 2,
            },
            marker: {
              size: 4,
              color: chartColors[colorIndex % chartColors.length],
            },
            hovertemplate:
              "<b>%{fullData.name}</b><br>" +
              "Date: %{x}<br>" +
              "PnL: $%{y:.2f}<br>" +
              "<extra></extra>",
          });

          colorIndex++;
        });

        return chartData;
      }

      case "open-positions-pnl-timeseries-weekly": {
        const openPositionsPnLRows = data as OpenPositionPnLDataRow[];
        if (!openPositionsPnLRows || openPositionsPnLRows.length === 0) {
          return [];
        }

        // Convert to weekly data
        const weeklyPnLData =
          convertOpenPositionsPnLToWeekly(openPositionsPnLRows);
        if (weeklyPnLData.length === 0) {
          return [];
        }

        // Group weekly data by ticker to create separate time series for each position
        const positionMap: { [ticker: string]: OpenPositionPnLDataRow[] } = {};
        weeklyPnLData.forEach((row) => {
          if (!positionMap[row.Ticker]) {
            positionMap[row.Ticker] = [];
          }
          positionMap[row.Ticker].push(row);
        });

        // Create a line for each position using different colors
        const chartColors = [
          colors.multiStrategy, // #00BCD4 - Cyan
          colors.buyHold, // #9575CD - Purple
          colors.tertiary, // #4285F4 - Blue
          colors.drawdown, // #FF7043 - Orange
          colors.neutral, // #90A4AE - Gray
          "#FF6B6B", // Red
          "#4ECDC4", // Teal
          "#45B7D1", // Sky Blue
          "#96CEB4", // Mint Green
        ];

        const chartData: Data[] = [];
        let colorIndex = 0;

        Object.entries(positionMap).forEach(([ticker, rows]) => {
          // Sort rows by date
          const sortedRows = rows.sort(
            (a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime(),
          );

          const dates = sortedRows.map((row) => row.Date);
          const pnlValues = sortedRows.map((row) => parseFloat(row.PnL));

          chartData.push({
            type: "scatter",
            mode: "lines+markers",
            x: dates,
            y: pnlValues,
            name: ticker,
            line: {
              color: chartColors[colorIndex % chartColors.length],
              width: 2,
            },
            marker: {
              size: 6, // Slightly larger markers for weekly data
              color: chartColors[colorIndex % chartColors.length],
            },
            hovertemplate:
              "<b>%{fullData.name}</b><br>" +
              "Week Ending: %{x}<br>" +
              "PnL: $%{y:.2f}<br>" +
              "<extra></extra>",
          });

          colorIndex++;
        });

        return chartData;
      }

      default:
        return [];
    }
  }, [
    chartType,
    data,
    isDarkMode,
    loading,
    error,
    convertToWeeklyOHLC,
    convertOpenPositionsPnLToWeekly,
  ]);

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
          return "Daily Returns Comparison";
        case "portfolio-drawdowns":
          return "Portfolio Drawdown Analysis";
        case "live-signals-equity-curve":
          return "Live Signals Portfolio Equity Curve";
        case "live-signals-drawdowns":
          return "Live Signals Portfolio Drawdowns";
        case "live-signals-weekly-candlestick":
          return "Live Signals Weekly Candlestick Chart";
        case "trade-pnl-waterfall":
          return "Trade PnL Waterfall Chart";
        case "open-positions-pnl-timeseries":
          return "Open Positions Cumulative PnL Time Series";
        case "open-positions-pnl-timeseries-weekly":
          return "Open Positions Cumulative PnL Time Series (Weekly)";
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
        case "live-signals-equity-curve":
          return "Equity ($)";
        case "live-signals-drawdowns":
          return "Drawdown ($)";
        case "live-signals-weekly-candlestick":
          return "Equity ($)";
        case "trade-pnl-waterfall":
          return "PnL ($)";
        case "open-positions-pnl-timeseries":
          return "Cumulative PnL ($)";
        case "open-positions-pnl-timeseries-weekly":
          return "Cumulative PnL ($)";
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
            : chartType === "trade-pnl-waterfall"
              ? undefined
              : undefined,
        type: chartType === "trade-pnl-waterfall" ? "category" : "date",
        title: {
          text: chartType === "trade-pnl-waterfall" ? "Ticker" : "Date",
          font: themeColors.font,
        },
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: themeColors.font,
        rangeslider:
          chartType === "live-signals-weekly-candlestick" ||
          chartType === "trade-pnl-waterfall"
            ? { visible: false }
            : undefined,
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
      hovermode: chartType === "trade-pnl-waterfall" ? "closest" : "x unified",
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
