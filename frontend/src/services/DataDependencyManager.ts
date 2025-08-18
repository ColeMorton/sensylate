/**
 * Data Dependency Manager
 *
 * Coordinates chart data dependencies, refresh policies, and data source management.
 * Works with ChartDataService to provide intelligent data refresh capabilities.
 */

import type { ChartType } from "@/types/ChartTypes";

import type {
  DataDependencyRegistry,
  DataDependencyRegistryEntry,
  DataSourceStatus,
  DataRefreshRequest,
  DataRefreshResult,
  ChartRefreshCapability,
  ChartDataDependency,
} from "@/types/DataDependencyTypes";

// Import the configuration
import chartDependencyConfig from "@/config/chart-data-dependencies.json";

/**
 * Data Dependency Manager Service
 */
export class DataDependencyManager {
  private registry: DataDependencyRegistry;
  private refreshQueue: Map<ChartType, DataRefreshRequest> = new Map();
  private activeRefreshes: Set<ChartType> = new Set();
  private statusCache: Map<ChartType, DataSourceStatus> = new Map();
  private fileWatchers: Map<string, number> = new Map();

  constructor() {
    this.registry = this.initializeRegistry();
    this.startPeriodicStatusChecks();

    // Initialize file watching if enabled
    if (this.registry.settings.enableFileWatching) {
      this.initializeFileWatching();
    }
  }

  /**
   * Initialize the data dependency registry from configuration
   */
  private initializeRegistry(): DataDependencyRegistry {
    const config = chartDependencyConfig;
    const entries = new Map<ChartType, DataDependencyRegistryEntry>();

    // Convert configuration to registry entries
    Object.entries(config.dependencies).forEach(([chartType, dependency]) => {
      const entry: DataDependencyRegistryEntry = {
        id: `${chartType}_${Date.now()}`,
        config: dependency as ChartDataDependency,
        status: this.createInitialStatus(),
        capabilities: this.assessRefreshCapability(
          dependency as ChartDataDependency,
        ),
        configuredAt: Date.now(),
        lastChecked: Date.now(),
      };

      entries.set(chartType as ChartType, entry);
    });

    return {
      entries,
      settings: {
        defaultCacheDuration: config.settings.defaultCacheDuration,
        enableFileWatching: config.settings.enableFileWatching,
        enableCLIDiscovery: config.settings.enableCLIDiscovery,
        maxConcurrentRefresh: config.settings.maxConcurrentRefresh,
      },
      version: config.version,
    };
  }

  /**
   * Create initial data source status
   */
  private createInitialStatus(): DataSourceStatus {
    return {
      status: "available",
      lastUpdated: Date.now(),
      ageHours: 0,
      retryCount: 0,
      refreshing: false,
    };
  }

  /**
   * Assess refresh capability for a chart data dependency
   */
  private assessRefreshCapability(
    dependency: ChartDataDependency,
  ): ChartRefreshCapability {
    const { primarySource, refreshPolicy } = dependency;

    let canRefresh = false;
    let reason = "";
    const availableMethods = [primarySource.refreshMethod];

    switch (primarySource.type) {
      case "static":
        canRefresh = false;
        reason = "Static data source - no refresh available";
        break;

      case "manual":
        canRefresh = refreshPolicy.allowManualRefresh;
        reason = canRefresh
          ? "Manual refresh available"
          : "Manual refresh disabled";
        break;

      case "cli-api":
        canRefresh = Boolean(
          primarySource.cliService && refreshPolicy.autoRefresh,
        );
        reason = canRefresh
          ? "API refresh available"
          : "CLI service not configured";
        break;

      case "hybrid":
        canRefresh = Boolean(
          primarySource.cliService || refreshPolicy.allowManualRefresh,
        );
        reason = canRefresh
          ? "Hybrid refresh available"
          : "No refresh methods available";
        break;

      default:
        canRefresh = false;
        reason = "Unknown data source type";
    }

    return {
      canRefresh,
      reason,
      availableMethods,
      estimatedDuration: this.estimateRefreshDuration(primarySource.type),
      requiresAuth: primarySource.cliService ? true : false,
    };
  }

