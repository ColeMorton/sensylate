import React from "react";
import type { ChartDisplayProps } from "@/types/ChartTypes";
import ChartContainer from "@/layouts/components/charts/ChartContainer";
import PortfolioChart from "@/layouts/components/charts/PortfolioChart";
import FundamentalChart from "@/layouts/components/charts/FundamentalCharts";
import { chartRegistry } from "@/charts/chart-registry";

const ChartDisplay: React.FC<ChartDisplayProps> = ({
  title,
  category,
  description,
  chartType = "apple-price",
  timeframe = "daily",
  indexed = false,
  positionType = "auto",
  samePercentageScale = true,
  className = "",
  titleOnly = false,
}) => {
  // Use chart registry instead of hardcoded array
  const isSupported = chartRegistry.isSupported(chartType);
  const isFundamentalChart = chartRegistry.isFundamentalChart(chartType);
  const isProductionReady = chartRegistry.isProductionReady(chartType);

  if (!isSupported) {
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

  if (isFundamentalChart) {
    // In production, show a message that fundamental charts are not available
    if (!import.meta.env.DEV || !isProductionReady) {
      return (
        <ChartContainer
          title={title}
          category={category}
          description={description}
          className={className}
        >
          <div className="flex items-center justify-center p-8">
            <div className="text-center">
              <p className="text-gray-600 dark:text-gray-400">
                Fundamental analysis charts are only available in development
                mode
              </p>
            </div>
          </div>
        </ChartContainer>
      );
    }

    // Development: Use a separate component to handle hooks properly
    const DevelopmentFundamentalChart = () => {
      const [fundamentalData, setFundamentalData] = React.useState(null);

      React.useEffect(() => {
        import("@/test/mocks/fundamentalAnalysis.mock")
          .then((module) => {
            const data = module.getFundamentalMockData("GOOGL");
            setFundamentalData(data);
          })
          .catch(() => {
            // Silently fail - mock data not available
          });
      }, []);

      if (!fundamentalData) {
        return (
          <ChartContainer
            title={title}
            category={category}
            description={description}
            className={className}
          >
            <div className="flex items-center justify-center p-8">
              <div className="text-center">
                <p className="text-gray-600 dark:text-gray-400">
                  Loading fundamental data...
                </p>
              </div>
            </div>
          </ChartContainer>
        );
      }

      return (
        <FundamentalChart
          chartType={chartType}
          data={fundamentalData}
          title={title}
          className={className}
        />
      );
    };

    return <DevelopmentFundamentalChart />;
  }

  // Render portfolio charts normally
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
        samePercentageScale={samePercentageScale}
      />
    </ChartContainer>
  );
};

export default ChartDisplay;
