/**
 * Click Navigation Debug Test
 * Tests navigation by clicking links on homepage to reproduce the PostSingle error
 * Simulates the exact user flow: homepage → click blog → click analysis
 */
import { describe, test, beforeAll, afterAll, expect } from "vitest";
import { setupE2ETest, cleanupE2ETest, type TestContext } from "./setup";

describe("Click Navigation Debug - Homepage Link Clicks", () => {
  let testContext: TestContext;

  beforeAll(async () => {
    testContext = await setupE2ETest();
    console.log(`🔍 Testing click navigation against: ${testContext.baseURL}`);
  });

  afterAll(async () => {
    await cleanupE2ETest();
  });

  test("simulate user clicking navigation links from homepage", async () => {
    const { page } = testContext;

    const allConsoleMessages: string[] = [];
    const allErrors: string[] = [];

    // Capture all console messages
    page.on("console", (msg) => {
      const text = msg.text();
      allConsoleMessages.push(`[${msg.type()}] ${text}`);

      // Look for the specific PostSingle error
      if (
        text.includes("Post not found: Unable to render undefined post entry")
      ) {
        console.error(`🚨 FOUND THE ERROR: ${text}`);
        allErrors.push(text);
      }

      // Log routing debug messages
      if (
        text.includes("[ROUTE DEBUG]") ||
        text.includes("[ROUTE ERROR]") ||
        text.includes("[POST ERROR]") ||
        text.includes("incorrectly handling")
      ) {
        console.log(`🔍 ${text}`);
      }
    });

    // Capture page errors
    page.on("pageerror", (error) => {
      const errorText = `Page Error: ${error.message}`;
      console.error(`🚨 ${errorText}`);
      allErrors.push(errorText);
    });

    // Start at homepage
    console.log("\n🏠 Loading homepage...");
    await page.goto(`${testContext.baseURL}/`, {
      waitUntil: "networkidle0",
      timeout: 15000,
    });

    // Wait for page to fully load
    await page.waitForSelector("nav", { timeout: 10000 });
    await new Promise((resolve) => setTimeout(resolve, 2000));

    console.log("✅ Homepage loaded");

    // Find and click the Blog link
    console.log("\n📰 Clicking Blog navigation link...");

    try {
      // Look for blog link in navigation
      const blogLink = await page.$(
        'nav a[href="/blog"], nav a[href*="blog"], a[href="/blog"]',
      );

      if (!blogLink) {
        console.error("❌ Could not find blog link in navigation");
        // Let's see what navigation links are available
        const navLinks = await page.$$eval("nav a", (links) =>
          links.map((link) => ({
            href: link.href,
            text: link.textContent?.trim(),
          })),
        );
        console.log("Available navigation links:", navLinks);
        throw new Error("Blog link not found");
      }

      // Click the blog link
      await blogLink.click();

      // Wait for navigation to complete
      await page.waitForNavigation({
        waitUntil: "networkidle0",
        timeout: 15000,
      });
      await new Promise((resolve) => setTimeout(resolve, 2000));

      console.log(`✅ Navigated to blog page: ${page.url()}`);

      // Check for errors after blog navigation
      const blogErrors = allErrors.filter(
        (error) =>
          error.includes("Post not found") ||
          error.includes("undefined post entry"),
      );

      if (blogErrors.length > 0) {
        console.error(
          `❌ Found ${blogErrors.length} errors after blog navigation:`,
        );
        blogErrors.forEach((error) => console.error(`  - ${error}`));
      } else {
        console.log("✅ No PostSingle errors found after blog navigation");
      }
    } catch (error) {
      console.error(`❌ Blog navigation failed: ${error.message}`);
    }

    // Go back to homepage for analysis test
    console.log("\n🏠 Returning to homepage...");
    await page.goto(`${testContext.baseURL}/`, {
      waitUntil: "networkidle0",
      timeout: 15000,
    });
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Find and click the Analysis link
    console.log("\n📊 Clicking Analysis navigation link...");

    try {
      // Look for analysis link in navigation
      const analysisLink = await page.$(
        'nav a[href="/categories/analysis"], nav a[href*="analysis"], a[href*="analysis"]',
      );

      if (!analysisLink) {
        console.error("❌ Could not find analysis link in navigation");
        // Let's see what navigation links are available
        const navLinks = await page.$$eval("nav a", (links) =>
          links.map((link) => ({
            href: link.href,
            text: link.textContent?.trim(),
          })),
        );
        console.log("Available navigation links:", navLinks);
        throw new Error("Analysis link not found");
      }

      // Click the analysis link
      await analysisLink.click();

      // Wait for navigation to complete
      await page.waitForNavigation({
        waitUntil: "networkidle0",
        timeout: 15000,
      });
      await new Promise((resolve) => setTimeout(resolve, 2000));

      console.log(`✅ Navigated to analysis page: ${page.url()}`);

      // Check for errors after analysis navigation
      const analysisErrors = allErrors.filter(
        (error) =>
          error.includes("Post not found") ||
          error.includes("undefined post entry"),
      );

      if (analysisErrors.length > 0) {
        console.error(
          `❌ Found ${analysisErrors.length} errors after analysis navigation:`,
        );
        analysisErrors.forEach((error) => console.error(`  - ${error}`));
      } else {
        console.log("✅ No PostSingle errors found after analysis navigation");
      }
    } catch (error) {
      console.error(`❌ Analysis navigation failed: ${error.message}`);
    }

    // Final analysis
    console.log("\n🔍 =========================");
    console.log("🔍 CLICK NAVIGATION ANALYSIS");
    console.log("🔍 =========================");
    console.log(`📊 Total console messages: ${allConsoleMessages.length}`);
    console.log(`❌ Total errors found: ${allErrors.length}`);

    if (allErrors.length > 0) {
      console.log("\n❌ All errors detected:");
      allErrors.forEach((error, index) => {
        console.log(`  ${index + 1}. ${error}`);
      });
    }

    // Show routing debug messages
    const routingMessages = allConsoleMessages.filter(
      (msg) =>
        msg.includes("[ROUTE DEBUG]") ||
        msg.includes("[ROUTE ERROR]") ||
        msg.includes("[POST ERROR]") ||
        msg.includes("incorrectly handling"),
    );

    if (routingMessages.length > 0) {
      console.log("\n📝 Routing debug messages:");
      routingMessages.forEach((msg) => console.log(`  - ${msg}`));
    }

    // Test assertions
    expect(
      allErrors.length,
      "Should not have any PostSingle errors during click navigation",
    ).toBe(0);
  });

  test("test rapid navigation clicking to trigger race conditions", async () => {
    const { page } = testContext;

    const errors: string[] = [];

    page.on("console", (msg) => {
      if (
        msg.text().includes("Post not found") ||
        msg.text().includes("undefined post entry") ||
        msg.text().includes("[POST ERROR]")
      ) {
        console.error(`🚨 RAPID NAV ERROR: ${msg.text()}`);
        errors.push(msg.text());
      }
    });

    page.on("pageerror", (error) => {
      console.error(`🚨 RAPID NAV PAGE ERROR: ${error.message}`);
      errors.push(error.message);
    });

    console.log("\n🏃‍♂️ Testing rapid navigation clicks...");

    // Start at homepage
    await page.goto(`${testContext.baseURL}/`, { waitUntil: "networkidle0" });
    await page.waitForSelector("nav", { timeout: 10000 });

    // Rapid clicking sequence to potentially trigger race conditions
    const clickSequence = [
      'a[href="/blog"]',
      'a[href="/categories/analysis"]',
      'a[href="/"]',
      'a[href="/blog"]',
      'a[href="/categories/analysis"]',
    ];

    for (let i = 0; i < clickSequence.length; i++) {
      const selector = clickSequence[i];
      console.log(`🔄 Rapid click ${i + 1}: ${selector}`);

      try {
        const link = await page.$(selector);
        if (link) {
          await link.click();
          // Very short delay to potentially trigger race conditions
          await new Promise((resolve) => setTimeout(resolve, 100));
        }
      } catch (error) {
        console.log(`⚠️  Rapid click ${i + 1} failed: ${error.message}`);
      }
    }

    // Wait for any pending navigation/errors to settle
    await new Promise((resolve) => setTimeout(resolve, 3000));

    console.log(`📊 Rapid navigation errors found: ${errors.length}`);

    if (errors.length > 0) {
      console.log("❌ Rapid navigation errors:");
      errors.forEach((error) => console.log(`  - ${error}`));
    }

    expect(
      errors.length,
      "Rapid navigation should not cause PostSingle errors",
    ).toBe(0);
  });
});
