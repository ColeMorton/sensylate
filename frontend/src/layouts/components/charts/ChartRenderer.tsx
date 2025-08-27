import React, { lazy, Suspense, useRef, useEffect } from "react";
import type { ChartRendererProps } from "@/types/ChartTypes";
import ChartLoadingSkeleton from "./shared/ChartLoadingSkeleton";
import ChartErrorBoundary from "./shared/ChartErrorBoundary";

// Simple lazy loading for client-only rendering
const Plot = lazy(() => {
  return import("react-plotly.js").then((module) => {
    return { default: module.default };
  });
});

const ChartRenderer: React.FC<ChartRendererProps> = ({
  data,
  layout,
  config,
  loading = false,
  error = null,
}) => {
  const plotRef = useRef<HTMLDivElement | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleInitialized = (figure: unknown, graphDiv: HTMLDivElement) => {
    plotRef.current = graphDiv;
  };

  // Cleanup effect to properly destroy Plotly instances
  useEffect(() => {
    return () => {
      if (plotRef.current && typeof window !== "undefined" && window.Plotly) {
        try {
          window.Plotly.purge(plotRef.current);
        } catch {
          // Ignore cleanup errors
        }
      }
    };
  }, []);

  if (loading) {
    return <ChartLoadingSkeleton />;
  }

  if (error) {
    return <ChartErrorBoundary error={error} />;
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex h-full items-center justify-center rounded-lg bg-blue-100 p-8 text-center dark:bg-blue-900">
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
    <div
      ref={containerRef}
      className="h-full w-full flex-1"
      style={{
        position: "relative",
        overflow: "hidden",
      }}
    >
      <Suspense fallback={<ChartLoadingSkeleton />}>
        <Plot
          data={data}
          layout={layout}
          config={config}
          onInitialized={handleInitialized}
          useResizeHandler={true}
          style={{
            width: "100%",
            height: "100%",
            position: "relative",
          }}
          className="plotly-chart"
        />
      </Suspense>
    </div>
  );
};

export default ChartRenderer;
