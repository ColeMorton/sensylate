import {
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
  beforeAll,
} from "vitest";
import {
  photoBoothE2EHelper,
  setupPhotoBoothE2E,
  cleanupPhotoBoothE2E,
  type E2ETestContext,
  skipIfNotDevelopmentMode,
  isPhotoBoothDevelopmentMode,
} from "../utils/e2e-setup";
import type { Page } from "puppeteer";

// Theme state interface for type safety
interface LogoThemeState {
  hasDarkClass: boolean;
  containerClasses: string;
  textColorVar: string;
  darkTextColorVar: string;
  logoTextColor: string;
  logoComputedStyles: {
    color: string;
    backgroundColor: string;
    fontFamily: string;
    fontSize: string;
  };
  brandText: string;
  dashboardMode: string;
}

describe("Photo-Booth Light Theme Logo Validation", () => {
  let context: E2ETestContext;
  let page: Page;

  beforeAll(async () => {
    // Validate environment before running PhotoBooth E2E tests
    if (!isPhotoBoothDevelopmentMode()) {
      console.warn(
        "⚠️  PhotoBooth Light Theme tests are skipped - development environment required",
      );
      console.warn("   Run with: yarn test:photo-booth:light-theme");
    }
  });

  beforeEach(async () => {
    // Skip tests if not in development mode
    if (!isPhotoBoothDevelopmentMode()) {
      return; // Skip setup for production mode
    }

    // Use shared server and browser from globalSetup
    context = await setupPhotoBoothE2E();
    page = context.page;
  });

  afterEach(async () => {
    // Skip cleanup if not in development mode
    if (!isPhotoBoothDevelopmentMode()) {
      return; // Skip cleanup for production mode
    }

    // Only cleanup test-specific resources (pages)
    await cleanupPhotoBoothE2E();
  });

  // Helper function to get detailed logo theme state
  async function getLogoThemeState(): Promise<LogoThemeState> {
    return await page.evaluate(() => {
      const html = document.documentElement;
      const dashboardContainer = document.querySelector(
        ".photo-booth-dashboard",
      ) as HTMLElement;
      const logoElement = document.querySelector(".brand-text") as HTMLElement;

      if (!logoElement) {
        throw new Error("Logo element not found");
      }

      // Get CSS custom properties
      const rootStyles = window.getComputedStyle(html);
      const textColorVar = rootStyles
        .getPropertyValue("--color-text-dark")
        .trim();
      const darkTextColorVar = rootStyles
        .getPropertyValue("--color-darkmode-text-dark")
        .trim();

      // Get computed styles for logo
      const logoStyles = window.getComputedStyle(logoElement);

      return {
        hasDarkClass: html.classList.contains("dark"),
        containerClasses: dashboardContainer?.className || "",
        textColorVar,
        darkTextColorVar,
        logoTextColor: logoStyles.color,
        logoComputedStyles: {
          color: logoStyles.color,
          backgroundColor: logoStyles.backgroundColor,
          fontFamily: logoStyles.fontFamily,
          fontSize: logoStyles.fontSize,
        },
        brandText: logoElement.textContent?.trim() || "",
        dashboardMode: dashboardContainer?.getAttribute("data-mode") || "",
      };
    });
  }

  // Helper function to navigate to logo dashboard with specific parameters
  async function navigateToLogoDashboard(
    mode: "light" | "dark" = "light",
    brand: "personal" | "attribution" = "personal",
    aspectRatio: string = "16:9",
  ) {
    const url = `${context.baseURL}/photo-booth?dashboard=logo_generation&mode=${mode}&brand=${brand}&aspect_ratio=${aspectRatio}`;

    console.log(`🌐 Navigating to: ${url}`);

    await page.goto(url, {
      waitUntil: "networkidle0",
      timeout: 30000,
    });

    // Wait for dashboard to be ready
    await page.waitForSelector(".photo-booth-ready", {
      timeout: 15000,
    });

    // Additional wait for theme application
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  // Helper function to take themed screenshot
  async function takeThemedScreenshot(
    testName: string,
    mode: "light" | "dark" = "light",
    brand: "personal" | "attribution" = "personal",
  ) {
    if (photoBoothE2EHelper.takeScreenshot) {
      const screenshotName = `${testName}-${mode}-${brand}`;
      await photoBoothE2EHelper.takeScreenshot(page, screenshotName);
      return screenshotName;
    }
  }

  describe("CSS Variable Resolution", () => {
    it("should have correct light theme CSS variables", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");
      const themeState = await getLogoThemeState();

      console.log("🎨 Light theme state:", themeState);

      // Validate CSS custom properties
      expect(themeState.textColorVar).toBe("#1A1A1A"); // Black color for light theme
      expect(themeState.darkTextColorVar).toBe("#F9FAFB"); // White color for dark theme

      // Ensure we're not in dark mode
      expect(themeState.hasDarkClass).toBe(false);
      expect(themeState.dashboardMode).toBe("light");

      // Validate container classes don't have conflicting mode classes
      expect(themeState.containerClasses).not.toMatch(/dark-mode|dark(?:\s|$)/);
      expect(themeState.containerClasses).toContain(
        "logo-generation-container",
      );
    });

    it("should resolve light theme text color correctly", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");
      const themeState = await getLogoThemeState();

      // The computed color should be black (RGB 26, 26, 26)
      expect(themeState.logoTextColor).toBe("rgb(26, 26, 26)");

      // Background should be transparent or rgba(0, 0, 0, 0)
      const bgColor = themeState.logoComputedStyles.backgroundColor;
      expect(bgColor === "rgba(0, 0, 0, 0)" || bgColor === "transparent").toBe(
        true,
      );
    });
  });

  describe("Logo Color Rendering", () => {
    it("should render personal brand logo with black text in light theme", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");
      const themeState = await getLogoThemeState();

      // Validate brand text
      expect(themeState.brandText).toBe("Cole Morton");

      // Validate color is black
      expect(themeState.logoTextColor).toBe("rgb(26, 26, 26)");

      // Take screenshot for visual validation
      await takeThemedScreenshot("personal-brand-light", "light", "personal");
    });

    it("should render attribution brand logo with black text in light theme", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "attribution");
      const themeState = await getLogoThemeState();

      // Validate brand text
      expect(themeState.brandText).toBe("colemorton.com");

      // Validate color is black
      expect(themeState.logoTextColor).toBe("rgb(26, 26, 26)");

      // Take screenshot for visual validation
      await takeThemedScreenshot(
        "attribution-brand-light",
        "light",
        "attribution",
      );
    });

    it("should maintain consistent styling across different aspect ratios", async () => {
      skipIfNotDevelopmentMode();

      const aspectRatios = ["16:9", "3:4"];

      for (const aspectRatio of aspectRatios) {
        await navigateToLogoDashboard("light", "personal", aspectRatio);
        const themeState = await getLogoThemeState();

        // Color should be consistent regardless of aspect ratio
        expect(themeState.logoTextColor).toBe("rgb(26, 26, 26)");
        expect(themeState.brandText).toBe("Cole Morton");

        // Font properties should be consistent
        expect(themeState.logoComputedStyles.fontFamily).toContain("Heebo");
        expect(themeState.logoComputedStyles.fontSize).toBeTruthy();
      }
    });
  });

  describe("Visual Regression Protection", () => {
    it("should generate visually different images for light vs dark themes", async () => {
      skipIfNotDevelopmentMode();

      // Test light theme
      await navigateToLogoDashboard("light", "personal");
      const lightThemeState = await getLogoThemeState();
      await takeThemedScreenshot("theme-comparison", "light", "personal");

      // Test dark theme
      await navigateToLogoDashboard("dark", "personal");
      const darkThemeState = await getLogoThemeState();
      await takeThemedScreenshot("theme-comparison", "dark", "personal");

      // Validate they have different colors
      expect(lightThemeState.logoTextColor).toBe("rgb(26, 26, 26)"); // Black
      expect(darkThemeState.logoTextColor).toBe("rgb(249, 250, 251)"); // White
      expect(lightThemeState.logoTextColor).not.toBe(
        darkThemeState.logoTextColor,
      );

      // Validate theme states are different
      expect(lightThemeState.hasDarkClass).toBe(false);
      expect(darkThemeState.hasDarkClass).toBe(true);
      expect(lightThemeState.dashboardMode).toBe("light");
      expect(darkThemeState.dashboardMode).toBe("dark");
    });

    it("should maintain visual consistency across browser sessions", async () => {
      skipIfNotDevelopmentMode();

      const testResults = [];

      // Test multiple sessions
      for (let i = 0; i < 3; i++) {
        await navigateToLogoDashboard("light", "personal");
        const themeState = await getLogoThemeState();
        testResults.push(themeState);

        // Small delay between tests
        await new Promise((resolve) => setTimeout(resolve, 500));
      }

      // All results should be consistent
      const firstResult = testResults[0];
      testResults.forEach((result, _index) => {
        expect(result.logoTextColor).toBe(firstResult.logoTextColor);
        expect(result.brandText).toBe(firstResult.brandText);
        expect(result.hasDarkClass).toBe(firstResult.hasDarkClass);
      });
    });
  });

  describe("DOM Structure Validation", () => {
    it("should have clean class hierarchy without conflicting mode classes", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");
      const themeState = await getLogoThemeState();

      // Container should not have conflicting dark mode classes
      expect(themeState.containerClasses).not.toMatch(/dark-mode/);
      expect(themeState.containerClasses).not.toMatch(/\bdark\b/);

      // Should have correct classes
      expect(themeState.containerClasses).toContain(
        "logo-generation-container",
      );

      // Root should not have dark class for light theme
      expect(themeState.hasDarkClass).toBe(false);
    });

    it("should have correct data attributes on dashboard container", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");

      const dataAttributes = await page.evaluate(() => {
        const container = document.querySelector(
          ".photo-booth-dashboard",
        ) as HTMLElement;
        return {
          mode: container?.getAttribute("data-mode"),
          dashboard: container?.getAttribute("data-dashboard-id"),
          aspectRatio: container?.getAttribute("data-aspect-ratio"),
        };
      });

      expect(dataAttributes.mode).toBe("light");
      expect(dataAttributes.dashboard).toBe("logo_generation");
      expect(dataAttributes.aspectRatio).toBeTruthy();
    });

    it("should have proper brand text content switching", async () => {
      skipIfNotDevelopmentMode();

      // Test personal brand
      await navigateToLogoDashboard("light", "personal");
      let themeState = await getLogoThemeState();
      expect(themeState.brandText).toBe("Cole Morton");

      // Test attribution brand
      await navigateToLogoDashboard("light", "attribution");
      themeState = await getLogoThemeState();
      expect(themeState.brandText).toBe("colemorton.com");
    });
  });

  describe("Integration with Photo-Booth System", () => {
    it("should work with existing photo booth infrastructure", async () => {
      skipIfNotDevelopmentMode();

      await navigateToLogoDashboard("light", "personal");

      // Check for photo booth ready indicator
      const readyIndicator = await page.waitForSelector(".photo-booth-ready", {
        timeout: 10000,
      });
      expect(readyIndicator).toBeTruthy();

      // Validate dashboard is loaded
      const dashboardLoaded = await page.evaluate(() => {
        return document.querySelector(".photo-booth-dashboard") !== null;
      });
      expect(dashboardLoaded).toBe(true);

      // Validate control panel exists (but hidden in screenshot mode)
      const controlPanel = await page.evaluate(() => {
        return document.querySelector(".photo-booth-controls") !== null;
      });
      expect(controlPanel).toBe(true);
    });

    it("should maintain theme consistency during navigation", async () => {
      skipIfNotDevelopmentMode();

      // Navigate to light theme
      await navigateToLogoDashboard("light", "personal");
      const lightState = await getLogoThemeState();

      // Navigate to different dashboard and back
      await page.goto(
        `${context.baseURL}/photo-booth?dashboard=trading_performance&mode=light`,
      );
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Navigate back to logo dashboard
      await navigateToLogoDashboard("light", "personal");
      const returnState = await getLogoThemeState();

      // Theme should be consistent
      expect(returnState.logoTextColor).toBe(lightState.logoTextColor);
      expect(returnState.hasDarkClass).toBe(lightState.hasDarkClass);
      expect(returnState.dashboardMode).toBe(lightState.dashboardMode);
    });
  });
});
