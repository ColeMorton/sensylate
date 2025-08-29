import React from "react";
import type { IconProps } from "@tabler/icons-react";

interface MetricCardProps {
  icon: React.ComponentType<IconProps>;
  value: string;
  label: string;
  trend?: "up" | "down" | "neutral";
  className?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
  icon: Icon,
  value,
  label,
  trend,
  className = "",
}) => {
  const trendColorClass = {
    up: "text-green-600 dark:text-green-400",
    down: "text-red-600 dark:text-red-400",
    neutral: "text-gray-600 dark:text-gray-400",
  };

  return (
    <div
      className={`flex items-center gap-3 rounded-lg bg-white p-4 shadow-sm dark:bg-gray-800 ${className}`}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-700">
        <Icon
          size={24}
          className={
            trend ? trendColorClass[trend] : "text-gray-700 dark:text-gray-300"
          }
        />
      </div>
      <div className="flex flex-col">
        <span className="text-dark text-2xl font-bold dark:text-white">
          {value}
        </span>
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {label}
        </span>
      </div>
    </div>
  );
};

export default MetricCard;
