import { describe, it, expect, beforeEach, vi } from "vitest";

// Mock environment variables
const mockEnv = {
  PUBLIC_FEATURE_SEARCH: "true",
  PUBLIC_FEATURE_THEME_SWITCHER: "false",
  PUBLIC_FEATURE_COMMENTS: "true",
  PUBLIC_FEATURE_GTM: "false",
  PUBLIC_FEATURE_CALCULATORS: "true",
  PUBLIC_FEATURE_CALCULATOR_ADVANCED: "true",
  PUBLIC_FEATURE_ELEMENTS_PAGE: "true",
  PUBLIC_FEATURE_AUTHORS_PAGE: "true",
  PUBLIC_FEATURE_CHARTS_PAGE: "true",
  PUBLIC_ENV: "test",
};

// Mock import.meta.env
vi.stubGlobal("import.meta.env", {
  DEV: true,
  PROD: false,
  ...mockEnv,
});

// Mock config.json  
vi.mock("@/config/config.json", () => ({
  default: {
    settings: {
      search: false,
      theme_switcher: true, // Keep original snake_case for compatibility
      sticky_header: true,
      default_theme: "system",
      pagination: 2,
      summary_length: 200,
      blog_folder: "blog",
    },
    disqus: {
      enable: false,
    },
    google_tag_manager: {
      enable: false,
    },
    site: {},
    params: {},
    navigation_button: {},
    metadata: {},
  },
}));

describe("Feature Flags Configuration", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Environment Variable Override", () => {
    it("should override static config with environment variables", async () => {
      const { enhancedConfig } = await import("@/lib/config");

      // Environment variables should override static config
      expect(enhancedConfig.features.search).toBe(true); // env: true, config: false
      expect(enhancedConfig.features.themeSwitcher).toBe(false); // env: false, config: true
      expect(enhancedConfig.features.comments).toBe(true); // env: true, config: false
      expect(enhancedConfig.features.gtm).toBe(false); // env: false, config: false
      expect(enhancedConfig.features.calculatorAdvanced).toBe(true); // env: true, config: undefined
      expect(enhancedConfig.features.elementsPage).toBe(true); // env: true, config: undefined
      expect(enhancedConfig.features.authorsPage).toBe(true); // env: true, config: undefined
    });

    it("should fall back to static config when environment variable is undefined", async () => {
      // Mock environment without some variables
      vi.stubGlobal("import.meta.env", {
        DEV: true,
        PROD: false,
        PUBLIC_FEATURE_SEARCH: undefined,
        PUBLIC_FEATURE_THEME_SWITCHER: "false",
        PUBLIC_ENV: "test",
      });

      // Re-import to get fresh module
      vi.resetModules();
      const { enhancedConfig } = await import("@/lib/config");

      // Should fall back to static config for search
      expect(enhancedConfig.features.search).toBe(false); // fallback to config
      expect(enhancedConfig.features.themeSwitcher).toBe(false); // env override
    });
  });

  describe("Feature Flag Utilities", () => {
    it("should provide correct feature flag status", async () => {
      const { isFeatureEnabled, features } = await import("@/lib/featureFlags");

      expect(isFeatureEnabled("search")).toBe(true);
      expect(isFeatureEnabled("themeSwitcher")).toBe(false);
      expect(isFeatureEnabled("calculatorAdvanced")).toBe(true);
      expect(isFeatureEnabled("elementsPage")).toBe(true);
      expect(isFeatureEnabled("authorsPage")).toBe(true);

      expect(features.search).toBe(true);
      expect(features.themeSwitcher).toBe(false);
      expect(features.elementsPage).toBe(true);
      expect(features.authorsPage).toBe(true);
    });

    it("should handle multiple feature flag checks", async () => {
      const { areAllFeaturesEnabled, isAnyFeatureEnabled } = await import(
        "@/lib/featureFlags"
      );

      expect(areAllFeaturesEnabled(["search", "comments"])).toBe(true);
      expect(areAllFeaturesEnabled(["search", "themeSwitcher"])).toBe(false);

      expect(isAnyFeatureEnabled(["search", "themeSwitcher"])).toBe(true);
      expect(isAnyFeatureEnabled(["themeSwitcher", "gtm"])).toBe(false);
    });
  });

  describe("Environment Detection", () => {
    it("should correctly detect environment", async () => {
      const { env } = await import("@/lib/config");

      expect(env.isDevelopment()).toBe(true);
      expect(env.isProduction()).toBe(false);
      expect(env.current).toBe("test");
    });
  });

  describe("Configuration Validation", () => {
    it("should have all required feature flags as booleans", async () => {
      const { enhancedConfig } = await import("@/lib/config");

      const requiredFlags = [
        "search",
        "themeSwitcher",
        "comments",
        "gtm",
        "calculatorAdvanced",
        "elementsPage",
        "authorsPage",
      ];

      requiredFlags.forEach((flag) => {
        expect(
          typeof enhancedConfig.features[
            flag as keyof typeof enhancedConfig.features
          ],
        ).toBe("boolean");
      });
    });

    it("should maintain backward compatibility with original config", async () => {
      const { enhancedConfig } = await import("@/lib/config");

      // Should still have all original config properties
      expect(enhancedConfig.settings).toBeDefined();
      expect(enhancedConfig.disqus).toBeDefined();
      expect(enhancedConfig.google_tag_manager).toBeDefined();
      expect(enhancedConfig.site).toBeDefined();
    });
  });
});
