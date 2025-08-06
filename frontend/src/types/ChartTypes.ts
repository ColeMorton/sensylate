import type { Data, Layout, Config } from "plotly.js";

// Portfolio data structure from CSV files
export interface PortfolioDataRow {
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

// Live signals equity data structure from CSV files
export interface LiveSignalsDataRow {
  timestamp: string;
  equity: string;
  equity_pct: string;
  equity_change: string;
  equity_change_pct: string;
  drawdown: string;
  drawdown_pct: string;
  peak_equity: string;
  mfe: string;
  mae: string;
}

// Weekly OHLC data structure for candlestick charts
export interface WeeklyOHLCDataRow {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

// Trade history data structure from trade_history CSV files
export interface TradeHistoryDataRow {
  Position_UUID: string;
  Ticker: string;
  Strategy_Type: string;
  Short_Window: string;
  Long_Window: string;
  Signal_Window: string;
  Entry_Timestamp: string;
  Exit_Timestamp: string;
  Avg_Entry_Price: string;
  Avg_Exit_Price: string;
  Position_Size: string;
  Direction: string;
  PnL: string;
  Return: string;
  Duration_Days: string;
  Trade_Type: string;
  Status: string;
  Max_Favourable_Excursion: string;
  Max_Adverse_Excursion: string;
  MFE_MAE_Ratio: string;
  Exit_Efficiency: string;
  Days_Since_Entry: string;
  Current_Unrealized_PnL: string;
  Current_Excursion_Status: string;
  Exit_Efficiency_Fixed: string;
  Trade_Quality: string;
  X_Status: string;
}

// Enhanced closed position data with real daily price progression
export interface ClosedPositionPnLDataRow {
  Date: string;
  Ticker: string;
  Price: string;
  PnL: string;
  Position_Size: string;
  Entry_Date: string;
  Entry_Price: string;
  Direction: string;
  Position_UUID: string;
  Duration_Days: string;
}

// Open positions PnL time series data structure
export interface OpenPositionPnLDataRow {
  Date: string;
  Ticker: string;
  Price: string;
  PnL: string;
  Position_Size: string;
  Entry_Date: string;
  Entry_Price: string;
  Direction: string;
  Position_UUID: string;
}

// Legacy stock data structure (for Apple stock chart)
export interface StockDataRow {
  Date: string;
  "AAPL.High": string;
  "AAPL.Low": string;
  [key: string]: string;
}

// Benchmark data structure for comparison charts
export interface BenchmarkDataRow {
  date: string;
  ticker: string;
  close: string;
}

// Live Signals Benchmark Comparison data structure from pre-processed CSV
export interface LiveSignalsBenchmarkDataRow {
  Date: string;
  Portfolio: string;
  SPY: string;
  QQQ: string;
  "BTC-USD": string;
}
// Chart configuration types
export type ChartType =
  | "apple-stock"
  | "portfolio-value-comparison"
  | "returns-comparison"
  | "portfolio-drawdowns"
  | "live-signals-equity-curve"
  | "live-signals-benchmark-comparison"
  | "live-signals-drawdowns"
  | "live-signals-weekly-candlestick"
  | "trade-pnl-waterfall"
  | "open-positions-pnl-timeseries"
  | "closed-positions-pnl-timeseries";

export interface ChartConfig {
  title: string;
  yAxisTitle: string;
  colors: string[];
  dataKeys: string[];
  chartSpecificOptions?: Partial<Layout>;
}

// Theme integration
export interface ThemeColors {
  primary: string;
  body: string;
  border: string;
  light: string;
  dark: string;
  text: string;
  textDark: string;
  textLight: string;
  primaryData: string;
  secondaryData: string;
  tertiaryData: string;
  quaternary: string;
  neutralData: string;
}

// Chart component props
export interface ChartDisplayProps {
  title: string;
  category?: string;
  description?: string;
  chartType?: ChartType;
  timeframe?: "daily" | "weekly";
  indexed?: boolean;
  positionType?: "open" | "closed" | "auto";
  className?: string;
}

export interface ChartContainerProps {
  title: string;
  category?: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export interface ChartRendererProps {
  data: Data[];
  layout: Partial<Layout>;
  config?: Partial<Config>;
  loading?: boolean;
  error?: string | null;
}

// Data service types
export interface PortfolioDataCache {
  multiStrategyValue: PortfolioDataRow[];
  buyHoldValue: PortfolioDataRow[];
  multiStrategyCumulative: PortfolioDataRow[];
  multiStrategyReturns: PortfolioDataRow[];
  buyHoldReturns: PortfolioDataRow[];
  multiStrategyDrawdowns: PortfolioDataRow[];
  lastFetched: number;
}

export interface DataServiceResponse<T> {
  data: T;
  loading: boolean;
  error: string | null;
}
