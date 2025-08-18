/**
 * Chart Data Dependency Management Types
 *
 * Defines the structure for managing data dependencies across chart types,
 * handling mixed data ecosystems with manual, CLI-API, and static sources.
 */

import type { ChartType } from "./ChartTypes";

/**
 * Core data source classification
 */
export type DataSourceType =
  | "manual" // Manually created/updated files (unpredictable timing)
  | "cli-api" // Data available via CLI services (can be auto-refreshed)
  | "static" // Historical/demo data (never updates)
  | "hybrid"; // Combination of manual + API data

/**
 * How data gets updated when available
 */
export type RefreshMethod =
  | "never" // Static data that never changes
  | "file-watch" // Monitor file system for manual updates
  | "api-poll" // Periodic API calls via CLI services
  | "user-trigger" // Only refresh when user explicitly requests
  | "hybrid-sync"; // Coordinate between manual and API sources

/**
 * Update frequency classification
 */
export type UpdateFrequency =
  | "never" // Static/historical data
  | "on-demand" // Manual refresh only
  | "scheduled" // Regular intervals (minutes/hours/days)
  | "real-time" // High-frequency updates (seconds/minutes)
  | "event-driven"; // Updates when external files change

/**
 * Configuration for a single data source
 */
export interface DataSourceConfig {
  /** Source type classification */
  type: DataSourceType;

  /** File path(s) or API endpoint identifier */
  location: string | string[];

  /** How this data source gets refreshed */
  refreshMethod: RefreshMethod;

  /** Expected update frequency */
  frequency: UpdateFrequency;

  /** CLI service name if applicable */
  cliService?: string;

  /** Additional metadata for the data source */
  metadata?: {
    /** Human-readable description */
    description?: string;
    /** Last known update source */
    lastUpdatedBy?: string;
    /** Expected data format */
    format?: "csv" | "json" | "api";
  };
}

/**
 * Data freshness and staleness configuration
 */
export interface DataFreshnessConfig {
  /** Hours before showing warning indicator */
  warningThreshold: number;

  /** Hours before showing error state */
  errorThreshold: number;

  /** Whether stale data should block chart rendering */
  blockOnStale: boolean;

  /** Grace period for manual data sources (hours) */
  manualGracePeriod?: number;
}

/**
 * Refresh policy for chart data
 */
export interface RefreshPolicy {
  /** Whether automatic refresh is enabled */
  autoRefresh: boolean;

  /** Interval for automatic refresh (milliseconds) */
  refreshInterval?: number;

  /** Whether user can trigger manual refresh */
  allowManualRefresh: boolean;

  /** Whether to refresh on chart visibility */
  refreshOnVisible: boolean;

  /** Maximum retry attempts for failed refreshes */
  maxRetries: number;

  /** Backoff strategy for retries */
  retryBackoff: "linear" | "exponential";
}

/**
 * Complete chart data dependency configuration
 */
export interface ChartDataDependency {
  /** Chart type this configuration applies to */
  chartType: ChartType;

  /** Primary data source configuration */
  primarySource: DataSourceConfig;

  /** Optional fallback data sources */
  fallbackSources?: DataSourceConfig[];

  /** Data freshness requirements */
  freshness: DataFreshnessConfig;

  /** Refresh behavior configuration */
  refreshPolicy: RefreshPolicy;

  /** Dependencies on other chart data */
  dependencies?: string[];

  /** Custom validation rules */
  validation?: {
    /** Minimum required rows */
    minRows?: number;
    /** Required columns */
    requiredColumns?: string[];
    /** Custom validation function name */
    customValidator?: string;
  };
}

/**
 * Runtime status of a data source
 */
export interface DataSourceStatus {
  /** Current availability state */
  status: "available" | "stale" | "missing" | "error";

  /** Last successful update timestamp */
  lastUpdated?: number;

  /** Data age in hours */
  ageHours: number;

  /** Current error message if any */
  error?: string;

  /** Number of retry attempts */
  retryCount: number;

  /** Whether refresh is currently in progress */
  refreshing: boolean;

  /** Source of the last update */
  lastUpdateSource?: "manual" | "api" | "scheduled";
}

/**
 * Chart refresh capability information
 */
export interface ChartRefreshCapability {
  /** Whether chart data can be refreshed */
  canRefresh: boolean;

  /** Reason why refresh is/isn't available */
  reason: string;

  /** Available refresh methods */
  availableMethods: RefreshMethod[];

  /** Estimated refresh time (milliseconds) */
  estimatedDuration?: number;

  /** Whether refresh requires user authentication */
  requiresAuth: boolean;
}

/**
 * Data dependency registry entry
 */
export interface DataDependencyRegistryEntry {
  /** Unique identifier */
  id: string;

  /** Chart data dependency configuration */
  config: ChartDataDependency;

  /** Current runtime status */
  status: DataSourceStatus;

  /** Refresh capabilities */
  capabilities: ChartRefreshCapability;

  /** Configuration timestamp */
  configuredAt: number;

  /** Last status check timestamp */
  lastChecked: number;
}

/**
 * Complete data dependency registry
 */
export interface DataDependencyRegistry {
  /** Registry entries by chart type */
  entries: Map<ChartType, DataDependencyRegistryEntry>;

  /** Global settings */
  settings: {
    /** Default cache duration (milliseconds) */
    defaultCacheDuration: number;

    /** Enable file system monitoring */
    enableFileWatching: boolean;

    /** Enable automatic CLI service discovery */
    enableCLIDiscovery: boolean;

    /** Maximum concurrent refresh operations */
    maxConcurrentRefresh: number;
  };

  /** Registry version for configuration migration */
  version: string;
}

/**
 * Data refresh request configuration
 */
export interface DataRefreshRequest {
  /** Target chart type */
  chartType: ChartType;

  /** Force refresh even if data is fresh */
  force?: boolean;

  /** Specific data source to refresh */
  specificSource?: string;

  /** Skip cache and fetch directly */
  skipCache?: boolean;

  /** Request priority */
  priority?: "low" | "normal" | "high";

  /** Optional callback for completion */
  onComplete?: (result: DataRefreshResult) => void;

  /** Optional callback for progress updates */
  onProgress?: (progress: DataRefreshProgress) => void;
}

/**
 * Data refresh operation result
 */
export interface DataRefreshResult {
  /** Whether refresh was successful */
  success: boolean;

  /** Updated data source status */
  status: DataSourceStatus;

  /** Number of rows/records updated */
  recordsUpdated?: number;

  /** Refresh duration in milliseconds */
  duration: number;

  /** Error details if failed */
  error?: {
    message: string;
    code?: string;
    retryable: boolean;
  };

  /** Data source that provided the update */
  source: DataSourceConfig;
}

/**
 * Data refresh progress information
 */
export interface DataRefreshProgress {
  /** Current operation stage */
  stage: "connecting" | "downloading" | "parsing" | "validating" | "caching";

  /** Progress percentage (0-100) */
  progress: number;

  /** Current operation description */
  message: string;

  /** Estimated time remaining (milliseconds) */
  estimatedTimeRemaining?: number;
}
