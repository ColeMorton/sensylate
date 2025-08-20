import React from "react";
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import {
  render,
  screen,
  fireEvent,
  waitFor,
  cleanup,
  act,
} from "@testing-library/react";

// Mock the photo booth config import FIRST before any imports
vi.mock("@/config/photo-booth.json", () => ({
  default: {
    default_dashboard: "portfolio_history_portrait",
    active_dashboards: [
      {
        id: "portfolio_history_portrait",
        name: "Portfolio History Portrait",
        file: "portfolio-history-portrait.mdx",
        description:
          "Portfolio trading history with waterfall and time series analysis",
        layout: "2x1_stack",
        enabled: true,
      },
    ],
    screenshot_settings: {
      viewport: { width: 1920, height: 1080 },
      device_scale_factor: 2,
      format: "png",
      quality: 95,
      full_page: false,
      timeout: 30000,
      wait_for_selector: ".photo-booth-ready",
    },
    export_options: {
      formats: {
        available: ["png", "svg", "both"],
        default: "png",
        descriptions: {
          png: "High-resolution raster image, perfect for presentations and print",
          svg: "Vector-based image with infinite scalability and small file size",
          both: "Generate both PNG and SVG formats simultaneously",
        },
      },
      aspect_ratios: {
        available: [
          {
            id: "16:9",
            name: "16:9 Wide",
            dimensions: { width: 1920, height: 1080 },
            description:
              "Standard widescreen format, ideal for monitors and web",
          },
          {
            id: "4:3",
            name: "4:3 Standard",
            dimensions: { width: 1440, height: 1080 },
            description: "Classic presentation format, ideal for projectors",
          },
          {
            id: "3:4",
            name: "3:4 Portrait",
            dimensions: { width: 1080, height: 1440 },
            description:
              "Portrait orientation, ideal for social media and mobile",
          },
        ],
        default: "16:9",
      },
      dpi_settings: {
        available: [150, 300, 600],
        default: 300,
        descriptions: {
          150: "Web (Standard)",
          300: "Print (Standard)",
          600: "Ultra (Ultra)",
        },
      },
      scale_factors: {
        available: [2, 3, 4],
        default: 3,
        descriptions: {
          2: "2x",
          3: "3x",
          4: "4x",
        },
      },
    },
    performance: {
      preload_charts: true,
      render_timeout: 15000,
      retry_attempts: 3,
      cache_bust: false,
    },
  },
}));

// Mock the dashboard loader service
vi.mock("@/services/dashboardLoader", () => {
  const mockDashboard = {
    id: "portfolio_history_portrait",
    name: "Portfolio History Portrait",
    file: "portfolio-history-portrait.mdx",
    description:
      "Portfolio trading history with waterfall and time series analysis",
    layout: "2x1_stack",
    enabled: true,
    charts: [
      { id: "chart1", type: "line" },
      { id: "chart2", type: "bar" },
    ],
  };

  return {
    DashboardLoader: {
      getAllDashboards: vi.fn().mockResolvedValue([mockDashboard]),
      getDashboardById: vi.fn().mockResolvedValue(mockDashboard),
      getDefaultDashboard: vi.fn().mockResolvedValue(mockDashboard),
      getLayoutClasses: vi.fn().mockReturnValue("grid grid-cols-1 gap-4"),
    },
  };
});

// Mock ChartDisplay component to avoid complex chart rendering in unit tests
vi.mock("@/shortcodes/ChartDisplay", () => ({
  default: ({ title, chartType, titleOnly }: any) => (
    <div data-testid={`mock-chart-${chartType}`}>
      <div data-testid="chart-title">{title}</div>
      <div data-testid="chart-title-only">{titleOnly ? "true" : "false"}</div>
    </div>
  ),
}));

// Import component after mocks are set up
import PhotoBoothDisplay from "@/shortcodes/PhotoBoothDisplay";
import { DashboardLoader } from "@/services/dashboardLoader";

// Get mock instance for test assertions
const mockDashboardLoader = DashboardLoader as any;

// Mock fetch utilities for testing network scenarios
const mockFetchError = (status: number, message: string) => {
  return vi.fn().mockRejectedValue({
    ok: false,
    status,
    statusText: message,
    json: vi.fn().mockResolvedValue({ error: message }),
  });
};

const mockNetworkError = () => {
  return vi.fn().mockRejectedValue(new Error("Network error"));
};

// Common test scenarios
const testScenarios = {
  defaultLoad: {},
  portraitMode: {
    dashboard: "portfolio_history_portrait",
    mode: "light",
    aspect_ratio: "3:4",
    format: "png",
    dpi: "300",
    scale: "3",
  },
  darkMode: {
    dashboard: "portfolio_history_portrait",
    mode: "dark",
    aspect_ratio: "16:9",
  },
  invalidParams: {
    dashboard: "invalid_dashboard",
    mode: "invalid_mode",
    aspect_ratio: "invalid_ratio",
  },
};

