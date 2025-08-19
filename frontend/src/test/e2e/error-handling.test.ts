import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  e2eHelper,
  setupE2ETest,
  cleanupE2ETest,
  type TestContext,
  E2ETestHelper,
} from "../e2e/setup";

describe("Error Handling and Edge Cases E2E Tests", () => {
  let context: TestContext;

  beforeEach(async () => {
    context = await setupE2ETest();
  });

  afterEach(async () => {
    await cleanupE2ETest();
  });

  describe("Network Error Scenarios", () => {
    it("handles dashboard API failure gracefully", async () => {
      const { page, baseURL } = context;

      // Mock API failure using Puppeteer request interception
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/dashboards.json")) {
          request.respond({
            status: 500,
            contentType: "application/json",
            body: JSON.stringify({
              success: false,
              error: "Internal server error",
              message: "Database connection failed",
            }),
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

      // Should show specific error message
      await page.waitForSelector(
        "text=Could not load dashboard configurations",
        { timeout: 5000 },
      );

      // Should show retry button
      const retryButton = await page.waitForSelector(
        'button:has-text("Retry")',
        { timeout: 5000 },
      );
      expect(retryButton).toBeTruthy();

      await e2eHelper.takeScreenshot(page, "api-failure-error-state");

      // Verify no photo booth controls are visible during error
      const controls = await page.$(".photo-booth-controls");
      expect(controls).toBeFalsy();
    });

    it("handles network timeout during dashboard loading", async () => {
      const { page, baseURL } = context;

      // Mock slow/hanging API using Puppeteer request interception
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/dashboards.json")) {
          // Never respond to simulate timeout
          // Don't call request.respond() or request.continue()
        } else {
          request.continue();
        }
      });

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      // Should show loading state indefinitely
      await page.waitForSelector("text=Loading dashboards...", {
        timeout: 5000,
      });

      // Wait longer to ensure it stays in loading state
      await E2ETestHelper.sleep(10000);

      const loadingText = await page.$("text=Loading dashboards...");
      expect(loadingText).toBeTruthy();

      await e2eHelper.takeScreenshot(page, "network-timeout-loading-state");
    });

    it("recovers from transient network errors", async () => {
      const { page, baseURL } = context;

      let requestCount = 0;

      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/dashboards.json")) {
          requestCount++;
          if (requestCount <= 2) {
            // Fail first two requests
            request.respond({
              status: 503,
              contentType: "application/json",
              body: JSON.stringify({
                success: false,
                error: "Service unavailable",
              }),
            });
          } else {
            // Succeed on third request
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

      // Should show error initially
      await page.waitForSelector('button:has-text("Retry")', {
        timeout: 10000,
      });

      // First retry - should fail again
      await page.click('button:has-text("Retry")');
      await page.waitForSelector('button:has-text("Retry")', {
        timeout: 10000,
      });

      // Second retry - should succeed
      await page.click('button:has-text("Retry")');

      // Should eventually load successfully
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      await e2eHelper.takeScreenshot(page, "transient-error-recovery-success");

      // Verify dashboard loaded properly
      const dashboardTitle = await page.$eval("h3", (el) => el.textContent);
      expect(dashboardTitle).toBe("Portfolio History Portrait");
    });
  });

  describe("Export Error Scenarios", () => {
    beforeEach(async () => {
      const { page, baseURL } = context;
      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
    });

    it("handles export API failure gracefully", async () => {
      const { page } = context;

      // Mock export API failure using Puppeteer request interception
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/export-dashboard")) {
          request.respond({
            status: 500,
            contentType: "application/json",
            body: JSON.stringify({
              success: false,
              message: "Export generation failed",
              error: "Python script execution failed: Module not found",
            }),
          });
        } else {
          request.continue();
        }
      });

      const exportButton = await page.waitForSelector(
        'button:has-text("Export Dashboard")',
        { timeout: 5000 },
      );
      await exportButton.click();

      // Should show exporting state briefly
      await page.waitForSelector("text=Exporting...", { timeout: 5000 });

      // Should then show error message
      await page.waitForSelector("text=Export generation failed", {
        timeout: 10000,
      });

      await e2eHelper.takeScreenshot(page, "export-api-failure-error");

      // Export button should be enabled again
      const exportButtonAfterError = await page.$(
        'button:has-text("Export Dashboard")',
      );
      const isDisabled = await exportButtonAfterError?.evaluate(
        (el) => (el as HTMLButtonElement).disabled,
      );
      expect(isDisabled).toBe(false);

      // Error should be dismissible
      const dismissButton = await page.$('button:has-text("×")');
      expect(dismissButton).toBeTruthy();
    });

    it("handles export timeout gracefully", async () => {
      const { page } = context;

      // Mock hanging export API using Puppeteer request interception
      await page.setRequestInterception(true);
      page.on("request", (request) => {
        if (request.url().includes("/api/export-dashboard")) {
          // Never respond to simulate timeout
          // Don't call request.respond() or request.continue()
        } else {
          request.continue();
        }
      });

      const exportButton = await page.waitForSelector(
        'button:has-text("Export Dashboard")',
        { timeout: 5000 },
      );
      await exportButton.click();

      // Should show exporting state
      await page.waitForSelector("text=Exporting...", { timeout: 5000 });

      // Button should be disabled during export
      const isDisabled = await exportButton.evaluate(
        (el) => (el as HTMLButtonElement).disabled,
      );
      expect(isDisabled).toBe(true);

      await e2eHelper.takeScreenshot(page, "export-timeout-hanging-state");

      // Should remain in exporting state for extended time
      await E2ETestHelper.sleep(10000);
      const stillExporting = await page.$("text=Exporting...");
      expect(stillExporting).toBeTruthy();
    });

    it("prevents multiple simultaneous exports", async () => {
      const { page } = context;

      let requestCount = 0;

      // Mock slow export API using Puppeteer request interception
      await page.setRequestInterception(true);
      page.on("request", async (request) => {
        if (request.url().includes("/api/export-dashboard")) {
          requestCount++;
          // Delay response to simulate slow export
          await new Promise((resolve) => setTimeout(resolve, 5000));
          request.respond({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify({
              success: true,
              message: "Export completed successfully",
              files: ["test-file.png"],
            }),
          });
        } else {
          request.continue();
        }
      });

      const exportButton = await page.waitForSelector(
        'button:has-text("Export Dashboard")',
        { timeout: 5000 },
      );

      // Start first export
      await exportButton.click();
      await page.waitForSelector("text=Exporting...", { timeout: 5000 });

      // Try to start second export - button should be disabled
      const isDisabledDuringExport = await exportButton.evaluate(
        (el) => (el as HTMLButtonElement).disabled,
      );
      expect(isDisabledDuringExport).toBe(true);

      // Click should have no effect
      await exportButton.click();

      // Should still only have one request
      expect(requestCount).toBe(1);

      await e2eHelper.takeScreenshot(page, "multiple-export-prevention");

      // Wait for export to complete
      await page.waitForSelector("text=Export completed successfully", {
        timeout: 10000,
      });

      // Button should be enabled again
      const isEnabledAfterExport = await exportButton.evaluate(
        (el) => (el as HTMLButtonElement).disabled,
      );
      expect(isEnabledAfterExport).toBe(false);
    });
  });

  describe("Invalid Parameter Handling", () => {
    it("handles malformed URL parameters gracefully", async () => {
      const { page, baseURL } = context;

      const malformedParams = [
        "?dashboard=",
        "?mode=invalid",
        "?aspect_ratio=abc:def",
        "?format=invalid",
        "?dpi=abc",
        "?scale=xyz",
        '?dashboard=<script>alert("xss")</script>',
        "?mode=" + "x".repeat(1000), // Very long parameter
        "?aspect_ratio=null",
        "?format=undefined",
      ];

      for (const params of malformedParams) {
        await page.goto(`${baseURL}/photo-booth${params}`, {
          waitUntil: "networkidle0",
          timeout: 15000,
        });

        // Should not crash and should load with default values
        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Should fall back to safe defaults
        const selectedRatio = await page.$eval(
          "#aspect-ratio-select",
          (el) => (el as HTMLSelectElement).value,
        );
        expect(["16:9", "4:3", "3:4"]).toContain(selectedRatio);

        const formatValue = await page.$eval(
          "#format-select",
          (el) => (el as HTMLSelectElement).value,
        );
        expect(["png", "svg", "both"]).toContain(formatValue);

        await e2eHelper.takeScreenshot(
          page,
          `malformed-params-${btoa(params).substring(0, 10)}`,
        );
      }
    });

    it("handles missing dashboard gracefully", async () => {
      const { page, baseURL } = context;

      await page.goto(
        `${baseURL}/photo-booth?dashboard=nonexistent_dashboard`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      // Should show dashboard not found error
      await page.waitForSelector("text=Dashboard Not Found", {
        timeout: 10000,
      });

      // Should show helpful message
      await page.waitForSelector(
        'text=The requested dashboard "nonexistent_dashboard" is not available',
        { timeout: 5000 },
      );

      // Should show available dashboards
      await page.waitForSelector("text=Available dashboards:", {
        timeout: 5000,
      });

      await e2eHelper.takeScreenshot(page, "missing-dashboard-error");
    });

    it("handles extremely large viewport dimensions", async () => {
      const { page, baseURL } = context;

      // Set extremely large viewport
      await page.setViewport({ width: 7680, height: 4320 }); // 8K resolution

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=16:9`,
        {
          waitUntil: "networkidle0",
          timeout: 20000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 25000 });

      // Should handle large viewport without breaking
      const dashboard = await page.$(".photo-booth-dashboard");
      const dashboardBox = await dashboard?.boundingBox();

      expect(dashboardBox).toBeTruthy();
      expect(dashboardBox!.width).toBeGreaterThan(1000);
      expect(dashboardBox!.height).toBeGreaterThan(500);

      await e2eHelper.takeScreenshot(page, "extreme-large-viewport");
    });

    it("handles extremely small viewport dimensions", async () => {
      const { page, baseURL } = context;

      // Set very small viewport
      await page.setViewport({ width: 320, height: 240 });

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Should handle small viewport gracefully
      const dashboard = await page.$(".photo-booth-dashboard");
      expect(dashboard).toBeTruthy();

      // Controls might be hidden or adapted for small screen
      await e2eHelper.takeScreenshot(page, "extreme-small-viewport");

      // Content should still be accessible
      const header = await page.$(".dashboard-header h1");
      expect(header).toBeTruthy();
    });
  });

  describe("Browser Compatibility Edge Cases", () => {
    it("handles JavaScript disabled scenario", async () => {
      const { page, baseURL } = context;

      // Disable JavaScript
      await page.setJavaScriptEnabled(false);

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "load",
        timeout: 15000,
      });

      // Should show basic HTML content without interactive features
      const pageContent = await page.content();
      expect(pageContent.length).toBeGreaterThan(100);

      await e2eHelper.takeScreenshot(page, "javascript-disabled");

      // Re-enable JavaScript for cleanup
      await page.setJavaScriptEnabled(true);
    });

    it("handles slow CPU performance", async () => {
      const { page, baseURL } = context;

      // Simulate slow CPU
      const client = await page.target().createCDPSession();
      await client.send("Emulation.setCPUThrottlingRate", { rate: 6 }); // 6x slower

      const startTime = Date.now();

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait`,
        {
          waitUntil: "networkidle0",
          timeout: 30000, // Increased timeout
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 40000 });

      const loadTime = Date.now() - startTime;

      // Should still load within reasonable time even with CPU throttling
      expect(loadTime).toBeLessThan(40000);

      await e2eHelper.takeScreenshot(page, "slow-cpu-performance");

      // Disable CPU throttling
      await client.send("Emulation.setCPUThrottlingRate", { rate: 1 });
    });

    it("handles memory pressure scenarios", async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Simulate memory pressure by creating many objects
      await page.evaluate(() => {
        (window as any).memoryPressureTest = [];
        for (let i = 0; i < 10000; i++) {
          (window as any).memoryPressureTest.push(
            new Array(1000).fill(Math.random()),
          );
        }
      });

      // Should still function under memory pressure
      const aspectSelect = await page.$("#aspect-ratio-select");
      expect(aspectSelect).toBeTruthy();

      await page.selectOption("#aspect-ratio-select", "3:4");
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      await e2eHelper.takeScreenshot(page, "memory-pressure-scenario");

      // Cleanup
      await page.evaluate(() => {
        delete (window as any).memoryPressureTest;
      });
    });
  });

  describe("Content Security and XSS Prevention", () => {
    it("prevents XSS through URL parameters", async () => {
      const { page, baseURL } = context;

      const xssPayloads = [
        '<script>alert("xss")</script>',
        'javascript:alert("xss")',
        'data:text/html,<script>alert("xss")</script>',
        '"><script>alert("xss")</script>',
        "onload=\"alert('xss')\"",
      ];

      for (const payload of xssPayloads) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=${encodeURIComponent(payload)}`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        // Should not execute malicious scripts
        // XSS would typically show in browser console or trigger alerts
        const alerts: string[] = [];
        page.on("dialog", (dialog) => {
          alerts.push(dialog.message());
          dialog.dismiss();
        });

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Should not have triggered any alerts
        expect(alerts).toHaveLength(0);

        // Content should be safely escaped
        const pageContent = await page.content();
        expect(pageContent).not.toContain("<script>alert");

        await e2eHelper.takeScreenshot(
          page,
          `xss-prevention-${btoa(payload.substring(0, 10))}`,
        );
      }
    });

    it("validates secure content handling", async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Check for security headers or CSP violations
      const securityErrors: string[] = [];
      page.on("pageerror", (error) => {
        if (
          error.message.includes("Content Security Policy") ||
          error.message.includes("blocked")
        ) {
          securityErrors.push(error.message);
        }
      });

      // Interact with various UI elements
      await page.selectOption("#aspect-ratio-select", "3:4");
      await page.click('button:has-text("Dark")');
      await page.selectOption("#format-select", "svg");

      await E2ETestHelper.sleep(5000);

      // Should not have security violations during normal operation
      expect(securityErrors).toHaveLength(0);

      await e2eHelper.takeScreenshot(page, "security-validation-passed");
    });
  });

  describe("Race Condition Prevention", () => {
    it("handles rapid parameter changes without race conditions", async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth`, {
        waitUntil: "networkidle0",
        timeout: 15000,
      });

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Rapidly change parameters
      const changes = [
        () => page.selectOption("#aspect-ratio-select", "3:4"),
        () => page.click('button:has-text("Dark")'),
        () => page.selectOption("#format-select", "svg"),
        () => page.selectOption("#dpi-select", "600"),
        () => page.selectOption("#scale-select", "4"),
        () => page.selectOption("#aspect-ratio-select", "16:9"),
        () => page.click('button:has-text("Light")'),
      ];

      // Execute all changes rapidly
      await Promise.all(changes.map((change) => change()));

      // Should eventually stabilize
      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Final state should be consistent
      const finalRatio = await page.$eval(
        "#aspect-ratio-select",
        (el) => (el as HTMLSelectElement).value,
      );
      const finalFormat = await page.$eval(
        "#format-select",
        (el) => (el as HTMLSelectElement).value,
      );

      expect(["16:9", "4:3", "3:4"]).toContain(finalRatio);
      expect(["png", "svg", "both"]).toContain(finalFormat);

      await e2eHelper.takeScreenshot(page, "race-condition-prevention-final");
    });
  });
});
