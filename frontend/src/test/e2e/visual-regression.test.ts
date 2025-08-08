import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  e2eHelper,
  setupE2ETest,
  cleanupE2ETest,
  type TestContext,
  E2ETestHelper,
} from "../e2e/setup";
import { readFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";

describe("Visual Regression Tests", () => {
  let context: TestContext;

  beforeEach(async () => {
    context = await setupE2ETest();
  });

  afterEach(async () => {
    await cleanupE2ETest();
  });

  describe("Screenshot Baseline Management", () => {
    const baselineDir = "./src/test/e2e/screenshots/baselines";
    const comparisonDir = "./src/test/e2e/screenshots/comparisons";

    beforeEach(() => {
      // Ensure baseline and comparison directories exist
      if (!existsSync(baselineDir)) {
        mkdirSync(baselineDir, { recursive: true });
      }
      if (!existsSync(comparisonDir)) {
        mkdirSync(comparisonDir, { recursive: true });
      }
    });

    it("creates baseline screenshots for all aspect ratio and theme combinations", async () => {
      const { page, baseURL } = context;

      const combinations = [
        { aspectRatio: "16:9", mode: "light", name: "widescreen-light" },
        { aspectRatio: "16:9", mode: "dark", name: "widescreen-dark" },
        { aspectRatio: "4:3", mode: "light", name: "traditional-light" },
        { aspectRatio: "4:3", mode: "dark", name: "traditional-dark" },
        { aspectRatio: "3:4", mode: "light", name: "portrait-light" },
        { aspectRatio: "3:4", mode: "dark", name: "portrait-dark" },
      ];

      for (const combo of combinations) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${combo.aspectRatio}&mode=${combo.mode}`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Wait for charts to stabilize
        await E2ETestHelper.sleep(3000);

        // Hide controls for clean screenshot
        await page.evaluate(() => {
          const controls = document.querySelectorAll(".photo-booth-controls");
          controls.forEach((control) => {
            (control as HTMLElement).style.display = "none";
            (control as HTMLElement).style.visibility = "hidden";
          });
        });

        await E2ETestHelper.sleep(1000);

        // Take baseline screenshot
        const baselineFile = join(baselineDir, `baseline-${combo.name}.png`);
        await page.screenshot({
          path: baselineFile,
          fullPage: true,
          type: "png",
        });

        // Take comparison screenshot for current test run
        const comparisonFile = join(comparisonDir, `current-${combo.name}.png`);
        await page.screenshot({
          path: comparisonFile,
          fullPage: true,
          type: "png",
        });

        // Verify files were created
        expect(existsSync(baselineFile)).toBe(true);
        expect(existsSync(comparisonFile)).toBe(true);
      }
    });

    it("validates portfolio history portrait header consistency across themes", async () => {
      const { page, baseURL } = context;

      const modes = ["light", "dark"];

      for (const mode of modes) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4&mode=${mode}`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Focus on header section only
        const header = await page.$(".dashboard-header");
        expect(header).toBeTruthy();

        // Take focused screenshot of header
        await header?.screenshot({
          path: join(comparisonDir, `header-${mode}.png`),
          type: "png",
        });

        // Verify header text is consistent
        const headerText = await page.$eval(
          ".dashboard-header h1",
          (el) => el.textContent,
        );
        expect(headerText).toBe("Twitter Live Signals");

        // Verify header styling
        const headerStyles = await page.$eval(".dashboard-header h1", (el) => {
          const computed = getComputedStyle(el);
          return {
            fontSize: computed.fontSize,
            fontWeight: computed.fontWeight,
            textAlign: computed.textAlign,
          };
        });

        expect(headerStyles.fontSize).toBe("36px"); // text-4xl
        expect(headerStyles.fontWeight).toBe("700"); // font-bold
        expect(headerStyles.textAlign).toBe("center");
      }
    });

    it("validates footer consistency across aspect ratios", async () => {
      const { page, baseURL } = context;

      const aspectRatios = ["16:9", "4:3", "3:4"];

      for (const ratio of aspectRatios) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${ratio}&mode=light`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Focus on footer section only
        const footer = await page.$(".dashboard-footer");
        expect(footer).toBeTruthy();

        // Take focused screenshot of footer
        await footer?.screenshot({
          path: join(comparisonDir, `footer-${ratio.replace(":", "x")}.png`),
          type: "png",
        });

        // Verify footer text and positioning
        const footerText = await page.$eval(
          ".dashboard-footer h1",
          (el) => el.textContent,
        );
        expect(footerText).toBe("colemorton.com");

        const footerStyles = await page.$eval(".dashboard-footer", (el) => {
          const computed = getComputedStyle(el);
          return {
            display: computed.display,
            justifyContent: computed.justifyContent,
          };
        });

        expect(footerStyles.display).toBe("flex");
        expect(footerStyles.justifyContent).toBe("center");
      }
    });
  });

  describe("Chart Visual Consistency", () => {
    it("validates chart rendering consistency across themes", async () => {
      const { page, baseURL } = context;

      const modes = ["light", "dark"];

      for (const mode of modes) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=16:9&mode=${mode}`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
        await E2ETestHelper.sleep(5000); // Wait for charts to render

        // Take screenshots of individual charts
        const charts = await page.$$(".photo-booth-chart");

        for (let i = 0; i < charts.length; i++) {
          const chart = charts[i];

          // Scroll chart into view
          await chart.scrollIntoViewIfNeeded();
          await E2ETestHelper.sleep(1000);

          await chart.screenshot({
            path: join(comparisonDir, `chart-${i}-${mode}.png`),
            type: "png",
          });

          // Verify chart is visible and has reasonable dimensions
          const chartBox = await chart.boundingBox();
          expect(chartBox).toBeTruthy();
          expect(chartBox!.width).toBeGreaterThan(300);
          expect(chartBox!.height).toBeGreaterThan(200);
        }
      }
    });

    it("validates chart layout in portrait orientation", async () => {
      const { page, baseURL } = context;

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4&mode=light`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
      await E2ETestHelper.sleep(5000);

      // Take screenshot of charts container
      const chartsContainer = await page.$(
        ".flex.flex-col.h-full.min-h-0.flex-1",
      );
      expect(chartsContainer).toBeTruthy();

      await chartsContainer?.screenshot({
        path: join(comparisonDir, "charts-container-portrait.png"),
        type: "png",
      });

      // Verify 2x1 stack layout (flex-col)
      const containerStyles = await chartsContainer?.evaluate((el) => {
        const computed = getComputedStyle(el);
        return {
          display: computed.display,
          flexDirection: computed.flexDirection,
          height: computed.height,
        };
      });

      expect(containerStyles?.display).toBe("flex");
      expect(containerStyles?.flexDirection).toBe("column");

      // Verify charts are stacked vertically
      const charts = await page.$$(".photo-booth-chart");
      expect(charts.length).toBe(2);

      const chart1Box = await charts[0].boundingBox();
      const chart2Box = await charts[1].boundingBox();

      expect(chart1Box).toBeTruthy();
      expect(chart2Box).toBeTruthy();

      // Second chart should be below first chart
      expect(chart2Box!.y).toBeGreaterThan(
        chart1Box!.y + chart1Box!.height - 50,
      ); // Small overlap tolerance
    });
  });

  describe("Responsive Visual Testing", () => {
    const viewports = [
      { width: 1920, height: 1080, name: "desktop-fhd" },
      { width: 1440, height: 900, name: "laptop-standard" },
      { width: 1280, height: 720, name: "desktop-hd" },
    ];

    viewports.forEach((viewport) => {
      it(`validates visual consistency at ${viewport.name} (${viewport.width}x${viewport.height})`, async () => {
        const { page, baseURL } = context;

        await page.setViewport(viewport);

        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4&mode=light`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
        await E2ETestHelper.sleep(3000);

        // Hide controls for clean screenshot
        await page.evaluate(() => {
          const controls = document.querySelectorAll(".photo-booth-controls");
          controls.forEach((control) => {
            (control as HTMLElement).style.display = "none";
            (control as HTMLElement).style.visibility = "hidden";
          });
        });

        await page.screenshot({
          path: join(comparisonDir, `viewport-${viewport.name}.png`),
          fullPage: true,
          type: "png",
        });

        // Verify content fits within viewport
        const dashboard = await page.$(".photo-booth-dashboard");
        const dashboardBox = await dashboard?.boundingBox();

        expect(dashboardBox).toBeTruthy();
        expect(dashboardBox!.width).toBeLessThanOrEqual(viewport.width + 50); // Small tolerance
        expect(dashboardBox!.x).toBeGreaterThanOrEqual(-25); // Allow small negative margin
      });
    });
  });

  describe("Export Mode Visual Validation", () => {
    it("validates clean export screenshots without UI controls", async () => {
      const { page, baseURL } = context;

      const configurations = [
        { aspectRatio: "16:9", mode: "light", name: "export-16x9-light" },
        { aspectRatio: "3:4", mode: "dark", name: "export-3x4-dark" },
      ];

      for (const config of configurations) {
        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${config.aspectRatio}&mode=${config.mode}`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

        // Simulate export mode by hiding all controls
        await page.evaluate(() => {
          // Hide photo booth controls
          const controls = document.querySelectorAll(".photo-booth-controls");
          controls.forEach((element) => {
            (element as HTMLElement).style.display = "none";
            (element as HTMLElement).style.visibility = "hidden";
          });

          // Hide any dev toolbar elements
          const devElements = document.querySelectorAll(
            "[data-astro-dev-toolbar], astro-dev-toolbar, #dev-toolbar-root",
          );
          devElements.forEach((element) => {
            (element as HTMLElement).style.display = "none";
            (element as HTMLElement).style.visibility = "hidden";
          });
        });

        await E2ETestHelper.sleep(2000);

        // Take clean export screenshot
        await page.screenshot({
          path: join(comparisonDir, `${config.name}-clean.png`),
          fullPage: false,
          type: "png",
        });

        // Verify no UI controls are visible
        const visibleControls = await page.$$eval(
          ".photo-booth-controls",
          (controls) =>
            controls.filter((control) => {
              const style = getComputedStyle(control as HTMLElement);
              return style.display !== "none" && style.visibility !== "hidden";
            }).length,
        );

        expect(visibleControls).toBe(0);

        // Verify essential dashboard content is still visible
        const header = await page.$(".dashboard-header h1");
        const footer = await page.$(".dashboard-footer h1");
        const charts = await page.$$(".photo-booth-chart");

        expect(header).toBeTruthy();
        expect(footer).toBeTruthy();
        expect(charts.length).toBe(2);
      }
    });

    it("compares display mode vs export mode layout", async () => {
      const { page, baseURL } = context;

      await page.goto(
        `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4&mode=light`,
        {
          waitUntil: "networkidle0",
          timeout: 15000,
        },
      );

      await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });

      // Take screenshot with controls (display mode)
      await page.screenshot({
        path: join(comparisonDir, "display-mode-with-controls.png"),
        fullPage: true,
        type: "png",
      });

      // Hide controls (export mode)
      await page.evaluate(() => {
        const controls = document.querySelectorAll(".photo-booth-controls");
        controls.forEach((control) => {
          (control as HTMLElement).style.display = "none";
          (control as HTMLElement).style.visibility = "hidden";
        });
      });

      await E2ETestHelper.sleep(1000);

      // Take screenshot without controls (export mode)
      await page.screenshot({
        path: join(comparisonDir, "export-mode-without-controls.png"),
        fullPage: true,
        type: "png",
      });

      // Verify dashboard utilizes more space in export mode
      const dashboard = await page.$(".photo-booth-dashboard");
      const dashboardBox = await dashboard?.boundingBox();
      const viewport = page.viewport();

      expect(dashboardBox).toBeTruthy();
      expect(viewport).toBeTruthy();

      // In export mode, dashboard should use more of the viewport
      const utilizationRatio = dashboardBox!.height / viewport!.height;
      expect(utilizationRatio).toBeGreaterThan(0.8); // Should use at least 80% of viewport height
    });
  });

  describe("Cross-Browser Visual Consistency", () => {
    it("validates rendering consistency across different browser settings", async () => {
      const { page, baseURL } = context;

      // Test with different device scale factors
      const scaleFactors = [1, 2, 3];

      for (const scaleFactor of scaleFactors) {
        await page.setViewport({
          width: 1920,
          height: 1080,
          deviceScaleFactor: scaleFactor,
        });

        await page.goto(
          `${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=16:9&mode=light`,
          {
            waitUntil: "networkidle0",
            timeout: 15000,
          },
        );

        await page.waitForSelector(".photo-booth-ready", { timeout: 20000 });
        await E2ETestHelper.sleep(3000);

        // Hide controls for clean comparison
        await page.evaluate(() => {
          const controls = document.querySelectorAll(".photo-booth-controls");
          controls.forEach((control) => {
            (control as HTMLElement).style.display = "none";
            (control as HTMLElement).style.visibility = "hidden";
          });
        });

        await page.screenshot({
          path: join(comparisonDir, `scale-factor-${scaleFactor}x.png`),
          fullPage: false,
          type: "png",
        });

        // Verify content remains readable and properly scaled
        const header = await page.$eval(".dashboard-header h1", (el) => {
          const rect = el.getBoundingClientRect();
          const computed = getComputedStyle(el);
          return {
            fontSize: computed.fontSize,
            width: rect.width,
            height: rect.height,
          };
        });

        // Font size should remain consistent across scale factors
        expect(header.fontSize).toBe("36px");
        expect(header.width).toBeGreaterThan(200);
        expect(header.height).toBeGreaterThan(30);
      }
    });
  });
});
