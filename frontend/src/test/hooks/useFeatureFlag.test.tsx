import { describe, it, expect, beforeEach, vi } from "vitest";
import { render } from "@testing-library/react";
import React from "react";

// Mock environment variables
const mockEnv = {
  PUBLIC_FEATURE_SEARCH: "true",
  PUBLIC_FEATURE_THEME_SWITCHER: "false",
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
  });

  // Test component that uses the hook
  const TestComponent = ({ flag }: { flag: string }) => {
    const { useFeatureFlag } = require("@/hooks/useFeatureFlag");
    const isEnabled = useFeatureFlag(flag);
    return (
      <div data-testid="feature-status">
        {isEnabled ? "enabled" : "disabled"}
      </div>
    );
  };

  const TestMultipleComponent = () => {
    const {
      useFeatureFlags,
      useAllFeatures,
      useAnyFeature,
    } = require("@/hooks/useFeatureFlag");
    const allFlags = useFeatureFlags();
    const allEnabled = useAllFeatures(["search", "comments"]);
    const anyEnabled = useAnyFeature(["theme_switcher", "gtm"]);

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

  it("should return correct feature flag status", () => {
    const { getByTestId } = render(<TestComponent flag="search" />);
    expect(getByTestId("feature-status")).toHaveTextContent("enabled");
  });

  it("should return false for disabled features", () => {
    const { getByTestId } = render(<TestComponent flag="theme_switcher" />);
    expect(getByTestId("feature-status")).toHaveTextContent("disabled");
  });

  it("should handle multiple feature flag operations", () => {
    const { getByTestId } = render(<TestMultipleComponent />);

    const allFlags = JSON.parse(getByTestId("all-flags").textContent || "{}");
    expect(allFlags.search).toBe(true);
    expect(allFlags.theme_switcher).toBe(false);

    expect(getByTestId("all-enabled")).toHaveTextContent("all-true"); // search and comments both true
    expect(getByTestId("any-enabled")).toHaveTextContent("all-false"); // theme_switcher and gtm both false
  });
});
