import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";

// Mock environment variables for different scenarios
const createMockEnv = (overrides: Record<string, string> = {}) => ({
  PUBLIC_FEATURE_SEARCH: "true",
  PUBLIC_FEATURE_THEME_SWITCHER: "true",
  PUBLIC_FEATURE_COMMENTS: "false",
  PUBLIC_FEATURE_GTM: "false",
  PUBLIC_FEATURE_CALCULATOR_ADVANCED: "false",
  PUBLIC_ENV: "test",
  DEV: true,
  PROD: false,
  ...overrides,
});

// Mock config.json
vi.mock("@/config/config.json", () => ({
  default: {
    settings: {
      search: false,
      theme_switcher: false,
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

describe("Component Conditional Rendering", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("SearchModal Conditional Rendering", () => {
    const MockSearchModal = () => {
      // Mock the SearchModal component behavior
      const { useFeatureFlag } = require("@/hooks/useFeatureFlag");
      const isSearchEnabled = useFeatureFlag("search");

      if (!isSearchEnabled) {
        return null;
      }

      return <div data-testid="search-modal">Search Modal Content</div>;
    };

    it("should render when search feature is enabled", () => {
      vi.stubGlobal(
        "import.meta.env",
        createMockEnv({ PUBLIC_FEATURE_SEARCH: "true" }),
      );
      vi.resetModules();

      render(<MockSearchModal />);
      expect(screen.getByTestId("search-modal")).toBeInTheDocument();
    });

    it("should not render when search feature is disabled", () => {
      vi.stubGlobal(
        "import.meta.env",
        createMockEnv({ PUBLIC_FEATURE_SEARCH: "false" }),
      );
      vi.resetModules();

      render(<MockSearchModal />);
      expect(screen.queryByTestId("search-modal")).not.toBeInTheDocument();
    });
  });

  describe("Calculator Feature Integration", () => {
    const MockCalculatorList = () => {
      const { features } = require("@/lib/featureFlags");
      const baseCalculators = ["pocket", "dca", "mortgage"];
      const advancedCalculators = ["compound-interest", "roi-tracker"];

      const availableCalculators = features.calculator_advanced
        ? [...baseCalculators, ...advancedCalculators]
        : baseCalculators;

      return (
        <div>
          {availableCalculators.map((calc) => (
            <div key={calc} data-testid={`calculator-${calc}`}>
              {calc}
            </div>
          ))}
        </div>
      );
    };

    it("should show only basic calculators when advanced feature is disabled", () => {
      vi.stubGlobal(
        "import.meta.env",
        createMockEnv({ PUBLIC_FEATURE_CALCULATOR_ADVANCED: "false" }),
      );
      vi.resetModules();

      render(<MockCalculatorList />);

      expect(screen.getByTestId("calculator-pocket")).toBeInTheDocument();
      expect(screen.getByTestId("calculator-dca")).toBeInTheDocument();
      expect(screen.getByTestId("calculator-mortgage")).toBeInTheDocument();
      expect(
        screen.queryByTestId("calculator-compound-interest"),
      ).not.toBeInTheDocument();
      expect(
        screen.queryByTestId("calculator-roi-tracker"),
      ).not.toBeInTheDocument();
    });

    it("should show all calculators when advanced feature is enabled", () => {
      vi.stubGlobal(
        "import.meta.env",
        createMockEnv({ PUBLIC_FEATURE_CALCULATOR_ADVANCED: "true" }),
      );
      vi.resetModules();

      render(<MockCalculatorList />);

      expect(screen.getByTestId("calculator-pocket")).toBeInTheDocument();
      expect(screen.getByTestId("calculator-dca")).toBeInTheDocument();
      expect(screen.getByTestId("calculator-mortgage")).toBeInTheDocument();
      expect(
        screen.getByTestId("calculator-compound-interest"),
      ).toBeInTheDocument();
      expect(screen.getByTestId("calculator-roi-tracker")).toBeInTheDocument();
    });
  });

  describe("Feature Flag Fallback Behavior", () => {
    const MockComponent = () => {
      const { useFeatureFlag } = require("@/hooks/useFeatureFlag");
      const searchEnabled = useFeatureFlag("search");
      const themeEnabled = useFeatureFlag("theme_switcher");

      return (
        <div>
          <div data-testid="search-status">
            {searchEnabled ? "search-on" : "search-off"}
          </div>
          <div data-testid="theme-status">
            {themeEnabled ? "theme-on" : "theme-off"}
          </div>
        </div>
      );
    };

    it("should fallback to static config when environment variables are undefined", () => {
      // Don't set environment variables, should fall back to config.json
      vi.stubGlobal("import.meta.env", {
        DEV: true,
        PROD: false,
        PUBLIC_ENV: "test",
        // No feature flag environment variables
      });
      vi.resetModules();

      render(<MockComponent />);

      // Should use config.json values: search=false, theme_switcher=false
      expect(screen.getByTestId("search-status")).toHaveTextContent(
        "search-off",
      );
      expect(screen.getByTestId("theme-status")).toHaveTextContent("theme-off");
    });
  });
});
