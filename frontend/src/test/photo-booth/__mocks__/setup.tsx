import React from "react";
import { vi } from "vitest";
import { mockPhotoBoothConfig } from "./photo-booth-config.mock";
import {
  mockDashboardLoader,
  mockAllDashboards,
} from "./dashboard-loader.mock";

// Mock the photo booth config import
vi.mock("@/config/photo-booth.json", () => ({
  default: mockPhotoBoothConfig,
}));

// Mock the dashboard loader service
vi.mock("@/services/dashboardLoader", () => ({
  DashboardLoader: mockDashboardLoader,
}));

// Mock ChartDisplay component to avoid complex chart rendering in unit tests
vi.mock("@/shortcodes/ChartDisplay", () => ({
  default: ({ title, chartType, titleOnly, className }: any) => (
    <div data-testid={`mock-chart-${chartType}`} className={className || ""}>
      <div data-testid="chart-title">{title}</div>
      <div data-testid="chart-title-only">{titleOnly ? "true" : "false"}</div>
    </div>
  ),
}));

// Setup default mock behaviors
export const setupPhotoBoothMocks = () => {
  vi.clearAllMocks();

  // Mock successful dashboard loading by default
  mockDashboardLoader.getAllDashboards.mockResolvedValue(mockAllDashboards);

  // Mock successful fetch by default
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () =>
        Promise.resolve({
          success: true,
          message: "Successfully exported dashboard",
          files: ["/path/to/generated/file.png"],
        }),
    }),
  ) as any;
};

// Export all mocks for individual use
export { mockPhotoBoothConfig } from "./photo-booth-config.mock";
export {
  mockDashboardLoader,
  mockAllDashboards,
  mockPortfolioHistoryPortraitDashboard,
  mockExportSuccess,
  mockExportError,
  mockFetchSuccess,
  mockFetchError,
  mockNetworkError,
  createMockDashboard,
  createMockChart,
} from "./dashboard-loader.mock";
