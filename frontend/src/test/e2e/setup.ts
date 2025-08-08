import puppeteer, { type Browser, type Page } from "puppeteer";
import { setTimeout } from "node:timers/promises";

export interface TestContext {
  browser: Browser;
  page: Page;
  baseURL: string;
}

export class E2ETestHelper {
  private browser: Browser | null = null;
  private pages: Page[] = [];

  readonly baseURL = process.env.E2E_BASE_URL || "http://localhost:4321";

  async setupBrowser(): Promise<Browser> {
    if (this.browser) {
      return this.browser;
    }

    this.browser = await puppeteer.launch({
      headless: process.env.CI ? true : "new", // Use new headless mode, full browser in dev
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--no-first-run",
        "--no-zygote",
        "--disable-gpu",
      ],
      defaultViewport: {
        width: 1280,
        height: 720,
      },
    });

    return this.browser;
  }

  async createPage(): Promise<Page> {
    const browser = await this.setupBrowser();
    const page = await browser.newPage();

    // Enhanced error handling and logging
    page.on("console", (msg) => {
      if (msg.type() === "error") {
        console.error("Browser console error:", msg.text());
      }
    });

    page.on("pageerror", (error) => {
      console.error("Page error:", error.message);
    });

    // Set reasonable timeouts
    page.setDefaultTimeout(10000);
    page.setDefaultNavigationTimeout(15000);

    this.pages.push(page);
    return page;
  }

  // Helper function to replace page.waitForTimeout
  static async sleep(milliseconds: number): Promise<void> {
    await setTimeout(milliseconds);
  }

  // Helper function for request interception (replaces page.route)
  static async setupRequestInterception(
    page: Page, 
    urlPattern: string, 
    handler: (request: any) => void
  ): Promise<void> {
    await page.setRequestInterception(true);
    page.on('request', (request) => {
      if (request.url().includes(urlPattern) || new RegExp(urlPattern).test(request.url())) {
        handler(request);
      } else {
        request.continue();
      }
    });
  }

  async navigateToCalculator(
    page: Page,
    calculatorId: string = "pocket-calculator",
  ): Promise<void> {
    const url = `${this.baseURL}/calculators/${calculatorId}`;

    await page.goto(url, {
      waitUntil: "networkidle0",
      timeout: 15000,
    });

    // Wait for React hydration to complete
    await page.waitForSelector(
      '[data-testid="calculator-widget"], .calculator-container',
      {
        timeout: 10000,
      },
    );

    // Additional wait for React component to be interactive
    await page.waitForFunction(
      () => {
        const input = document.querySelector(
          'input[type="text"], input[placeholder*="expression"]',
        );
        return input && !input.hasAttribute("disabled");
      },
      { timeout: 5000 },
    );
  }

  async waitForCalculatorReady(page: Page): Promise<void> {
    // Wait for calculator widget to be fully loaded and interactive
    await page.waitForFunction(
      () => {
        const widget = document.querySelector(
          '.calculator-container, [data-testid="calculator-widget"]',
        );
        const input = document.querySelector(
          'input[type="text"], input[placeholder*="expression"]',
        );
        const button = document.querySelector(
          'button[type="submit"], [data-testid="calculate-button"]',
        );

        return widget && input && button && !input.hasAttribute("disabled");
      },
      { timeout: 10000 },
    );
  }

  async typeExpression(page: Page, expression: string): Promise<void> {
    const inputSelector =
      'input[type="text"], input[placeholder*="expression"], input[name="expression"]';

    await page.waitForSelector(inputSelector, { timeout: 5000 });

    // Clear existing content and type new expression
    await page.click(inputSelector, { clickCount: 3 }); // Select all
    await page.type(inputSelector, expression);

    // Verify the expression was typed correctly
    const inputValue = await page.$eval(inputSelector, (el: any) => el.value);
    if (inputValue !== expression) {
      throw new Error(
        `Expression not typed correctly. Expected: "${expression}", Got: "${inputValue}"`,
      );
    }
  }

  async clickCalculate(page: Page): Promise<void> {
    const buttonSelector =
      'button[type="submit"], [data-testid="calculate-button"]';

    await page.waitForSelector(buttonSelector, { timeout: 5000 });
    await page.click(buttonSelector);

    // Wait for calculation to complete (either result or error)
    await page.waitForFunction(
      () => {
        const result = document.querySelector(
          '[data-testid="result-value-result"], [data-testid="result-value-formattedResult"], [data-testid="results-container"]',
        );
        const error = document.querySelector(
          '[data-testid="error"], .error, .error-message',
        );
        return result || error;
      },
      { timeout: 5000 },
    );
  }

  async getCalculationResult(page: Page): Promise<string | null> {
    const resultSelectors = [
      '[data-testid="result-value-result"]',
      '[data-testid="result-value-formattedResult"]',
      '[data-testid="result"]',
      ".result",
      ".output",
    ];

    for (const selector of resultSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          return await element.evaluate((el) => el.textContent?.trim() || null);
        }
      } catch {
        continue;
      }
    }

    return null;
  }

  async getErrorMessage(page: Page): Promise<string | null> {
    const errorSelectors = [
      '[data-testid="error"]',
      ".error",
      ".error-message",
      '[role="alert"]',
    ];

    for (const selector of errorSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          return await element.evaluate((el) => el.textContent?.trim() || null);
        }
      } catch {
        continue;
      }
    }

    return null;
  }

  async pressEnterToCalculate(page: Page): Promise<void> {
    const inputSelector =
      'input[type="text"], input[placeholder*="expression"], input[name="expression"]';

    await page.focus(inputSelector);
    await page.keyboard.press("Enter");

    // Wait for calculation to complete
    await page.waitForFunction(
      () => {
        const result = document.querySelector(
          '[data-testid="result"], .result, .output',
        );
        const error = document.querySelector(
          '[data-testid="error"], .error, .error-message',
        );
        return result || error;
      },
      { timeout: 5000 },
    );
  }

  async clickReset(page: Page): Promise<void> {
    const resetSelector = '[data-testid="reset-button"], button[type="reset"]';

    try {
      await page.waitForSelector(resetSelector, { timeout: 3000 });
      await page.click(resetSelector);

      // Wait for reset to complete
      await page.waitForFunction(
        () => {
          const input = document.querySelector(
            'input[type="text"], input[placeholder*="expression"]',
          ) as HTMLInputElement;
          return input && input.value === "";
        },
        { timeout: 3000 },
      );
    } catch {
      // Reset button might not exist, that's okay
    }
  }

  async takeScreenshot(page: Page, name: string): Promise<void> {
    if (process.env.E2E_SCREENSHOTS !== "false") {
      const fs = await import("fs");
      const path = await import("path");

      // Ensure screenshots directory exists
      const screenshotDir = "./src/test/e2e/screenshots";
      if (!fs.existsSync(screenshotDir)) {
        fs.mkdirSync(screenshotDir, { recursive: true });
      }

      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const filename = path.join(screenshotDir, `${name}-${timestamp}.png`);

      await page.screenshot({
        path: filename,
        fullPage: true,
      });
    }
  }

  async cleanup(): Promise<void> {
    // Close all pages
    for (const page of this.pages) {
      if (!page.isClosed()) {
        await page.close();
      }
    }
    this.pages = [];

    // Close browser
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}

// Global test helper instance
export const e2eHelper = new E2ETestHelper();

// Utility function for test setup
export async function setupE2ETest(): Promise<TestContext> {
  const browser = await e2eHelper.setupBrowser();
  const page = await e2eHelper.createPage();

  return {
    browser,
    page,
    baseURL: e2eHelper.baseURL,
  };
}

// Utility function for test cleanup
export async function cleanupE2ETest(): Promise<void> {
  await e2eHelper.cleanup();
}
