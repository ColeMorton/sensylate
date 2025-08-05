/**
 * Conditional PhotoBoothDisplay Component
 *
 * This component uses build-time feature flags to conditionally load
 * the PhotoBoothDisplay component, enabling dead code elimination
 * when the photo booth feature is disabled.
 */

import React, { Suspense } from "react";
import { BuildTimeFeatures } from "@/lib/conditionalImports";

// Debug logging for build-time feature flags
console.log("🔍 ConditionalPhotoBoothDisplay Debug:");
console.log("  BuildTimeFeatures.photoBooth:", BuildTimeFeatures.photoBooth);
console.log(
  "  typeof BuildTimeFeatures.photoBooth:",
  typeof BuildTimeFeatures.photoBooth,
);

// Build-time conditional import
const PhotoBoothDisplay = BuildTimeFeatures.photoBooth
  ? React.lazy(() => import("./PhotoBoothDisplay"))
  : null;

interface ConditionalPhotoBoothDisplayProps {
  className?: string;
}

const ConditionalPhotoBoothDisplay: React.FC<
  ConditionalPhotoBoothDisplayProps
> = ({ className }) => {
  // If feature is disabled at build time, this component is completely removed
  if (!BuildTimeFeatures.photoBooth || !PhotoBoothDisplay) {
    return (
      <div className="rounded-lg border-2 border-dashed border-gray-300 bg-gray-100 p-8 text-center">
        <p className="text-gray-600">Photo booth feature is disabled</p>
      </div>
    );
  }

  return (
    <Suspense
      fallback={
        <div className="flex h-96 animate-pulse items-center justify-center rounded bg-gray-200">
          <span className="text-gray-500">Loading photo booth...</span>
        </div>
      }
    >
      <PhotoBoothDisplay className={className} />
    </Suspense>
  );
};

export default ConditionalPhotoBoothDisplay;
