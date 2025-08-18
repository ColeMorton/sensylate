import React, { useMemo, useState, useEffect, useCallback } from "react";
import type { Data, Layout } from "plotly.js";
import type {
  ChartType,
  PortfolioDataRow,
  StockDataRow,
  LiveSignalsDataRow,
  WeeklyOHLCDataRow,
  TradeHistoryDataRow,
  ClosedPositionPnLDataRow,
  OpenPositionPnLDataRow,
  LiveSignalsBenchmarkDataRow,
} from "@/types/ChartTypes";
import {
  usePortfolioData,
  useAppleStockData,
  useLiveSignalsData,
  // useTradeHistoryData,
  useWaterfallTradeData,
  useClosedPositionsPnLData,
  useOpenPositionsPnLData,
  useLiveSignalsBenchmarkData,
} from "@/hooks/usePortfolioData";
import { getChartColors, getPlotlyThemeColors } from "@/utils/chartTheme";
import ChartRenderer from "./ChartRenderer";

interface PortfolioChartProps {
  chartType: ChartType;
  title?: string;
  timeframe?: "daily" | "weekly";
  indexed?: boolean;
  positionType?: "open" | "closed" | "auto";
}

const PortfolioChart: React.FC<PortfolioChartProps> = ({
  chartType,
  title,
  timeframe = "daily",
  indexed = false,
  positionType = "auto",
}) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Data hooks
  const portfolioData = usePortfolioData(chartType);
  const appleData = useAppleStockData();
  const liveSignalsData = useLiveSignalsData();
  // const tradeHistoryData = useTradeHistoryData(); // Not currently used
  // Removed import for now
  const waterfallTradeData = useWaterfallTradeData();
  const closedPositionsPnLData = useClosedPositionsPnLData();
  const openPositionsPnLData = useOpenPositionsPnLData();
  const liveSignalsBenchmarkData = useLiveSignalsBenchmarkData();

  // Smart position data selection logic
  const isPositionChart = chartType === "open-positions-pnl-timeseries";
  const shouldUseClosedData =
    isPositionChart &&
    (positionType === "closed" ||
      (positionType === "auto" &&
        (!openPositionsPnLData.data ||
          openPositionsPnLData.data.length === 0)));
  const actualDataType = isPositionChart
    ? shouldUseClosedData
      ? "closed"
      : "open"
    : null;

  // Use appropriate data source based on chart type
  const { data, loading, error } =
    chartType === "apple-stock"
      ? appleData
      : chartType === "live-signals-benchmark-comparison"
        ? liveSignalsBenchmarkData
        : chartType.startsWith("live-signals-")
          ? liveSignalsData
          : chartType === "trade-pnl-waterfall"
            ? waterfallTradeData
            : chartType === "closed-positions-pnl-timeseries"
              ? closedPositionsPnLData
              : chartType === "open-positions-pnl-timeseries"
                ? shouldUseClosedData
                  ? closedPositionsPnLData
                  : openPositionsPnLData
                : portfolioData;

  // Dynamic legend visibility based on data volume
  const shouldShowLegend = useMemo(() => {
    // Hide legend for specific chart types
    const hideLegendChartTypes = [
      "live-signals-drawdowns",
      "live-signals-weekly-candlestick",
      "trade-pnl-waterfall",
    ];

    if (hideLegendChartTypes.includes(chartType)) {
      return false;
    }

    const isAnyPositionChart =
      chartType === "open-positions-pnl-timeseries" ||
      chartType === "closed-positions-pnl-timeseries";

    if (isAnyPositionChart && shouldUseClosedData) {
      // For closed data, hide legend if > 7 positions
      const closedData = data as ClosedPositionPnLDataRow[];
      if (closedData && closedData.length > 0) {
        const uniquePositions = new Set(
          closedData.map((row) => row.Position_UUID),
        ).size;
        return uniquePositions <= 7;
      }
      return true;
    }

    if (isAnyPositionChart && !shouldUseClosedData) {
      // For open data, hide legend if > 7 positions
      const openData = data as OpenPositionPnLDataRow[];
      if (openData && openData.length > 0) {
        const uniquePositions = new Set(openData.map((row) => row.Ticker)).size;
        return uniquePositions <= 7;
      }
      return true;
    }

    // For all other charts, show legend
    return true;
  }, [chartType, shouldUseClosedData, data]);

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
  const convertToWeeklyOHLC = useCallback(
    (rows: LiveSignalsDataRow[]): WeeklyOHLCDataRow[] => {
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
        if (
          currentWeekStart &&
          monday.getTime() !== currentWeekStart.getTime()
        ) {
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
    },
    [],
  );

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

  // Create indexed data with synthetic entry point (Position Bar 0 = $0 PnL)
  const createIndexedDataWithEntry = useCallback(
    (rows: OpenPositionPnLDataRow[]): OpenPositionPnLDataRow[] => {
      if (!rows || rows.length === 0) {
        return [];
      }

      // Get the first row to extract entry information
      const firstRow = rows[0];
      if (!firstRow.Entry_Date || !firstRow.Entry_Price) {
        // If no entry information available, return original data
        // console.warn(`Missing entry information for ticker ${firstRow.Ticker}`);
        return rows;
      }

      // Create synthetic entry point with PnL = $0
      const entryPoint: OpenPositionPnLDataRow = {
        Date: firstRow.Entry_Date,
        Ticker: firstRow.Ticker,
        Price: firstRow.Entry_Price,
        PnL: "0.00", // Entry point always has $0 PnL
        Position_Size: firstRow.Position_Size,
        Entry_Date: firstRow.Entry_Date,
        Entry_Price: firstRow.Entry_Price,
        Direction: firstRow.Direction,
        Position_UUID: firstRow.Position_UUID,
      };

      // Combine entry point with existing data
      return [entryPoint, ...rows];
    },
    [],
  );

  // Create indexed data for closed positions using real historical price data
  const createClosedPositionIndexedData = useCallback(
    (
      closedPositionsData: ClosedPositionPnLDataRow[],
    ): Array<{
      ticker: string;
      data: Array<{ bar: number; pnl: number }>;
      color: string;
      finalPnL: number;
    }> => {
      if (!closedPositionsData || closedPositionsData.length === 0) {
        return [];
      }

      // Group data by ticker (Position_UUID for unique trades)
      const tradeMap: { [uuid: string]: ClosedPositionPnLDataRow[] } = {};

      closedPositionsData.forEach((row) => {
        const uuid = row.Position_UUID;
        if (!tradeMap[uuid]) {
          tradeMap[uuid] = [];
        }
        tradeMap[uuid].push(row);
      });

      return Object.entries(tradeMap).map(([_uuid, tradeData]) => {
        // Sort by date to ensure proper position bar ordering
        const sortedData = tradeData.sort(
          (a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime(),
        );

        if (sortedData.length === 0) {
          return { ticker: "", data: [], color: "#26c6da", finalPnL: 0 };
        }

        const ticker = sortedData[0].Ticker;
        const finalPnL = parseFloat(sortedData[sortedData.length - 1].PnL);

        // Create indexed data points from real price data
        const data: Array<{ bar: number; pnl: number }> = sortedData.map(
          (row, index) => ({
            bar: index,
            pnl: parseFloat(row.PnL),
          }),
        );

        return {
          ticker,
          data,
          color: finalPnL >= 0 ? "#26c6da" : "#7e57c2", // Exact hex colors: cyan for winners, purple for losers
          finalPnL,
        };
      });
    },
    [],
  );

  // Calculate average trade progression across all closed positions
  const calculateAverageTradeProgression = useCallback(
    (
      positionsData: Array<{
        ticker: string;
        data: Array<{ bar: number; pnl: number }>;
        color: string;
        finalPnL: number;
      }>,
    ): Array<{ bar: number; pnl: number }> => {
      if (!positionsData || positionsData.length === 0) {
        return [];
      }

      // Find the maximum trade length to determine the range
      const maxLength = Math.max(
        ...positionsData.map((position) => position.data.length),
      );

      if (maxLength === 0) {
        return [];
      }

      // Calculate average PnL at each position bar
      const averageData: Array<{ bar: number; pnl: number }> = [];

      for (let bar = 0; bar < maxLength; bar++) {
        let totalPnL = 0;
        let count = 0;

        // Sum PnL values from all positions that have data at this bar
        positionsData.forEach((position) => {
          if (position.data.length > bar) {
            totalPnL += position.data[bar].pnl;
            count++;
          }
        });

        if (count > 0) {
          averageData.push({
            bar,
            pnl: totalPnL / count,
          });
        }
      }

      return averageData;
    },
    [],
  );

  // Convert daily PnL data to weekly for open positions
  const convertOpenPositionsPnLToWeekly = useCallback(
    (rows: OpenPositionPnLDataRow[]): OpenPositionPnLDataRow[] => {
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
    },
    [],
  );

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
            x: unpack(stockRows, "date"),
            y: unpack(stockRows, "close"),
            line: { color: colors.tertiary, width: 2 },
            name: "Apple Price",
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
            y: unpackLiveSignals(liveSignalsRows, "mfe"),
            line: { color: "#26C6DA", width: 3 }, // Prominent cyan for MFE
            name: "MFE (Maximum Favorable Excursion)",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "mae"),
            line: { color: "#FF5722", width: 3 }, // Prominent red for MAE
            name: "MAE (Maximum Adverse Excursion)",
          },
          {
            type: "scatter",
            mode: "lines",
            x: unpackLiveSignals(liveSignalsRows, "timestamp"),
            y: unpackLiveSignals(liveSignalsRows, "equity"),
            line: { color: colors.neutral, width: 2, dash: "dot" }, // Muted dotted line for context
            name: "Portfolio Equity",
          },
        ];
      }

      case "live-signals-benchmark-comparison": {
        const benchmarkRows = data as LiveSignalsBenchmarkDataRow[];

        if (!benchmarkRows || benchmarkRows.length === 0) {
          return [];
        }

        const chartData: Data[] = [];

        // Define color mapping for series
        const seriesColors = {
          Portfolio: colors.tertiary, // Cyan for portfolio
          SPY: colors.multiStrategy, // Blue for SPY
          QQQ: colors.buyHold, // Purple for QQQ
          "BTC-USD": colors.drawdown, // Orange for BTC
        };

        // Define display names
        const seriesNames = {
          Portfolio: "Live Signals Portfolio",
          SPY: "SPY",
          QQQ: "QQQ",
          "BTC-USD": "Bitcoin",
        };

        // Create series for each column (Portfolio, SPY, QQQ, BTC-USD)
        const seriesColumns = ["Portfolio", "SPY", "QQQ", "BTC-USD"] as const;

        seriesColumns.forEach((column) => {
          const values = benchmarkRows.map((row) => parseFloat(row[column]));
          const dates = benchmarkRows.map((row) => row.Date);

          chartData.push({
            type: "scatter",
            mode: "lines",
            x: dates,
            y: values,
            line: {
              color: seriesColors[column],
              width: column === "Portfolio" ? 3 : 2,
            },
            name: seriesNames[column],
          });
        });

        return chartData;
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

        // Data is already pre-sorted by PnL magnitude from backend
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
        // Handle both open and closed position data based on shouldUseClosedData
        if (shouldUseClosedData) {
          // Use existing closed positions logic when showing closed data
          const closedPositionsRows = data as ClosedPositionPnLDataRow[];
          if (!closedPositionsRows || closedPositionsRows.length === 0) {
            return [];
          }

          const closedPositionsData =
            createClosedPositionIndexedData(closedPositionsRows);
          if (closedPositionsData.length === 0) {
            return [];
          }

          const chartData: Data[] = [];

          // Add individual positions as scatter plots
          closedPositionsData.forEach((position) => {
            chartData.push({
              type: "scatter",
              mode: "markers",
              x: position.data.map((point) => point.bar),
              y: position.data.map((point) => point.pnl),
              name: position.ticker,
              marker: {
                color: position.color,
                size: 6,
              },
              hovertemplate:
                "<b>%{fullData.name}</b><br>" +
                "Position Bar: %{x}<br>" +
                "PnL: $%{y:.2f}<br>" +
                "<extra></extra>",
            });
          });

          // Calculate and add average trade progression line
          const averageTradeData =
            calculateAverageTradeProgression(closedPositionsData);
          if (averageTradeData.length > 0) {
            chartData.push({
              type: "scatter",
              mode: "lines",
              x: averageTradeData.map((point) => point.bar),
              y: averageTradeData.map((point) => point.pnl),
              name: "Average Trade",
              line: {
                color: "#3179f5", // tertiary_data color
                width: 3,
              },
              hovertemplate:
                "<b>Average Trade</b><br>" +
                "Position Bar: %{x}<br>" +
                "Avg PnL: $%{y:.2f}<br>" +
                "<extra></extra>",
            });
          }

          return chartData;
        }

        // Original open positions logic
        const openPositionsPnLRows = data as OpenPositionPnLDataRow[];
        if (!openPositionsPnLRows || openPositionsPnLRows.length === 0) {
          return [];
        }

        // Apply timeframe-specific data processing
        const processedData =
          timeframe === "weekly"
            ? convertOpenPositionsPnLToWeekly(openPositionsPnLRows)
            : openPositionsPnLRows;

        if (processedData.length === 0) {
          return [];
        }

        // Group data by ticker to create separate time series for each position
        const positionMap: { [ticker: string]: OpenPositionPnLDataRow[] } = {};
        processedData.forEach((row) => {
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

          // For indexed charts, ensure Position Bar 0 starts with PnL = $0
          const finalRows = indexed
            ? createIndexedDataWithEntry(sortedRows)
            : sortedRows;

          // Use either dates or indexed bars based on indexed prop
          const xValues = indexed
            ? finalRows.map((_, index) => index) // Sequential indices: 0, 1, 2, 3...
            : finalRows.map((row) => row.Date); // Original dates
          const pnlValues = finalRows.map((row) => parseFloat(row.PnL));

          chartData.push({
            type: "scatter",
            mode: "lines+markers",
            x: xValues,
            y: pnlValues,
            name: ticker,
            line: {
              color: chartColors[colorIndex % chartColors.length],
              width: 2,
            },
            marker: {
              size: timeframe === "weekly" ? 6 : 4, // Larger markers for weekly data
              color: chartColors[colorIndex % chartColors.length],
            },
            hovertemplate:
              "<b>%{fullData.name}</b><br>" +
              (indexed
                ? "Position Bar: %{x}<br>"
                : timeframe === "weekly"
                  ? "Week Ending: %{x}<br>"
                  : "Date: %{x}<br>") +
              "PnL: $%{y:.2f}<br>" +
              "<extra></extra>",
          });

          colorIndex++;
        });

        return chartData;
      }

      case "closed-positions-pnl-timeseries": {
        const closedPositionsRows = data as ClosedPositionPnLDataRow[];
        if (!closedPositionsRows || closedPositionsRows.length === 0) {
          return [];
        }

        const closedPositionsData =
          createClosedPositionIndexedData(closedPositionsRows);
        if (closedPositionsData.length === 0) {
          return [];
        }

        const chartData: Data[] = [];

        // Add individual positions as scatter plots
        closedPositionsData.forEach((position) => {
          chartData.push({
            type: "scatter",
            mode: "markers",
            x: position.data.map((point) => point.bar),
            y: position.data.map((point) => point.pnl),
            name: position.ticker,
            marker: {
              color: position.color,
              size: 6,
            },
            hovertemplate:
              "<b>%{fullData.name}</b><br>" +
              "Position Bar: %{x}<br>" +
              "PnL: $%{y:.2f}<br>" +
              "<extra></extra>",
          });
        });

        // Calculate and add average trade progression line
        const averageTradeData =
          calculateAverageTradeProgression(closedPositionsData);
        if (averageTradeData.length > 0) {
          chartData.push({
            type: "scatter",
            mode: "lines",
            x: averageTradeData.map((point) => point.bar),
            y: averageTradeData.map((point) => point.pnl),
            name: "Average Trade",
            line: {
              color: "#3179f5", // tertiary_data color
              width: 3,
            },
            hovertemplate:
              "<b>Average Trade</b><br>" +
              "Position Bar: %{x}<br>" +
              "Avg PnL: $%{y:.2f}<br>" +
              "<extra></extra>",
          });
        }

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
    timeframe,
    indexed,
    shouldUseClosedData,
    convertToWeeklyOHLC,
    convertOpenPositionsPnLToWeekly,
    createIndexedDataWithEntry,
    createClosedPositionIndexedData,
    calculateAverageTradeProgression,
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
          return "Apple Price";
        case "portfolio-value-comparison":
          return "Portfolio Value Comparison";
        case "returns-comparison":
          return "Daily Returns Comparison";
        case "portfolio-drawdowns":
          return "Portfolio Drawdown Analysis";
        case "live-signals-equity-curve":
          return "Live Signals MFE/MAE Analysis";
        case "live-signals-benchmark-comparison":
          return "Live Signals vs Market Benchmarks";
        case "live-signals-drawdowns":
          return "Live Signals Portfolio Drawdowns";
        case "live-signals-weekly-candlestick":
          return "Live Signals Weekly Candlestick Chart";
        case "trade-pnl-waterfall":
          return "Closed Position PnL Waterfall";
        case "closed-positions-pnl-timeseries":
          return "Closed Position PnL Performance";
        case "open-positions-pnl-timeseries": {
          const positionTypeText =
            actualDataType === "closed" ? "Closed" : "Open";
          if (indexed) {
            return `${positionTypeText} Positions Cumulative PnL Time Series (Indexed)`;
          }
          return timeframe === "weekly"
            ? `${positionTypeText} Positions Cumulative PnL Time Series (Weekly)`
            : `${positionTypeText} Positions Cumulative PnL Time Series`;
        }
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
          return "Value ($)";
        case "live-signals-benchmark-comparison":
          return "Relative Performance (%)";
        case "live-signals-drawdowns":
          return "Drawdown ($)";
        case "live-signals-weekly-candlestick":
          return "Equity ($)";
        case "trade-pnl-waterfall":
          return "PnL ($)";
        case "closed-positions-pnl-timeseries":
          return "PnL ($)";
        case "open-positions-pnl-timeseries":
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
      showlegend: shouldShowLegend,
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
          chartType === "trade-pnl-waterfall"
            ? undefined
            : undefined,
        type:
          chartType === "trade-pnl-waterfall"
            ? "category"
            : chartType === "closed-positions-pnl-timeseries"
              ? "linear"
              : chartType === "open-positions-pnl-timeseries" && indexed
                ? "linear"
                : "date",
        title: {
          text:
            chartType === "trade-pnl-waterfall"
              ? "Ticker"
              : chartType === "closed-positions-pnl-timeseries"
                ? "Position Bar"
                : chartType === "open-positions-pnl-timeseries" && indexed
                  ? "Position Bar"
                  : "Date",
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
        type: "linear",
        title: {
          text: getYAxisTitle(),
          font: themeColors.font,
        },
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: themeColors.font,
      },
      hovermode: "closest",
    };
  }, [
    isDarkMode,
    chartType,
    title,
    timeframe,
    indexed,
    shouldShowLegend,
    actualDataType,
  ]);

  // Chart config
  const config = useMemo(
    () => ({
      responsive: true,
      displayModeBar: false,
      displaylogo: false,
      toImageButtonOptions: {
        format: "png" as const,
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
