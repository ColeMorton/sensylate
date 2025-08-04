/**
 * Conditional ChartDisplay Component
 *
 * This component uses build-time feature flags to conditionally load
 * the ChartDisplay component, enabling dead code elimination
 * when the charts page feature is disabled.
 */

import React, { Suspense } from "react";
import { BuildTimeFeatures } from "@/lib/conditionalImports";
import type { ChartDisplayProps } from "@/types/ChartTypes";

// Build-time conditional import
const ChartDisplay = BuildTimeFeatures.chartsPage
  ? React.lazy(() => import("./ChartDisplay"))
  : null;

const ConditionalChartDisplay: React.FC<ChartDisplayProps> = (props) => {
  // If feature is disabled at build time, this component is completely removed
  if (!BuildTimeFeatures.chartsPage || !ChartDisplay) {
    return (
      <div className="rounded-lg border-2 border-dashed border-gray-300 bg-gray-100 p-4 text-center">
        <p className="text-gray-600">Charts feature is disabled</p>
      </div>
    );
  }

  return (
    <Suspense
      fallback={
        <div className="flex h-96 animate-pulse items-center justify-center rounded bg-gray-200">
          <span className="text-gray-500">Loading chart...</span>
        </div>
      }
    >
      <ChartDisplay {...props} />
    </Suspense>
  );
};

export default ConditionalChartDisplay;
