import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { DataStatusIndicator } from "@/layouts/components/charts/DataStatusIndicator";
import type { ChartType } from "@/types/ChartTypes";

// Mock the useChartDataManager hook
vi.mock("@/hooks/useEnhancedPortfolioData", () => ({
  useChartDataManager: vi.fn(),
}));

describe("DataStatusIndicator Component", () => {
  let mockUseChartDataManager: ReturnType<typeof vi.fn>;

  const getBaseReturn = () => ({
    dataStatus: {
      status: "available" as const,
      lastUpdated: Date.now() - 3600000, // 1 hour ago
      ageHours: 1,
      retryCount: 0,
      refreshing: false,
      lastUpdateSource: "manual",
    },
    refreshCapability: {
      canRefresh: true,
      reason: "Manual refresh available",
      availableMethods: ["file-watch"],
      estimatedDuration: 1000,
      requiresAuth: false,
    },
    isRefreshing: false,
    canRefresh: true,
    refresh: vi.fn(),
  });

  beforeEach(async () => {
    vi.clearAllMocks();

    // Get mocked function
    const module = await import("@/hooks/useEnhancedPortfolioData");
    mockUseChartDataManager = vi.mocked(module.useChartDataManager);

    // Setup default mock implementation
    mockUseChartDataManager.mockReturnValue(getBaseReturn());
  });

  describe("Basic Rendering", () => {
    it("renders available status indicator", () => {
      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
        />,
      );

      // Should show green indicator for available status
      const indicator = screen.getByTitle("Data Available");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("text-green-600");
    });

    it("renders stale status indicator", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          status: "stale",
          ageHours: 8,
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
        />,
      );

      const indicator = screen.getByTitle("Data Stale");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("text-yellow-600");
    });

    it("renders error status indicator", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          status: "error",
          error: "Failed to load data",
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
        />,
      );

      const indicator = screen.getByTitle("Data Error");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("text-red-600");
    });
  });

  describe("Compact Mode", () => {
    it("renders compact indicator with refresh button", () => {
      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
          showRefreshButton={true}
        />,
      );

      // Should show compact status symbol
      expect(screen.getByTitle("Data Available")).toBeInTheDocument();

      // Should show refresh button
      const refreshButton = screen.getByTitle("Refresh data");
      expect(refreshButton).toBeInTheDocument();
      expect(refreshButton).toHaveTextContent("↻");
    });

    it("hides refresh button when showRefreshButton is false", () => {
      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
          showRefreshButton={false}
        />,
      );

      expect(screen.queryByTitle("Refresh data")).not.toBeInTheDocument();
    });

    it("disables refresh button when refresh not available", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        canRefresh: false,
        refreshCapability: {
          ...getBaseReturn().refreshCapability,
          canRefresh: false,
          reason: "Static data source - no refresh available",
        },
      });

      render(
        <DataStatusIndicator
          chartType="apple-stock"
          compact={true}
          showRefreshButton={true}
        />,
      );

      // Refresh button should not be present for non-refreshable sources
      expect(screen.queryByTitle("Refresh data")).not.toBeInTheDocument();
    });
  });

  describe("Full Mode", () => {
    it("renders full status display", () => {
      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      // Should show status label
      expect(screen.getByText("Data Available")).toBeInTheDocument();

      // Should show age information
      expect(screen.getByText(/Updated 1h ago/)).toBeInTheDocument();

      // Should show refresh button
      expect(screen.getByText("Refresh")).toBeInTheDocument();

      // Should show details button
      expect(screen.getByText("Details")).toBeInTheDocument();
    });

    it("shows detailed information when expanded", () => {
      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      // Click details button
      fireEvent.click(screen.getByText("Details"));

      // Should show detailed information
      expect(screen.getByText("Source:")).toBeInTheDocument();
      expect(screen.getByText("manual")).toBeInTheDocument();
      expect(screen.getByText("Retries:")).toBeInTheDocument();
      expect(screen.getByText("Can Refresh:")).toBeInTheDocument();
      expect(screen.getByText("Methods:")).toBeInTheDocument();
    });

    it("shows error details when present", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          status: "error",
          error: "Network timeout error",
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      // Click details button
      fireEvent.click(screen.getByText("Details"));

      // Should show error information
      expect(screen.getByText("Error:")).toBeInTheDocument();
      expect(screen.getByText("Network timeout error")).toBeInTheDocument();
    });
  });

  describe("Refresh Functionality", () => {
    it("calls refresh function when refresh button clicked", () => {
      const mockRefresh = vi.fn();
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        refresh: mockRefresh,
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      fireEvent.click(screen.getByText("Refresh"));

      expect(mockRefresh).toHaveBeenCalledWith({ priority: "high" });
    });

    it("shows refreshing state", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        isRefreshing: true,
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      // Should show refreshing text
      expect(screen.getByText("Refreshing...")).toBeInTheDocument();

      // Button should be disabled
      const refreshButton = screen.getByText("Refreshing...");
      expect(refreshButton).toBeDisabled();
    });

    it("shows compact refreshing state", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        isRefreshing: true,
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={true}
        />,
      );

      // Should show refreshing indicator
      const refreshButton = screen.getByTitle("Refresh data");
      expect(refreshButton).toHaveTextContent("...");
      expect(refreshButton).toBeDisabled();
    });
  });

  describe("Chart Type Handling", () => {
    it("calls useChartDataManager with correct chart type", () => {
      const chartType: ChartType = "trade-pnl-waterfall";
      render(<DataStatusIndicator chartType={chartType} />);

      expect(mockUseChartDataManager).toHaveBeenCalledWith(chartType);
    });

    it("handles missing data status gracefully", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: undefined,
      });

      const { container } = render(
        <DataStatusIndicator chartType="live-signals-equity-curve" />,
      );

      // Should render nothing when no data status
      expect(container.firstChild).toBeNull();
    });
  });

  describe("Age Formatting", () => {
    it("formats age in minutes", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          ageHours: 0.5, // 30 minutes
          lastUpdated: Date.now() - 1800000, // 30 minutes ago
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      expect(screen.getByText(/Updated 30m ago/)).toBeInTheDocument();
    });

    it("formats age in days", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          ageHours: 48, // 2 days
          lastUpdated: Date.now() - 172800000, // 48 hours ago
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      expect(screen.getByText(/Updated 2d ago/)).toBeInTheDocument();
    });

    it("handles missing lastUpdated gracefully", () => {
      mockUseChartDataManager.mockReturnValue({
        ...getBaseReturn(),
        dataStatus: {
          ...getBaseReturn().dataStatus,
          lastUpdated: undefined,
        },
      });

      render(
        <DataStatusIndicator
          chartType="live-signals-equity-curve"
          compact={false}
        />,
      );

      expect(screen.getByText("No update info")).toBeInTheDocument();
    });
  });
});
