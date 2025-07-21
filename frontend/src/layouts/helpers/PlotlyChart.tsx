import React, {
  useState,
  useCallback,
  useMemo,
  lazy,
  Suspense,
  useEffect,
} from "react";
import type { Data, Layout, Config } from "plotly.js";

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

  return import("react-plotly.js/factory").then((factory) => {
    const Plotly = require("plotly.js-basic-dist");
    return { default: factory.default(Plotly) };
  });
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
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    mediaQuery.addEventListener("change", checkDarkMode);

    return () => {
      observer.disconnect();
      mediaQuery.removeEventListener("change", checkDarkMode);
    };
  }, []);

  // Default layout with responsive and dark mode support
  const defaultLayout: Partial<Layout> = useMemo(
    () => ({
      autosize: true,
      responsive: true,
      margin: { l: 50, r: 50, t: 50, b: 50 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: {
        family: '"Inter", ui-sans-serif, system-ui, -apple-system, sans-serif',
        size: 12,
        color: isDarkMode ? "#E5E7EB" : "#374151",
      },
      showlegend: true,
      legend: {
        x: 0,
        xanchor: "left",
        y: 1,
        yanchor: "top",
        bgcolor: isDarkMode
          ? "rgba(31, 41, 55, 0.8)"
          : "rgba(255, 255, 255, 0.8)",
        bordercolor: isDarkMode
          ? "rgba(156, 163, 175, 0.3)"
          : "rgba(0, 0, 0, 0.2)",
        borderwidth: 1,
        font: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
      },
      xaxis: {
        ...initialLayout?.xaxis,
        gridcolor: isDarkMode
          ? "rgba(156, 163, 175, 0.2)"
          : "rgba(0, 0, 0, 0.1)",
        tickcolor: isDarkMode ? "#9CA3AF" : "#6B7280",
        tickfont: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
        title: {
          ...initialLayout?.xaxis?.title,
          font: {
            color: isDarkMode ? "#E5E7EB" : "#374151",
          },
        },
      },
      yaxis: {
        ...initialLayout?.yaxis,
        gridcolor: isDarkMode
          ? "rgba(156, 163, 175, 0.2)"
          : "rgba(0, 0, 0, 0.1)",
        tickcolor: isDarkMode ? "#9CA3AF" : "#6B7280",
        tickfont: {
          color: isDarkMode ? "#E5E7EB" : "#374151",
        },
        title: {
          ...initialLayout?.yaxis?.title,
          font: {
            color: isDarkMode ? "#E5E7EB" : "#374151",
          },
        },
      },
      ...initialLayout,
    }),
    [initialLayout, isDarkMode],
  );

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

  // Handle plot initialization
  const handleInitialized = useCallback(
    (figure: Partial<{ layout: Layout; data: Data[] }>) => {
      if (figure.data) {
        setChartData(figure.data);
      }
    },
    [],
  );

  return (
    <div className={`plotly-chart-container h-full w-full ${className}`}>
      <Suspense
        fallback={
          <div className="flex h-full min-h-[400px] items-center justify-center">
            <div className="text-center">
              <div className="border-primary mx-auto mb-2 h-8 w-8 animate-spin rounded-full border-b-2"></div>
              <p className="text-text/60 dark:text-gray-500">
                Loading chart...
              </p>
            </div>
          </div>
        }
      >
        <Plot
          data={chartData}
          layout={defaultLayout}
          config={defaultConfig}
          onInitialized={handleInitialized}
          onUpdate={handleUpdate}
          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}
          className="plotly-chart"
        />
      </Suspense>
    </div>
  );
};

export default PlotlyChart;
