import React from "react";

interface ChartErrorBoundaryProps {
  error: string | null;
  onRetry?: () => void;
  className?: string;
}

const ChartErrorBoundary: React.FC<ChartErrorBoundaryProps> = ({
  error,
  onRetry,
  className = "",
}) => {
  if (!error) {
    return null;
  }

  return (
    <div
      className={`flex h-full min-h-[400px] items-center justify-center ${className}`}
    >
      <div className="text-center">
        <div className="mb-4">
          <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900">
            <svg
              className="h-6 w-6 text-red-600 dark:text-red-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
          </div>
        </div>
        <p className="mb-2 font-medium text-red-600 dark:text-red-400">
          Error loading chart
        </p>
        <p className="text-text/60 mb-4 max-w-md text-sm dark:text-gray-500">
          {error}
        </p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="bg-primary hover:bg-primary/90 rounded-md px-4 py-2 text-sm font-medium text-white transition-colors duration-200"
          >
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default ChartErrorBoundary;
