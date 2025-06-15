import fs from "node:fs";
import path from "node:path";

// Get feature flags from environment
const envToBoolean = (value) => value?.toLowerCase() === 'true';

const featureFlags = {
  not_found_page: envToBoolean(process.env.PUBLIC_FEATURE_NOT_FOUND_PAGE) ?? true,
  authors_page: envToBoolean(process.env.PUBLIC_FEATURE_AUTHORS_PAGE) ?? true,
};

// Template content for 404 page
const content404 = `---
import Base from "@/layouts/Base.astro";
---

<Base title="Page Not Found">
  <section class="section-sm text-center">
    <div class="container">
      <div class="row justify-center">
        <div class="sm:col-10 md:col-8 lg:col-6">
          <span
            class="text-[8rem] block font-bold text-text-dark dark:text-darkmode-text-dark"
          >
            404
          </span>
          <h1 class="h2 mb-4">Page not found</h1>
          <div class="content">
            <p>
              The page you are looking for might have been removed, had its name
              changed, or is temporarily unavailable.
            </p>
          </div>
          <a href="/" class="btn btn-primary mt-8">Back to home</a>
        </div>
      </div>
    </div>
  </section>
</Base>`;

const PAGES_FOLDER = "src/pages";
const page404Path = path.join(PAGES_FOLDER, "404.astro");
const authorsIndexPath = path.join(PAGES_FOLDER, "authors", "index.astro");
const authorsSinglePath = path.join(PAGES_FOLDER, "authors", "[single].astro");
const authorsDir = path.join(PAGES_FOLDER, "authors");

try {
  // Handle 404 page
  if (featureFlags.not_found_page) {
    // Create 404.astro if feature is enabled
    fs.writeFileSync(page404Path, content404);
    console.log("✅ Created 404.astro (feature enabled)");
  } else {
    // Remove 404.astro if feature is disabled
    if (fs.existsSync(page404Path)) {
      fs.unlinkSync(page404Path);
      console.log("🗑️  Removed 404.astro (feature disabled)");
    }
  }

  // Handle authors pages
  if (featureFlags.authors_page) {
    // Ensure authors directory exists (it should already exist)
    if (!fs.existsSync(authorsDir)) {
      // Restore from backup if needed
      if (fs.existsSync(path.join(PAGES_FOLDER, "_authors.backup"))) {
        fs.cpSync(path.join(PAGES_FOLDER, "_authors.backup"), authorsDir, { recursive: true });
        console.log("✅ Restored authors pages (feature enabled)");
      }
    }
  } else {
    // Remove authors directory if feature is disabled
    if (fs.existsSync(authorsDir)) {
      fs.rmSync(authorsDir, { recursive: true, force: true });
      console.log("🗑️  Removed authors pages (feature disabled)");
    }
  }
} catch (err) {
  console.error("Error in page generation:", err);
}