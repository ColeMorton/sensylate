/**
 * Type definitions for extensible blog chart system
 * Supports different blog post types with chart integrations
 */

export interface BlogChartConfig {
  chartType: string;
  enabled: boolean;
  viewportThreshold: number; // Minimum viewport width for chart display
}

export interface BitcoinCycleData {
  confidence: number;
  data_quality: number;
  cycle_phase: string;
  mvrv_z_score: number;
  nupl_value: number;
  nupl_zone: string;
  pi_cycle_active: boolean;
  rainbow_position: string;
  network_health_score: number;
  institutional_flow: string;
  risk_score: string;
}

export interface BlogPostWithChart {
  // Bitcoin Cycle Intelligence posts
  bitcoin_cycle_data?: BitcoinCycleData;

  // Future extensibility for other post types
  trading_analysis_data?: any;
  sector_analysis_data?: any;
  macro_analysis_data?: any;
}

export type SupportedChartType =
  | "btc-price"
  | "portfolio-performance"
  | "sector-comparison"
  | "macro-indicators";

export interface ChartLightboxProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  thumbnailClassName?: string;
  chartType: SupportedChartType;
  chartTitle?: string;
  viewportThreshold?: number;
}
