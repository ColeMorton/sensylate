import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

describe("Theme Debug Test", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  it("should debug the theme issue step by step", async () => {
    console.log("=== Starting theme debug test ===");

    // Step 1: Load homepage and set light mode
    await page.goto(`${e2eHelper.baseURL}/`, { waitUntil: "networkidle0" });
    await new Promise((resolve) => setTimeout(resolve, 2000));

    await page.evaluate(() => {
      localStorage.setItem("theme", "light");
      document.documentElement.classList.remove("dark");
    });
    await page.reload({ waitUntil: "networkidle0" });
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const homepageState = await page.evaluate(() => {
      const html = document.documentElement;
      const body = document.body;
      const styles = window.getComputedStyle(body);
      return {
        hasDarkClass: html.classList.contains("dark"),
        storedTheme: localStorage.getItem("theme"),
        backgroundColor: styles.backgroundColor,
        htmlClasses: html.className,
        bodyClasses: body.className,
      };
    });

    console.log("Homepage state:", homepageState);
    await e2eHelper.takeScreenshot(page, "debug-homepage-light");

    expect(homepageState.hasDarkClass).toBe(false);
    expect(homepageState.storedTheme).toBe("light");

    // Step 2: Navigate to about page
    console.log("=== Navigating to about page ===");
    await page.goto(`${e2eHelper.baseURL}/about`, {
      waitUntil: "networkidle0",
    });
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const aboutState = await page.evaluate(() => {
      const html = document.documentElement;
      const body = document.body;
      const styles = window.getComputedStyle(body);
      return {
        hasDarkClass: html.classList.contains("dark"),
        storedTheme: localStorage.getItem("theme"),
        backgroundColor: styles.backgroundColor,
        htmlClasses: html.className,
        bodyClasses: body.className,
      };
    });

    console.log("About page state:", aboutState);
    await e2eHelper.takeScreenshot(page, "debug-about-light");

    // THE BUG: These should be the same as homepage
    console.log("=== Comparing states ===");
    console.log("Homepage background:", homepageState.backgroundColor);
    console.log("About background:", aboutState.backgroundColor);
    console.log("Expected: both should be white (rgb(255, 255, 255))");

    expect(aboutState.hasDarkClass).toBe(false);
    expect(aboutState.storedTheme).toBe("light");
    expect(aboutState.backgroundColor).toBe(homepageState.backgroundColor);
  }, 30000);
});
