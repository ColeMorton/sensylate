import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

/**
 * CONTACT FORM VISUAL REGRESSION TESTS
 *
 * These tests capture screenshots of the contact form in different states
 * to prevent visual regressions in styling and layout.
 *
 * Screenshots are saved with timestamps for manual review.
 * To update baselines, set UPDATE_CONTACT_BASELINES=true
 */

describe("Contact Form - Visual Regression", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  describe("Page Layout Screenshots", () => {
    it("should capture contact page initial state - light mode", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Ensure light mode
      await page.evaluate(() => {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
      });

      // Wait for theme to apply
      await e2eHelper.sleep(1000);

      await e2eHelper.takeScreenshot(page, "contact-page-initial-light");
    }, 15000);

    it("should capture contact page initial state - dark mode", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Ensure dark mode
      await page.evaluate(() => {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
      });

      // Wait for theme to apply
      await e2eHelper.sleep(1000);

      await e2eHelper.takeScreenshot(page, "contact-page-initial-dark");
    }, 15000);
  });

  describe("Form State Screenshots", () => {
    it("should capture form with validation errors", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Try to submit empty form to trigger validation
      const submitButton = await page.$('button[type="submit"]');
      await submitButton?.click();

      // Wait for validation to appear
      await e2eHelper.sleep(500);

      await e2eHelper.takeScreenshot(page, "contact-form-validation-errors");
    }, 15000);

    it("should capture form partially filled", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill some fields to show different states
      await page.type("#name", "John Doe");
      await page.type("#email", "john.doe@example.com");
      await page.select("#inquiry-type", "technical-collaboration");

      // Focus on message field to show focus state
      await page.focus("#message");

      await e2eHelper.takeScreenshot(page, "contact-form-partially-filled");
    }, 15000);

    it("should capture form completely filled", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill all fields
      await page.type("#name", "Jane Smith");
      await page.type("#email", "jane.smith@company.com");
      await page.type("#organization", "Professional Testing Solutions Inc.");
      await page.select("#inquiry-type", "professional-opportunity");
      await page.type(
        "#message",
        "This is a comprehensive professional inquiry message that demonstrates the full form functionality with all fields properly filled out and ready for submission.",
      );

      await e2eHelper.takeScreenshot(page, "contact-form-completely-filled");
    }, 15000);
  });

  describe("Responsive Layout Screenshots", () => {
    it("should capture mobile layout", async () => {
      await page.setViewport({ width: 375, height: 667 }); // iPhone SE

      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill form to show mobile layout with content
      await page.type("#name", "Mobile User");
      await page.type("#email", "mobile@test.com");
      await page.select("#inquiry-type", "platform-inquiry");
      await page.type(
        "#message",
        "Testing mobile form layout and responsive design.",
      );

      await e2eHelper.takeScreenshot(page, "contact-form-mobile-375px");
    }, 15000);

    it("should capture tablet layout", async () => {
      await page.setViewport({ width: 768, height: 1024 }); // iPad

      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill form to show tablet layout
      await page.type("#name", "Tablet User");
      await page.type("#email", "tablet@test.com");
      await page.type("#organization", "Tablet Testing Corp");
      await page.select("#inquiry-type", "consulting");
      await page.type(
        "#message",
        "Testing tablet form layout and responsive design with proper spacing and field sizing.",
      );

      await e2eHelper.takeScreenshot(page, "contact-form-tablet-768px");
    }, 15000);

    it("should capture desktop layout", async () => {
      await page.setViewport({ width: 1920, height: 1080 }); // Desktop FHD

      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill form to show desktop layout
      await page.type("#name", "Desktop Professional User");
      await page.type("#email", "desktop.professional@enterprise.com");
      await page.type(
        "#organization",
        "Enterprise Desktop Solutions Corporation",
      );
      await page.select("#inquiry-type", "technical-collaboration");
      await page.type(
        "#message",
        "Comprehensive desktop testing message that demonstrates the full form functionality at desktop resolution with proper spacing, typography, and professional presentation suitable for enterprise use.",
      );

      await e2eHelper.takeScreenshot(page, "contact-form-desktop-1920px");
    }, 15000);
  });

  describe("Theme Comparison Screenshots", () => {
    it("should capture form styling comparison across themes", async () => {
      // Reset to standard desktop viewport
      await page.setViewport({ width: 1280, height: 720 });

      // Light theme filled form
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      await page.evaluate(() => {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
      });

      await e2eHelper.sleep(500);

      await page.type("#name", "Theme Comparison User");
      await page.type("#email", "theme@comparison.com");
      await page.type("#organization", "Visual Regression Testing Corp");
      await page.select("#inquiry-type", "platform-inquiry");
      await page.type(
        "#message",
        "This message tests the visual consistency of form styling across light and dark themes.",
      );

      await e2eHelper.takeScreenshot(page, "contact-form-theme-light");

      // Switch to dark theme (same form content)
      await page.evaluate(() => {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
      });

      await e2eHelper.sleep(500);

      await e2eHelper.takeScreenshot(page, "contact-form-theme-dark");
    }, 20000);
  });

  describe("Success Page Screenshots", () => {
    it("should capture success page in light mode", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact-success`, {
        waitUntil: "networkidle0",
      });

      await page.evaluate(() => {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("theme", "light");
      });

      await e2eHelper.sleep(500);

      await e2eHelper.takeScreenshot(page, "contact-success-page-light");
    }, 15000);

    it("should capture success page in dark mode", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact-success`, {
        waitUntil: "networkidle0",
      });

      await page.evaluate(() => {
        document.documentElement.classList.add("dark");
        localStorage.setItem("theme", "dark");
      });

      await e2eHelper.sleep(500);

      await e2eHelper.takeScreenshot(page, "contact-success-page-dark");
    }, 15000);
  });

  describe("Visual Regression Validation", () => {
    it("should provide visual regression checklist", async () => {
      console.log(`
🎨 CONTACT FORM VISUAL REGRESSION CHECKLIST

Screenshots Generated:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Mobile (375px): Form layout and responsiveness
📟 Tablet (768px): Form layout at tablet breakpoint
🖥️  Desktop (1920px): Full desktop form presentation
🌞 Light Theme: Professional form styling and colors
🌙 Dark Theme: Dark mode form styling and contrast
✅ Success Page: Professional confirmation styling

Visual Elements to Verify:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Form container styling (background, border, shadow)
✓ Professional form title and typography hierarchy
✓ Field labels and required asterisks styling
✓ Input field styling (border, padding, focus states)
✓ Dropdown styling and options presentation
✓ Button styling and hover/focus states
✓ Success page styling and visual hierarchy
✓ Responsive behavior across breakpoints
✓ Theme consistency (light/dark mode)
✓ Professional color scheme and branding
✓ Typography consistency with site standards
✓ Proper spacing and visual rhythm

Regression Prevention:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Compare screenshots against previous versions
• Verify form maintains professional appearance
• Check responsive behavior at all breakpoints
• Ensure theme switching works correctly
• Validate accessibility of form styling
• Confirm button and interactive elements are clear
• Verify success page maintains consistent branding

Manual Review Process:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Review all generated screenshots
2. Compare against expected professional styling
3. Verify no visual regressions in form presentation
4. Check that styling matches site design standards
5. Validate responsive behavior across device sizes
6. Confirm theme consistency and proper contrast
7. Ensure form maintains enterprise-quality appearance
      `);

      expect(true).toBe(true); // Pass - this is a documentation test
    });
  });
});
