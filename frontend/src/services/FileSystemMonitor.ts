/**
 * File System Monitor Service
 *
 * Monitors file system changes for manual data sources and triggers
 * appropriate notifications when data files are updated.
 */

import type { ChartType } from "@/types/ChartTypes";

/**
 * File change event
 */
export interface FileChangeEvent {
  filePath: string;
  changeType: "created" | "modified" | "deleted";
  timestamp: number;
  size?: number;
  lastModified?: number;
}

/**
 * File watcher configuration
 */
export interface FileWatchConfig {
  filePath: string;
  chartTypes: ChartType[];
  pollInterval?: number;
  debounceMs?: number;
}

/**
 * File status information
 */
export interface FileStatus {
  exists: boolean;
  size: number;
  lastModified: number;
  permissions: {
    readable: boolean;
    writable: boolean;
  };
}

/**
 * File System Monitor class
 */
export class FileSystemMonitor {
  private watchers: Map<
    string,
    {
      config: FileWatchConfig;
      lastStatus: FileStatus | null;
      timer: number | null;
      listeners: Set<(event: FileChangeEvent) => void>;
    }
  > = new Map();

  private globalListeners: Set<(event: FileChangeEvent) => void> = new Set();
  private isEnabled = true;
  private pollInterval = 5000; // 5 seconds default

  constructor(enabled = true) {
    this.isEnabled = enabled;

    if (this.isEnabled) {
      this.startGlobalMonitoring();
    }
  }

  /**
   * Start global monitoring for all registered watchers
   */
  private startGlobalMonitoring(): void {
    // Global check every 30 seconds for all watchers
    setInterval(() => {
      this.checkAllWatchers();
    }, 30000);
  }

  /**
   * Check all active watchers for changes
   */
  private async checkAllWatchers(): Promise<void> {
    const promises = Array.from(this.watchers.keys()).map((filePath) =>
      this.checkFileStatus(filePath),
    );

    await Promise.allSettled(promises);
  }

  /**
   * Add file watcher
   */
  public addWatcher(config: FileWatchConfig): void {
    if (!this.isEnabled) {
      // FileSystemMonitor is disabled
      return;
    }

    const { filePath, pollInterval = this.pollInterval } = config;

    // Remove existing watcher if present
    this.removeWatcher(filePath);

    const watcher = {
      config,
      lastStatus: null,
      timer: null,
      listeners: new Set<(event: FileChangeEvent) => void>(),
    };

    this.watchers.set(filePath, watcher);

    // Start polling for this file
    this.startPolling(filePath, pollInterval);

    // Initial check
    this.checkFileStatus(filePath);
  }

  /**
   * Remove file watcher
   */
  public removeWatcher(filePath: string): void {
    const watcher = this.watchers.get(filePath);
    if (watcher) {
      if (watcher.timer !== null) {
        clearInterval(watcher.timer);
      }
      this.watchers.delete(filePath);
    }
  }

  /**
   * Start polling for a specific file
   */
  private startPolling(filePath: string, interval: number): void {
    const watcher = this.watchers.get(filePath);
    if (!watcher) {
      return;
    }

    watcher.timer = window.setInterval(() => {
      this.checkFileStatus(filePath);
    }, interval);
  }

  /**
   * Check file status and detect changes
   */
  private async checkFileStatus(filePath: string): Promise<void> {
    const watcher = this.watchers.get(filePath);
    if (!watcher) {
      return;
    }

    try {
      const currentStatus = await this.getFileStatus(filePath);
      const previousStatus = watcher.lastStatus;

      // Detect changes
      if (this.hasFileChanged(previousStatus, currentStatus)) {
        const changeType = this.determineChangeType(
          previousStatus,
          currentStatus,
        );

        const event: FileChangeEvent = {
          filePath,
          changeType,
          timestamp: Date.now(),
          size: currentStatus?.size,
          lastModified: currentStatus?.lastModified,
        };

        // Debounce rapid changes
        this.debounceAndEmit(filePath, event);
      }

      watcher.lastStatus = currentStatus;
    } catch {
      // Error checking file status

      // Emit error event if file was previously accessible
      if (watcher.lastStatus?.exists) {
        const event: FileChangeEvent = {
          filePath,
          changeType: "deleted",
          timestamp: Date.now(),
        };

        this.debounceAndEmit(filePath, event);
      }

      watcher.lastStatus = null;
    }
  }

  /**
   * Get file status information
   */
  private async getFileStatus(filePath: string): Promise<FileStatus | null> {
    // In a real browser environment, we can't directly access file system
    // This would need to be implemented via a backend API or Node.js service
    // For now, we'll simulate file status checking

    return this.simulateFileStatus(filePath);
  }

  /**
   * Simulate file status for demonstration
   */
  private simulateFileStatus(filePath: string): FileStatus | null {
    // Simulate different file states based on path patterns
    const now = Date.now();

    // Simulate live signals data being updated more frequently
    if (filePath.includes("live_signals")) {
      const randomAge = Math.random() * 3600000; // Random age up to 1 hour
      return {
        exists: true,
        size: Math.floor(Math.random() * 100000) + 50000, // 50KB - 150KB
        lastModified: now - randomAge,
        permissions: {
          readable: true,
          writable: false,
        },
      };
    }

    // Simulate portfolio data being updated less frequently
    if (filePath.includes("portfolio")) {
      const randomAge = Math.random() * 86400000; // Random age up to 24 hours
      return {
        exists: true,
        size: Math.floor(Math.random() * 50000) + 20000, // 20KB - 70KB
        lastModified: now - randomAge,
        permissions: {
          readable: true,
          writable: false,
        },
      };
    }

    // Simulate trade history being updated occasionally
    if (filePath.includes("trade_history")) {
      const randomAge = Math.random() * 172800000; // Random age up to 48 hours
      return {
        exists: Math.random() > 0.1, // 90% chance file exists
        size: Math.floor(Math.random() * 200000) + 100000, // 100KB - 300KB
        lastModified: now - randomAge,
        permissions: {
          readable: true,
          writable: false,
        },
      };
    }

    // Default simulation
    return {
      exists: Math.random() > 0.05, // 95% chance file exists
      size: Math.floor(Math.random() * 100000) + 10000,
      lastModified: now - Math.random() * 86400000,
      permissions: {
        readable: true,
        writable: false,
      },
    };
  }

