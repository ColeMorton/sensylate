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
