import { vi } from "vitest";

// Mock photo booth configuration data
export const mockPhotoBoothConfig = {
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
          name: "Widescreen (16:9)",
          dimensions: { width: 1920, height: 1080 },
          description: "Standard widescreen format, ideal for monitors and web",
        },
        {
          id: "4:3",
          name: "Traditional (4:3)",
          dimensions: { width: 1440, height: 1080 },
          description: "Classic presentation format, ideal for projectors",
        },
        {
          id: "3:4",
          name: "Portrait (3:4)",
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
        150: "Web/Digital - Standard screen resolution",
        300: "Print/Professional - High-quality printing standard",
        600: "Ultra-High - Professional publishing and large format",
      },
    },
    scale_factors: {
      available: [2, 3, 4],
      default: 3,
      descriptions: {
        2: "Standard high-DPI (2x resolution)",
        3: "Enhanced high-DPI (3x resolution)",
        4: "Ultra high-DPI (4x resolution)",
      },
    },
  },
  output: {
    directory: "data/outputs/photo-booth",
    filename_template:
      "{dashboard_id}_{mode}_{aspect_ratio}_{format}_{dpi}dpi_{timestamp}.{extension}",
    modes: ["light", "dark"],
    auto_cleanup: {
      enabled: true,
      keep_latest: 10,
      older_than_days: 30,
    },
  },
  performance: {
    preload_charts: true,
    render_timeout: 15000,
    retry_attempts: 3,
    cache_bust: false,
  },
};

// Mock photo booth config import
export const mockPhotoBoothConfigImport = vi.fn(() => mockPhotoBoothConfig);

// Mock URL search params for testing different scenarios
export const mockURLSearchParams = (params: Record<string, string>) => {
  const searchParams = new URLSearchParams(params);

  Object.defineProperty(window, "location", {
    value: {
      search: searchParams.toString(),
      href: `http://localhost:4321/photo-booth?${searchParams.toString()}`,
      origin: "http://localhost:4321",
      pathname: "/photo-booth",
    },
    writable: true,
  });

  return searchParams;
};

// Mock window.history for URL state management testing
export const mockWindowHistory = () => {
  const mockReplaceState = vi.fn();

  Object.defineProperty(window, "history", {
    value: {
      replaceState: mockReplaceState,
    },
    writable: true,
  });

  return { mockReplaceState };
};

// Common test scenarios
export const testScenarios = {
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
