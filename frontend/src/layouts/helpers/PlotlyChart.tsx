import React, {
  useState,
  useCallback,
  useMemo,
  lazy,
  Suspense,
  useEffect,
  useRef,
} from "react";
import type { Data, Layout, Config } from "plotly.js";

// Direct dynamic import approach to avoid complex lazy loading issues
const Plot = lazy(() => {
  if (typeof window === "undefined") {
    // Return a mock component for SSR
    return Promise.resolve({
      default: () =>
        React.createElement("div", {
          className: "plotly-loading",
          children: "Chart loading (SSR)...",
        }),
    });
  }

  // Simplified import chain - try to avoid the complex factory pattern
  try {
    return import("react-plotly.js").then((module) => {
      console.log("✅ Successfully imported react-plotly.js:", !!module.default);
      return { default: module.default };
    }).catch((error) => {
      console.error("❌ Failed to import react-plotly.js:", error);
      // Fallback to factory approach
      return import("react-plotly.js/factory").then(async (factory) => {
        const Plotly = await import("plotly.js-basic-dist");
        console.log("✅ Factory fallback loaded:", !!factory.default, !!Plotly.default);
        return { default: factory.default(Plotly.default || Plotly) };
      });
    });
  } catch (error) {
    console.error("❌ Critical Plotly import error:", error);
    return Promise.resolve({
      default: () =>
        React.createElement("div", {
          className: "plotly-error bg-red-100 p-4",
          children: "Chart import failed: " + String(error),
        }),
    });
  }
});

export interface PlotlyChartProps {
  data: Data[];
  layout?: Partial<Layout>;
  config?: Partial<Config>;
  className?: string;
  title?: string;
}