  /**
   * Estimate refresh duration based on source type
   */
  private estimateRefreshDuration(sourceType: string): number {
    switch (sourceType) {
      case "static":
        return 0;
      case "manual":
        return 1000; // File check
      case "cli-api":
        return 5000; // API call
      case "hybrid":
        return 7000; // API + file operations
      default:
        return 3000;
    }
  }

  /**
   * Get data dependency information for a chart type
   */
  public getDependencyInfo(
    chartType: ChartType,
  ): DataDependencyRegistryEntry | undefined {
    return this.registry.entries.get(chartType);
  }

  /**
   * Get current data source status for a chart type
   */
  public getDataStatus(chartType: ChartType): DataSourceStatus {
    const cached = this.statusCache.get(chartType);
    if (cached) {
      return cached;
    }

    const entry = this.registry.entries.get(chartType);
    if (!entry) {
      return {
        status: "missing",
        ageHours: Infinity,
        error: "Chart dependency not configured",
        retryCount: 0,
        refreshing: false,
      };
    }

    return this.checkDataFreshness(entry);
  }

  /**
   * Check data freshness for a registry entry
   */
  private checkDataFreshness(
    entry: DataDependencyRegistryEntry,
  ): DataSourceStatus {
    const { config } = entry;
    const now = Date.now();

    // For manual/file-based sources, check file modification time
    if (
      config.primarySource.type === "manual" &&
      typeof config.primarySource.location === "string"
    ) {
      return this.checkFileStatus(
        config.primarySource.location,
        config.freshness,
      );
    }

    // For API sources, check cache age
    if (config.primarySource.type === "cli-api") {
      return this.checkCacheStatus(entry, now);
    }

    // Default status
    return {
      status: "available",
      lastUpdated: now,
      ageHours: 0,
      retryCount: 0,
      refreshing: false,
    };
  }

  /**
   * Check file-based data source status
   */
  private checkFileStatus(
    filePath: string,
    freshnessConfig: any,
  ): DataSourceStatus {
    // In a real implementation, this would check file modification time
    // For now, we'll simulate based on configuration
    const now = Date.now();
    const simulatedAge = Math.random() * 48; // Random age up to 48 hours

    let status: DataSourceStatus["status"] = "available";

    if (simulatedAge > freshnessConfig.errorThreshold) {
      status = "error";
    } else if (simulatedAge > freshnessConfig.warningThreshold) {
      status = "stale";
    }

    return {
      status,
      lastUpdated: now - simulatedAge * 3600000, // Convert hours to milliseconds
      ageHours: simulatedAge,
      retryCount: 0,
      refreshing: false,
      lastUpdateSource: "manual",
    };
  }

  /**
   * Check cache-based data source status
   */
  private checkCacheStatus(
    entry: DataDependencyRegistryEntry,
    now: number,
  ): DataSourceStatus {
    const ageMs = now - entry.status.lastUpdated!;
    const ageHours = ageMs / (1000 * 60 * 60);

    let status: DataSourceStatus["status"] = "available";

    if (ageHours > entry.config.freshness.errorThreshold) {
      status = "error";
    } else if (ageHours > entry.config.freshness.warningThreshold) {
      status = "stale";
    }

    return {
      status,
      lastUpdated: entry.status.lastUpdated,
      ageHours,
      retryCount: entry.status.retryCount,
      refreshing: entry.status.refreshing,
      lastUpdateSource: "api",
    };
  }

  /**
   * Check if chart data can be refreshed
   */
  public canRefreshChart(chartType: ChartType): boolean {
    const entry = this.registry.entries.get(chartType);
    return entry?.capabilities.canRefresh ?? false;
  }

  /**
   * Get refresh capability details for a chart
   */
  public getRefreshCapability(
    chartType: ChartType,
  ): ChartRefreshCapability | undefined {
    const entry = this.registry.entries.get(chartType);
    return entry?.capabilities;
  }