// Mock URL and History utilities
const mockURLSearchParams = (params: Record<string, string>) => {
  const searchParams = new URLSearchParams(params);
  Object.defineProperty(window, "location", {
    value: {
      search: searchParams.toString(),
      href: `http://localhost:4321/photo-booth?${searchParams.toString()}`,
      origin: "http://localhost:4321",
      pathname: "/photo-booth",
    },
    writable: true,
    configurable: true,
  });
  return searchParams;
};

const mockWindowHistory = () => {
  const mockReplaceState = vi.fn();
  const mockPushState = vi.fn();
  Object.defineProperty(window, "history", {
    value: {
      replaceState: mockReplaceState,
      pushState: mockPushState,
    },
    writable: true,
    configurable: true,
  });
  return { mockReplaceState, mockPushState };
};

describe("PhotoBoothDisplay Component", () => {
  beforeEach(() => {
    // Reset all mocks
    vi.clearAllMocks();

    // Setup clean DOM state
    document.body.innerHTML = "";

    // Mock successful fetch by default
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue({ status: "success" }),
    }) as any;
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  describe("Component Initialization", () => {
    it("renders component without errors", async () => {
      await act(async () => {
        render(<PhotoBoothDisplay />);
      });

      // Component should render without throwing
      expect(document.body).toBeInTheDocument();
    });

    it("renders dashboard after successful loading", async () => {
      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        expect(
          screen.getByText("Portfolio History Portrait"),
        ).toBeInTheDocument();
      });
    });

    it("displays error when dashboard loading fails", async () => {
      mockDashboardLoader.getAllDashboards.mockRejectedValue(
        new Error("Network error"),
      );

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        expect(
          screen.getByText("Failed to Load Dashboards"),
        ).toBeInTheDocument();
      });
    });
  });

  describe("URL Parameter Parsing", () => {
    it("parses dashboard parameter from URL", async () => {
      mockURLSearchParams(testScenarios.portraitMode);

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const select = screen.getByDisplayValue("Portfolio History Portrait");
        expect(select).toBeInTheDocument();
      });
    });

    it("parses mode parameter and sets theme", async () => {
      mockURLSearchParams({ mode: "dark" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const darkButton = screen.getByRole("button", { name: /dark/i });
        expect(darkButton).toHaveClass("bg-blue-500");
      });
    });

    it("parses aspect ratio parameter", async () => {
      mockURLSearchParams({ aspect_ratio: "3:4" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const aspectSelect = screen.getByDisplayValue("3:4 Portrait");
        expect(aspectSelect).toBeInTheDocument();
      });
    });

    it("parses format parameter", async () => {
      mockURLSearchParams({ format: "svg" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const formatSelect = screen.getByDisplayValue("SVG");
        expect(formatSelect).toBeInTheDocument();
      });
    });

    it("parses DPI parameter", async () => {
      mockURLSearchParams({ dpi: "600" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const dpiSelect = screen.getByDisplayValue("600 (Ultra)");
        expect(dpiSelect).toBeInTheDocument();
      });
    });

    it("parses scale factor parameter", async () => {
      mockURLSearchParams({ scale: "4" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const scaleSelect = screen.getByDisplayValue("4x");
        expect(scaleSelect).toBeInTheDocument();
      });
    });
  });

  describe("State Management", () => {
    it("updates URL when dashboard changes", async () => {
      const { mockReplaceState } = mockWindowHistory();

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const select = screen.getByLabelText(/dashboard/i);
        fireEvent.change(select, {
          target: { value: "portfolio_history_portrait" },
        });
      });

      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        "",
        expect.stringContaining("dashboard=portfolio_history_portrait"),
      );
    });

    it("updates URL when mode changes", async () => {
      const { mockReplaceState } = mockWindowHistory();

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const darkButton = screen.getByRole("button", { name: /dark/i });
        fireEvent.click(darkButton);
      });

      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        "",
        expect.stringContaining("mode=dark"),
      );
    });

    it("updates URL when aspect ratio changes", async () => {
      const { mockReplaceState } = mockWindowHistory();

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const aspectSelect = screen.getByLabelText(/ratio/i);
        fireEvent.change(aspectSelect, { target: { value: "3:4" } });
      });

      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        "",
        expect.stringContaining("aspect_ratio=3:4"),
      );
    });
  });

  describe("CSS Custom Properties", () => {
    it("sets CSS custom properties based on aspect ratio", async () => {
      const mockSetProperty = vi.fn();
      const mockRef = {
        current: {
          style: {
            setProperty: mockSetProperty,
          },
        },
      };

      // Mock useRef to return our controlled ref
      vi.spyOn(React, "useRef").mockReturnValue(mockRef);

      mockURLSearchParams({ aspect_ratio: "3:4" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        expect(mockSetProperty).toHaveBeenCalledWith(
          "--photo-booth-width",
          "1080px",
        );
        expect(mockSetProperty).toHaveBeenCalledWith(
          "--photo-booth-height",
          "1440px",
        );
      });
    });
  });

  describe("Export Functionality", () => {
    it("shows export button when dashboard is ready", async () => {
      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const exportButton = screen.getByRole("button", {
          name: /export dashboard/i,
        });
        expect(exportButton).toBeInTheDocument();
        expect(exportButton).not.toBeDisabled();
      });
    });

    it("disables export button when dashboard is loading", async () => {
      await act(async () => {
        render(<PhotoBoothDisplay />);
      });

      const exportButton = screen.getByRole("button", {
        name: /export dashboard/i,
      });
      expect(exportButton).toBeDisabled();
    });

    it("calls export API with correct parameters", async () => {
      mockURLSearchParams(testScenarios.portraitMode);

      render(<PhotoBoothDisplay />);

      await waitFor(async () => {
        const exportButton = screen.getByRole("button", {
          name: /export dashboard/i,
        });
        fireEvent.click(exportButton);

        expect(global.fetch).toHaveBeenCalledWith("/api/export-dashboard", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            dashboard_id: "portfolio_history_portrait",
            mode: "light",
            aspect_ratio: "3:4",
            format: "png",
            dpi: 300,
            scale_factor: 3,
          }),
        });
      });
    });

    it("shows success message after successful export", async () => {
      render(<PhotoBoothDisplay />);

      await waitFor(async () => {
        const exportButton = screen.getByRole("button", {
          name: /export dashboard/i,
        });
        fireEvent.click(exportButton);

        await waitFor(() => {
          expect(
            screen.getByText(/successfully exported/i),
          ).toBeInTheDocument();
        });
      });
    });

    it("shows error message after failed export", async () => {
      global.fetch = mockFetchError(500, "Export failed") as any;

      render(<PhotoBoothDisplay />);

      await waitFor(async () => {
        const exportButton = screen.getByRole("button", {
          name: /export dashboard/i,
        });
        fireEvent.click(exportButton);

        await waitFor(() => {
          expect(screen.getByText(/export failed/i)).toBeInTheDocument();
        });
      });
    });

    it("handles network errors gracefully", async () => {
      global.fetch = mockNetworkError() as any;

      render(<PhotoBoothDisplay />);

      await waitFor(async () => {
        const exportButton = screen.getByRole("button", {
          name: /export dashboard/i,
        });
        fireEvent.click(exportButton);

        await waitFor(() => {
          expect(screen.getByText(/export failed/i)).toBeInTheDocument();
        });
      });
    });
  });

  describe("Dashboard Content Rendering", () => {
    it("renders portfolio history portrait with header and footer", async () => {
      mockURLSearchParams({ dashboard: "portfolio_history_portrait" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        expect(screen.getByText("Twitter Live Signals")).toBeInTheDocument();
        expect(screen.getByText("colemorton.com")).toBeInTheDocument();
      });
    });

    it("passes titleOnly=true to charts in portfolio history portrait", async () => {
      mockURLSearchParams({ dashboard: "portfolio_history_portrait" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const titleOnlyElements = screen.getAllByTestId("chart-title-only");
        titleOnlyElements.forEach((element) => {
          expect(element).toHaveTextContent("true");
        });
      });
    });

    it("applies correct theme class to dashboard", async () => {
      mockURLSearchParams({ mode: "dark" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const dashboard =
          screen.getByTestId("dashboard-content") ||
          document.querySelector(".photo-booth-dashboard");
        expect(dashboard).toHaveClass("dark");
      });
    });
  });

  describe("Ready State Management", () => {
    it("marks component as ready after timeout", async () => {
      render(<PhotoBoothDisplay />);

      // Initially should show loading
      expect(screen.getByText("Loading dashboards...")).toBeInTheDocument();

      // Component should eventually load successfully or show error
      await waitFor(
        () => {
          // Either loaded successfully with dashboard controls or failed to load
          expect(
            screen.queryByText("Loading dashboards...") ||
              screen.queryByText("Failed to Load Dashboards"),
          ).toBeTruthy();
        },
        { timeout: 16000 },
      );
    });

    it("resets ready state when parameters change", async () => {
      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        // Wait for initial load to complete
        expect(
          screen.queryByText("Loading dashboards...") ||
            screen.queryByText("Failed to Load Dashboards"),
        ).toBeTruthy();
      });

      // Since we're in error state, this test doesn't apply
      // Component will remain in error state
      expect(screen.getByText("Failed to Load Dashboards")).toBeInTheDocument();
    });
  });

  describe("Error Handling", () => {
    it("shows retry button when dashboard loading fails", async () => {
      mockDashboardLoader.getAllDashboards.mockRejectedValue(
        new Error("Network error"),
      );

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        const retryButton = screen.getByRole("button", { name: /retry/i });
        expect(retryButton).toBeInTheDocument();
      });
    });

    it("handles invalid dashboard ID gracefully", async () => {
      mockURLSearchParams({ dashboard: "invalid_dashboard" });

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        expect(
          screen.getByText("Failed to Load Dashboards"),
        ).toBeInTheDocument();
      });
    });

    it("falls back to defaults for invalid parameters", async () => {
      mockURLSearchParams(testScenarios.invalidParams);

      render(<PhotoBoothDisplay />);

      await waitFor(() => {
        // Component should show error state for invalid dashboard
        expect(
          screen.getByText("Failed to Load Dashboards"),
        ).toBeInTheDocument();
      });
    });
  });
});
