import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  e2eHelper,
  setupE2ETest,
  cleanupE2ETest,
  type TestContext,
  E2ETestHelper,
} from "../e2e/setup";

describe("Photo Booth E2E Tests", () => {
  let context: TestContext;

  beforeEach(async () => {
    context = await setupE2ETest();
  });

  afterEach(async () => {
    await cleanupE2ETest();
  });

  describe("Page Loading and Navigation", () => {
    it("loads photo booth page successfully", async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      // Wait for photo booth to be ready
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Take screenshot for visual verification
      await e2eHelper.takeScreenshot(page, "photo-booth-initial-load");

      // Verify core elements are present
      const title = await page.$eval("h1", (el) => el.textContent);
      expect(title).toContain("Twitter Live Signals");

      const footer = await page.$eval(
        ".dashboard-footer h1",
        (el) => el.textContent,
      );
      expect(footer).toContain("colemorton.com");
    });

    it("loads specific dashboard via URL parameters", async () => {
      const { page, baseURL } = context;

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&mode=light&aspect_ratio=3:4`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Verify dashboard selection
      const selectedDashboard = await page.$eval(
        "#dashboard-select",
        (el) => (el as HTMLSelectElement).value,
      );
      expect(selectedDashboard).toBe("portfolio_history_portrait");

      // Verify mode selection
      const lightButton = await page.$(".bg-blue-500");
      const buttonText = await lightButton?.evaluate((el) => el.textContent);
      expect(buttonText?.trim()).toBe("Light");

      // Verify aspect ratio selection
      const selectedRatio = await page.$eval(
        "#aspect-ratio-select",
        (el) => (el as HTMLSelectElement).value,
      );
      expect(selectedRatio).toBe("3:4");
    });

    it("handles malformed URL parameters gracefully", async () => {
      const { page, baseURL } = context;

      await page.goto(
        `${baseURL}/photo-booth?dashboard=invalid&mode=invalid&aspect_ratio=invalid`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Should fall back to defaults
      const selectedRatio = await page.$eval(
        "#aspect-ratio-select",
        (el) => (el as HTMLSelectElement).value,
      );
      expect(selectedRatio).toBe("16:9");

      const lightButton = await page.$(".bg-blue-500");
      const buttonText = await lightButton?.evaluate((el) => el.textContent);
      expect(buttonText?.trim()).toBe("Light");
    });
  });

  describe("Dashboard Interaction", () => {
    beforeEach(async () => {
      const { page, baseURL } = context;
      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
    });

    it("switches between light and dark modes", async () => {
      const { page } = context;

      // Initially light mode
      await e2eHelper.takeScreenshot(page, "dashboard-light-mode");

      // Switch to dark mode
      await page.click('button:has-text("Dark")');

      // Wait for theme change
      await page.waitForSelector(".photo-booth-dashboard.dark", {
        timeout: 5000,
      });

      await e2eHelper.takeScreenshot(page, "dashboard-dark-mode");

      // Verify dark mode is applied
      const isDark = await page.$eval(".photo-booth-dashboard", (el) =>
        el.classList.contains("dark"),
      );
      expect(isDark).toBe(true);

      // Switch back to light mode
      await page.click('button:has-text("Light")');

      // Wait for theme change
      await page.waitForSelector(".photo-booth-dashboard:not(.dark)", {
        timeout: 5000,
      });

      // Verify light mode is applied
      const isLight = await page.$eval(
        ".photo-booth-dashboard",
        (el) => !el.classList.contains("dark"),
      );
      expect(isLight).toBe(true);
    });

    it("changes aspect ratios and updates display", async () => {
      const { page } = context;

      const aspectRatios = ["16:9", "4:3", "3:4"];

      for (const ratio of aspectRatios) {
        await page.selectOption("#aspect-ratio-select", ratio);

        // Wait for ready state after ratio change
        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Take screenshot for each aspect ratio
        await e2eHelper.takeScreenshot(
          page,
          `dashboard-${ratio.replace(":", "x")}-aspect-ratio`,
        );

        // Verify the selection is reflected in UI
        const selectedRatio = await page.$eval(
          "#aspect-ratio-select",
          (el) => (el as HTMLSelectElement).value,
        );
        expect(selectedRatio).toBe(ratio);
      }
    });

    it("updates export parameters dynamically", async () => {
      const { page } = context;

      // Change format
      await page.selectOption("#format-select", "svg");

      // Change DPI
      await page.selectOption("#dpi-select", "600");

      // Change scale factor
      await page.selectOption("#scale-select", "4");

      // Wait for ready state
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Verify output info is updated
      const outputInfo = await page.$eval(
        ".ml-auto.text-xs",
        (el) => el.textContent,
      );
      expect(outputInfo).toContain("600 DPI");
      expect(outputInfo).toContain("4× scale");
    });
  });

  describe("Dashboard Content Verification", () => {
    beforeEach(async () => {
      const { page, baseURL } = context;
      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
    });

    it("renders portfolio history portrait with correct structure", async () => {
      const { page } = context;

      // Verify header is present
      const header = await page.$(".dashboard-header h1");
      expect(header).toBeTruthy();
      const headerText = await header?.evaluate((el) => el.textContent);
      expect(headerText).toBe("Twitter Live Signals");

      // Verify footer is present
      const footer = await page.$(".dashboard-footer h1");
      expect(footer).toBeTruthy();
      const footerText = await footer?.evaluate((el) => el.textContent);
      expect(footerText).toBe("colemorton.com");

      // Verify charts are present
      const charts = await page.$$(".photo-booth-chart");
      expect(charts.length).toBeGreaterThan(0);

      await e2eHelper.takeScreenshot(
        page,
        "portfolio-history-portrait-structure",
      );
    });

    it("applies correct layout classes", async () => {
      const { page } = context;

      // Verify layout classes are applied
      const layoutContainer = await page.$(".flex.flex-col.h-full");
      expect(layoutContainer).toBeTruthy();

      // Verify dashboard content structure
      const dashboardContent = await page.$(".dashboard-content.2x1_stack");
      expect(dashboardContent).toBeTruthy();
    });

    it("renders charts with proper dimensions", async () => {
      const { page } = context;

      // Wait for charts to fully load
      await E2ETestHelper.sleep(5000);

      // Get chart container dimensions
      const chartContainers = await page.$$(".photo-booth-chart");

      for (const chart of chartContainers) {
        const box = await chart.boundingBox();
        expect(box).toBeTruthy();
        expect(box!.width).toBeGreaterThan(0);
        expect(box!.height).toBeGreaterThan(0);
      }

      await e2eHelper.takeScreenshot(page, "charts-rendered-with-dimensions");
    });
  });

  describe("Responsive Behavior", () => {
    it("adapts to different viewport sizes", async () => {
      const { page } = context;

      const viewports = [
        { width: 1920, height: 1080, name: "desktop" },
        { width: 1440, height: 900, name: "laptop" },
        { width: 768, height: 1024, name: "tablet" },
      ];

      for (const viewport of viewports) {
        await page.setViewport(viewport);

        await page.goto(
          `${context.baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
        await e2eHelper.takeScreenshot(
          page,
          `responsive-${viewport.name}-${viewport.width}x${viewport.height}`,
        );

        // Verify dashboard is visible and not cut off
        const dashboard = await page.$(".photo-booth-dashboard");
        const box = await dashboard?.boundingBox();
        expect(box).toBeTruthy();
        expect(box!.width).toBeGreaterThan(0);
        expect(box!.height).toBeGreaterThan(0);
      }
    });

    it("handles mobile viewport gracefully", async () => {
      const { page } = context;

      await page.setViewport({ width: 375, height: 667 }); // iPhone SE size

      await page.goto(
        `${context.baseURL}/photo-booth?dashboard=portfolio_history_portrait`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Controls might be hidden or collapsed on mobile
      const controls = await page.$(".photo-booth-controls");
      expect(controls).toBeTruthy();

      await e2eHelper.takeScreenshot(page, "mobile-viewport-375x667");
    });
  });

  describe("Performance and Loading", () => {
    it("loads dashboard within acceptable time limits", async () => {
      const { page, baseURL } = context;

      const startTime = Date.now();

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      const loadTime = Date.now() - startTime;

      // Should load within 20 seconds (generous for E2E)
      expect(loadTime).toBeLessThan(20000);
    });

    it("handles slow network conditions", async () => {
      const { page, baseURL } = context;

      // Simulate slow 3G
      const client = await page.target().createCDPSession();
      await client.send("Network.enable");
      await client.send("Network.emulateNetworkConditions", {
        offline: false,
        downloadThroughput: (1.5 * 1024 * 1024) / 8, // 1.5 Mbps
        uploadThroughput: (750 * 1024) / 8, // 750 Kbps
        latency: 40,
      });

      const startTime = Date.now();

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 30000, // Longer timeout for slow network
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 30000 });

      const loadTime = Date.now() - startTime;

      // Should still load within 30 seconds even on slow network
      expect(loadTime).toBeLessThan(30000);

      await e2eHelper.takeScreenshot(page, "slow-network-loading-complete");
    });
  });

  describe("Error Handling", () => {
    it("handles dashboard loading errors gracefully", async () => {
      const { page, baseURL } = context;

      // Mock API failure by intercepting requests using Puppeteer
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/dashboards.json")) {
          request.respond({
            status: 500,
            contentType: "application/json",
            body: JSON.stringify({ success: false, error: "Server error" }),
          });
        } else {
          request.continue();
        }
      });

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      // Should show error state
      await page.waitForSelector("text=Failed to Load Dashboards", {
        timeout: 10000,
      });

      // Should show retry button
      await page.waitForSelector('button:has-text("Retry")', { timeout: 5000 });

      await e2eHelper.takeScreenshot(page, "dashboard-loading-error-state");
    });

    it("recovers from network errors on retry", async () => {
      const { page, baseURL } = context;

      let requestCount = 0;
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/dashboards.json")) {
          requestCount++;
          if (requestCount === 1) {
            // Fail first request
            request.respond({
              status: 500,
              contentType: "application/json",
              body: JSON.stringify({ success: false, error: "Network error" }),
            });
          } else {
            // Succeed on retry
            request.continue();
          }
        } else {
          request.continue();
        }
      });

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      // Wait for error state
      await page.waitForSelector('button:has-text("Retry")', {
        timeout: 10000,
      });

      // Click retry
      await page.click('button:has-text("Retry")');

      // Should successfully load after retry
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      await e2eHelper.takeScreenshot(page, "successful-retry-after-error");
    });

    it("handles JavaScript errors without crashing", async () => {
      const { page, baseURL } = context;

      // Listen for console errors
      const errors: string[] = [];
      page.on("pageerror", (error) => {
        errors.push(error.message);
      });

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Should not have any critical JavaScript errors
      const criticalErrors = errors.filter(
        (error) =>
          error.includes("TypeError") ||
          error.includes("ReferenceError") ||
          error.includes("Cannot read property"),
      );

      expect(criticalErrors).toHaveLength(0);
    });
  });
});
