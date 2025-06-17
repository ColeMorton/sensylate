import fs from "node:fs";
import path from "node:path";

// Get feature flags from environment
const envToBoolean = (value) => value?.toLowerCase() === 'true';

const featureFlags = {
  authors_page: envToBoolean(process.env.PUBLIC_FEATURE_AUTHORS_PAGE) ?? true,
};

const PAGES_FOLDER = "src/pages";
const authorsDir = path.join(PAGES_FOLDER, "authors");

try {
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
