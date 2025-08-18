/**
 * Data Status Dashboard Component
 * 
 * Comprehensive dashboard showing the status of all chart data dependencies
 * with bulk refresh capabilities and dependency management.
 */

import React, { useState } from "react";
import type { ChartType } from "@/types/ChartTypes";
import { useDataStatusManager } from "@/hooks/useEnhancedPortfolioData";
import { DataStatusIndicator } from "./DataStatusIndicator";

interface DataStatusDashboardProps {
  className?: string;
  showCompact?: boolean;
}

export const DataStatusDashboard: React.FC<DataStatusDashboardProps> = ({
  className = "",
  showCompact = false,
}) => {
  const { allStatuses, loading, getStatusSummary, getStaleCharts, refreshAll } = useDataStatusManager();
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshResults, setRefreshResults] = useState<string[]>([]);

  const statusSummary = getStatusSummary();
  const staleCharts = getStaleCharts();

  const handleRefreshAll = async (priority: "low" | "normal" | "high" = "normal") => {
    setIsRefreshing(true);
    setRefreshResults([]);

    try {
      const results = await refreshAll(priority);
      const resultMessages = results.map((result, index) => {
        if (result.status === "fulfilled") {
          return result.value.success 
            ? `Chart ${index + 1}: Success`
            : `Chart ${index + 1}: ${result.value.error?.message || "Failed"}`;
        } else {
          return `Chart ${index + 1}: ${result.reason}`;
        }
      });
      
      setRefreshResults(resultMessages);
    } catch (error) {
      setRefreshResults([`Bulk refresh failed: ${error}`]);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleRefreshStale = async () => {
    setIsRefreshing(true);
    setRefreshResults([]);

    try {
      // Only refresh stale charts
      const results = await refreshAll("high");
      setRefreshResults([`Refreshed ${staleCharts.length} stale charts`]);
    } catch (error) {
      setRefreshResults([`Stale refresh failed: ${error}`]);
    } finally {
      setIsRefreshing(false);
    }
  };

  if (loading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="bg-gray-200 dark:bg-gray-700 h-20 rounded-lg"></div>
      </div>
    );
  }

  if (showCompact) {
    return (
      <div className={`bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm ${className}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
              Data Status
            </h3>
            <div className="flex items-center space-x-3 text-xs">
              <span className="text-green-600 dark:text-green-400">
                ● {statusSummary.available} Available
              </span>
              {statusSummary.stale > 0 && (
                <span className="text-yellow-600 dark:text-yellow-400">
                  ◐ {statusSummary.stale} Stale
                </span>
              )}
              {statusSummary.error > 0 && (
                <span className="text-red-600 dark:text-red-400">
                  ✕ {statusSummary.error} Errors
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {staleCharts.length > 0 && (
              <button
                onClick={handleRefreshStale}
                disabled={isRefreshing}
                className="px-2 py-1 text-xs bg-yellow-600 text-white rounded hover:bg-yellow-700 disabled:opacity-50"
              >
                Refresh Stale ({staleCharts.length})
              </button>
            )}
            <button
              onClick={() => handleRefreshAll("normal")}
              disabled={isRefreshing}
              className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isRefreshing ? "Refreshing..." : "Refresh All"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const chartTypes: ChartType[] = Array.from(allStatuses.keys());

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg shadow-sm ${className}`}>
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Chart Data Dependencies
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Monitor and manage data sources for all charts
            </p>
          </div>

          <div className="flex items-center space-x-3">
            {staleCharts.length > 0 && (
              <button
                onClick={handleRefreshStale}
                disabled={isRefreshing}
                className="px-3 py-2 text-sm bg-yellow-600 text-white rounded hover:bg-yellow-700 disabled:opacity-50"
              >
                Refresh Stale ({staleCharts.length})
              </button>
            )}
            <button
              onClick={() => handleRefreshAll("high")}
              disabled={isRefreshing}
              className="px-3 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isRefreshing ? "Refreshing..." : "Refresh All"}
            </button>
          </div>
        </div>

        {/* Status Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {statusSummary.total}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Total Charts</div>
          </div>

          <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {statusSummary.available}
            </div>
            <div className="text-sm text-green-700 dark:text-green-300">Available</div>
          </div>

          <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
              {statusSummary.stale}
            </div>
            <div className="text-sm text-yellow-700 dark:text-yellow-300">Stale</div>
          </div>

          <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
            <div className="text-2xl font-bold text-red-600 dark:text-red-400">
              {statusSummary.error + statusSummary.missing}
            </div>
            <div className="text-sm text-red-700 dark:text-red-300">Issues</div>
          </div>
        </div>

        {/* Individual Chart Status */}
        <div className="space-y-3">
          <h3 className="text-md font-medium text-gray-900 dark:text-gray-100 mb-3">
            Chart Status Details
          </h3>
          
          {chartTypes.map((chartType) => (
            <div key={chartType} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="text-sm font-medium text-gray-900 dark:text-gray-100 capitalize">
                  {chartType.replace(/-/g, " ")}
                </div>
              </div>
              
              <DataStatusIndicator
                chartType={chartType}
                compact={true}
                showRefreshButton={true}
                className="flex-shrink-0"
              />
            </div>
          ))}
        </div>

        {/* Refresh Results */}
        {refreshResults.length > 0 && (
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <h4 className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2">
              Refresh Results
            </h4>
            <div className="space-y-1">
              {refreshResults.map((result, index) => (
                <div key={index} className="text-sm text-blue-800 dark:text-blue-200">
                  {result}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stale Charts Warning */}
        {staleCharts.length > 0 && (
          <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
            <div className="flex items-center space-x-2">
              <span className="text-yellow-600 dark:text-yellow-400">⚠️</span>
              <h4 className="text-sm font-medium text-yellow-900 dark:text-yellow-100">
                Stale Data Warning
              </h4>
            </div>
            <p className="text-sm text-yellow-800 dark:text-yellow-200 mt-1">
              {staleCharts.length} chart{staleCharts.length > 1 ? "s have" : " has"} stale data that may affect accuracy.
              Consider refreshing: {staleCharts.map(chart => chart.replace(/-/g, " ")).join(", ")}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};