const PlotlyChart: React.FC<PlotlyChartProps> = ({
  data,
  layout: initialLayout,
  config: initialConfig,
  className = "",
  title,
}) => {
  const [chartData, setChartData] = useState<Data[]>(data);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isChartLoaded, setIsChartLoaded] = useState(false);
  const [isChartRendered, setIsChartRendered] = useState(false);
  const plotRef = useRef<HTMLDivElement | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Detect dark mode
  useEffect(() => {
    const checkDarkMode = () => {
      if (typeof window !== "undefined") {
        const darkMode =
          document.documentElement.classList.contains("dark") ||
          window.matchMedia("(prefers-color-scheme: dark)").matches;
        setIsDarkMode(darkMode);
      }
    };

    checkDarkMode();

    // Listen for theme changes
    const observer = new MutationObserver(checkDarkMode);
    if (typeof window !== "undefined") {
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }

    // Listen for system theme changes
    if (typeof window !== "undefined") {
      const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
      mediaQuery.addEventListener("change", checkDarkMode);
    }

    return () => {
      observer.disconnect();
      if (typeof window !== "undefined") {
        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        mediaQuery.removeEventListener("change", checkDarkMode);
      }
    };
  }, []);

  // Stable base layout configuration (without theme dependencies)
  const baseLayout: Partial<Layout> = useMemo(
    () => ({
      autosize: true,
      responsive: true,
      margin: { l: 50, r: 50, t: 50, b: 50 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      showlegend: true,
      legend: {
        x: 0,
        xanchor: "left",
        y: 1,
        yanchor: "top",
        orientation: "v",
        borderwidth: 1,
      },
      ...initialLayout,
    }),
    [initialLayout],
  );

  // Dynamic theme-aware layout (applied separately)
  const defaultLayout: Partial<Layout> = useMemo(() => {
    const themeColors = {
      font: isDarkMode ? "#E5E7EB" : "#374151",
      legendBg: isDarkMode
        ? "rgba(31, 41, 55, 0.8)"
        : "rgba(255, 255, 255, 0.8)",
      legendBorder: isDarkMode
        ? "rgba(156, 163, 175, 0.3)"
        : "rgba(0, 0, 0, 0.2)",
      gridColor: isDarkMode ? "rgba(156, 163, 175, 0.2)" : "rgba(0, 0, 0, 0.1)",
      tickColor: isDarkMode ? "#9CA3AF" : "#6B7280",
    };

    return {
      ...baseLayout,
      font: {
        family: '"Inter", ui-sans-serif, system-ui, -apple-system, sans-serif',
        size: 12,
        color: themeColors.font,
      },
      legend: {
        ...baseLayout.legend,
        bgcolor: themeColors.legendBg,
        bordercolor: themeColors.legendBorder,
        font: {
          color: themeColors.font,
        },
      },
      xaxis: {
        ...baseLayout.xaxis,
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: {
          color: themeColors.font,
        },
        title: {
          ...baseLayout.xaxis?.title,
          font: {
            color: themeColors.font,
          },
        },
      },
      yaxis: {
        ...baseLayout.yaxis,
        gridcolor: themeColors.gridColor,
        tickcolor: themeColors.tickColor,
        tickfont: {
          color: themeColors.font,
        },
        title: {
          ...baseLayout.yaxis?.title,
          font: {
            color: themeColors.font,
          },
        },
      },
    };
  }, [baseLayout, isDarkMode]);

  // Default config for better user experience
  const defaultConfig: Partial<Config> = useMemo(
    () => ({
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      toImageButtonOptions: {
        format: "png",
        filename: title || "chart",
        height: 500,
        width: 700,
        scale: 1,
      },
      autosizable: true,
      ...initialConfig,
    }),
    [initialConfig, title],
  );

  // Handle plot updates (zoom, pan, etc.)
  const handleUpdate = useCallback(
    (figure: Partial<{ layout: Layout; data: Data[] }>) => {
      if (figure.data) {
        setChartData(figure.data);
      }
    },
    [],
  );

  // Handle plot initialization with aggressive layout fixing
  const handleInitialized = useCallback(
    (
      figure: Partial<{ layout: Layout; data: Data[] }>,
      graphDiv: HTMLDivElement,
    ) => {
      plotRef.current = graphDiv;
      setIsChartLoaded(true);

      if (figure.data) {
        setChartData(figure.data);
      }

      // Aggressive legend position fixing with multiple attempts
      const fixLegendPosition = () => {
        if (typeof window !== "undefined" && window.Plotly && graphDiv) {
          const legendUpdate = {
            "legend.x": 0,
            "legend.y": 1,
            "legend.xanchor": "left",
            "legend.yanchor": "top",
            "legend.orientation": "v",
          };

          // Multiple attempts to ensure positioning sticks
          window.Plotly.relayout(graphDiv, legendUpdate)
            .then(() => {
              // Second attempt after 50ms
              setTimeout(() => {
                if (window.Plotly && graphDiv) {
                  window.Plotly.relayout(graphDiv, legendUpdate).catch(
                    () => {},
                  );
                }
              }, 50);
            })
            .catch(() => {
              // Fallback attempt
              setTimeout(() => {
                if (window.Plotly && graphDiv) {
                  window.Plotly.relayout(graphDiv, legendUpdate).catch(
                    () => {},
                  );
                }
              }, 200);
            });
        }
      };

      // Immediate fix
      setTimeout(fixLegendPosition, 10);
      // Delayed fix for navigation scenarios
      setTimeout(fixLegendPosition, 100);
      // Final fix attempt and mark as rendered
      setTimeout(() => {
        fixLegendPosition();
        setIsChartRendered(true);
      }, 500);
    },
    [],
  );

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

  // Comprehensive layout fixing on any state change
  useEffect(() => {
    if (plotRef.current && typeof window !== "undefined" && window.Plotly) {
      const fixLayout = () => {
        try {
          const legendUpdate = {
            "legend.x": 0,
            "legend.y": 1,
            "legend.xanchor": "left",
            "legend.yanchor": "top",
            "legend.orientation": "v",
          };

          window.Plotly.relayout(plotRef.current, legendUpdate)
            .then(() => {
              // Verify the fix worked by checking DOM
              setTimeout(() => {
                if (plotRef.current) {
                  const legendElement =
                    plotRef.current.querySelector(".legend");
                  if (legendElement) {
                    const rect = legendElement.getBoundingClientRect();
                    const chartRect = plotRef.current.getBoundingClientRect();

                    // If legend is still displaced, force another fix
                    if (rect.top > chartRect.bottom + 100) {
                      window.Plotly.relayout(
                        plotRef.current,
                        legendUpdate,
                      ).catch(() => {});
                    }
                  }
                }
              }, 100);
            })
            .catch(() => {
              // Fallback relayout attempt
              setTimeout(() => {
                if (window.Plotly && plotRef.current) {
                  window.Plotly.relayout(plotRef.current, legendUpdate).catch(
                    () => {},
                  );
                }
              }, 300);
            });
        } catch {
          // Silent error handling
        }
      };

      // Immediate fix
      const timeoutId1 = setTimeout(fixLayout, 50);
      // Secondary fix for stubborn cases
      const timeoutId2 = setTimeout(fixLayout, 200);
      // Final fix attempt
      const timeoutId3 = setTimeout(fixLayout, 500);

      return () => {
        clearTimeout(timeoutId1);
        clearTimeout(timeoutId2);
        clearTimeout(timeoutId3);
      };
    }
  }, [data, isDarkMode]);

  // Navigation-specific layout reset
  useEffect(() => {
    const handleNavigationFix = () => {
      if (plotRef.current && typeof window !== "undefined" && window.Plotly) {
        setTimeout(() => {
          const legendUpdate = {
            "legend.x": 0,
            "legend.y": 1,
            "legend.xanchor": "left",
            "legend.yanchor": "top",
            "legend.orientation": "v",
          };
          window.Plotly.relayout(plotRef.current, legendUpdate).catch(() => {});
        }, 100);
      }
    };

    // Listen for navigation events
    window.addEventListener("popstate", handleNavigationFix);

    return () => {
      window.removeEventListener("popstate", handleNavigationFix);
    };
  }, []);

  // Add comprehensive error boundary logging
  console.log("PlotlyChart render:", {
    title,
    dataLength: chartData?.length,
    hasLayout: !!defaultLayout,
    hasConfig: !!defaultConfig,
    isChartLoaded,
    isChartRendered
  });

  return (
    <div
      ref={containerRef}
      className={`plotly-chart-container h-full w-full ${className}`}
      style={{
        position: "relative",
        overflow: "hidden",
        minHeight: "400px",
      }}
      data-testid="plotly-chart-container"
      data-chart-loaded={isChartLoaded}
      data-chart-rendered={isChartRendered}
      data-chart-ready={isChartLoaded && isChartRendered}
    >
      <Suspense
        fallback={
          <div
            className="flex h-full min-h-[400px] items-center justify-center bg-yellow-100"
            data-testid="plotly-chart-loading"
          >
            <div className="text-center">
              <div className="border-primary mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-b-2"></div>
              <p className="text-text/60 dark:text-gray-500">
                Loading chart... ({chartData?.length || 0} data series)
              </p>
            </div>
          </div>
        }
      >
        <ErrorBoundary
          fallback={
            <div className="bg-red-100 p-4 text-red-800">
              <h3 className="font-bold">Chart Error</h3>
              <p className="text-sm">Failed to render Plotly chart. Check console for details.</p>
              <p className="text-xs">Data: {chartData?.length || 0} series</p>
            </div>
          }
        >
          <Plot
            data={chartData}
            layout={defaultLayout}
            config={defaultConfig}
            onInitialized={handleInitialized}
            onUpdate={handleUpdate}
            onError={(error) => console.error("Plotly chart error:", error)}
            useResizeHandler={false}
            style={{
              width: "100%",
              height: "100%",
              position: "relative",
            }}
            className="plotly-chart"
            data-testid="plotly-chart"
          />
        </ErrorBoundary>
      </Suspense>
    </div>
  );

// Simple Error Boundary component
class ErrorBoundary extends React.Component<
  { fallback: React.ReactElement; children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    console.error("PlotlyChart ErrorBoundary caught error:", error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error("PlotlyChart ErrorBoundary details:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

export default PlotlyChart;
