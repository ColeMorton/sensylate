import React, { useState, useEffect } from "react";
import { chartDataService } from "@/services/ChartDataService";

interface DataQualityStatus {
  overall: "healthy" | "warning" | "error";
  categories: {
    [key: string]: {
      status: "healthy" | "warning" | "error";
      recordCount: number;
      issues: string[];
      freshness: {
        isFresh: boolean;
        ageHours: number;
      };
    };
  };
  generatedAt: string;
}

interface DataQualityMonitorProps {
  compact?: boolean;
  showDetails?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number; // in milliseconds
}

const DataQualityMonitor: React.FC<DataQualityMonitorProps> = ({
  compact = false,
  showDetails = false,
  autoRefresh = true,
  refreshInterval = 300000, // 5 minutes
}) => {
  const [status, setStatus] = useState<DataQualityStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchDataQuality = async () => {
    try {
      setLoading(true);
      setError(null);

      const qualityReport = await chartDataService.getDataQualityReport();
      setStatus(qualityReport);
      setLastUpdated(new Date());
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to fetch data quality",
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDataQuality();

    if (autoRefresh) {
      const interval = setInterval(fetchDataQuality, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval]);

  const getStatusIcon = (status: "healthy" | "warning" | "error"): string => {
    switch (status) {
      case "healthy":
        return "✅";
      case "warning":
        return "⚠️";
      case "error":
        return "❌";
      default:
        return "❓";
    }
  };

  const getStatusColor = (status: "healthy" | "warning" | "error"): string => {
    switch (status) {
      case "healthy":
        return "text-green-600 dark:text-green-400";
      case "warning":
        return "text-yellow-600 dark:text-yellow-400";
      case "error":
        return "text-red-600 dark:text-red-400";
      default:
        return "text-gray-500";
    }
  };

  const formatAgeHours = (ageHours: number): string => {
    if (ageHours === Infinity) {
      return "Unknown";
    }
    if (ageHours < 1) {
      return "< 1 hour";
    }
    if (ageHours < 24) {
      return `${Math.round(ageHours)} hours`;
    }
    const days = Math.round(ageHours / 24);
    return `${days} day${days > 1 ? "s" : ""}`;
  };

  if (loading && !status) {
    return (
      <div
        className={`${compact ? "p-2" : "p-4"} rounded-lg bg-gray-100 dark:bg-gray-800`}
      >
        <div className="flex animate-pulse items-center space-x-2">
          <div className="h-4 w-4 rounded-full bg-gray-300 dark:bg-gray-600"></div>
          <div className="h-4 w-32 rounded bg-gray-300 dark:bg-gray-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className={`${compact ? "p-2" : "p-4"} rounded-lg border border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20`}
      >
        <div className="flex items-center space-x-2">
          <span className="text-red-600 dark:text-red-400">❌</span>
          <span className="text-sm text-red-700 dark:text-red-300">
            Data quality check failed: {error}
          </span>
        </div>
      </div>
    );
  }

  if (!status) {
    return null;
  }

  if (compact) {
    return (
      <div className="inline-flex items-center space-x-2 rounded-md bg-gray-100 px-3 py-1 text-sm dark:bg-gray-800">
        <span>{getStatusIcon(status.overall)}</span>
        <span className={getStatusColor(status.overall)}>
          Data: {status.overall}
        </span>
        {lastUpdated && (
          <span className="text-xs text-gray-500">
            Updated {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-900">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <span className="text-xl">{getStatusIcon(status.overall)}</span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Chart Data Quality
            </h3>
            <p
              className={`text-sm font-medium ${getStatusColor(status.overall)}`}
            >
              Overall Status:{" "}
              {status.overall.charAt(0).toUpperCase() + status.overall.slice(1)}
            </p>
          </div>
        </div>

        <button
          onClick={fetchDataQuality}
          disabled={loading}
          className="rounded-md bg-blue-500 px-3 py-1 text-sm text-white transition-colors hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? "Checking..." : "Refresh"}
        </button>
      </div>

      {showDetails && (
        <div className="space-y-3">
          {Object.entries(status.categories).map(([category, details]) => (
            <div
              key={category}
              className="rounded-md border border-gray-200 bg-gray-50 p-3 dark:border-gray-700 dark:bg-gray-800"
            >
              <div className="mb-2 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span>{getStatusIcon(details.status)}</span>
                  <span className="font-medium text-gray-900 capitalize dark:text-white">
                    {category.replace("_", " ")}
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  {details.recordCount} records
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span
                  className={`font-medium ${getStatusColor(details.status)}`}
                >
                  {details.status.charAt(0).toUpperCase() +
                    details.status.slice(1)}
                </span>
                <span className="text-gray-500">
                  Age: {formatAgeHours(details.freshness.ageHours)}
                </span>
              </div>

              {details.issues.length > 0 && (
                <div className="mt-2 rounded border border-yellow-200 bg-yellow-50 p-2 dark:border-yellow-800 dark:bg-yellow-900/20">
                  <p className="mb-1 text-xs font-medium text-yellow-800 dark:text-yellow-200">
                    Issues:
                  </p>
                  <ul className="space-y-1 text-xs text-yellow-700 dark:text-yellow-300">
                    {details.issues.map((issue, index) => (
                      <li key={index}>• {issue}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="mt-4 border-t border-gray-200 pt-3 dark:border-gray-700">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>
            Last checked: {lastUpdated ? lastUpdated.toLocaleString() : "Never"}
          </span>
          <span>
            Generated: {new Date(status.generatedAt).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  );
};

export default DataQualityMonitor;
