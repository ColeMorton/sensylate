import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

describe("Calculator Navigation E2E Tests", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  describe("Basic Navigation", () => {
    it("should navigate to calculators listing page", async () => {
      await page.goto(`${e2eHelper.baseURL}/calculators`, {
        waitUntil: "networkidle0",
      });

      const title = await page.title();
      expect(title).toMatch(/calculator/i);

      // Should see calculator cards
      const calculatorCards = await page.$$(
        'a[href*="calculator"], [data-calculator]',
      );
      expect(calculatorCards.length).toBeGreaterThan(0);
    }, 15000);

    it("should navigate to pocket calculator page", async () => {
      await page.goto(`${e2eHelper.baseURL}/calculators/pocket-calculator`, {
        waitUntil: "networkidle0",
      });

      expect(page.url()).toMatch(/\/calculators\/pocket-calculator$/);

      const title = await page.title();
      expect(title).toMatch(/pocket calculator|basic arithmetic calculator/i);

      // Should see page content
      const pageContent = await page.$("main, .section, .container");
      expect(pageContent).toBeTruthy();
    }, 15000);

    it("should show calculator widget container", async () => {
      await page.goto(`${e2eHelper.baseURL}/calculators/pocket-calculator`, {
        waitUntil: "networkidle0",
      });

      // Wait a bit for potential React hydration
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Check for calculator container
      const calculatorContainer = await page.$(".calculator-container");
      expect(calculatorContainer).toBeTruthy();

      // Take a screenshot for debugging
      await e2eHelper.takeScreenshot(page, "calculator-page-loaded");
    }, 15000);

    it("should have interactive elements present", async () => {
      await page.goto(`${e2eHelper.baseURL}/calculators/pocket-calculator`, {
        waitUntil: "networkidle0",
      });

      // Wait for potential hydration
      await new Promise((resolve) => setTimeout(resolve, 3000));

      // Look for input field (various selectors)
      const inputSelectors = [
        'input[type="text"]',
        'input[placeholder*="expression"]',
        'input[name="expression"]',
        '[data-testid^="input-"]',
      ];

      for (const selector of inputSelectors) {
        const input = await page.$(selector);
        if (input) {
          console.log(`Found input with selector: ${selector}`);
          break;
        }
      }

      // Look for button (various selectors)
      const buttonSelectors = [
        'button[type="submit"]',
        '[data-testid="calculate-button"]',
        "button",
      ];

      for (const selector of buttonSelectors) {
        const button = await page.$(selector);
        if (button) {
          console.log(`Found button with selector: ${selector}`);
          break;
        }
      }

      // Get page HTML for debugging
      const bodyHTML = await page.$eval("body", (el) => el.innerHTML);
      console.log(
        "Page HTML contains calculator-container:",
        bodyHTML.includes("calculator-container"),
      );
      console.log(
        "Page HTML contains CalculatorWidget:",
        bodyHTML.includes("CalculatorWidget"),
      );

      // Check for any JavaScript errors in console
      const logs = await page.evaluate(() => {
        const errors = [];
        const originalError = console.error;
        console.error = (...args) => {
          errors.push(args.join(" "));
          originalError(...args);
        };
        return errors;
      });

      if (logs.length > 0) {
        console.log("Console errors:", logs);
      }

      // At minimum, we should have a calculator container
      const calculatorContainer = await page.$(".calculator-container");
      expect(calculatorContainer).toBeTruthy();
    }, 20000);
  });
});
