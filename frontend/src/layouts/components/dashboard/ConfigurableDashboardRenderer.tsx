/**
 * Configurable Dashboard Renderer
 * 
 * Replaces hardcoded dashboard logic with configuration-driven rendering.
 * Dynamically renders headers, footers, and charts based on dashboard configuration.
 */

import React from 'react';
import { DashboardLoader } from "@/services/dashboardLoader";
import ChartDisplay from "@/shortcodes/ChartDisplay";
import FundamentalAnalysisDashboard from "@/layouts/components/fundamentals/FundamentalAnalysisDashboard";
import ErrorBoundary from "@/layouts/components/ErrorBoundary";
import DashboardHeader from './DashboardHeader';
import DashboardFooter from './DashboardFooter';
import type { ExtendedDashboardConfig } from '@/types/DashboardLayoutTypes';

interface ConfigurableDashboardRendererProps {
  dashboard: ExtendedDashboardConfig;
  mode: 'light' | 'dark';
  aspectRatio: '16:9' | '4:3' | '3:4';
  selectedTicker?: string;
  fundamentalMockDataFn?: ((ticker: string) => any) | null;
}

const ConfigurableDashboardRenderer: React.FC<ConfigurableDashboardRendererProps> = ({
  dashboard,
  mode,
  aspectRatio: _aspectRatio,
  selectedTicker,
  fundamentalMockDataFn,
}) => {
  const layoutClasses = DashboardLoader.getLayoutClasses(dashboard.layout);
  const layoutConfig = dashboard.layout_config;

  // Handle fundamental analysis dashboard (special case for now)
  if (dashboard.layout === "fundamental_3x3") {
    const ticker = selectedTicker || "GOOGL";

    if (!import.meta.env.DEV || !fundamentalMockDataFn) {
      return (
        <div className="flex items-center justify-center rounded-lg border p-8">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Fundamental analysis dashboard is only available in development mode
            </p>
          </div>
        </div>
      );
    }

    const fundamentalData = fundamentalMockDataFn(ticker);

    return (
      <div
        className={`${mode}-mode ${mode}`}
        style={{
          width: "100%",
          height: "100%",
          colorScheme: mode === "dark" ? "dark" : "light",
        }}
      >
        <ErrorBoundary
          onError={(error, errorInfo) => {
            console.error("FundamentalAnalysisDashboard error:", error);
          }}
          fallback={
            <div className="flex min-h-[400px] items-center justify-center">
              <div className="text-center">
                <h3 className="text-lg font-semibold text-red-600">
                  Fundamental Analysis Error
                </h3>
                <p className="text-gray-600">
                  Unable to load fundamental analysis dashboard for {ticker}
                </p>
                <button
                  onClick={() => window.location.reload()}
                  className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600"
                >
                  Reload Page
                </button>
              </div>
            </div>
          }
        >
          <FundamentalAnalysisDashboard
            data={fundamentalData}
            ticker={ticker}
            exportMode={true}
            className="photo-booth-chart"
          />
        </ErrorBoundary>
      </div>
    );
  }

  // Configuration-driven dashboard rendering
  const containerClasses = layoutConfig?.containerClassName 
    ? `dashboard-content ${dashboard.layout} ${mode}-mode flex flex-col ${layoutConfig.containerClassName}`
    : `dashboard-content ${dashboard.layout} ${mode}-mode flex flex-col`;

  const chartDisplayMode = layoutConfig?.chartOptions?.displayMode || 'full';
  const titleOnly = layoutConfig?.chartOptions?.titleOnly ?? false;
  const chartClassName = layoutConfig?.chartOptions?.chartClassName || 'photo-booth-chart';

  return (
    <div
      className={containerClasses}
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
      }}
    >
      {/* Dynamic Header */}
      {layoutConfig?.header && (
        <DashboardHeader config={layoutConfig.header} mode={mode} />
      )}

      {/* Charts Section */}
      <div className={`${layoutClasses} min-h-0 flex-1`}>
        {dashboard.charts.map((chart, index) => (
          <ChartDisplay
            key={`${dashboard.id}-${chart.chartType}-${index}`}
            title={chart.title}
            category={chart.category}
            description={chart.description}
            chartType={chart.chartType}
            className={chartClassName}
            titleOnly={titleOnly}
          />
        ))}
      </div>

      {/* Dynamic Footer */}
      {layoutConfig?.footer && (
        <DashboardFooter config={layoutConfig.footer} mode={mode} />
      )}
    </div>
  );
};

export default ConfigurableDashboardRenderer;