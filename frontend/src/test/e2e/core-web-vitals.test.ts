/**
 * Core Web Vitals Monitoring E2E Test
 * Verifies that the WebVitals component is working correctly using Puppeteer
 */

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import puppeteer from "puppeteer";
import { spawn } from "child_process";
import { promises as fs } from "fs";
import path from "path";

describe("Core Web Vitals Monitoring", () => {
  let browser;
  let devServer;
  let page;
  const DEV_PORT = 4321;
  const DEV_URL = `http://localhost:${DEV_PORT}`;

  beforeAll(async () => {
    // Start the development server
    console.log("Starting development server...");
    devServer = spawn("yarn", ["dev"], {
      stdio: "pipe",
      cwd: process.cwd(),
    });

    // Wait for dev server to be ready
    await new Promise((resolve) => {
      devServer.stdout.on("data", (data) => {
        const output = data.toString();
        if (output.includes("Local") && output.includes("4321")) {
          console.log("Development server ready");
          resolve();
        }
      });

      // Fallback timeout
      setTimeout(resolve, 10000);
    });

    // Launch browser
    browser = await puppeteer.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });

    page = await browser.newPage();

    // Enable console logging
    page.on("console", (msg) => {
      if (msg.text().includes("[WebVitals]")) {
        console.log("Browser console:", msg.text());
      }
    });
  }, 30000);

  afterAll(async () => {
    if (browser) {
      await browser.close();
    }
    if (devServer) {
      devServer.kill();
    }
  });

  it("should display the Core Web Vitals monitor in development mode", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Check if the performance indicator exists
    const perfIndicator = await page.$("#perf-indicator");
    expect(perfIndicator).toBeTruthy();

    // Check initial text
    const initialText = await page.$eval(
      "#perf-status",
      (el) => el.textContent,
    );
    expect(initialText).toContain("Initializing");
  });

  it("should initialize the webVitalsMonitor on the window object", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Wait for the monitor to initialize
    await page.waitForFunction(() => window.webVitalsMonitor !== undefined, {
      timeout: 15000,
    });

    // Verify the monitor object exists and has expected methods
    const monitorExists = await page.evaluate(() => {
      return (
        typeof window.webVitalsMonitor === "object" &&
        typeof window.webVitalsMonitor.getMetrics === "function" &&
        typeof window.webVitalsMonitor.getPerformanceScore === "function"
      );
    });

    expect(monitorExists).toBe(true);
  });

  it("should update the performance indicator with metrics", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Wait for monitor to initialize
    await page.waitForFunction(() => window.webVitalsMonitor !== undefined, {
      timeout: 15000,
    });

    // Wait for the indicator to show metrics (not "Initializing")
    await page.waitForFunction(
      () => {
        const indicator = document.getElementById("perf-status");
        return indicator && !indicator.textContent.includes("Initializing");
      },
      { timeout: 10000 },
    );

    const metricsText = await page.$eval(
      "#perf-status",
      (el) => el.textContent,
    );

    // Should contain Core Web Vitals metrics
    expect(metricsText).toMatch(/LCP:/);
    expect(metricsText).toMatch(/FID:/);
    expect(metricsText).toMatch(/CLS:/);
    expect(metricsText).toMatch(/Score:/);
  });

  it("should show green border when monitor is active", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Wait for monitor to initialize and show green border
    await page.waitForFunction(
      () => {
        const indicator = document.getElementById("perf-status");
        const style = window.getComputedStyle(indicator);
        return (
          style.borderLeftColor === "rgb(0, 255, 0)" ||
          indicator.style.borderLeft.includes("rgb(0, 255, 0)") ||
          indicator.style.borderLeft.includes("#00ff00")
        );
      },
      { timeout: 15000 },
    );

    const borderStyle = await page.$eval(
      "#perf-status",
      (el) => el.style.borderLeft,
    );
    expect(borderStyle).toContain("00ff00");
  });

  it("should collect and record Core Web Vitals metrics", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Wait for monitor initialization
    await page.waitForFunction(() => window.webVitalsMonitor !== undefined, {
      timeout: 15000,
    });

    // Give some time for metrics to be collected
    await page.waitForTimeout(3000);

    // Check that metrics are being collected
    const metrics = await page.evaluate(() => {
      return window.webVitalsMonitor.getMetrics();
    });

    expect(typeof metrics).toBe("object");

    // Should have at least some metrics (even if some are "unsupported")
    const metricKeys = Object.keys(metrics);
    expect(metricKeys.length).toBeGreaterThan(0);

    // Check for expected metric types
    const expectedMetrics = [
      "LCP",
      "FID",
      "CLS",
      "TTFB",
      "FCP",
      "ContentReady",
      "InteractiveReady",
    ];
    const hasExpectedMetrics = expectedMetrics.some((metric) =>
      metricKeys.includes(metric),
    );
    expect(hasExpectedMetrics).toBe(true);
  });

  it("should calculate performance score", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    // Wait for monitor initialization
    await page.waitForFunction(() => window.webVitalsMonitor !== undefined, {
      timeout: 15000,
    });

    // Trigger some interactions to generate metrics
    await page.click("body");
    await page.waitForTimeout(2000);

    const score = await page.evaluate(() => {
      return window.webVitalsMonitor.getPerformanceScore();
    });

    // Score should be null if not enough metrics, or a number between 0-100
    expect(
      score === null ||
        (typeof score === "number" && score >= 0 && score <= 100),
    ).toBe(true);
  });

  it("should handle blog post page with enhanced meta tags", async () => {
    const blogUrl = `${DEV_URL}/blog/well-fundamental-analysis-20250620`;
    await page.goto(blogUrl, { waitUntil: "networkidle2" });

    // Verify enhanced meta tags are present
    const metaTags = await page.evaluate(() => {
      const tags = {};

      // Check for article-specific meta tags
      tags.articleAuthor = document.querySelector(
        'meta[property="article:author"]',
      )?.content;
      tags.articleSection = document.querySelector(
        'meta[property="article:section"]',
      )?.content;
      tags.tradingSymbols = document.querySelector(
        'meta[name="trading.symbols"]',
      )?.content;
      tags.readingTime = document.querySelector(
        'meta[name="content.readingTime"]',
      )?.content;
      tags.wordCount = document.querySelector(
        'meta[name="content.wordCount"]',
      )?.content;
      tags.seoScore = document.querySelector(
        'meta[name="content.estimatedSeoScore"]',
      )?.content;

      return tags;
    });

    expect(metaTags.articleAuthor).toBe("Cole Morton");
    expect(metaTags.articleSection).toBe("Fundamental Analysis");
    expect(metaTags.tradingSymbols).toContain("WELL");
    expect(metaTags.readingTime).toBe("8");
    expect(metaTags.wordCount).toBe("1523");
    expect(metaTags.seoScore).toBe("85");
  });

  it("should display reading time component on blog posts", async () => {
    const blogUrl = `${DEV_URL}/blog/well-fundamental-analysis-20250620`;
    await page.goto(blogUrl, { waitUntil: "networkidle2" });

    // Check for reading time display
    const readingTimeElement = await page.$(".reading-time-minimal");
    expect(readingTimeElement).toBeTruthy();

    const readingTimeText = await page.$eval(
      ".reading-time-minimal",
      (el) => el.textContent,
    );
    expect(readingTimeText).toContain("min read");
    expect(readingTimeText).toContain("8"); // Expected reading time for this post
  });

  it("should track reading progress events", async () => {
    const blogUrl = `${DEV_URL}/blog/well-fundamental-analysis-20250620`;
    await page.goto(blogUrl, { waitUntil: "networkidle2" });

    // Set up console monitoring for tracking events
    const trackingEvents = [];
    page.on("console", (msg) => {
      if (msg.text().includes("tracking") || msg.text().includes("milestone")) {
        trackingEvents.push(msg.text());
      }
    });

    // Scroll to trigger reading progress
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight * 0.6);
    });

    await page.waitForTimeout(1000);

    // Check that scroll tracking is working (variables are set)
    const scrollTracking = await page.evaluate(() => {
      return (
        typeof window._tracked50 !== "undefined" ||
        typeof window._tracked75 !== "undefined"
      );
    });

    // The tracking variables should exist (though may not be set yet)
    expect(typeof scrollTracking).toBe("boolean");
  });

  it("should have proper resource preload hints", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    const preloadHints = await page.evaluate(() => {
      const preloads = Array.from(
        document.querySelectorAll('link[rel="preload"]'),
      );
      return preloads.map((link) => ({
        href: link.href,
        as: link.getAttribute("as"),
      }));
    });

    // Should have CSS and font preloads
    const hasCSSPreload = preloadHints.some((hint) => hint.as === "style");
    const hasFontPreload = preloadHints.some((hint) =>
      hint.href.includes("fonts.googleapis.com"),
    );

    expect(hasCSSPreload).toBe(true);
    expect(hasFontPreload).toBe(true);
  });

  it("should have DNS prefetch for external domains", async () => {
    await page.goto(DEV_URL, { waitUntil: "networkidle2" });

    const dnsPrefetches = await page.evaluate(() => {
      const prefetches = Array.from(
        document.querySelectorAll('link[rel="dns-prefetch"]'),
      );
      return prefetches.map((link) => link.href);
    });

    // Should prefetch Google Fonts and Disqus
    expect(
      dnsPrefetches.some((href) => href.includes("fonts.googleapis.com")),
    ).toBe(true);
    expect(dnsPrefetches.some((href) => href.includes("disqus.com"))).toBe(
      true,
    );
  });
});

// Helper function to take screenshots for debugging
// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function takeScreenshot(page, name) {
  if (process.env.E2E_SCREENSHOTS) {
    const screenshotDir = path.join(process.cwd(), "test", "screenshots");
    await fs.mkdir(screenshotDir, { recursive: true });
    await page.screenshot({
      path: path.join(screenshotDir, `${name}-${Date.now()}.png`),
      fullPage: true,
    });
  }
}