  /**
   * Check if file has changed
   */
  private hasFileChanged(
    previous: FileStatus | null,
    current: FileStatus | null,
  ): boolean {
    if (!previous && !current) {
      return false;
    }
    if (!previous && current) {
      return true;
    }
    if (previous && !current) {
      return true;
    }

    if (previous && current) {
      return (
        previous.exists !== current.exists ||
        previous.size !== current.size ||
        previous.lastModified !== current.lastModified
      );
    }

    return false;
  }

  /**
   * Determine the type of change
   */
  private determineChangeType(
    previous: FileStatus | null,
    current: FileStatus | null,
  ): FileChangeEvent["changeType"] {
    if (!previous && current?.exists) {
      return "created";
    }
    if (previous?.exists && !current?.exists) {
      return "deleted";
    }
    if (previous && current && current.exists) {
      return "modified";
    }
    return "modified";
  }

  /**
   * Debounce and emit file change events
   */
  private debounceAndEmit(filePath: string, event: FileChangeEvent): void {
    const watcher = this.watchers.get(filePath);
    if (!watcher) {
      return;
    }

    const debounceMs = watcher.config.debounceMs || 1000;

    // Clear any existing timeout
    if ((watcher as any).debounceTimer) {
      clearTimeout((watcher as any).debounceTimer);
    }

    // Set new timeout
    (watcher as any).debounceTimer = setTimeout(() => {
      this.emitFileChangeEvent(filePath, event);
    }, debounceMs);
  }

  /**
   * Emit file change event to listeners
   */
  private emitFileChangeEvent(filePath: string, event: FileChangeEvent): void {
    const watcher = this.watchers.get(filePath);
    if (!watcher) {
      return;
    }

    // Notify file-specific listeners
    watcher.listeners.forEach((listener) => {
      try {
        listener(event);
      } catch {
        // Error in file change listener
      }
    });

    // Notify global listeners
    this.globalListeners.forEach((listener) => {
      try {
        listener(event);
      } catch {
        // Error in global file change listener
      }
    });
  }

  /**
   * Add listener for specific file changes
   */
  public addFileListener(
    filePath: string,
    listener: (event: FileChangeEvent) => void,
  ): () => void {
    const watcher = this.watchers.get(filePath);
    if (!watcher) {
      // No watcher found for file
      return () => {}; // Return no-op cleanup function
    }

    watcher.listeners.add(listener);

    // Return cleanup function
    return () => {
      watcher.listeners.delete(listener);
    };
  }

  /**
   * Add global listener for all file changes
   */
  public addGlobalListener(
    listener: (event: FileChangeEvent) => void,
  ): () => void {
    this.globalListeners.add(listener);

    // Return cleanup function
    return () => {
      this.globalListeners.delete(listener);
    };
  }

  /**
   * Get current status of all monitored files
   */
  public async getAllFileStatuses(): Promise<Map<string, FileStatus | null>> {
    const statuses = new Map<string, FileStatus | null>();

    const promises = Array.from(this.watchers.keys()).map(async (filePath) => {
      const status = await this.getFileStatus(filePath);
      statuses.set(filePath, status);
    });

    await Promise.allSettled(promises);
    return statuses;
  }

  /**
   * Get list of monitored file paths
   */
  public getMonitoredFiles(): string[] {
    return Array.from(this.watchers.keys());
  }

  /**
   * Get watcher configuration for a file
   */
  public getWatcherConfig(filePath: string): FileWatchConfig | undefined {
    return this.watchers.get(filePath)?.config;
  }

  /**
   * Check if monitoring is enabled
   */
  public isMonitoringEnabled(): boolean {
    return this.isEnabled;
  }

  /**
   * Enable/disable monitoring
   */
  public setEnabled(enabled: boolean): void {
    if (this.isEnabled === enabled) {
      return;
    }

    this.isEnabled = enabled;

    if (enabled) {
      this.startGlobalMonitoring();
      // Restart all individual watchers
      this.watchers.forEach((watcher, filePath) => {
        if (watcher.timer === null) {
          this.startPolling(
            filePath,
            watcher.config.pollInterval || this.pollInterval,
          );
        }
      });
    } else {
      // Stop all watchers
      this.watchers.forEach((watcher) => {
        if (watcher.timer !== null) {
          clearInterval(watcher.timer);
          watcher.timer = null;
        }
      });
    }
  }

  /**
   * Force check all watchers immediately
   */
  public async forceCheckAll(): Promise<void> {
    if (!this.isEnabled) {
      return;
    }
    await this.checkAllWatchers();
  }

  /**
   * Cleanup all watchers and listeners
   */
  public cleanup(): void {
    this.watchers.forEach((watcher, filePath) => {
      this.removeWatcher(filePath);
    });
    this.globalListeners.clear();
    this.isEnabled = false;
  }
}

// Export singleton instance
export const fileSystemMonitor = new FileSystemMonitor();
export default fileSystemMonitor;
