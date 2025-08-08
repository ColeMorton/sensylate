import { vi } from "vitest";
import type {
  DashboardConfig,
  DashboardChart,
} from "@/services/dashboardLoader";

// Mock dashboard configuration for portfolio_history_portrait
export const mockPortfolioHistoryPortraitDashboard: DashboardConfig = {
  id: "portfolio_history_portrait",
  title: "Portfolio History Portrait",
  description:
    "Portfolio trading history with waterfall and time series analysis",
  layout: "2x1_stack",
  mode: "both",
  enabled: true,
  charts: [
    {
      title: "Closed Position PnL Waterfall",
      category: "Trading Performance",
      description:
        "Waterfall chart showing individual trade profits and losses from closed positions, sorted from highest to lowest PnL. Visualizes contribution of each trade to overall portfolio performance.",
      chartType: "trade-pnl-waterfall",
    },
    {
      title: "Closed Position PnL Performance",
      category: "Trading Performance",
      description:
        "Multi-line time series showing cumulative PnL for each closed position, indexed to $0 at entry date. Track performance progression across the closed portfolio with individual lines for each ticker.",
      chartType: "closed-positions-pnl-timeseries",
    },
  ],
};

// Mock all dashboard configurations
export const mockAllDashboards: DashboardConfig[] = [
  mockPortfolioHistoryPortraitDashboard,
  {
    id: "trading_performance",
    title: "Trading Performance Dashboard",
    description: "Comprehensive trading strategy performance overview",
    layout: "2x2_grid",
    mode: "both",
    enabled: true,
    charts: [
      {
        title: "Bitcoin Portfolio Value Comparison",
        category: "Bitcoin Performance",
        description:
          "Multi-strategy Bitcoin trading vs buy-and-hold approach from 2014-2025",
        chartType: "portfolio-value-comparison",
      },
    ],
  },
];

// Mock DashboardLoader service
export const mockDashboardLoader = {
  getAllDashboards: vi.fn(() => Promise.resolve(mockAllDashboards)),
  getDashboard: vi.fn((id: string) => {
    const dashboard = mockAllDashboards.find((d) => d.id === id);
    return Promise.resolve(dashboard || null);
  }),
  getLayoutClasses: vi.fn((layout: string) => {
    const layoutMappings: Record<string, string> = {
      "2x2_grid": "grid grid-cols-1 gap-6 lg:grid-cols-2 h-full",
      "1x3_stack": "flex flex-col gap-6 h-full",
      "2x1_stack": "flex flex-col h-full",
      "3x1_row": "grid grid-cols-1 gap-6 lg:grid-cols-3 h-full",
      "1x2_column": "grid grid-cols-1 gap-6 lg:grid-cols-2 h-full",
    };
    return layoutMappings[layout] || "flex flex-col gap-6 h-full";
  }),
};

// Mock API responses
export const mockDashboardsApiResponse = {
  success: true,
  dashboards: mockAllDashboards,
  timestamp: new Date().toISOString(),
  source: "static_config",
};

export const mockDashboardsApiError = {
  success: false,
  error: "Failed to load dashboards",
  message: "Network error",
  timestamp: new Date().toISOString(),
};

// Mock export API responses
export const mockExportSuccess = {
  success: true,
  message: 'Successfully exported dashboard "portfolio_history_portrait"',
  files: ["/path/to/generated/file.png"],
};

export const mockExportError = {
  success: false,
  message: "Export generation failed",
  error: "Python script execution failed",
};

// Mock fetch responses
export const mockFetchSuccess = (data: any) =>
  vi.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(data),
    }),
  );

export const mockFetchError = (status: number, message: string) =>
  vi.fn(() =>
    Promise.resolve({
      ok: false,
      status,
      json: () => Promise.resolve({ error: message }),
    }),
  );

// Mock network failure
export const mockNetworkError = () =>
  vi.fn(() => Promise.reject(new Error("Network connection failed")));

// Test data factory
export const createMockDashboard = (
  overrides: Partial<DashboardConfig> = {},
): DashboardConfig => ({
  ...mockPortfolioHistoryPortraitDashboard,
  ...overrides,
});

export const createMockChart = (
  overrides: Partial<DashboardChart> = {},
): DashboardChart => ({
  title: "Test Chart",
  category: "Test Category",
  description: "Test chart description",
  chartType: "trade-pnl-waterfall",
  ...overrides,
});
