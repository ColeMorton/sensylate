/**
 * Routing Validation Tests
 * Tests to identify and prevent routing collision between charts page and blog routes
 */
import { describe, test, beforeAll, afterAll, expect } from "vitest";
import { setupE2ETest, cleanupE2ETest, type TestContext } from "./setup";

describe("Route Collision Detection", () => {
  let testContext: TestContext;

  beforeAll(async () => {
    testContext = await setupE2ETest();
  });

  afterAll(async () => {
    await cleanupE2ETest();
  });

  test("charts page should be handled by [regular].astro, not [single].astro", async () => {
    const { page } = testContext;

    // Listen to console messages to detect route handler
    const consoleMessages: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      if (text.includes("[ROUTE DEBUG]") || text.includes("[ROUTE ERROR]")) {
        consoleMessages.push(text);
      }
    });

    // Navigate to charts page
    const response = await page.goto(`${testContext.baseURL}/charts`);

    // Should load successfully
    expect(response?.status()).toBe(200);

    // Wait for page to load completely
    await page.waitForSelector("h1", { timeout: 10000 });

    // Check that charts page loaded correctly
    const h1Text = await page.$eval("h1", (el) => el.textContent);
    expect(h1Text).toContain("Interactive Charts");

    // Analyze console messages to identify route handler
    const blogRouteErrors = consoleMessages.filter(
      (msg) =>
        msg.includes("[single].astro incorrectly handling") ||
        msg.includes("This should be handled by [regular].astro"),
    );

    const regularRouteMessages = consoleMessages.filter((msg) =>
      msg.includes("[regular].astro processing URL: /charts"),
    );

    const blogRouteMessages = consoleMessages.filter((msg) =>
      msg.includes("[single].astro processing URL: /charts"),
    );

    // Log findings for debugging
    console.log("🔍 Route Analysis for /charts:");
    console.log(`  - Regular route messages: ${regularRouteMessages.length}`);
    console.log(`  - Blog route messages: ${blogRouteMessages.length}`);
    console.log(`  - Route collision errors: ${blogRouteErrors.length}`);

    // Verify correct routing behavior
    expect(
      blogRouteErrors.length,
      "Charts page should not trigger blog route errors",
    ).toBe(0);
    expect(
      regularRouteMessages.length,
      "Charts page should be processed by [regular].astro",
    ).toBeGreaterThan(0);
    expect(
      blogRouteMessages.length,
      "Charts page should NOT be processed by [single].astro",
    ).toBe(0);
  });

  test("blog posts should be handled by [single].astro correctly", async () => {
    const { page } = testContext;

    const consoleMessages: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      if (text.includes("[ROUTE DEBUG]") || text.includes("[POST ERROR]")) {
        consoleMessages.push(text);
      }
    });

    // Navigate to a blog post
    const response = await page.goto(`${testContext.baseURL}/blog/post-1`);
    expect(response?.status()).toBe(200);

    // Wait for blog post to load
    await page.waitForSelector("h1", { timeout: 10000 });

    // Check route handling
    const blogRouteMessages = consoleMessages.filter((msg) =>
      msg.includes("[single].astro processing URL: /blog/post-1"),
    );

    const postErrors = consoleMessages.filter((msg) =>
      msg.includes("[POST ERROR]"),
    );

    console.log("🔍 Route Analysis for /blog/post-1:");
    console.log(`  - Blog route messages: ${blogRouteMessages.length}`);
    console.log(`  - Post errors: ${postErrors.length}`);

    expect(
      blogRouteMessages.length,
      "Blog posts should be processed by [single].astro",
    ).toBeGreaterThan(0);
    expect(postErrors.length, "Blog posts should not have post errors").toBe(0);
  });

  test("direct navigation patterns should not cause routing confusion", async () => {
    const { page } = testContext;

    const consoleMessages: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      if (
        text.includes("[ROUTE DEBUG]") ||
        text.includes("[ROUTE ERROR]") ||
        text.includes("[POST ERROR]")
      ) {
        consoleMessages.push(text);
      }
    });

    // Test sequence: Home → Charts → Blog → Specific Post
    const navigationSequence = [
      { url: "/", expectedTitle: /Cole Morton|Home/ },
      { url: "/charts", expectedTitle: /Interactive Charts/ },
      { url: "/blog", expectedTitle: /Blog Posts/ },
      { url: "/blog/post-1", expectedTitle: /.*/ }, // Blog post title varies
    ];

    for (const { url, expectedTitle } of navigationSequence) {
      console.log(`🔍 Testing navigation to: ${url}`);

      const response = await page.goto(`${testContext.baseURL}${url}`);
      expect(response?.status()).toBe(200);

      await page.waitForSelector("h1", { timeout: 10000 });
      const h1Text = await page.$eval("h1", (el) => el.textContent);
      expect(h1Text).toMatch(expectedTitle);

      // Short delay between navigations
      await page.waitForTimeout(500);
    }

    // Analyze for any routing errors
    const routingErrors = consoleMessages.filter(
      (msg) =>
        msg.includes("[ROUTE ERROR]") ||
        msg.includes("incorrectly handling") ||
        msg.includes("[POST ERROR]"),
    );

    console.log("🔍 Navigation Sequence Analysis:");
    console.log(`  - Total console messages: ${consoleMessages.length}`);
    console.log(`  - Routing errors detected: ${routingErrors.length}`);

    if (routingErrors.length > 0) {
      console.log("❌ Routing errors found:");
      routingErrors.forEach((error) => console.log(`  - ${error}`));
    }

    expect(
      routingErrors.length,
      "Navigation sequence should not produce routing errors",
    ).toBe(0);
  });

  test("feature flag disabled pages should not cause routing issues", async () => {
    const { page } = testContext;

    const consoleMessages: string[] = [];
    page.on("console", (msg) => {
      const text = msg.text();
      if (text.includes("[ROUTE DEBUG]") || text.includes("[ROUTE ERROR]")) {
        consoleMessages.push(text);
      }
    });

    // Test access to elements page (may be feature flagged)
    const response = await page.goto(`${testContext.baseURL}/elements`);

    // Should either load successfully or redirect to 404
    expect([200, 404]).toContain(response?.status() || 0);

    // Check for routing confusion
    const routingErrors = consoleMessages.filter(
      (msg) =>
        msg.includes("incorrectly handling") && !msg.includes("/elements"), // Ignore expected elements route handling
    );

    expect(
      routingErrors.length,
      "Feature flagged pages should not cause routing confusion",
    ).toBe(0);
  });
});

