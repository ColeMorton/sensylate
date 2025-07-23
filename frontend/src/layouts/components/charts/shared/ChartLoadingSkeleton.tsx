import React from "react";

interface ChartLoadingSkeletonProps {
  className?: string;
}

const ChartLoadingSkeleton: React.FC<ChartLoadingSkeletonProps> = ({
  className = "",
}) => {
  return (
    <div
      className={`flex h-full min-h-[400px] items-center justify-center ${className}`}
    >
      <div className="text-center">
        <div className="border-primary mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-b-2"></div>
        <p className="text-text/60 dark:text-gray-500">Loading chart data...</p>
      </div>
    </div>
  );
};

export default ChartLoadingSkeleton;
