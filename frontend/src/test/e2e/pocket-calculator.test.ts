import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

describe("Pocket Calculator E2E Tests", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  beforeEach(async () => {
    // Navigate to pocket calculator before each test
    await e2eHelper.navigateToCalculator(page, "pocket-calculator");
    await e2eHelper.waitForCalculatorReady(page);
  }, 15000);

  describe("Navigation and Page Load", () => {
    it("should load the pocket calculator page successfully", async () => {
      expect(page.url()).toMatch(/\/calculators\/pocket-calculator$/);

      // Verify page title and meta information
      const title = await page.title();
      expect(title).toMatch(/Pocket Calculator|Basic Arithmetic Calculator/i);

      // Verify calculator widget is present
      const calculatorWidget = await page.$(
        '.calculator-container, [data-testid="calculator-widget"]',
      );
      expect(calculatorWidget).toBeTruthy();

      // Verify essential elements are present
      const input = await page.$(
        'input[type="text"], input[placeholder*="expression"]',
      );
      const button = await page.$(
        'button[type="submit"], button:contains("Calculate")',
      );

      expect(input).toBeTruthy();
      expect(button).toBeTruthy();
    });

    it("should be accessible from calculators listing page", async () => {
      // Navigate to calculators listing page
      await page.goto(`${e2eHelper.baseURL}/calculators`, {
        waitUntil: "networkidle0",
      });

      // Find and click the pocket calculator card
      await page.waitForSelector(
        'a[href*="pocket-calculator"], [data-calculator="pocket-calculator"]',
      );
      await page.click(
        'a[href*="pocket-calculator"], [data-calculator="pocket-calculator"]',
      );

      // Verify navigation to pocket calculator page
      await page.waitForURL(/\/calculators\/pocket-calculator$/);
      await e2eHelper.waitForCalculatorReady(page);

      const calculatorWidget = await page.$(
        '.calculator-container, [data-testid="calculator-widget"]',
      );
      expect(calculatorWidget).toBeTruthy();
    });
  });

  describe("Basic Arithmetic Operations", () => {
    const basicTests = [
      { expression: "2 + 3", expected: "5", description: "Simple addition" },
      {
        expression: "10 - 4",
        expected: "6",
        description: "Simple subtraction",
      },
      {
        expression: "6 * 7",
        expected: "42",
        description: "Simple multiplication",
      },
      { expression: "15 / 3", expected: "5", description: "Simple division" },
      {
        expression: "2.5 + 1.5",
        expected: "4",
        description: "Decimal addition",
      },
      {
        expression: "10.5 / 2.1",
        expected: "5",
        description: "Decimal division",
      },
    ];

    basicTests.forEach(({ expression, expected, description }) => {
      it(`should calculate ${description} correctly: ${expression} = ${expected}`, async () => {
        await e2eHelper.typeExpression(page, expression);
        await e2eHelper.clickCalculate(page);

        const result = await e2eHelper.getCalculationResult(page);
        expect(result).toBe(expected);

        // Verify no error message is shown
        const error = await e2eHelper.getErrorMessage(page);
        expect(error).toBeNull();
      });
    });
  });

  describe("Order of Operations (PEMDAS)", () => {
    const pemdas_tests = [
      {
        expression: "2 + 3 * 4",
        expected: "14",
        description: "Multiplication before addition",
      },
      {
        expression: "(2 + 3) * 4",
        expected: "20",
        description: "Parentheses override order",
      },
      {
        expression: "10 / 2 + 3",
        expected: "8",
        description: "Division before addition",
      },
      {
        expression: "2 * 3 + 4 * 5",
        expected: "26",
        description: "Multiple operations",
      },
      {
        expression: "(5 + 3) / (4 - 2)",
        expected: "4",
        description: "Complex parentheses",
      },
      {
        expression: "2 + 3 * 4 - 1",
        expected: "13",
        description: "Mixed operations",
      },
    ];

    pemdas_tests.forEach(({ expression, expected, description }) => {
      it(`should follow PEMDAS: ${description}`, async () => {
        await e2eHelper.typeExpression(page, expression);
        await e2eHelper.clickCalculate(page);

        const result = await e2eHelper.getCalculationResult(page);
        expect(result).toBe(expected);
      });
    });
  });

  describe("Number Formatting", () => {
    it("should format large numbers with commas", async () => {
      await e2eHelper.typeExpression(page, "999999 + 1");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      // Accept various formatting (1,000,000 or 1000000)
      expect(result).toMatch(/1[,]?000[,]?000/);
    });

    it("should handle decimal precision correctly", async () => {
      await e2eHelper.typeExpression(page, "1 / 3");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      expect(result).toMatch(/0\.333/); // Should show reasonable precision
    });
  });

  describe("Error Handling", () => {
    const errorTests = [
      { expression: "2 +", description: "Incomplete expression" },
      { expression: "2 ++ 3", description: "Invalid operators" },
      { expression: "abc + 123", description: "Invalid characters" },
      { expression: "((2 + 3)", description: "Mismatched parentheses" },
      { expression: "2 + 3)", description: "Extra closing parenthesis" },
      { expression: "", description: "Empty expression" },
    ];

    errorTests.forEach(({ expression, description }) => {
      it(`should handle error case: ${description}`, async () => {
        if (expression) {
          await e2eHelper.typeExpression(page, expression);
        }
        await e2eHelper.clickCalculate(page);

        const error = await e2eHelper.getErrorMessage(page);
        expect(error).toBeTruthy();
        expect(error).not.toBe("");

        // Verify no result is shown when there's an error
        const result = await e2eHelper.getCalculationResult(page);
        expect(result).toBeNull();
      });
    });

    it("should clear error message when typing new expression", async () => {
      // First create an error
      await e2eHelper.typeExpression(page, "invalid + expression");
      await e2eHelper.clickCalculate(page);

      let error = await e2eHelper.getErrorMessage(page);
      expect(error).toBeTruthy();

      // Now type a valid expression
      await e2eHelper.typeExpression(page, "2 + 3");

      // Error should clear (or at least not interfere with new calculation)
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      expect(result).toBe("5");

      error = await e2eHelper.getErrorMessage(page);
      expect(error).toBeNull();
    });
  });

  describe("User Interactions", () => {
    it("should calculate when pressing Enter key", async () => {
      await e2eHelper.typeExpression(page, "5 + 7");
      await e2eHelper.pressEnterToCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      expect(result).toBe("12");
    });

    it("should reset calculator state when reset button is clicked", async () => {
      // First perform a calculation
      await e2eHelper.typeExpression(page, "10 + 20");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      expect(result).toBe("30");

      // Click reset
      await e2eHelper.clickReset(page);

      // Verify input is cleared
      const inputValue = await page.$eval(
        'input[type="text"], input[placeholder*="expression"]',
        (el: any) => el.value,
      );
      expect(inputValue).toBe("");
    });

    it("should maintain focus on input field during interaction", async () => {
      const inputSelector =
        'input[type="text"], input[placeholder*="expression"]';

      await page.focus(inputSelector);
      await page.keyboard.type("2 + 2");

      // Verify input has focus and content
      const isFocused = await page.$eval(
        inputSelector,
        (el) => el === document.activeElement,
      );
      expect(isFocused).toBe(true);

      const inputValue = await page.$eval(inputSelector, (el: any) => el.value);
      expect(inputValue).toBe("2 + 2");
    });
  });

  describe("Mobile Responsiveness", () => {
    beforeEach(async () => {
      // Set mobile viewport
      await page.setViewport({ width: 375, height: 667 });
      await e2eHelper.navigateToCalculator(page, "pocket-calculator");
      await e2eHelper.waitForCalculatorReady(page);
    });

    afterEach(async () => {
      // Reset to desktop viewport
      await page.setViewport({ width: 1280, height: 720 });
    });

    it("should be fully functional on mobile viewport", async () => {
      // Verify calculator is visible and interactive on mobile
      const calculatorWidget = await page.$(
        '.calculator-container, [data-testid="calculator-widget"]',
      );
      expect(calculatorWidget).toBeTruthy();

      // Test touch interaction
      await e2eHelper.typeExpression(page, "3 + 4");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      expect(result).toBe("7");
    });
  });

  describe("Performance", () => {
    it("should calculate simple expressions quickly", async () => {
      const startTime = performance.now();

      await e2eHelper.typeExpression(page, "123 + 456");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      const endTime = performance.now();

      expect(result).toBe("579");
      expect(endTime - startTime).toBeLessThan(1000); // Should complete within 1 second
    });

    it("should handle complex expressions within reasonable time", async () => {
      const startTime = performance.now();

      await e2eHelper.typeExpression(page, "(123 + 456) * (789 - 321) / 2");
      await e2eHelper.clickCalculate(page);

      const result = await e2eHelper.getCalculationResult(page);
      const endTime = performance.now();

      expect(result).toBeTruthy(); // Just verify we got a result
      expect(endTime - startTime).toBeLessThan(2000); // Should complete within 2 seconds
    });
  });
});
