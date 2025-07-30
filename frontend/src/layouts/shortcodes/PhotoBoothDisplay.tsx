import React, { useState, useEffect, useCallback } from "react";
import photoBoothConfig from "@/config/photo-booth.json";
import { DashboardLoader, type DashboardConfig } from "@/lib/dashboardLoader";
import ChartDisplay from "@/shortcodes/ChartDisplay";

interface Dashboard {
  id: string;
  name: string;
  file: string;
  description: string;
  layout: string;
  enabled: boolean;
}

interface PhotoBoothDisplayProps {
  className?: string;
}

const PhotoBoothDisplay: React.FC<PhotoBoothDisplayProps> = ({
  className = "",
}) => {
  const [selectedDashboard, setSelectedDashboard] = useState<string>(
    photoBoothConfig.default_dashboard
  );
  const [activeDashboards, setActiveDashboards] = useState<DashboardConfig[]>([]);
  const [isReady, setIsReady] = useState(false);
  const [currentMode, setCurrentMode] = useState<"light" | "dark">("light");
  const [loading, setLoading] = useState(true);

  // Load dashboards on component mount
  useEffect(() => {
    const loadDashboards = async () => {
      try {
        const dashboards = await DashboardLoader.getAllDashboards();
        setActiveDashboards(dashboards);
        
        // Get dashboard from URL parameters or use default
        const urlParams = new URLSearchParams(window.location.search);
        const dashboardParam = urlParams.get("dashboard");
        const modeParam = urlParams.get("mode") as "light" | "dark" | null;
        
        if (dashboardParam && dashboards.some(d => d.id === dashboardParam)) {
          setSelectedDashboard(dashboardParam);
        }
        
        if (modeParam && ["light", "dark"].includes(modeParam)) {
          setCurrentMode(modeParam);
        }
        
        setLoading(false);
      } catch (error) {
        console.error("Failed to load dashboards:", error);
        
        // Show user-friendly error message
        setActiveDashboards([]);
        setLoading(false);
        
        // Optional: Set error state for better UX
        // This could be expanded to show retry functionality
      }
    };

    loadDashboards();
  }, []);

  // Mark component as ready for screenshots
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsReady(true);
    }, photoBoothConfig.performance.render_timeout);

    return () => clearTimeout(timer);
  }, [selectedDashboard, currentMode]);

  const handleDashboardChange = useCallback((dashboardId: string) => {
    setIsReady(false);
    setSelectedDashboard(dashboardId);
    
    // Update URL without page reload
    const url = new URL(window.location.href);
    url.searchParams.set("dashboard", dashboardId);
    window.history.replaceState({}, "", url.toString());
  }, []);

  const handleModeChange = useCallback((mode: "light" | "dark") => {
    setIsReady(false);
    setCurrentMode(mode);
    
    // Update URL without page reload
    const url = new URL(window.location.href);
    url.searchParams.set("mode", mode);
    window.history.replaceState({}, "", url.toString());
  }, []);

  const currentDashboard = activeDashboards.find(d => d.id === selectedDashboard);

  if (loading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading dashboards...</p>
        </div>
      </div>
    );
  }

  if (!currentDashboard) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <div className="text-center">
          <h3 className="text-lg font-semibold text-red-600">
            {activeDashboards.length === 0 ? "Failed to Load Dashboards" : "Dashboard Not Found"}
          </h3>
          <p className="text-gray-600">
            {activeDashboards.length === 0 
              ? "Could not load dashboard configurations. Please check your connection and try again."
              : `The requested dashboard "${selectedDashboard}" is not available.`
            }
          </p>
          {activeDashboards.length > 0 && (
            <p className="text-sm text-gray-500 mt-2">
              Available dashboards: {activeDashboards.map(d => d.id).join(", ")}
            </p>
          )}
          {activeDashboards.length === 0 && (
            <button 
              onClick={() => window.location.reload()} 
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
            >
              Retry
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={`photo-booth-container ${className} ${isReady ? "photo-booth-ready" : ""}`}>
      {/* Control Panel - Hidden in screenshot mode */}
      <div className="photo-booth-controls mb-6 print:hidden">
        <div className="flex flex-wrap items-center gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          {/* Dashboard Selector */}
          <div className="flex items-center gap-2">
            <label htmlFor="dashboard-select" className="text-sm font-medium">
              Dashboard:
            </label>
            <select
              id="dashboard-select"
              value={selectedDashboard}
              onChange={(e) => handleDashboardChange(e.target.value)}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
            >
              {activeDashboards.map((dashboard) => (
                <option key={dashboard.id} value={dashboard.id}>
                  {dashboard.title}
                </option>
              ))}
            </select>
          </div>

          {/* Mode Selector */}
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium">Mode:</label>
            <div className="flex gap-1">
              <button
                onClick={() => handleModeChange("light")}
                className={`px-3 py-1 text-sm rounded-md ${
                  currentMode === "light"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300"
                }`}
              >
                Light
              </button>
              <button
                onClick={() => handleModeChange("dark")}
                className={`px-3 py-1 text-sm rounded-md ${
                  currentMode === "dark"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300"
                }`}
              >
                Dark
              </button>
            </div>
          </div>

          {/* Status Indicator */}
          <div className="flex items-center gap-2 ml-auto">
            <div
              className={`w-3 h-3 rounded-full ${
                isReady ? "bg-green-500" : "bg-yellow-500"
              }`}
            />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {isReady ? "Ready for screenshot" : "Loading..."}
            </span>
          </div>
        </div>

        {/* Dashboard Info */}
        <div className="mt-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-md">
          <h3 className="font-semibold text-blue-900 dark:text-blue-100">
            {currentDashboard.title}
          </h3>
          <p className="text-sm text-blue-700 dark:text-blue-300">
            {currentDashboard.description}
          </p>
          <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
            Layout: {currentDashboard.layout} • Charts: {currentDashboard.charts.length}
          </p>
        </div>
      </div>

      {/* Dashboard Content */}
      <div 
        className={`photo-booth-dashboard ${currentMode === "dark" ? "dark" : ""}`}
        data-dashboard-id={selectedDashboard}
        data-mode={currentMode}
      >
        <DashboardRenderer 
          dashboard={currentDashboard}
          mode={currentMode}
        />
      </div>
    </div>
  );
};

// Dashboard renderer component that renders actual chart content
const DashboardRenderer: React.FC<{
  dashboard: DashboardConfig;
  mode: "light" | "dark";
}> = ({ dashboard, mode }) => {
  const layoutClasses = DashboardLoader.getLayoutClasses(dashboard.layout);
  
  return (
    <div className={`dashboard-content ${dashboard.layout} ${mode}-mode`}>
      <div className={layoutClasses}>
        {dashboard.charts.map((chart, index) => (
          <ChartDisplay
            key={`${dashboard.id}-${chart.chartType}-${index}`}
            title={chart.title}
            category={chart.category}
            description={chart.description}
            chartType={chart.chartType as any}
            className="photo-booth-chart"
          />
        ))}
      </div>
    </div>
  );
};

export default PhotoBoothDisplay;