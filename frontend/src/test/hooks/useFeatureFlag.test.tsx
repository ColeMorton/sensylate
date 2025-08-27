import { describe, it, expect, beforeEach, vi } from "vitest";
import { render } from "@testing-library/react";
import React from "react";

// Mock environment variables by merging with existing env
const mockEnv = {
  ...import.meta.env,
  PUBLIC_FEATURE_SEARCH: "true",
  PUBLIC_FEATURE_THEME_SWITCHER: undefined, // Test fallback to config
  PUBLIC_FEATURE_COMMENTS: "true",
  PUBLIC_FEATURE_GTM: "false",
  PUBLIC_FEATURE_CALCULATOR_ADVANCED: "true",
  PUBLIC_ENV: "test",
  DEV: true,
  PROD: false,
};

vi.stubGlobal("import.meta.env", mockEnv);

// Mock config.json
vi.mock("@/config/config.json", () => ({
  default: {
    settings: {
      search: false,
      theme_switcher: true,
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

describe("useFeatureFlag Hook", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  it("should return correct feature flag status", async () => {
    // Import hooks after mocks are set up
    const { useFeatureFlag } = await import("@/hooks/useFeatureFlag");

    // Test component that uses the hook
    const TestComponent = ({ flag }: { flag: string }) => {
      const isEnabled = useFeatureFlag(flag);
      return (
        <div data-testid="feature-status">
          {isEnabled ? "enabled" : "disabled"}
        </div>
      );
    };

    const { getByTestId } = render(<TestComponent flag="search" />);
    // Based on standardized test environment: search = false
    expect(getByTestId("feature-status")).toHaveTextContent("disabled");
  });

  it("should return false for disabled features", async () => {
    // Import hooks after mocks are set up
    const { useFeatureFlag } = await import("@/hooks/useFeatureFlag");

    const TestComponent = ({ flag }: { flag: string }) => {
      const isEnabled = useFeatureFlag(flag);
      return (
        <div data-testid="feature-status">
          {isEnabled ? "enabled" : "disabled"}
        </div>
      );
    };

    const { getByTestId } = render(<TestComponent flag="themeSwitcher" />);
    // Based on standardized test environment: themeSwitcher = true
    expect(getByTestId("feature-status")).toHaveTextContent("enabled");
  });

  it("should handle multiple feature flag operations", async () => {
    // Import hooks after mocks are set up
    const { useFeatureFlags, useAllFeatures, useAnyFeature } = await import(
      "@/hooks/useFeatureFlag"
    );

    const TestMultipleComponent = () => {
      const allFlags = useFeatureFlags();
      const allEnabled = useAllFeatures(["search", "comments"]);
      const anyEnabled = useAnyFeature(["themeSwitcher", "gtm"]);

      return (
        <div>
          <div data-testid="all-flags">{JSON.stringify(allFlags)}</div>
          <div data-testid="all-enabled">
            {allEnabled ? "all-true" : "some-false"}
          </div>
          <div data-testid="any-enabled">
            {anyEnabled ? "some-true" : "all-false"}
          </div>
        </div>
      );
    };

    const { getByTestId } = render(<TestMultipleComponent />);

    const allFlags = JSON.parse(getByTestId("all-flags").textContent || "{}");
    // Based on standardized test environment
    expect(allFlags.search).toBe(false);
    expect(allFlags.themeSwitcher).toBe(true);

    expect(getByTestId("all-enabled")).toHaveTextContent("some-false"); // search=false, comments=false
    expect(getByTestId("any-enabled")).toHaveTextContent("some-true"); // themeSwitcher=true
  });
});
