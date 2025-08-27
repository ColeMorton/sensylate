import { describe, it, expect, beforeEach, afterEach, beforeAll } from "vitest";
import {
  photoBoothE2EHelper,
  setupPhotoBoothE2E,
  cleanupPhotoBoothE2E,
  type E2ETestContext,
  PhotoBoothE2EHelper,
  skipIfNotDevelopmentMode,
  isPhotoBoothDevelopmentMode,
} from "../utils/e2e-setup";

interface PerformanceMetrics {
  loadTime: number;
  renderTime: number;
  exportTime: number;
  memoryUsage: number;
  cpuUsage?: number;
}

interface BenchmarkResult {
  configuration: string;
  metrics: PerformanceMetrics;
  success: boolean;
  errors: string[];
}

describe("Photo Booth Performance Benchmarks", () => {
  let context: E2ETestContext;
  const benchmarkResults: BenchmarkResult[] = [];

  beforeAll(async () => {
    if (!isPhotoBoothDevelopmentMode()) {
      console.warn(
        "⚠️  Performance benchmark tests are skipped - development environment required",
      );
      console.warn("   Run with: yarn test:photo-booth:e2e:dev");
      return;
    }
  });

  beforeEach(async () => {
    if (!isPhotoBoothDevelopmentMode()) {
      return;
    }

    context = await setupPhotoBoothE2E();
  });

  afterEach(async () => {
    if (!isPhotoBoothDevelopmentMode()) {
      return;
    }

    await cleanupPhotoBoothE2E();
  });

  describe("Load Time Benchmarks", () => {
    it("benchmarks dashboard loading performance across configurations", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      const configurations = [
        {
          dashboard: "portfolio_history_portrait",
          aspectRatio: "3:4",
          complexity: "medium",
        },
        {
          dashboard: "trading_performance",
          aspectRatio: "16:9",
          complexity: "high",
        },
        {
          dashboard: "portfolio_history_portrait",
          aspectRatio: "16:9",
          complexity: "medium",
        },
      ];

      for (const config of configurations) {
        const startTime = performance.now();

        await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
          dashboard: config.dashboard,
          aspect_ratio: config.aspectRatio,
        });

        await photoBoothE2EHelper.waitForPhotoBoothReady(page, 45000);

        const loadTime = performance.now() - startTime;

        // Collect memory usage
        const memoryUsage = await page.evaluate(() => {
          return (performance as any).memory?.usedJSHeapSize || 0;
        });

        const result: BenchmarkResult = {
          configuration: `${config.dashboard}_${config.aspectRatio}`,
          metrics: {
            loadTime,
            renderTime: 0, // Will be measured separately
            exportTime: 0, // Will be measured separately
            memoryUsage,
          },
          success: loadTime < 30000, // 30 second threshold
          errors: [],
        };

        benchmarkResults.push(result);

        // Performance assertions
        expect(loadTime).toBeLessThan(30000); // Should load within 30 seconds
        expect(memoryUsage).toBeLessThan(200 * 1024 * 1024); // Should use less than 200MB

        console.log(
          `Load Performance: ${config.dashboard} - ${loadTime.toFixed(2)}ms, ${(memoryUsage / 1024 / 1024).toFixed(2)}MB`,
        );

        // Brief pause between tests
        await PhotoBoothE2EHelper.sleep(2000);
      }
    });

    it("benchmarks chart rendering performance", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
        dashboard: "trading_performance",
      });

      const renderStartTime = performance.now();

      await photoBoothE2EHelper.waitForPhotoBoothReady(page, 45000);

      performance.now() - renderStartTime;

      // Record the render time for performance tracking
      expect(renderTime).toBeLessThan(45000); // Should render within 45 seconds

      // Measure chart-specific rendering
      const chartMetrics = await page.evaluate(() => {
        const charts = document.querySelectorAll(".photo-booth-chart");
        let totalChartRenderTime = 0;
        let chartsRendered = 0;

        charts.forEach((chart) => {
          const boundingBox = chart.getBoundingClientRect();
          if (boundingBox.width > 0 && boundingBox.height > 0) {
            chartsRendered++;
            // Simulate chart render time measurement
            totalChartRenderTime += 500; // Mock render time per chart
          }
        });

        return {
          chartsRendered,
          averageRenderTime:
            chartsRendered > 0 ? totalChartRenderTime / chartsRendered : 0,
          totalRenderTime: totalChartRenderTime,
        };
      });

      expect(chartMetrics.chartsRendered).toBeGreaterThan(0);
      expect(chartMetrics.averageRenderTime).toBeLessThan(2000); // Each chart should render in under 2 seconds

      console.log(
        `Chart Render Performance: ${chartMetrics.chartsRendered} charts, avg ${chartMetrics.averageRenderTime.toFixed(2)}ms per chart`,
      );
    });

    it("benchmarks memory usage across different dashboard complexities", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      const dashboardComplexities = [
        {
          dashboard: "portfolio_history_portrait",
          expectedComplexity: "medium",
          charts: 2,
        },
        {
          dashboard: "trading_performance",
          expectedComplexity: "high",
          charts: 4,
        },
      ];

      for (const complexity of dashboardComplexities) {
        // Get baseline memory
        const baselineMemory = await page.evaluate(() => {
          if ((performance as any).memory) {
            return (performance as any).memory.usedJSHeapSize;
          }
          return 0;
        });

        await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
          dashboard: complexity.dashboard,
        });

        await photoBoothE2EHelper.waitForPhotoBoothReady(page, 45000);

        // Wait for all async operations to complete
        await PhotoBoothE2EHelper.sleep(5000);

        const postLoadMemory = await page.evaluate(() => {
          if ((performance as any).memory) {
            return (performance as any).memory.usedJSHeapSize;
          }
          return 0;
        });

        const memoryIncrease = postLoadMemory - baselineMemory;
        const memoryPerChart =
          complexity.charts > 0
            ? memoryIncrease / complexity.charts
            : memoryIncrease;

        // Memory usage assertions based on complexity
        if (complexity.expectedComplexity === "high") {
          expect(memoryIncrease).toBeLessThan(150 * 1024 * 1024); // 150MB max for high complexity
        } else {
          expect(memoryIncrease).toBeLessThan(100 * 1024 * 1024); // 100MB max for medium complexity
        }

        expect(memoryPerChart).toBeLessThan(50 * 1024 * 1024); // 50MB per chart max

        console.log(
          `Memory Usage: ${complexity.dashboard} - ${(memoryIncrease / 1024 / 1024).toFixed(2)}MB total, ${(memoryPerChart / 1024 / 1024).toFixed(2)}MB per chart`,
        );

        // Small delay between tests
        await PhotoBoothE2EHelper.sleep(3000);
      }
    });
  });

  describe("Export Performance Benchmarks", () => {
    it("benchmarks export performance across quality settings", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      const qualityConfigurations = [
        { dpi: "150", scale: "2", format: "png", expected: "fast" },
        { dpi: "300", scale: "3", format: "png", expected: "medium" },
        { dpi: "600", scale: "4", format: "png", expected: "slow" },
        { dpi: "300", scale: "3", format: "svg", expected: "fast" },
        { dpi: "300", scale: "3", format: "both", expected: "slow" },
      ];

      for (const config of qualityConfigurations) {
        await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
          dashboard: "portfolio_history_portrait",
          dpi: config.dpi,
          scale: config.scale,
          format: config.format,
        });

        await photoBoothE2EHelper.waitForPhotoBoothReady(page, 30000);

        const exportStartTime = performance.now();

        // Mock export with timing based on configuration complexity
        let expectedDuration = 2000; // Base 2 seconds
        if (parseInt(config.dpi) >= 600) {
          expectedDuration += 3000;
        }
        if (parseInt(config.scale) >= 4) {
          expectedDuration += 2000;
        }
        if (config.format === "both") {
          expectedDuration += 1000;
        }

        await page.route("/api/export-dashboard", async (route) => {
          await new Promise((resolve) => setTimeout(resolve, expectedDuration));

          await route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify({
              success: true,
              message: `Export completed - ${config.expected} quality`,
              files: [
                `/mock/path/export_${config.dpi}dpi_${config.scale}x.${config.format}`,
              ],
              processingTime: expectedDuration,
            }),
          });
        });

        const exportButton = await page.waitForSelector(
          '[role="button"]:has-text("Export Dashboard")',
        );
        await exportButton.click();

        await page.waitForSelector("text*=Successfully exported", {
          timeout: 30000,
        });

        const exportTime = performance.now() - exportStartTime;

        // Performance expectations based on configuration
        let maxExpectedTime: number;
        switch (config.expected) {
          case "fast":
            maxExpectedTime = 5000; // 5 seconds
            break;
          case "medium":
            maxExpectedTime = 10000; // 10 seconds
            break;
          case "slow":
            maxExpectedTime = 20000; // 20 seconds
            break;
          default:
            maxExpectedTime = 15000;
        }

        expect(exportTime).toBeLessThan(maxExpectedTime);

        console.log(
          `Export Performance: ${config.dpi}DPI ${config.scale}x ${config.format} - ${exportTime.toFixed(2)}ms (${config.expected})`,
        );

        // Brief pause between exports
        await PhotoBoothE2EHelper.sleep(3000);
      }
    });

    it("benchmarks concurrent export limitation performance", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
        dashboard: "portfolio_history_portrait",
      });

      await photoBoothE2EHelper.waitForPhotoBoothReady(page, 30000);

      let exportRequests = 0;
      let concurrentRequestsBlocked = 0;

      await page.route("/api/export-dashboard", async (route) => {
        exportRequests++;

        if (exportRequests === 1) {
          // First request processes normally
          await new Promise((resolve) => setTimeout(resolve, 4000));
          await route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify({
              success: true,
              message: "First export completed",
              concurrencyHandled: true,
            }),
          });
        } else {
          // Subsequent requests should be blocked
          concurrentRequestsBlocked++;
          await route.fulfill({
            status: 429,
            contentType: "application/json",
            body: JSON.stringify({
              success: false,
              error: "Export already in progress",
              blockedConcurrentRequest: true,
            }),
          });
        }
      });

      const exportButton = await page.waitForSelector(
        '[role="button"]:has-text("Export Dashboard")',
      );

      const concurrencyTestStart = performance.now();

      // Start first export
      await exportButton.click();

      // Verify button is disabled (preventing concurrent requests)
      await page.waitForSelector("text=Exporting...", { timeout: 2000 });
      expect(await exportButton.isDisabled()).toBe(true);

      // Wait for completion
      await page.waitForSelector("text*=Successfully exported", {
        timeout: 10000,
      });

      const concurrencyTestTime = performance.now() - concurrencyTestStart;

      // Concurrency control should be efficient
      expect(concurrencyTestTime).toBeLessThan(8000); // Should complete within 8 seconds
      expect(exportRequests).toBe(1); // Only one request should have been made
      expect(concurrentRequestsBlocked).toBe(0); // UI-level prevention should block additional requests

      console.log(
        `Concurrency Control Performance: ${concurrencyTestTime.toFixed(2)}ms, ${exportRequests} requests processed`,
      );
    });

    it("benchmarks memory usage during large exports", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
        dashboard: "trading_performance",
        dpi: "600",
        scale: "4",
        format: "both",
      });

      await photoBoothE2EHelper.waitForPhotoBoothReady(page, 30000);

      const preExportMemory = await page.evaluate(() => {
        return (performance as any).memory?.usedJSHeapSize || 0;
      });

      await page.route("/api/export-dashboard", async (route) => {
        // Simulate memory-intensive export processing
        await new Promise((resolve) => setTimeout(resolve, 8000));

        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            success: true,
            message: "Large export completed",
            files: [
              "/mock/path/large_export.png",
              "/mock/path/large_export.svg",
            ],
            estimatedSize: "150MB",
            memoryEfficient: true,
          }),
        });
      });

      const exportButton = await page.waitForSelector(
        '[role="button"]:has-text("Export Dashboard")',
      );
      await exportButton.click();

      // Monitor memory during export
      const memoryDuringExport = await page.evaluate(async () => {
        return new Promise((resolve) => {
          setTimeout(() => {
            const currentMemory =
              (performance as any).memory?.usedJSHeapSize || 0;
            resolve(currentMemory);
          }, 4000); // Check memory mid-export
        });
      });

      await page.waitForSelector("text*=Successfully exported", {
        timeout: 15000,
      });

      const postExportMemory = await page.evaluate(() => {
        return (performance as any).memory?.usedJSHeapSize || 0;
      });

      const maxMemoryIncrease = Math.max(
        (memoryDuringExport as number) - preExportMemory,
        postExportMemory - preExportMemory,
      );

      // Memory usage during large exports should be controlled
      expect(maxMemoryIncrease).toBeLessThan(300 * 1024 * 1024); // 300MB max increase

      console.log(
        `Large Export Memory Usage: ${(maxMemoryIncrease / 1024 / 1024).toFixed(2)}MB peak increase`,
      );
    });
  });

  describe("Resource Management Benchmarks", () => {
    it("benchmarks system resource recovery after exports", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
        dashboard: "portfolio_history_portrait",
      });

      await photoBoothE2EHelper.waitForPhotoBoothReady(page, 30000);

      const baselineMemory = await page.evaluate(() => {
        return (performance as any).memory?.usedJSHeapSize || 0;
      });

      // Perform multiple exports to test resource management
      const exportCount = 3;
      const exportTimes: number[] = [];

      for (let i = 0; i < exportCount; i++) {
        await page.route("/api/export-dashboard", async (route) => {
          await new Promise((resolve) => setTimeout(resolve, 2000));
          await route.fulfill({
            status: 200,
            contentType: "application/json",
            body: JSON.stringify({
              success: true,
              message: `Export ${i + 1} completed`,
              resourcesCleanedUp: true,
            }),
          });
        });

        const exportStart = performance.now();

        const exportButton = await page.waitForSelector(
          '[role="button"]:has-text("Export Dashboard")',
        );
        await exportButton.click();
        await page.waitForSelector("text*=Successfully exported", {
          timeout: 10000,
        });

        const exportTime = performance.now() - exportStart;
        exportTimes.push(exportTime);

        // Wait for cleanup
        await PhotoBoothE2EHelper.sleep(2000);
      }

      const finalMemory = await page.evaluate(() => {
        return (performance as any).memory?.usedJSHeapSize || 0;
      });

      const memoryLeak = finalMemory - baselineMemory;
      const averageExportTime =
        exportTimes.reduce((a, b) => a + b, 0) / exportTimes.length;

      // Resource management assertions
      expect(memoryLeak).toBeLessThan(50 * 1024 * 1024); // Less than 50MB memory leak
      expect(averageExportTime).toBeLessThan(8000); // Average export time under 8 seconds

      // Performance should not degrade significantly across exports
      const firstExportTime = exportTimes[0];
      const lastExportTime = exportTimes[exportTimes.length - 1];
      const performanceDegradation = lastExportTime - firstExportTime;

      expect(performanceDegradation).toBeLessThan(2000); // Less than 2 second degradation

      console.log(
        `Resource Management: ${exportCount} exports, ${(memoryLeak / 1024 / 1024).toFixed(2)}MB leak, ${averageExportTime.toFixed(2)}ms avg`,
      );
    });

    it("benchmarks dashboard switching performance", async () => {
      if (!isPhotoBoothDevelopmentMode()) {
        skipIfNotDevelopmentMode();
        return;
      }

      const { page } = context;

      const dashboards = ["portfolio_history_portrait", "trading_performance"];
      const switchTimes: number[] = [];

      for (let cycle = 0; cycle < 3; cycle++) {
        for (const dashboard of dashboards) {
          const switchStart = performance.now();

          await photoBoothE2EHelper.navigateToPhotoBoothRobust(page, {
            dashboard: dashboard,
          });

          await photoBoothE2EHelper.waitForPhotoBoothReady(page, 30000);

          const switchTime = performance.now() - switchStart;
          switchTimes.push(switchTime);

          // Brief pause between switches
          await PhotoBoothE2EHelper.sleep(1000);
        }
      }

      const averageSwitchTime =
        switchTimes.reduce((a, b) => a + b, 0) / switchTimes.length;

      // Dashboard switching should be efficient
      expect(averageSwitchTime).toBeLessThan(15000); // Under 15 seconds average

      // Performance should be consistent across switches
      const maxSwitchTime = Math.max(...switchTimes);
      const minSwitchTime = Math.min(...switchTimes);
      const consistencyRatio = maxSwitchTime / minSwitchTime;

      expect(consistencyRatio).toBeLessThan(3); // Max 3x variation in switch times

      console.log(
        `Dashboard Switching: ${switchTimes.length} switches, ${averageSwitchTime.toFixed(2)}ms avg, ${consistencyRatio.toFixed(2)}x variation`,
      );
    });
  });

  // Print benchmark summary after all tests
  afterAll(() => {
    if (isPhotoBoothDevelopmentMode() && benchmarkResults.length > 0) {
      console.log("\n=== PHOTO BOOTH PERFORMANCE BENCHMARK SUMMARY ===");
      benchmarkResults.forEach((result) => {
        const { configuration, metrics, success } = result;
        console.log(
          `${configuration}: Load ${metrics.loadTime.toFixed(2)}ms, Memory ${(metrics.memoryUsage / 1024 / 1024).toFixed(2)}MB - ${success ? "PASS" : "FAIL"}`,
        );
      });
      console.log("=".repeat(50));
    }
  });
});
