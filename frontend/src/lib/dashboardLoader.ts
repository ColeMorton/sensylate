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

interface DashboardAPIResponse {
  success: boolean;
  dashboards?: DashboardConfig[];
  error?: string;
  message?: string;
  timestamp: string;
  source?: string;
}

// Dashboard chart configurations - mapped from the actual dashboard MDX files
const DASHBOARD_CONFIGS: Record<string, DashboardConfig> = {
  trading_performance: {
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
  portfolio_analysis: {
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
  market_overview: {
    id: "market_overview",
    title: "Market Overview Dashboard",
    description: "Market trends and sector analysis",
    layout: "2x2_grid",
    mode: "both",
    enabled: false, // Disabled by default in config
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

export class DashboardLoader {
  private static cache: DashboardConfig[] | null = null;
  private static cacheTimestamp: number = 0;
  private static readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  static async getAllDashboards(): Promise<DashboardConfig[]> {
    // Check if cache is still valid
    const now = Date.now();
    if (this.cache && now - this.cacheTimestamp < this.CACHE_DURATION) {
      return this.cache;
    }

    try {
      // Fetching dashboards from API

      // Fetch from our API endpoint
      const response = await fetch("/api/dashboards.json");

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status} ${response.statusText}`,
        );
      }

      const data: DashboardAPIResponse = await response.json();

      if (!data.success || !data.dashboards) {
        throw new Error(`API error: ${data.error || "Unknown error"}`);
      }

      // Loaded dashboards from API

      this.cache = data.dashboards;
      this.cacheTimestamp = now;
      return data.dashboards;
    } catch {
      // Failed to load dashboards from API

      // Fallback to hardcoded configurations
      const fallbackDashboards = Object.values(DASHBOARD_CONFIGS).filter(
        (d) => d.enabled,
      );
      // Using fallback configurations

      // Cache fallback data but with shorter duration
      this.cache = fallbackDashboards;
      this.cacheTimestamp = now - this.CACHE_DURATION + 30000; // Retry API in 30 seconds

      return fallbackDashboards;
    }
  }

  static async getDashboard(id: string): Promise<DashboardConfig | null> {
    const dashboards = await this.getAllDashboards();
    return dashboards.find((dashboard) => dashboard.id === id) || null;
  }

  static clearCache(): void {
    this.cache = null;
  }

  // Get layout-specific CSS classes
  static getLayoutClasses(layout: string): string {
    switch (layout) {
      case "2x2_grid":
        return "grid grid-cols-1 gap-6 lg:grid-cols-2";
      case "1x3_stack":
        return "grid grid-cols-1 gap-6";
      case "1x4_stack":
        return "grid grid-cols-1 gap-4";
      default:
        return "grid grid-cols-1 gap-6 lg:grid-cols-2";
    }
  }

  // Validate that all chart types are supported
  static validateChartTypes(): { valid: boolean; errors: string[] } {
    const supportedChartTypes = [
      "apple-stock",
      "portfolio-value-comparison",
      "returns-comparison",
      "portfolio-drawdowns",
      "live-signals-equity-curve",
      "live-signals-drawdowns",
      "live-signals-weekly-candlestick",
      "trade-pnl-waterfall",
      "open-positions-pnl-timeseries",
    ];

    const errors: string[] = [];
    const allChartTypes = new Set<string>();

    // Collect all chart types from configurations
    Object.values(DASHBOARD_CONFIGS).forEach((config) => {
      config.charts.forEach((chart) => {
        allChartTypes.add(chart.chartType);
      });
    });

    // Check for unsupported chart types
    allChartTypes.forEach((chartType) => {
      if (!supportedChartTypes.includes(chartType)) {
        errors.push(`Unsupported chart type: ${chartType}`);
      }
    });

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}
