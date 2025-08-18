/**
 * Data Status Indicator Component
 *
 * Displays the status of chart data sources with visual indicators
 * and provides refresh controls where applicable.
 */

import React, { useState } from "react";
import type { ChartType } from "@/types/ChartTypes";
import type { DataSourceStatus } from "@/types/DataDependencyTypes";
import { useChartDataManager } from "@/hooks/useEnhancedPortfolioData";

interface DataStatusIndicatorProps {
  chartType: ChartType;
  compact?: boolean;
  showRefreshButton?: boolean;
  className?: string;
}

export const DataStatusIndicator: React.FC<DataStatusIndicatorProps> = ({
  chartType,
  compact = false,
  showRefreshButton = true,
  className = "",
}) => {
  const { dataStatus, refreshCapability, isRefreshing, canRefresh, refresh } =
    useChartDataManager(chartType);
  const [showDetails, setShowDetails] = useState(false);

  if (!dataStatus) {
    return null;
  }

  const getStatusColor = (status: DataSourceStatus["status"]) => {
    switch (status) {
      case "available":
        return "text-green-600 dark:text-green-400";
      case "stale":
        return "text-yellow-600 dark:text-yellow-400";
      case "missing":
        return "text-gray-500 dark:text-gray-400";
      case "error":
        return "text-red-600 dark:text-red-400";
      default:
        return "text-gray-500 dark:text-gray-400";
    }
  };

  const getStatusIcon = (status: DataSourceStatus["status"]) => {
    switch (status) {
      case "available":
        return "●";
      case "stale":
        return "◐";
      case "missing":
        return "○";
      case "error":
        return "✕";
      default:
        return "?";
    }
  };

  const getStatusLabel = (status: DataSourceStatus["status"]) => {
    switch (status) {
      case "available":
        return "Data Available";
      case "stale":
        return "Data Stale";
      case "missing":
        return "Data Missing";
      case "error":
        return "Data Error";
      default:
        return "Unknown Status";
    }
  };

  const formatAge = (ageHours: number): string => {
    if (ageHours < 1) {
      const minutes = Math.floor(ageHours * 60);
      return `${minutes}m ago`;
    } else if (ageHours < 24) {
      const hours = Math.floor(ageHours);
      return `${hours}h ago`;
    } else {
      const days = Math.floor(ageHours / 24);
      return `${days}d ago`;
    }
  };

  const handleRefresh = async () => {
    if (canRefresh && !isRefreshing) {
      try {
        await refresh({ priority: "high" });
      } catch {
        // Failed to refresh data
      }
    }
  };

  const statusColor = getStatusColor(dataStatus.status);
  const statusIcon = getStatusIcon(dataStatus.status);
  const statusLabel = getStatusLabel(dataStatus.status);

  if (compact) {
    return (
      <div className={`inline-flex items-center space-x-1 ${className}`}>
        <span className={`text-sm ${statusColor}`} title={statusLabel}>
          {statusIcon}
        </span>
        {showRefreshButton && canRefresh && (
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="text-xs text-blue-600 hover:underline disabled:opacity-50 dark:text-blue-400"
            title="Refresh data"
          >
            {isRefreshing ? "..." : "↻"}
          </button>
        )}
      </div>
    );
  }

  return (
    <div className={`rounded-lg bg-gray-50 p-3 dark:bg-gray-800 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className={`text-lg ${statusColor}`} title={statusLabel}>
            {statusIcon}
          </span>
          <div>
            <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {statusLabel}
            </div>
            <div className="text-xs text-gray-600 dark:text-gray-400">
              {dataStatus.lastUpdated
                ? `Updated ${formatAge(dataStatus.ageHours)}`
                : "No update info"}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {showRefreshButton && canRefresh && (
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="rounded bg-blue-600 px-3 py-1 text-sm text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              title={refreshCapability?.reason}
            >
              {isRefreshing ? "Refreshing..." : "Refresh"}
            </button>
          )}

          <button
            onClick={() => setShowDetails(!showDetails)}
            className="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            {showDetails ? "Hide" : "Details"}
          </button>
        </div>
      </div>

      {showDetails && (
        <div className="mt-3 border-t border-gray-200 pt-3 dark:border-gray-600">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="font-medium text-gray-700 dark:text-gray-300">
                Source:
              </span>
              <span className="ml-1 text-gray-600 dark:text-gray-400">
                {dataStatus.lastUpdateSource || "Unknown"}
              </span>
            </div>

            <div>
              <span className="font-medium text-gray-700 dark:text-gray-300">
                Retries:
              </span>
              <span className="ml-1 text-gray-600 dark:text-gray-400">
                {dataStatus.retryCount}
              </span>
            </div>

            {refreshCapability && (
              <>
                <div>
                  <span className="font-medium text-gray-700 dark:text-gray-300">
                    Can Refresh:
                  </span>
                  <span className="ml-1 text-gray-600 dark:text-gray-400">
                    {refreshCapability.canRefresh ? "Yes" : "No"}
                  </span>
                </div>

                <div>
                  <span className="font-medium text-gray-700 dark:text-gray-300">
                    Methods:
                  </span>
                  <span className="ml-1 text-gray-600 dark:text-gray-400">
                    {refreshCapability.availableMethods.join(", ")}
                  </span>
                </div>
              </>
            )}

            {dataStatus.error && (
              <div className="col-span-2">
                <span className="font-medium text-gray-700 dark:text-gray-300">
                  Error:
                </span>
                <div className="mt-1 rounded bg-red-50 p-2 text-xs text-red-600 dark:bg-red-900/20 dark:text-red-400">
                  {dataStatus.error}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
