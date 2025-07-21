import type { Data, Layout } from "plotly.js";

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

// Legacy stock data structure (for Apple stock chart)
export interface StockDataRow {
  Date: string;
  "AAPL.High": string;
  "AAPL.Low": string;
  [key: string]: string;
}

// Chart configuration types
export type ChartType =
  | "apple-stock"
  | "portfolio-value-comparison"
  | "returns-comparison"
  | "portfolio-drawdowns"
  | "normalized-performance";

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
  config?: any;
  loading?: boolean;
  error?: string | null;
}

// Data service types
export interface PortfolioDataCache {
  multiStrategyValue: PortfolioDataRow[];
  buyHoldValue: PortfolioDataRow[];
  multiStrategyCumulative: PortfolioDataRow[];
  buyHoldReturns: PortfolioDataRow[];
  multiStrategyDrawdowns: PortfolioDataRow[];
  lastFetched: number;
}

export interface DataServiceResponse<T> {
  data: T;
  loading: boolean;
  error: string | null;
}
