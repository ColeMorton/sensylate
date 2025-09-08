import React from "react";
import type { ChartContainerProps } from "@/types/ChartTypes";

const ChartContainer: React.FC<ChartContainerProps> = ({
  title,
  category,
  description,
  children,
  className = "",
  titleOnly = false,
}) => {
  // Detect if we're in dashboard context by checking for photo-booth-chart class
  const isDashboardContext = className.includes("photo-booth-chart");

  // Use min-h-0 for dashboards, min-h-[500px] for regular pages
  const heightClass = isDashboardContext ? "min-h-0" : "min-h-[400px]";

  return (
    <div
      className={`bg-body dark:bg-darkmode-body flex min-h-0 flex-1 flex-col rounded-lg p-6 ${isDashboardContext ? "" : "shadow-sm transition-all duration-300 hover:shadow-lg"} ${className}`}
    >
      {!titleOnly && category && (
        <div className="mb-4">
          <span className="text-text/80 text-xs font-medium tracking-wider uppercase dark:text-gray-400">
            {category}
          </span>
        </div>
      )}

      {!titleOnly && (
        <h3 className="text-dark mb-3 text-xl font-semibold dark:text-white">
          {title}
        </h3>
      )}

      {!titleOnly && description && (
        <p className="text-text mb-6 dark:text-gray-300">{description}</p>
      )}

      <div
        className={`chart-container flex h-full ${heightClass} w-full flex-col`}
      >
        {children}
      </div>
    </div>
  );
};

export default ChartContainer;
