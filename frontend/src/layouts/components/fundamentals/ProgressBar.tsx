import React from "react";

interface ProgressBarProps {
  label: string;
  value: number;
  color: "green" | "yellow" | "red" | "blue";
  showPercentage?: boolean;
  suffix?: string;
  className?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  label,
  value,
  color,
  showPercentage = true,
  suffix = "%",
  className = "",
}) => {
  const colorClasses = {
    green: {
      bg: "bg-green-500 dark:bg-green-400",
      text: "text-green-700 dark:text-green-300",
    },
    yellow: {
      bg: "bg-yellow-500 dark:bg-yellow-400",
      text: "text-yellow-700 dark:text-yellow-300",
    },
    red: {
      bg: "bg-red-500 dark:bg-red-400",
      text: "text-red-700 dark:text-red-300",
    },
    blue: {
      bg: "bg-blue-500 dark:bg-blue-400",
      text: "text-blue-700 dark:text-blue-300",
    },
  };

  // Ensure value is between 0 and 100 for percentage display
  const clampedValue = Math.min(100, Math.max(0, Math.abs(value)));
  const isNegative = value < 0;

  return (
    <div className={`mb-4 ${className}`}>
      <div className="mb-1 flex items-baseline justify-between">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
        </span>
        {showPercentage && (
          <span className={`text-lg font-bold ${colorClasses[color].text}`}>
            {isNegative ? "-" : "+"}
            {clampedValue.toFixed(0)}
            {suffix}
          </span>
        )}
      </div>
      <div className="h-6 w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
        <div
          className={`h-full transition-all duration-300 ${colorClasses[color].bg}`}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
