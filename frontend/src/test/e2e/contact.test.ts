import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Page } from "puppeteer";
import { setupE2ETest, cleanupE2ETest, e2eHelper } from "./setup";

describe("Contact Page E2E Tests", () => {
  let page: Page;

  beforeAll(async () => {
    const context = await setupE2ETest();
    page = context.page;
  }, 30000);

  afterAll(async () => {
    await cleanupE2ETest();
  }, 10000);

  describe("Contact Form Submission", () => {
    it("should load the contact page successfully", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      const title = await page.title();
      expect(title).toMatch(/contact/i);

      // Should see the contact form
      const contactForm = await page.$("form");
      expect(contactForm).toBeTruthy();
    }, 15000);

    it("should have all required form fields", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Check for name field
      const nameField = await page.$("#name");
      expect(nameField).toBeTruthy();

      // Check for email field
      const emailField = await page.$("#email");
      expect(emailField).toBeTruthy();

      // Check for message field
      const messageField = await page.$("#message");
      expect(messageField).toBeTruthy();

      // Check for submit button
      const submitButton = await page.$('button[type="submit"]');
      expect(submitButton).toBeTruthy();
    }, 15000);

    it("should fill out and submit the contact form", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill out the form fields
      await page.waitForSelector("#name", { timeout: 5000 });
      await page.type("#name", "John Doe");

      await page.waitForSelector("#email", { timeout: 5000 });
      await page.type("#email", "cole.morton@hotmail.com");

      await page.waitForSelector("#message", { timeout: 5000 });
      await page.type(
        "#message",
        "This is a test message from the E2E test suite. Testing the contact form submission flow.",
      );

      // Take a screenshot before submission
      await e2eHelper.takeScreenshot(page, "contact-form-filled");

      // Verify form fields are filled correctly
      const nameValue = await page.$eval("#name", (el: any) => el.value);
      const emailValue = await page.$eval("#email", (el: any) => el.value);
      const messageValue = await page.$eval("#message", (el: any) => el.value);

      expect(nameValue).toBe("John Doe");
      expect(emailValue).toBe("cole.morton@hotmail.com");
      expect(messageValue).toBe(
        "This is a test message from the E2E test suite. Testing the contact form submission flow.",
      );

      // For Netlify forms, we'll intercept the submission to prevent actual submission during testing
      // but verify that the form would be properly submitted
      await page.evaluate(() => {
        const form = document.querySelector("form");
        if (form) {
          form.addEventListener("submit", (e) => {
            e.preventDefault();
            // Add a marker to indicate submission was attempted
            document.body.setAttribute("data-form-submitted", "true");
            document.body.setAttribute(
              "data-form-method",
              form.getAttribute("method") || "",
            );
            document.body.setAttribute(
              "data-netlify-enabled",
              form.hasAttribute("data-netlify") ? "true" : "false",
            );
          });
        }
      });

      // Submit the form
      const submitButton = await page.$('button[type="submit"]');
      await submitButton?.click();

      // Wait for form submission to be intercepted
      await page.waitForFunction(
        () => document.body.getAttribute("data-form-submitted") === "true",
        { timeout: 5000 },
      );

      // Verify the form submission was properly configured for Netlify
      const formSubmitted = await page.evaluate(() =>
        document.body.getAttribute("data-form-submitted"),
      );
      const formMethod = await page.evaluate(() =>
        document.body.getAttribute("data-form-method"),
      );
      const netlifyEnabled = await page.evaluate(() =>
        document.body.getAttribute("data-netlify-enabled"),
      );

      expect(formSubmitted).toBe("true");
      expect(formMethod).toBe("POST");
      expect(netlifyEnabled).toBe("true");

      // Take a screenshot after submission attempt
      await e2eHelper.takeScreenshot(page, "contact-form-submitted");
    }, 20000);

    it("should validate required fields", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Try to submit empty form
      const submitButton = await page.$('button[type="submit"]');
      await submitButton?.click();

      // Check if browser validation is triggered (HTML5 validation)
      const nameField = await page.$("#name");
      const nameValid = await nameField?.evaluate(
        (el: any) => el.validity.valid,
      );

      // Since the name field is required but empty, it should be invalid
      expect(nameValid).toBe(false);
    }, 15000);

    it("should validate email format", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill name and message but put invalid email
      await page.type("#name", "Test User");
      await page.type("#email", "invalid-email");
      await page.type("#message", "Test message");

      // Try to submit
      const submitButton = await page.$('button[type="submit"]');
      await submitButton?.click();

      // Check if email validation is triggered
      const emailField = await page.$("#email");
      const emailValid = await emailField?.evaluate(
        (el: any) => el.validity.valid,
      );

      // Invalid email format should make the field invalid
      expect(emailValid).toBe(false);
    }, 15000);

    it("should accept valid form data", async () => {
      await page.goto(`${e2eHelper.baseURL}/contact`, {
        waitUntil: "networkidle0",
      });

      // Fill all fields with valid data
      await page.type("#name", "Jane Smith");
      await page.type("#email", "cole.morton@hotmail.com");
      await page.type(
        "#message",
        "This is a valid test message with proper content.",
      );

      // Check that all fields are valid
      const nameValid = await page.$eval(
        "#name",
        (el: any) => el.validity.valid,
      );
      const emailValid = await page.$eval(
        "#email",
        (el: any) => el.validity.valid,
      );
      const messageValid = await page.$eval(
        "#message",
        (el: any) => el.validity.valid,
      );

      expect(nameValid).toBe(true);
      expect(emailValid).toBe(true);
      expect(messageValid).toBe(true);

      // Verify form can be submitted (would submit if action was configured)
      const form = await page.$("form");
      const formValid = await form?.evaluate((el: any) => el.checkValidity());
      expect(formValid).toBe(true);
    }, 15000);
  });
});
