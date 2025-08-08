// Centralized test data for photo-booth tests

export const testURLParams = {
  default: {},
  portraitMode: {
    dashboard: "portfolio_history_portrait",
    mode: "light",
    aspect_ratio: "3:4",
    format: "png",
    dpi: "300",
    scale: "3",
  },
  darkMode: {
    dashboard: "portfolio_history_portrait",
    mode: "dark",
    aspect_ratio: "16:9",
  },
  invalidParams: {
    dashboard: "invalid_dashboard",
    mode: "invalid_mode",
    aspect_ratio: "invalid_ratio",
  },
};

export const testAspectRatios = [
  { id: "16:9", name: "Widescreen", width: 1920, height: 1080 },
  { id: "4:3", name: "Traditional", width: 1440, height: 1080 },
  { id: "3:4", name: "Portrait", width: 1080, height: 1440 },
];

export const testViewports = [
  { width: 1920, height: 1080, name: "desktop-fhd" },
  { width: 1440, height: 900, name: "laptop-standard" },
  { width: 1280, height: 720, name: "desktop-hd" },
  { width: 768, height: 1024, name: "tablet" },
  { width: 375, height: 667, name: "mobile" },
];

export const testExportConfigurations = [
  { aspectRatio: "16:9", mode: "light", format: "png", dpi: 300, scale: 3 },
  { aspectRatio: "3:4", mode: "dark", format: "svg", dpi: 600, scale: 4 },
  { aspectRatio: "4:3", mode: "light", format: "both", dpi: 150, scale: 2 },
];

export const testErrorScenarios = {
  networkTimeout: { error: "Network timeout", status: 0 },
  serverError: { error: "Internal server error", status: 500 },
  notFound: { error: "Dashboard not found", status: 404 },
  badRequest: { error: "Invalid parameters", status: 400 },
  pythonError: { error: "Python script execution failed", status: 500 },
};

export const xssTestPayloads = [
  '<script>alert("xss")</script>',
  'javascript:alert("xss")',
  'data:text/html,<script>alert("xss")</script>',
  '"><script>alert("xss")</script>',
  "onload=\"alert('xss')\"",
];

export const malformedURLParams = [
  "?dashboard=",
  "?mode=invalid",
  "?aspect_ratio=abc:def",
  "?format=invalid",
  "?dpi=abc",
  "?scale=xyz",
  '?dashboard=<script>alert("xss")</script>',
  "?mode=" + "x".repeat(1000),
  "?aspect_ratio=null",
  "?format=undefined",
];
