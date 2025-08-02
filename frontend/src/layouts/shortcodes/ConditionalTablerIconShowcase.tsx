/**
 * Conditional TablerIconShowcase Component
 *
 * This component uses build-time feature flags to conditionally load
 * the TablerIconShowcase component, enabling dead code elimination
 * when the elements page feature is disabled.
 */

import React, { Suspense } from "react";
import { BuildTimeFeatures } from "@/lib/conditionalImports";

// Build-time conditional import
const TablerIconShowcase = BuildTimeFeatures.elementsPage
  ? React.lazy(() => import("./TablerIconShowcase"))
  : null;

interface ConditionalTablerIconShowcaseProps {
  className?: string;
}

const ConditionalTablerIconShowcase: React.FC<
  ConditionalTablerIconShowcaseProps
> = ({ className: _className }) => {
  // If feature is disabled at build time, this component is completely removed
  if (!BuildTimeFeatures.elementsPage || !TablerIconShowcase) {
    return null;
  }

  return (
    <Suspense
      fallback={
        <div className="h-96 animate-pulse rounded bg-gray-200">
          Loading icons...
        </div>
      }
    >
      <TablerIconShowcase />
    </Suspense>
  );
};

export default ConditionalTablerIconShowcase;
