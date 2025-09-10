/**
 * Data Requirements Schema for DevContentOps Pipeline Integration
 *
 * Extends basic chart data requirements to include comprehensive pipeline configuration.
 * This bridges the gap between colocated chart configuration and backend data pipeline.
 */

/**
 * Service refresh policy configuration
 */
export interface RefreshPolicy {
  /** Enable automatic data refresh */
  autoRefresh: boolean;
  /** Refresh interval in milliseconds */
  refreshInterval: number;
  /** Allow manual refresh triggers */
  allowManualRefresh: boolean;
  /** Refresh when chart becomes visible */
  refreshOnVisible?: boolean;
  /** Maximum retry attempts on failure */
  maxRetries: number;
  /** Retry backoff strategy */
  retryBackoff: "exponential" | "linear" | "fixed";
}

/**
 * Data freshness monitoring configuration
 */
export interface FreshnessPolicy {
  /** Warning threshold in hours */
  warningThreshold: number;
  /** Error threshold in hours */
  errorThreshold: number;
  /** Block rendering if data is stale */
  blockOnStale: boolean;
  /** Grace period for manual updates in hours */
  manualGracePeriod?: number;
}

/**
 * CLI service configuration for data fetching
 */
export interface CLIServiceConfig {
  /** Service name (yahoo_finance, alpha_vantage, etc.) */
  name: string;
  /** Command to execute */
  command?: string;
  /** Command arguments */
  args?: string[];
  /** Service options */
  options?: Record<string, unknown>;
  /** Request timeout in seconds */
  timeout?: number;
}

/**
 * Symbol metadata for stock/crypto data
 */
export interface SymbolMetadata {
  /** Symbol ticker (e.g., 'AAPL', 'BITCOIN') */
  symbol: string;
  /** Display name */
  displayName?: string;
  /** Company/entity name */
  name?: string;
  /** Market sector */
  sector?: string;
  /** Data years to fetch */
  dataYears?: number;
}

/**
 * Data source configuration for pipeline
 */
export interface DataSourceConfig {
  /** Data source type */
  type: "cli-api" | "manual" | "hybrid" | "file-watch";
  /** File location relative to frontend/public/data */
  location: string;
  /** Data refresh method */
  refreshMethod: "api-poll" | "manual-update" | "hybrid-sync" | "file-watch";
  /** Update frequency */
  frequency: "real-time" | "daily" | "weekly" | "event-driven" | "scheduled";
  /** Required CLI service */
  cliService?: string;
  /** Additional metadata */
  metadata?: {
    description: string;
    format: "csv" | "json" | "api";
    lastUpdatedBy?: string;
  };
}

/**
 * Multi-symbol chart configuration
 */
export interface MultiSymbolConfig {
  /** List of symbols for comparison */
  symbols: string[];
  /** Display name for the comparison */
  displayName: string;
  /** Description of comparison purpose */
  description: string;
  /** Comparison type */
  comparisonType:
    | "peer_analysis"
    | "sector_comparison"
    | "benchmark"
    | "correlation";
  /** Use same percentage scale */
  samePercentageScale?: boolean;
}

/**
 * Comprehensive data requirements for pipeline integration
 */
export interface DataRequirements {
  /** Chart type identifier */
  chartType: string;

  /** Chart status for pipeline filtering */
  chartStatus: "active" | "frozen" | "disabled";

  /** Primary data source configuration */
  primarySource: DataSourceConfig;

  /** Fallback data sources */
  fallbackSources?: DataSourceConfig[];

  /** Data freshness monitoring */
  freshness: FreshnessPolicy;

  /** Data refresh policy */
  refreshPolicy: RefreshPolicy;

  /** Required CLI services */
  requiredServices: string[];

  /** Data category for pipeline organization */
  category:
    | "raw"
    | "portfolio"
    | "trade-history"
    | "open-positions"
    | "processed";

  /** Symbol metadata (for stock/crypto charts) */
  symbolMetadata?: SymbolMetadata;

  /** Multi-symbol configuration (for comparison charts) */
  multiSymbolConfig?: MultiSymbolConfig;

  /** CLI service configurations */
  serviceConfigs?: CLIServiceConfig[];

  /** Additional pipeline settings */
  pipelineSettings?: {
    /** Maximum concurrent operations */
    maxConcurrency?: number;
    /** Enable file watching */
    enableFileWatching?: boolean;
    /** Custom data processing script */
    customProcessor?: string;
  };
}

/**
 * Chart data requirements combining basic and pipeline requirements
 */
export interface ExtendedChartDataRequirements {
  /** Basic data requirements (for frontend) */
  basic: {
    /** Data sources required by this chart */
    dataSources: string[];
    /** Whether data should be cached */
    cacheable?: boolean;
    /** Cache duration in milliseconds */
    cacheDuration?: number;
  };

  /** Pipeline data requirements (for backend) */
  pipeline?: DataRequirements;
}

/**
 * Default configurations for common chart types
 */
export const DefaultDataRequirements = {
  /** Default for stock price charts */
  stockPrice: {
    chartStatus: "active" as const,
    category: "raw" as const,
    requiredServices: ["yahoo_finance"],
    freshness: {
      warningThreshold: 24,
      errorThreshold: 48,
      blockOnStale: false,
      manualGracePeriod: 12,
    },
    refreshPolicy: {
      autoRefresh: true,
      refreshInterval: 24 * 60 * 60 * 1000, // 24 hours
      allowManualRefresh: true,
      refreshOnVisible: true,
      maxRetries: 3,
      retryBackoff: "exponential" as const,
    },
  },

  /** Default for crypto price charts */
  cryptoPrice: {
    chartStatus: "active" as const,
    category: "raw" as const,
    requiredServices: ["yahoo_finance"],
    freshness: {
      warningThreshold: 6,
      errorThreshold: 24,
      blockOnStale: false,
      manualGracePeriod: 6,
    },
    refreshPolicy: {
      autoRefresh: false,
      refreshInterval: 24 * 60 * 60 * 1000, // 24 hours
      allowManualRefresh: true,
      refreshOnVisible: true,
      maxRetries: 2,
      retryBackoff: "exponential" as const,
    },
  },

  /** Default for portfolio charts */
  portfolio: {
    chartStatus: "frozen" as const,
    category: "portfolio" as const,
    requiredServices: ["trade_history"],
    freshness: {
      warningThreshold: 24,
      errorThreshold: 72,
      blockOnStale: false,
      manualGracePeriod: 48,
    },
    refreshPolicy: {
      autoRefresh: false,
      refreshInterval: 24 * 60 * 60 * 1000, // 24 hours
      allowManualRefresh: true,
      refreshOnVisible: true,
      maxRetries: 1,
      retryBackoff: "linear" as const,
    },
  },
} as const;
