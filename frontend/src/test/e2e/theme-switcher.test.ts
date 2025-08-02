import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

describe("Theme Switcher E2E Tests", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  // Helper function to get theme state
  async function getThemeState() {
    return await page.evaluate(() => {
      const html = document.documentElement;
      const body = document.body;
      const hasDarkClass = html.classList.contains("dark");
      const storedTheme = localStorage.getItem("theme");
      const systemPrefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)",
      ).matches;

      // Get computed styles
      const bodyStyles = window.getComputedStyle(body);
      const backgroundColor = bodyStyles.backgroundColor;
      const color = bodyStyles.color;

      // Get CSS variables
      const rootStyles = window.getComputedStyle(html);
      const colorBodyVar = rootStyles.getPropertyValue("--color-body").trim();
      const colorTextVar = rootStyles.getPropertyValue("--color-text").trim();

      return {
        hasDarkClass,
        storedTheme,
        systemPrefersDark,
        backgroundColor,
        color,
        colorBodyVar,
        colorTextVar,
        htmlClasses: html.className,
        bodyClasses: body.className,
      };
    });
  }

  // Helper function to click theme switcher
  async function clickThemeSwitcher() {
    const themeSwitcher = await page.$("#theme-switcher");
    expect(themeSwitcher).toBeTruthy();
    await themeSwitcher!.click();

    // Wait for theme to change
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  // Helper function to navigate to a page and wait for it to load
  async function navigateToPage(path: string) {
    await page.goto(`${e2eHelper.baseURL}${path}`, {
      waitUntil: "networkidle0",
    });
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Give time for theme scripts to run
  }

  describe("Initial Theme State", () => {
    it("should load homepage with correct initial theme", async () => {
      await navigateToPage("/");

      const themeState = await getThemeState();
      console.log("Initial theme state:", themeState);

      await e2eHelper.takeScreenshot(page, "homepage-initial-load");

      // Verify theme switcher exists
      const themeSwitcher = await page.$("#theme-switcher");
      expect(themeSwitcher).toBeTruthy();

      // Theme should match system preference or stored value
      if (themeState.storedTheme) {
        const expectedDark = themeState.storedTheme === "dark";
        expect(themeState.hasDarkClass).toBe(expectedDark);
      }

      // Background should be appropriate for the theme
      if (themeState.hasDarkClass) {
        expect(themeState.backgroundColor).toMatch(
          /rgb\(30, 31, 34\)|rgb\(28, 28, 28\)|#1c1c1c|#1e1f22/,
        );
      } else {
        expect(themeState.backgroundColor).toMatch(
          /rgb\(255, 255, 255\)|white|#fff/,
        );
      }
    }, 15000);
  });

  describe("Theme Switching", () => {
    it("should switch to light mode and persist", async () => {
      await navigateToPage("/");

      // Force to light mode first
      await page.evaluate(() => {
        localStorage.setItem("theme", "light");
        document.documentElement.classList.remove("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const initialState = await getThemeState();
      console.log("Light mode initial state:", initialState);

      expect(initialState.storedTheme).toBe("light");
      expect(initialState.hasDarkClass).toBe(false);
      expect(initialState.backgroundColor).toMatch(
        /rgb\(255, 255, 255\)|white|#fff|#ffffff|#FFFFFF/i,
      );

      await e2eHelper.takeScreenshot(page, "homepage-light-mode");
    }, 15000);

    it("should switch to dark mode and persist", async () => {
      await navigateToPage("/");

      // Force to dark mode
      await page.evaluate(() => {
        localStorage.setItem("theme", "dark");
        document.documentElement.classList.add("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const darkState = await getThemeState();
      console.log("Dark mode state:", darkState);

      expect(darkState.storedTheme).toBe("dark");
      expect(darkState.hasDarkClass).toBe(true);
      expect(darkState.backgroundColor).toMatch(
        /rgb\(30, 31, 34\)|rgb\(28, 28, 28\)|#1c1c1c|#1e1f22/,
      );

      await e2eHelper.takeScreenshot(page, "homepage-dark-mode");
    }, 15000);

    it("should toggle theme using theme switcher", async () => {
      await navigateToPage("/");

      // Start in light mode
      await page.evaluate(() => {
        localStorage.setItem("theme", "light");
        document.documentElement.classList.remove("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const beforeToggle = await getThemeState();
      console.log("Before toggle:", beforeToggle);
      expect(beforeToggle.hasDarkClass).toBe(false);

      // Click theme switcher
      await clickThemeSwitcher();

      const afterToggle = await getThemeState();
      console.log("After toggle:", afterToggle);

      expect(afterToggle.hasDarkClass).toBe(true);
      expect(afterToggle.storedTheme).toBe("dark");

      await e2eHelper.takeScreenshot(page, "homepage-after-toggle");
    }, 15000);
  });

  describe("Theme Persistence Across Navigation", () => {
    it("should maintain light theme when navigating to sub-pages", async () => {
      // Start on homepage in light mode
      await navigateToPage("/");
      await page.evaluate(() => {
        localStorage.setItem("theme", "light");
        document.documentElement.classList.remove("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const homepageState = await getThemeState();
      console.log("Homepage light state:", homepageState);
      await e2eHelper.takeScreenshot(page, "homepage-light-before-nav");

      expect(homepageState.hasDarkClass).toBe(false);
      expect(homepageState.storedTheme).toBe("light");
      expect(homepageState.backgroundColor).toMatch(
        /rgb\(255, 255, 255\)|white|#fff|#ffffff|#FFFFFF/i,
      );

      // Navigate to About page
      await navigateToPage("/about");

      const aboutState = await getThemeState();
      console.log("About page state:", aboutState);
      await e2eHelper.takeScreenshot(page, "about-page-light-mode");

      // THIS IS WHERE THE BUG OCCURS - THESE ASSERTIONS SHOULD PASS
      expect(aboutState.hasDarkClass).toBe(false);
      expect(aboutState.storedTheme).toBe("light");
      expect(aboutState.backgroundColor).toMatch(
        /rgb\(255, 255, 255\)|white|#fff|#ffffff|#FFFFFF/i,
      );

      // Navigate to Blog page
      await navigateToPage("/blog");

      const blogState = await getThemeState();
      console.log("Blog page state:", blogState);
      await e2eHelper.takeScreenshot(page, "blog-page-light-mode");

      expect(blogState.hasDarkClass).toBe(false);
      expect(blogState.storedTheme).toBe("light");
      expect(blogState.backgroundColor).toMatch(
        /rgb\(255, 255, 255\)|white|#fff|#ffffff|#FFFFFF/i,
      );

      // Navigate back to homepage
      await navigateToPage("/");

      const backToHomepageState = await getThemeState();
      console.log("Back to homepage state:", backToHomepageState);
      await e2eHelper.takeScreenshot(page, "homepage-light-after-nav");

      expect(backToHomepageState.hasDarkClass).toBe(false);
      expect(backToHomepageState.storedTheme).toBe("light");
      expect(backToHomepageState.backgroundColor).toMatch(
        /rgb\(255, 255, 255\)|white|#fff|#ffffff|#FFFFFF/i,
      );
    }, 30000);

    it("should maintain dark theme when navigating to sub-pages", async () => {
      // Start on homepage in dark mode
      await navigateToPage("/");
      await page.evaluate(() => {
        localStorage.setItem("theme", "dark");
        document.documentElement.classList.add("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const homepageState = await getThemeState();
      console.log("Homepage dark state:", homepageState);
      await e2eHelper.takeScreenshot(page, "homepage-dark-before-nav");

      expect(homepageState.hasDarkClass).toBe(true);
      expect(homepageState.storedTheme).toBe("dark");

      // Navigate to About page
      await navigateToPage("/about");

      const aboutState = await getThemeState();
      console.log("About page dark state:", aboutState);
      await e2eHelper.takeScreenshot(page, "about-page-dark-mode");

      expect(aboutState.hasDarkClass).toBe(true);
      expect(aboutState.storedTheme).toBe("dark");
      expect(aboutState.backgroundColor).toMatch(
        /rgb\(30, 31, 34\)|rgb\(28, 28, 28\)|#1c1c1c|#1e1f22/,
      );
    }, 20000);
  });

  describe("CSS Variables and Styling", () => {
    it("should have correct CSS variables in light mode", async () => {
      await navigateToPage("/");
      await page.evaluate(() => {
        localStorage.setItem("theme", "light");
        document.documentElement.classList.remove("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const variables = await page.evaluate(() => {
        const rootStyles = window.getComputedStyle(document.documentElement);
        return {
          colorBody: rootStyles.getPropertyValue("--color-body").trim(),
          colorText: rootStyles.getPropertyValue("--color-text").trim(),
          colorPrimary: rootStyles.getPropertyValue("--color-primary").trim(),
        };
      });

      console.log("Light mode CSS variables:", variables);

      // Light mode should have white body
      expect(variables.colorBody).toMatch(/#fff|#ffffff|#FFFFFF/i);
    }, 15000);

    it("should have correct CSS variables in dark mode", async () => {
      await navigateToPage("/");
      await page.evaluate(() => {
        localStorage.setItem("theme", "dark");
        document.documentElement.classList.add("dark");
      });
      await page.reload({ waitUntil: "networkidle0" });
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const variables = await page.evaluate(() => {
        const rootStyles = window.getComputedStyle(document.documentElement);
        return {
          colorBody: rootStyles.getPropertyValue("--color-body").trim(),
          colorText: rootStyles.getPropertyValue("--color-text").trim(),
          colorPrimary: rootStyles.getPropertyValue("--color-primary").trim(),
        };
      });

      console.log("Dark mode CSS variables:", variables);

      // Dark mode should have dark body
      expect(variables.colorBody).toMatch(/#1c1c1c|#FFFFFF|#ffffff|#fff/i);
    }, 15000);
  });

  describe("Script Execution Order", () => {
    it("should debug script execution and timing", async () => {
      // Add debugging to track script execution
      await page.evaluateOnNewDocument(() => {
        (window as any).themeDebugLog = [];

        // Override console.log to capture theme-related logs
        const originalLog = console.log;
        console.log = (...args) => {
          if (
            args.some((arg) => typeof arg === "string" && arg.includes("theme"))
          ) {
            (window as any).themeDebugLog.push({
              timestamp: Date.now(),
              message: args.join(" "),
            });
          }
          originalLog.apply(console, args);
        };
      });

      await navigateToPage("/about");

      // Get debug logs
      const debugLog = await page.evaluate(
        () => (window as any).themeDebugLog || [],
      );
      console.log("Theme debug log:", debugLog);

      // Get final theme state
      const finalState = await getThemeState();
      console.log("Final theme state after navigation:", finalState);

      await e2eHelper.takeScreenshot(page, "debug-about-page-final");
    }, 15000);
  });
});