  /**
   * Request data refresh for a chart type
   */
  public async requestRefresh(
    request: DataRefreshRequest,
  ): Promise<DataRefreshResult> {
    const { chartType } = request;

    // Check if refresh is already in progress
    if (this.activeRefreshes.has(chartType)) {
      return {
        success: false,
        status: this.getDataStatus(chartType),
        duration: 0,
        error: {
          message: "Refresh already in progress",
          code: "REFRESH_IN_PROGRESS",
          retryable: true,
        },
        source: this.registry.entries.get(chartType)!.config.primarySource,
      };
    }

    // Check refresh capability
    const capability = this.getRefreshCapability(chartType);
    if (!capability?.canRefresh) {
      return {
        success: false,
        status: this.getDataStatus(chartType),
        duration: 0,
        error: {
          message: capability?.reason || "Refresh not available",
          code: "REFRESH_NOT_AVAILABLE",
          retryable: false,
        },
        source: this.registry.entries.get(chartType)!.config.primarySource,
      };
    }

    // Add to refresh queue if at capacity
    const activeCount = this.activeRefreshes.size;
    if (activeCount >= this.registry.settings.maxConcurrentRefresh) {
      this.refreshQueue.set(chartType, request);
      return {
        success: false,
        status: this.getDataStatus(chartType),
        duration: 0,
        error: {
          message: "Refresh queued - at maximum concurrent refresh limit",
          code: "REFRESH_QUEUED",
          retryable: true,
        },
        source: this.registry.entries.get(chartType)!.config.primarySource,
      };
    }

    // Execute refresh
    return this.executeRefresh(chartType, request);
  }

  /**
   * Execute data refresh for a chart type
   */
  private async executeRefresh(
    chartType: ChartType,
    request: DataRefreshRequest,
  ): Promise<DataRefreshResult> {
    const entry = this.registry.entries.get(chartType)!;
    const startTime = Date.now();

    this.activeRefreshes.add(chartType);

    // Update status to refreshing
    const currentStatus = this.getDataStatus(chartType);
    currentStatus.refreshing = true;
    this.statusCache.set(chartType, currentStatus);

    try {
      // Progress callback for user feedback
      if (request.onProgress) {
        request.onProgress({
          stage: "connecting",
          progress: 0,
          message: "Initiating data refresh...",
        });
      }

      // Simulate refresh based on data source type
      const result = await this.simulateDataRefresh(entry, request);

      // Update status cache
      const updatedStatus: DataSourceStatus = {
        status: "available",
        lastUpdated: Date.now(),
        ageHours: 0,
        retryCount: 0,
        refreshing: false,
        lastUpdateSource:
          entry.config.primarySource.type === "cli-api" ? "api" : "manual",
      };

      this.statusCache.set(chartType, updatedStatus);
      entry.status = updatedStatus;
      entry.lastChecked = Date.now();

      const duration = Date.now() - startTime;

      // Complete callback
      if (request.onComplete) {
        request.onComplete({
          success: true,
          status: updatedStatus,
          recordsUpdated: result.recordsUpdated,
          duration,
          source: entry.config.primarySource,
        });
      }

      return {
        success: true,
        status: updatedStatus,
        recordsUpdated: result.recordsUpdated,
        duration,
        source: entry.config.primarySource,
      };
    } catch (error) {
      // Handle refresh failure
      const duration = Date.now() - startTime;
      const errorStatus = currentStatus;
      errorStatus.refreshing = false;
      errorStatus.retryCount += 1;
      errorStatus.error =
        error instanceof Error ? error.message : "Unknown error";

      this.statusCache.set(chartType, errorStatus);

      return {
        success: false,
        status: errorStatus,
        duration,
        error: {
          message: errorStatus.error,
          code: "REFRESH_FAILED",
          retryable:
            errorStatus.retryCount < entry.config.refreshPolicy.maxRetries,
        },
        source: entry.config.primarySource,
      };
    } finally {
      this.activeRefreshes.delete(chartType);

      // Process queue if there are waiting requests
      this.processRefreshQueue();
    }
  }

