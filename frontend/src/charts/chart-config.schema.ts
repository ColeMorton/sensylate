/**
 * Chart Configuration Schema
 * 
 * Defines the standard structure for chart configurations that enables:
 * - Chart component colocation
 * - Auto-discovery by GenContentOps pipeline
 * - Type-safe configuration management
 */

export interface ChartMetadata {
  /** Display title for the chart */
  title: string;
  /** Category for grouping charts */
  category: string;
  /** Description of what the chart shows */
  description: string;
  /** Chart type identifier (must be unique) */
  chartType: string;
}

export interface ChartDataRequirements {
  /** Data sources required by this chart */
  dataSources: string[];
  /** Whether data should be cached */
  cacheable?: boolean;
  /** Cache duration in milliseconds */
  cacheDuration?: number;
}

export interface ChartDisplayOptions {
  /** Default timeframe for chart data */
  defaultTimeframe?: string;
  /** Whether chart supports indexed view */
  supportsIndexed?: boolean;
  /** Whether chart supports position type selection */
  supportsPositionType?: boolean;
  /** Whether chart supports same percentage scale */
  supportsSamePercentageScale?: boolean;
}

export interface ChartConfig {
  /** Chart metadata for display and configuration */
  metadata: ChartMetadata;
  /** Data requirements and fetching configuration */
  dataRequirements: ChartDataRequirements;
  /** Display options and capabilities */
  displayOptions?: ChartDisplayOptions;
  /** Whether chart is available in production */
  productionReady?: boolean;
}

/**
 * Registry entry for a chart component
 */
export interface ChartRegistryEntry extends ChartConfig {
  /** The React component for this chart */
  component: React.ComponentType<any>;
  /** Data adapter for fetching chart-specific data */
  dataAdapter?: any;
}

/**
 * Type-safe chart type identifier
 */
export type ChartType = string;