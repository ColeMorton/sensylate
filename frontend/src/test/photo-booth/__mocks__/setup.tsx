import { vi } from "vitest";

// Setup default mock behaviors
export const setupPhotoBoothMocks = () => {
  vi.clearAllMocks();

  // Note: Dashboard loader is now mocked at module level via vi.mock()
  // Individual tests can override specific methods as needed

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
