import puppeteer, { type Browser, type Page } from "puppeteer";
import { spawn, type ChildProcess } from "child_process";
import { setTimeout } from "node:timers/promises";

export interface E2ETestContext {
  browser: Browser;
  page: Page;
  baseURL: string;
  devServer?: ChildProcess;
}

export class PhotoBoothE2EHelper {
  private browser: Browser | null = null;
  private pages: Page[] = [];
  private devServer: ChildProcess | null = null;

  readonly baseURL = process.env.E2E_BASE_URL || "http://localhost:4321";

  // Start development server if needed
  async startDevServer(): Promise<void> {
    if (process.env.CI || process.env.E2E_NO_DEV_SERVER) {
      return; // Skip in CI or when explicitly disabled
    }

    console.log("Starting development server...");

    this.devServer = spawn("yarn", ["dev"], {
      cwd: process.cwd(),
      shell: true,
      detached: false,
    });

    // Wait for server to be ready
    let attempts = 0;
    const maxAttempts = 30;

    while (attempts < maxAttempts) {
      try {
        const response = await fetch(this.baseURL);
        if (response.ok) {
          console.log("Development server is ready");
          return;
        }
      } catch (e) {
        // Server not ready yet
      }

      await setTimeout(1000);
      attempts++;
    }

    throw new Error("Development server failed to start");
  }

  async setupBrowser(): Promise<Browser> {
    if (this.browser) {
      return this.browser;
    }

    this.browser = await puppeteer.launch({
      headless: process.env.CI ? true : "new",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
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

    // Enhanced error handling
    page.on("console", (msg) => {
      if (
        msg.type() === "error" &&
        !msg.text().includes("Failed to load resource")
      ) {
        console.error("Browser console error:", msg.text());
      }
    });

    page.on("pageerror", (error) => {
      console.error("Page error:", error.message);
    });

    // Set timeouts
    page.setDefaultTimeout(10000);
    page.setDefaultNavigationTimeout(15000);

    this.pages.push(page);
    return page;
  }

  // Navigate to photo booth page with optional parameters
  async navigateToPhotoBooth(
    page: Page,
    params?: Record<string, string>,
  ): Promise<void> {
    const searchParams = new URLSearchParams(params);
    const url = `${this.baseURL}/photo-booth${searchParams.toString() ? "?" + searchParams.toString() : ""}`;

    await page.goto(url, {
      waitUntil: "networkidle0",
      timeout: 15000,
    });
  }

  // Wait for photo booth to be ready
  async waitForPhotoBoothReady(page: Page, timeout = 20000): Promise<void> {
    await page.waitForSelector(".photo-booth-ready", { timeout });
  }

  // Take screenshot with consistent naming
  async takeScreenshot(page: Page, name: string): Promise<string> {
    const fs = await import("fs");
    const path = await import("path");

    const screenshotDir = "./src/test/photo-booth/e2e/screenshots";
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const filename = path.join(screenshotDir, `${name}-${timestamp}.png`);

    await page.screenshot({
      path: filename,
      fullPage: true,
      type: "png",
    });

    return filename;
  }

  // Hide controls for clean export screenshots
  async hideControls(page: Page): Promise<void> {
    await page.evaluate(() => {
      const controls = document.querySelectorAll(".photo-booth-controls");
      controls.forEach((control) => {
        (control as HTMLElement).style.display = "none";
        (control as HTMLElement).style.visibility = "hidden";
      });

      // Also hide any dev toolbar elements
      const devElements = document.querySelectorAll(
        "[data-astro-dev-toolbar], astro-dev-toolbar, #dev-toolbar-root",
      );
      devElements.forEach((element) => {
        (element as HTMLElement).style.display = "none";
        (element as HTMLElement).style.visibility = "hidden";
      });
    });
  }

  // Clean up resources
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

    // Stop dev server
    if (this.devServer) {
      this.devServer.kill();
      this.devServer = null;
    }
  }

  // Helper to sleep
  static async sleep(ms: number): Promise<void> {
    await setTimeout(ms);
  }
}

// Global test helper instance
export const photoBoothE2EHelper = new PhotoBoothE2EHelper();

// Setup function for tests
export async function setupPhotoBoothE2E(): Promise<E2ETestContext> {
  await photoBoothE2EHelper.startDevServer();
  const browser = await photoBoothE2EHelper.setupBrowser();
  const page = await photoBoothE2EHelper.createPage();

  return {
    browser,
    page,
    baseURL: photoBoothE2EHelper.baseURL,
    devServer: photoBoothE2EHelper.devServer || undefined,
  };
}

// Cleanup function for tests
export async function cleanupPhotoBoothE2E(): Promise<void> {
  await photoBoothE2EHelper.cleanup();
}
