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
  return (
    <div
      className={`bg-body dark:bg-darkmode-body rounded-lg p-6 shadow-sm transition-all duration-300 hover:shadow-lg ${className}`}
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

      <div className="chart-container min-h-[400px] w-full">{children}</div>
    </div>
  );
};

export default ChartContainer;
