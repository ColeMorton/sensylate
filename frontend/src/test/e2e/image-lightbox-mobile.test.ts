import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { e2eHelper, type TestContext } from "./setup";
import type { Page } from "puppeteer";

describe("Image Lightbox Mobile Behavior", () => {
  let context: TestContext;
  let page: Page;

  beforeEach(async () => {
    const browser = await e2eHelper.setupBrowser();
    page = await e2eHelper.createPage();
    context = {
      browser,
      page,
      baseURL: e2eHelper.baseURL,
    };
  });

  afterEach(async () => {
    if (page && !page.isClosed()) {
      await page.close();
    }
  });

  it("should disable lightbox click behavior on mobile devices", async () => {
    // Set mobile viewport
    await page.setViewport({
      width: 375, // iPhone SE width
      height: 667, // iPhone SE height
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 2,
    });

    // Navigate to a blog post with images
    await page.goto(
      `${context.baseURL}/blog/smci-fundamental-analysis-20250623`,
      {
        waitUntil: "networkidle2",
        timeout: 15000,
      },
    );

    // Wait for React components to hydrate
    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Find the first image in the blog post
    const imageSelector = 'img[src*="/images/tradingview/SMCI_20250623.png"]';
    await page.waitForSelector(imageSelector, { timeout: 10000 });

    // Debug: Check actual window width detected by the component
    const windowWidth = await page.evaluate(() => window.innerWidth);
    console.log("Window width detected:", windowWidth);

    // Debug: Check image classes and attributes
    const imageData = await page.$eval(imageSelector, (img) => ({
      className: img.className,
      role: img.getAttribute("role"),
      tabIndex: img.tabIndex,
      ariaLabel: img.getAttribute("aria-label"),
    }));

    console.log("Image data:", imageData);

    // Check that the image doesn't have cursor-pointer class (indicating disabled click)
    expect(imageData.className).not.toContain("cursor-pointer");

    // Check that the image doesn't have role="button" (indicating disabled interaction)
    expect(imageData.role).toBeNull();

    // Check that tabIndex is -1 (indicating not focusable)
    expect(imageData.tabIndex).toBe(-1);

    // Verify that clicking the image doesn't open lightbox
    await page.click(imageSelector);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait a bit to see if lightbox opens

    // Check that no lightbox overlay is present
    const lightboxOverlay = await page.$(".yarl__root");
    expect(lightboxOverlay).toBeNull();

    // Take screenshot for verification
    await e2eHelper.takeScreenshot(page, "mobile-image-click-disabled");
  });

  it("should enable lightbox click behavior on desktop devices", async () => {
    // Set desktop viewport
    await page.setViewport({
      width: 1280,
      height: 720,
      isMobile: false,
      hasTouch: false,
      deviceScaleFactor: 1,
    });

    // Navigate to a blog post with images
    await page.goto(
      `${context.baseURL}/blog/smci-fundamental-analysis-20250623`,
      {
        waitUntil: "networkidle2",
        timeout: 15000,
      },
    );

    // Wait for React components to hydrate
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Find the first image in the blog post
    const imageSelector = 'img[src*="/images/tradingview/SMCI_20250623.png"]';
    await page.waitForSelector(imageSelector, { timeout: 10000 });

    // Check that the image has cursor-pointer class (indicating enabled click)
    const imageClasses = await page.$eval(
      imageSelector,
      (img) => img.className,
    );
    expect(imageClasses).toContain("cursor-pointer");

    // Check that the image has role="button" (indicating enabled interaction)
    const imageRole = await page.$eval(imageSelector, (img) =>
      img.getAttribute("role"),
    );
    expect(imageRole).toBe("button");

    // Check that tabIndex is 0 (indicating focusable)
    const tabIndex = await page.$eval(imageSelector, (img) => img.tabIndex);
    expect(tabIndex).toBe(0);

    // Verify that clicking the image opens lightbox
    await page.click(imageSelector);
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for lightbox to open

    // Check that lightbox overlay is present
    const lightboxOverlay = await page.$(
      '.yarl__root, [class*="lightbox"], [class*="overlay"]',
    );
    expect(lightboxOverlay).not.toBeNull();

    // Verify navigation buttons are not present (our desktop fix)
    const prevButton = await page.$('.yarl__button_prev, [class*="prev"]');
    const nextButton = await page.$('.yarl__button_next, [class*="next"]');
    expect(prevButton).toBeNull();
    expect(nextButton).toBeNull();

    // Take screenshot for verification
    await e2eHelper.takeScreenshot(page, "desktop-image-lightbox-no-nav");

    // Close lightbox by pressing Escape
    await page.keyboard.press("Escape");
    await new Promise((resolve) => setTimeout(resolve, 500));
  });

  it("should handle viewport resize correctly", async () => {
    // Start with desktop viewport
    await page.setViewport({
      width: 1280,
      height: 720,
      isMobile: false,
      hasTouch: false,
      deviceScaleFactor: 1,
    });

    // Navigate to a blog post with images
    await page.goto(
      `${context.baseURL}/blog/smci-fundamental-analysis-20250623`,
      {
        waitUntil: "networkidle2",
        timeout: 15000,
      },
    );

    // Wait for React components to hydrate
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const imageSelector = 'img[src*="/images/tradingview/SMCI_20250623.png"]';
    await page.waitForSelector(imageSelector, { timeout: 10000 });

    // Verify desktop behavior first
    let imageClasses = await page.$eval(imageSelector, (img) => img.className);
    expect(imageClasses).toContain("cursor-pointer");

    // Resize to mobile
    await page.setViewport({
      width: 375,
      height: 667,
      isMobile: true,
      hasTouch: true,
      deviceScaleFactor: 2,
    });

    // Wait for resize handler to trigger
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Verify mobile behavior after resize
    imageClasses = await page.$eval(imageSelector, (img) => img.className);
    expect(imageClasses).not.toContain("cursor-pointer");

    // Take screenshot for verification
    await e2eHelper.takeScreenshot(page, "mobile-after-resize");
  });
});
