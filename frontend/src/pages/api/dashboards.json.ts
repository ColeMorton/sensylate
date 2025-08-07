import type { APIRoute } from "astro";
import { getCollection } from "astro:content";

export interface DashboardChart {
  title: string;
  category?: string;
  description?: string;
  chartType: string;
}

export interface DashboardConfig {
  id: string;
  title: string;
  description?: string;
  layout: string;
  mode: string;
  enabled: boolean;
  charts: DashboardChart[];
}

// Static dashboard configurations that match the MDX files
const DASHBOARD_CONFIGS: Record<string, DashboardConfig> = {
  "trading-performance": {
    id: "trading_performance",
    title: "Trading Performance Dashboard",
    description: "Comprehensive trading strategy performance overview",
    layout: "2x2_grid",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Bitcoin Portfolio Value Comparison",
        category: "Bitcoin Performance",
        description:
          "Multi-strategy Bitcoin trading vs buy-and-hold approach from 2014-2025. Active strategy: $1,000 → $113,312 (11,231% return).",
        chartType: "portfolio-value-comparison",
      },
      {
        title: "Bitcoin Returns Comparison",
        category: "Bitcoin Performance",
        description:
          "Daily returns comparison: multi-strategy Bitcoin trading vs passive buy-and-hold showing day-to-day percentage changes over 3,960 days of market data.",
        chartType: "returns-comparison",
      },
      {
        title: "Bitcoin Portfolio Drawdown Analysis",
        category: "Bitcoin Risk Analysis",
        description:
          "Bitcoin portfolio risk analysis showing drawdown periods. Maximum drawdown: 53.23% with 839-day recovery duration.",
        chartType: "portfolio-drawdowns",
      },
      {
        title: "Live Signals Equity Curve",
        category: "Live Trading Performance",
        description:
          "Comprehensive live trading analysis showing equity curve, MFE (Maximum Favorable Excursion), and MAE (Maximum Adverse Excursion). Real-time performance from April to August 2025 with risk management insights.",
        chartType: "live-signals-equity-curve",
      },
    ],
  },
  "portfolio-analysis": {
    id: "portfolio_analysis",
    title: "Portfolio Analysis Dashboard",
    description: "Portfolio composition and risk analysis",
    layout: "1x3_stack",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Live Signals Equity Curve",
        category: "Live Trading Performance",
        description:
          "Comprehensive live trading analysis showing equity curve, MFE (Maximum Favorable Excursion), and MAE (Maximum Adverse Excursion). Real-time performance from April to August 2025 with risk management insights.",
        chartType: "live-signals-equity-curve",
      },
      {
        title: "Live Signals Drawdown Analysis",
        category: "Live Trading Risk",
        description:
          "Live portfolio drawdown periods showing risk management during real trading. Peak drawdown of $69.23 with successful recovery to profitability.",
        chartType: "live-signals-drawdowns",
      },
      {
        title: "Trade PnL Waterfall Chart",
        category: "Live Trading Individual Trades",
        description:
          "Waterfall chart showing individual trade profits and losses from closed positions, sorted from highest to lowest PnL. Visualizes contribution of each trade to overall portfolio performance.",
        chartType: "trade-pnl-waterfall",
      },
      {
        title: "Open Positions Cumulative PnL Time Series",
        category: "Live Trading Open Positions",
        description:
          "Multi-line time series showing cumulative PnL for each open position, indexed to $0 at entry date. Track real-time performance across the live portfolio with individual lines for each ticker.",
        chartType: "open-positions-pnl-timeseries",
      },
    ],
  },
  "portfolio-history-portrait": {
    id: "portfolio_history_portrait",
    title: "Portfolio History Portrait",
    description:
      "Portfolio trading history with waterfall and time series analysis",
    layout: "2x1_stack",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Trade PnL Waterfall Chart",
        category: "Trading Performance",
        description:
          "Waterfall chart showing individual trade profits and losses from closed positions, sorted from highest to lowest PnL. Visualizes contribution of each trade to overall portfolio performance.",
        chartType: "trade-pnl-waterfall",
      },
      {
        title: "Closed Position PnL Performance",
        category: "Trading Performance",
        description:
          "Multi-line time series showing cumulative PnL for each closed position, indexed to $0 at entry date. Track performance progression across the closed portfolio with individual lines for each ticker.",
        chartType: "closed-positions-pnl-timeseries",
      },
    ],
  },
  "market-overview": {
    id: "market_overview",
    title: "Market Overview Dashboard",
    description: "Market trends and sector analysis",
    layout: "2x2_grid",
    mode: "both",
    enabled: false, // Disabled by default
    charts: [
      {
        title: "Live Signals Weekly Candlestick Chart",
        category: "Live Trading Technical Analysis",
        description:
          "Weekly OHLC candlestick view of live signals equity performance. Aggregates daily equity data into weekly candles for technical analysis.",
        chartType: "live-signals-weekly-candlestick",
      },
      {
        title: "Apple Stock Reference",
        category: "Reference Data",
        description:
          "Interactive chart showing Apple stock high and low prices from July to December 2016. Data sourced from Plotly's public dataset.",
        chartType: "apple-stock",
      },
      {
        title: "Bitcoin Portfolio Value Comparison",
        category: "Bitcoin Performance",
        description:
          "Multi-strategy Bitcoin trading vs buy-and-hold approach from 2014-2025. Active strategy: $1,000 → $113,312 (11,231% return).",
        chartType: "portfolio-value-comparison",
      },
      {
        title: "Live Signals Equity Curve",
        category: "Live Trading Performance",
        description:
          "Comprehensive live trading analysis showing equity curve, MFE (Maximum Favorable Excursion), and MAE (Maximum Adverse Excursion). Real-time performance from April to August 2025 with risk management insights.",
        chartType: "live-signals-equity-curve",
      },
    ],
  },
};

export const GET: APIRoute = async () => {
  try {
    // Loading dashboards from content collection

    // Try to load from Astro content collection for validation
    try {
      await getCollection("dashboards");
      // Loaded dashboards from collection
    } catch {
      // Could not load from content collection, using static configs
    }

    // Use static configurations (since we can't easily parse MDX content)
    const dashboards = Object.values(DASHBOARD_CONFIGS);

    // Filter enabled dashboards
    const enabledDashboards = dashboards.filter(
      (dashboard) => dashboard.enabled,
    );

    // Returning enabled dashboards

    // Return JSON response
    return new Response(
      JSON.stringify({
        success: true,
        dashboards: enabledDashboards,
        timestamp: new Date().toISOString(),
        source: "static_config",
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "public, max-age=3600", // Cache for 1 hour
        },
      },
    );
  } catch (error) {
    // Dashboard API error occurred

    // Return error response
    return new Response(
      JSON.stringify({
        success: false,
        error: "Failed to load dashboards",
        message: error instanceof Error ? error.message : "Unknown error",
        timestamp: new Date().toISOString(),
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
        },
      },
    );
  }
};