  /**
   * Simulate data refresh (replace with actual refresh logic)
   */
  private async simulateDataRefresh(
    entry: DataDependencyRegistryEntry,
    request: DataRefreshRequest,
  ) {
    const { primarySource } = entry.config;

    // Simulate different refresh types
    if (request.onProgress) {
      request.onProgress({
        stage: "downloading",
        progress: 25,
        message: `Fetching data from ${primarySource.type} source...`,
      });
    }

    // Simulate network/file operation delay
    await new Promise((resolve) =>
      setTimeout(resolve, primarySource.type === "cli-api" ? 2000 : 500),
    );

    if (request.onProgress) {
      request.onProgress({
        stage: "parsing",
        progress: 75,
        message: "Processing data...",
      });
    }

    await new Promise((resolve) => setTimeout(resolve, 300));

    if (request.onProgress) {
      request.onProgress({
        stage: "caching",
        progress: 100,
        message: "Caching updated data...",
      });
    }

    // Return simulated result
    return {
      recordsUpdated: Math.floor(Math.random() * 1000) + 100,
    };
  }

  /**
   * Process queued refresh requests
   */
  private processRefreshQueue(): void {
    if (this.refreshQueue.size === 0) {
      return;
    }

    const activeCount = this.activeRefreshes.size;
    const capacity = this.registry.settings.maxConcurrentRefresh - activeCount;

    if (capacity <= 0) {
      return;
    }

    // Process highest priority requests first
    const sortedQueue = Array.from(this.refreshQueue.entries())
      .sort((a, b) => {
        const priorityOrder = { high: 3, normal: 2, low: 1 };
        return (
          priorityOrder[b[1].priority || "normal"] -
          priorityOrder[a[1].priority || "normal"]
        );
      })
      .slice(0, capacity);

    sortedQueue.forEach(([chartType, request]) => {
      this.refreshQueue.delete(chartType);
      this.executeRefresh(chartType, request);
    });
  }

  /**
   * Initialize file watching for manual data sources
   */
  private initializeFileWatching(): void {
    // In a real implementation, this would set up file system watchers
    // For now, we'll simulate periodic checks
    setInterval(() => {
      this.checkAllFileBasedSources();
    }, 30000); // Check every 30 seconds
  }

  /**
   * Check all file-based data sources for changes
   */
  private checkAllFileBasedSources(): void {
    this.registry.entries.forEach((entry, chartType) => {
      if (entry.config.primarySource.type === "manual") {
        const status = this.checkDataFreshness(entry);
        this.statusCache.set(chartType, status);
      }
    });
  }

  /**
   * Start periodic status checks
   */
  private startPeriodicStatusChecks(): void {
    // Check status every 5 minutes
    setInterval(
      () => {
        this.updateAllDataStatus();
      },
      5 * 60 * 1000,
    );
  }

  /**
   * Update status for all registered chart data dependencies
   */
  private updateAllDataStatus(): void {
    this.registry.entries.forEach((entry, chartType) => {
      if (!this.activeRefreshes.has(chartType)) {
        const status = this.checkDataFreshness(entry);
        this.statusCache.set(chartType, status);
        entry.lastChecked = Date.now();
      }
    });
  }

  /**
   * Get all data source statuses
   */
  public getAllDataStatuses(): Map<ChartType, DataSourceStatus> {
    // Ensure all statuses are current
    this.updateAllDataStatus();
    return new Map(this.statusCache);
  }

  /**
   * Clear cache for a specific chart type
   */
  public clearCache(chartType: ChartType): void {
    this.statusCache.delete(chartType);
  }

  /**
   * Clear all caches
   */
  public clearAllCaches(): void {
    this.statusCache.clear();
  }
}

// Export singleton instance
export const dataDependencyManager = new DataDependencyManager();
export default dataDependencyManager;
