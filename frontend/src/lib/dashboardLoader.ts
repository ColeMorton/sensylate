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
        title: "Closed Position PnL Waterfall",
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
  portfolio_history_portrait: {
    id: "portfolio_history_portrait",
    title: "Portfolio History Portrait",
    description:
      "Portfolio trading history with waterfall and time series analysis",
    layout: "1x3_stack",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Closed Position PnL Waterfall",
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
  fundamental_analysis: {
    id: "fundamental_analysis",
    title: "Fundamental Analysis Dashboard",
    description:
      "Comprehensive stock fundamental analysis with financial metrics and valuation",
    layout: "fundamental_3x3",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Revenue & FCF",
        category: "Financial Performance",
        description: "Revenue and free cash flow trends over time",
        chartType: "fundamental-revenue-fcf",
      },
      {
        title: "Revenue Source",
        category: "Revenue Breakdown",
        description: "Revenue distribution by business segment",
        chartType: "fundamental-revenue-source",
      },
      {
        title: "Geography",
        category: "Geographic Distribution",
        description: "Revenue distribution by geographic region",
        chartType: "fundamental-geography",
      },
      {
        title: "Key Metrics",
        category: "Growth Analysis",
        description: "Key growth metrics and performance indicators",
        chartType: "fundamental-key-metrics",
      },
      {
        title: "Quality",
        category: "Quality Assessment",
        description: "Quality ratings across multiple dimensions",
        chartType: "fundamental-quality-rating",
      },
      {
        title: "Financials",
        category: "Financial Health",
        description: "Revenue growth, FCF growth, and cash position",
        chartType: "fundamental-financial-health",
      },
      {
        title: "Pros & Cons",
        category: "Investment Analysis",
        description: "Key investment advantages and risks",
        chartType: "fundamental-pros-cons",
      },
      {
        title: "Valuation",
        category: "Valuation Analysis",
        description:
          "Multiple valuation methodologies and fair value estimates",
        chartType: "fundamental-valuation",
      },
      {
        title: "Balance Sheet",
        category: "Financial Position",
        description: "Balance sheet metrics and financial stability",
        chartType: "fundamental-balance-sheet",
      },
    ],
  },
  logo_generation: {
    id: "logo_generation",
    title: "Logo Generation Dashboard",
    description:
      "Brand logo generation with multiple sizes and formats for high-quality captures",
    layout: "logo_variants",
    mode: "both",
    enabled: true,
    charts: [], // Logo dashboard uses MDX content, not chart components
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

    // Use static configs directly to avoid circular dependency with API
    const dashboards = Object.values(DASHBOARD_CONFIGS).filter(
      (d) => d.enabled,
    );

    this.cache = dashboards;
    this.cacheTimestamp = now;
    return dashboards;
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
      case "fundamental_3x3":
        return "fundamental-dashboard-grid";
      case "logo_variants":
        return "logo-generation-layout flex items-center justify-center w-full h-full";
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
      "closed-positions-pnl-timeseries",
      "fundamental-revenue-fcf",
      "fundamental-revenue-source",
      "fundamental-geography",
      "fundamental-key-metrics",
      "fundamental-quality-rating",
      "fundamental-financial-health",
      "fundamental-pros-cons",
      "fundamental-valuation",
      "fundamental-balance-sheet",
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
