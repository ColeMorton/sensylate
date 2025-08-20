import React from "react";
import type { ChartDisplayProps } from "@/types/ChartTypes";
import ChartContainer from "@/components/charts/ChartContainer";
import PortfolioChart from "@/components/charts/PortfolioChart";

const ChartDisplay: React.FC<ChartDisplayProps> = ({
  title,
  category,
  description,
  chartType = "apple-stock",
  timeframe = "daily",
  indexed = false,
  positionType = "auto",
  status = "active",
  frozenDate,
  frozenBy,
  className = "",
  titleOnly = false,
}) => {
  // Handle unsupported chart types
  const supportedChartTypes = [
    "apple-stock",
    "portfolio-value-comparison",
    "returns-comparison",
    "portfolio-drawdowns",
    "live-signals-equity-curve",
    "live-signals-benchmark-comparison",
    "live-signals-drawdowns",
    "live-signals-weekly-candlestick",
    "trade-pnl-waterfall",
    "open-positions-pnl-timeseries",
    "closed-positions-pnl-timeseries",
  ];

  if (!supportedChartTypes.includes(chartType)) {
    return (
      <ChartContainer
        title={title}
        category={category}
        description={description}
        className={className}
        titleOnly={titleOnly}
      >
        <div className="flex min-h-[400px] items-center justify-center rounded-lg bg-blue-100 p-8 text-center dark:bg-blue-900">
          <div>
            <p className="font-semibold text-blue-700 dark:text-blue-300">
              📊 Charts Foundation Ready
            </p>
            <p className="mt-2 text-sm text-blue-600 dark:text-blue-400">
              More visualizations coming soon
            </p>
          </div>
        </div>
      </ChartContainer>
    );
  }

  // Handle frozen/static charts with status overlay
  if (status === "frozen" || status === "static") {
    return (
      <ChartContainer
        title={title}
        category={category}
        description={description}
        className={className}
        titleOnly={titleOnly}
      >
        <div className="relative">
          {/* Render chart with reduced opacity */}
          <div className="opacity-60">
            <PortfolioChart
              chartType={chartType}
              title={title}
              timeframe={timeframe}
              indexed={indexed}
              positionType={positionType}
            />
          </div>

          {/* Status overlay */}
          <div className="absolute inset-0 flex items-center justify-center rounded-lg bg-gray-100/80 backdrop-blur-sm dark:bg-gray-800/80">
            <div className="max-w-md p-6 text-center">
              <div className="mb-3 flex items-center justify-center">
                {status === "frozen" ? (
                  <div className="flex items-center gap-2 rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-800 dark:bg-amber-900 dark:text-amber-200">
                    ❄️ Frozen
                  </div>
                ) : (
                  <div className="flex items-center gap-2 rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700 dark:bg-gray-700 dark:text-gray-300">
                    📊 Static
                  </div>
                )}
              </div>

              {frozenDate && (
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  {status === "frozen" ? "Frozen" : "Since"}: {frozenDate}
                  {frozenBy && ` by ${frozenBy}`}
                </p>
              )}
            </div>
          </div>
        </div>
      </ChartContainer>
    );
  }

  // Render active charts normally
  return (
    <ChartContainer
      title={title}
      category={category}
      description={description}
      className={className}
      titleOnly={titleOnly}
    >
      <PortfolioChart
        chartType={chartType}
        title={title}
        timeframe={timeframe}
        indexed={indexed}
        positionType={positionType}
      />
    </ChartContainer>
  );
};

export default ChartDisplay;
