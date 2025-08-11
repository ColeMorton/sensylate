/**
 * Debug Navigation Error - Blog and Analysis Pages
 * Reproduces and debugs the "Post not found: Unable to render undefined post entry" error
 * when navigating from homepage to blog and analysis pages
 */
import { describe, test, beforeAll, afterAll, expect } from "vitest";
import {
  setupE2ETest,
  cleanupE2ETest,
  e2eHelper,
  type TestContext,
} from "./setup";

interface ConsoleMessage {
  type: string;
  text: string;
  timestamp: number;
}

interface NavigationResult {
  url: string;
  success: boolean;
  error?: string;
  consoleMessages: ConsoleMessage[];
  networkRequests: string[];
  routeHandler?: string;
}

describe("Debug Navigation Error - Blog and Analysis Pages", () => {
  let testContext: TestContext;
  const allConsoleMessages: ConsoleMessage[] = [];
  const allNetworkRequests: string[] = [];

  beforeAll(async () => {
    testContext = await setupE2ETest();
    console.log(`🔍 Testing against: ${testContext.baseURL}`);
  });

  afterAll(async () => {
    await cleanupE2ETest();
  });

  test("capture comprehensive debug data for homepage → blog → analysis navigation", async () => {
    const { page } = testContext;

    // Track all console messages with timestamps
    page.on("console", (msg) => {
      const message: ConsoleMessage = {
        type: msg.type(),
        text: msg.text(),
        timestamp: Date.now(),
      };
      allConsoleMessages.push(message);

      // Log important messages immediately
      if (
        msg.type() === "error" ||
        msg.text().includes("[ROUTE DEBUG]") ||
        msg.text().includes("[ROUTE ERROR]") ||
        msg.text().includes("[POST ERROR]") ||
        msg.text().includes("Post not found")
      ) {
        console.log(`🔍 [${msg.type().toUpperCase()}] ${msg.text()}`);
      }
    });

    // Track network requests
    page.on("request", (request) => {
      allNetworkRequests.push(`${request.method()} ${request.url()}`);
    });

    // Track page errors
    page.on("pageerror", (error) => {
      console.error("🚨 Page Error:", error.message);
      allConsoleMessages.push({
        type: "pageerror",
        text: error.message,
        timestamp: Date.now(),
      });
    });

    const navigationResults: NavigationResult[] = [];

    // Navigation sequence to reproduce the error
    const navigationSteps = [
      { path: "/", description: "Homepage" },
      { path: "/blog", description: "Blog listing page" },
      { path: "/categories/analysis", description: "Analysis category page" },
    ];

    for (const step of navigationSteps) {
      console.log(`\n🔍 Navigating to: ${step.description} (${step.path})`);

      const startTime = Date.now();
      const beforeMessages = allConsoleMessages.length;
      const beforeRequests = allNetworkRequests.length;

      try {
        const response = await page.goto(`${testContext.baseURL}${step.path}`, {
          waitUntil: "networkidle0",
          timeout: 15000,
        });

        // Wait for page to settle
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const endTime = Date.now();
        const stepMessages = allConsoleMessages.slice(beforeMessages);
        const stepRequests = allNetworkRequests.slice(beforeRequests);

        // Try to identify which route handler processed this request
        const routeHandler = stepMessages.find(
          (msg) =>
            msg.text.includes("[ROUTE DEBUG]") &&
            msg.text.includes("processing URL"),
        )?.text;

        const result: NavigationResult = {
          url: step.path,
          success: response?.status() === 200,
          consoleMessages: stepMessages,
          networkRequests: stepRequests,
          routeHandler,
        };

        // Check for the specific error we're debugging
        const postSingleError = stepMessages.find((msg) =>
          msg.text.includes(
            "Post not found: Unable to render undefined post entry",
          ),
        );

        if (postSingleError) {
          result.error = "PostSingle.astro received undefined post prop";
          console.error(`❌ Found PostSingle error on ${step.path}!`);
        }

        // Check for routing collision errors
        const routingErrors = stepMessages.filter(
          (msg) =>
            msg.text.includes("incorrectly handling") ||
            msg.text.includes("[ROUTE ERROR]") ||
            msg.text.includes("[POST ERROR]"),
        );

        if (routingErrors.length > 0) {
          console.error(`❌ Routing errors found on ${step.path}:`);
          routingErrors.forEach((error) => console.error(`  - ${error.text}`));
        }

        navigationResults.push(result);

        // Take screenshot for debugging
        await e2eHelper.takeScreenshot(
          page,
          `debug-navigation-${step.path.replace(/\//g, "-")}`,
        );

        console.log(
          `✅ ${step.description}: Status ${response?.status()}, took ${endTime - startTime}ms`,
        );
      } catch (error) {
        console.error(`❌ Navigation to ${step.path} failed:`, error.message);
        navigationResults.push({
          url: step.path,
          success: false,
          error: error.message,
          consoleMessages: allConsoleMessages.slice(beforeMessages),
          networkRequests: allNetworkRequests.slice(beforeRequests),
        });
      }

      // Small delay between navigations
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    // Analyze results
    console.log("\n🔍 =========================");
    console.log("🔍 NAVIGATION ANALYSIS REPORT");
    console.log("🔍 =========================");

    for (const result of navigationResults) {
      console.log(`\n📄 ${result.url}:`);
      console.log(`  ✅ Success: ${result.success}`);
      console.log(`  🛣️  Route handler: ${result.routeHandler || "Unknown"}`);
      console.log(`  🔢 Console messages: ${result.consoleMessages.length}`);
      console.log(`  🌐 Network requests: ${result.networkRequests.length}`);

      if (result.error) {
        console.log(`  ❌ Error: ${result.error}`);
      }

      // Show route debugging messages
      const routeDebugMessages = result.consoleMessages.filter(
        (msg) =>
          msg.text.includes("[ROUTE DEBUG]") ||
          msg.text.includes("[ROUTE ERROR]") ||
          msg.text.includes("[POST ERROR]"),
      );

      if (routeDebugMessages.length > 0) {
        console.log("  📝 Route debug messages:");
        routeDebugMessages.forEach((msg) =>
          console.log(`     - [${msg.type}] ${msg.text}`),
        );
      }
    }

    // Find the root cause
    const errorResults = navigationResults.filter((r) => r.error);
    const postSingleErrors = allConsoleMessages.filter((msg) =>
      msg.text.includes(
        "Post not found: Unable to render undefined post entry",
      ),
    );

    console.log("\n🔍 ROOT CAUSE ANALYSIS:");
    console.log(`  📊 Total navigation attempts: ${navigationResults.length}`);
    console.log(`  ❌ Failed navigations: ${errorResults.length}`);
    console.log(`  🚨 PostSingle errors: ${postSingleErrors.length}`);

    if (postSingleErrors.length > 0) {
      console.log("\n❌ PostSingle errors detected:");
      postSingleErrors.forEach((error) => {
        console.log(`  - ${error.text} (timestamp: ${error.timestamp})`);
      });
    }

    // Check for routing collisions
    const routingCollisions = allConsoleMessages.filter(
      (msg) =>
        msg.text.includes("incorrectly handling") ||
        msg.text.includes("This should be handled by [regular].astro"),
    );

    if (routingCollisions.length > 0) {
      console.log("\n🚨 Routing collisions detected:");
      routingCollisions.forEach((collision) => {
        console.log(`  - ${collision.text}`);
      });
    }

    // Assertions to fail the test if errors are found
    expect(
      postSingleErrors.length,
      "Should not have PostSingle errors during navigation",
    ).toBe(0);
    expect(routingCollisions.length, "Should not have routing collisions").toBe(
      0,
    );

    // All navigations should succeed
    const successfulNavigations = navigationResults.filter(
      (r) => r.success,
    ).length;
    expect(successfulNavigations, "All navigation steps should succeed").toBe(
      navigationSteps.length,
    );
  });

  test("isolate blog page navigation issue", async () => {
    const { page } = testContext;

    console.log("\n🔍 Testing direct blog page navigation...");

    const consoleMessages: ConsoleMessage[] = [];
    page.on("console", (msg) => {
      consoleMessages.push({
        type: msg.type(),
        text: msg.text(),
        timestamp: Date.now(),
      });
    });

    // Direct navigation to blog page
    const response = await page.goto(`${testContext.baseURL}/blog`);
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const blogErrors = consoleMessages.filter(
      (msg) =>
        msg.text.includes("Post not found") ||
        msg.text.includes("[POST ERROR]") ||
        msg.text.includes("incorrectly handling"),
    );

    console.log(`📊 Blog page navigation - Status: ${response?.status()}`);
    console.log(`📊 Console messages: ${consoleMessages.length}`);
    console.log(`❌ Error messages: ${blogErrors.length}`);

    if (blogErrors.length > 0) {
      console.log("❌ Blog page errors:");
      blogErrors.forEach((error) => console.log(`  - ${error.text}`));
    }

    expect(blogErrors.length, "Blog page should not have routing errors").toBe(
      0,
    );
  });

  test("isolate analysis page navigation issue", async () => {
    const { page } = testContext;

    console.log("\n🔍 Testing direct analysis page navigation...");

    const consoleMessages: ConsoleMessage[] = [];
    page.on("console", (msg) => {
      consoleMessages.push({
        type: msg.type(),
        text: msg.text(),
        timestamp: Date.now(),
      });
    });

    // Direct navigation to analysis page
    const response = await page.goto(
      `${testContext.baseURL}/categories/analysis`,
    );
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const analysisErrors = consoleMessages.filter(
      (msg) =>
        msg.text.includes("Post not found") ||
        msg.text.includes("[POST ERROR]") ||
        msg.text.includes("incorrectly handling"),
    );

    console.log(`📊 Analysis page navigation - Status: ${response?.status()}`);
    console.log(`📊 Console messages: ${consoleMessages.length}`);
    console.log(`❌ Error messages: ${analysisErrors.length}`);

    if (analysisErrors.length > 0) {
      console.log("❌ Analysis page errors:");
      analysisErrors.forEach((error) => console.log(`  - ${error.text}`));
    }

    expect(
      analysisErrors.length,
      "Analysis page should not have routing errors",
    ).toBe(0);
  });
});