describe("Charts Page Functionality", () => {
  let testContext: TestContext;

  beforeAll(async () => {
    testContext = await setupE2ETest();
  });

  afterAll(async () => {
    await cleanupE2ETest();
  });

  test("charts page loads without PostSingle.astro errors", async () => {
    const { page } = testContext;

    // Monitor for the specific error we're trying to fix
    let postSingleError = false;
    page.on("console", (msg) => {
      const text = msg.text();
      if (
        text.includes("Post not found: Unable to render undefined post entry")
      ) {
        postSingleError = true;
      }
    });

    // Navigate to charts page
    const response = await page.goto(`${testContext.baseURL}/charts`);
    expect(response?.status()).toBe(200);

    // Wait for charts to load
    await page.waitForSelector("h1", { timeout: 10000 });
    const h1Text = await page.$eval("h1", (el) => el.textContent);
    expect(h1Text).toContain("Interactive Charts");

    // Check for chart containers
    const chartContainers = await page.$$(
      '[data-testid="chart-container"], .chart-container, [class*="chart"]',
    );
    expect(
      chartContainers.length,
      "Charts page should contain chart elements",
    ).toBeGreaterThan(0);

    // Verify no PostSingle.astro errors occurred
    expect(
      postSingleError,
      "Charts page should not trigger PostSingle.astro errors",
    ).toBe(false);
  });

  test("charts page shows proper chart components", async () => {
    const { page } = testContext;
    await page.goto(`${testContext.baseURL}/charts`);

    // Wait for page load
    await page.waitForSelector("h1", { timeout: 10000 });

    // Look for chart-related elements
    const chartElements = await page.$$(
      'div[class*="chart"], [id*="plotly"], .plotly-graph-div',
    );

    // Should have at least one chart element
    expect(
      chartElements.length,
      "Charts page should contain chart elements",
    ).toBeGreaterThan(0);
  });
});
