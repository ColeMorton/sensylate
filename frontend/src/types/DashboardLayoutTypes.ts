/**
 * Dashboard Layout Configuration Types
 * 
 * Defines configuration-driven layout behavior for PhotoBooth dashboards.
 * Eliminates hardcoded dashboard-specific logic from components.
 */

export interface DashboardHeaderConfig {
  /** Header text to display */
  title: string;
  /** CSS classes for header styling */
  className?: string;
  /** Whether to show header */
  enabled: boolean;
}

export interface DashboardFooterConfig {
  /** Footer text to display */
  text: string;
  /** CSS classes for footer styling */
  className?: string;
  /** Whether to show footer */
  enabled: boolean;
}

export interface ChartDisplayOptions {
  /** Display charts with title only (no category/description) */
  titleOnly?: boolean;
  /** Custom chart display mode */
  displayMode?: 'full' | 'compact' | 'minimal';
  /** Chart-specific CSS classes */
  chartClassName?: string;
}

export interface DashboardLayoutConfig {
  /** Header configuration */
  header?: DashboardHeaderConfig;
  /** Footer configuration */
  footer?: DashboardFooterConfig;
  /** Chart display options */
  chartOptions?: ChartDisplayOptions;
  /** Custom CSS classes for dashboard container */
  containerClassName?: string;
  /** Special layout modes */
  layoutMode?: 'standard' | 'portrait' | 'landscape' | 'minimal';
}

/**
 * Extended dashboard configuration with layout information
 */
export interface ExtendedDashboardConfig {
  id: string;
  title: string;
  description: string;
  layout: string;
  mode: string;
  enabled: boolean;
  charts: any[];
  export_defaults: any;
  /** Layout and display configuration */
  layout_config?: DashboardLayoutConfig;
}