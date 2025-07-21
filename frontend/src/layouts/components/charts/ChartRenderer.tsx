import React, { lazy, Suspense } from "react";
import type { ChartRendererProps } from "@/types/ChartTypes";
import ChartLoadingSkeleton from "./shared/ChartLoadingSkeleton";
import ChartErrorBoundary from "./shared/ChartErrorBoundary";

// Lazy load the plot component to avoid SSR issues
const Plot = lazy(() => {
  if (typeof window === "undefined") {
    // Return a mock component for SSR
    return Promise.resolve({
      default: () =>
        React.createElement("div", {
          className: "plotly-loading",
          children: "Loading chart...",
        }),
    });
  }

  return import("react-plotly.js/factory").then(async (factory) => {
    const Plotly = await import("plotly.js-basic-dist-min");
    return { default: factory.default(Plotly) };
  });
});

const ChartRenderer: React.FC<ChartRendererProps> = ({
  data,
  layout,
  config,
  loading = false,
  error = null,
}) => {
  if (loading) {
    return <ChartLoadingSkeleton />;
  }

  if (error) {
    return <ChartErrorBoundary error={error} />;
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex min-h-[400px] items-center justify-center rounded-lg bg-blue-100 p-8 text-center dark:bg-blue-900">
        <div>
          <p className="font-semibold text-blue-700 dark:text-blue-300">
            📊 No Data Available
          </p>
          <p className="mt-2 text-sm text-blue-600 dark:text-blue-400">
            Chart data is not available at this time
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full min-h-[400px] w-full">
      <Suspense fallback={<ChartLoadingSkeleton />}>
        <Plot
          data={data}
          layout={layout}
          config={config}
          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}
          className="plotly-chart"
        />
      </Suspense>
    </div>
  );
};

export default ChartRenderer;
