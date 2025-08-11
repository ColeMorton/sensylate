import { spawn, type ChildProcess } from "child_process";
import { setTimeout } from "node:timers/promises";

// Global state for shared dev server only (browsers managed per-worker)
let globalDevServer: ChildProcess | null = null;
let globalServerReady = false;

const BASE_URL = "http://localhost:4321";
const MAX_SERVER_START_ATTEMPTS = 60;

// Environment detection for PhotoBooth E2E tests
const isPhotoBoothDevelopmentMode =
  process.env.PHOTOBOOTH_E2E_DEV === "true" ||
  process.env.NODE_ENV === "development";

async function findAvailablePort(startPort: number = 4321): Promise<number> {
  const net = await import("net");

  for (let port = startPort; port < startPort + 100; port++) {
    const available = await new Promise<boolean>((resolve) => {
      const server = net.createServer();
      server.listen(port, (err: any) => {
        if (err) {
          resolve(false);
        } else {
          server.close(() => resolve(true));
        }
      });
      server.on("error", () => resolve(false));
    });

    if (available) {
      return port;
    }
  }

  throw new Error("No available ports found");
}

async function startGlobalDevelopmentServer(): Promise<void> {
  if (globalDevServer || globalServerReady) {
    return;
  }

  console.log("🚀 Starting development server for PhotoBooth E2E tests...");

  const path = await import("path");
  const frontendDir = path.resolve(process.cwd(), "frontend");

  // Find available port and set environment
  const availablePort = await findAvailablePort();
  process.env.E2E_BASE_URL = `http://localhost:${availablePort}`;

  // Kill any existing process on the port
  try {
    const { execSync } = await import("child_process");
    execSync(`lsof -ti:${availablePort} | xargs kill -9`, { stdio: "ignore" });
    await setTimeout(2000); // Wait for cleanup
  } catch (e) {
    // Port was already free
  }

  // Start development server with PhotoBooth enabled
  globalDevServer = spawn(
    "yarn",
    ["dev", "--port", availablePort.toString(), "--host", "0.0.0.0"],
    {
      cwd: frontendDir,
      shell: true,
      detached: false,
      stdio: ["ignore", "pipe", "pipe"],
      env: {
        ...process.env,
        NODE_ENV: "development",
        PHOTOBOOTH_E2E_DEV: "true",
      },
    },
  );

  let serverOutput = "";

  globalDevServer.stdout?.on("data", (data) => {
    const output = data.toString();
    serverOutput += output;
    if (
      output.includes("Local:") ||
      output.includes("ready in") ||
      output.includes("astro")
    ) {
      console.log(`✅ Dev server output: ${output.trim()}`);
    }
  });

  globalDevServer.stderr?.on("data", (data) => {
    const error = data.toString();
    if (
      !error.includes("ExperimentalWarning") &&
      !error.includes("license field") &&
      error.trim()
    ) {
      console.warn("Dev server warning:", error.trim());
    }
  });

  // Wait for server to be ready
  let attempts = 0;
  console.log(
    `⏳ Waiting for development server at ${process.env.E2E_BASE_URL}...`,
  );

  while (attempts < MAX_SERVER_START_ATTEMPTS) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      const response = await fetch(process.env.E2E_BASE_URL, {
        signal: controller.signal,
        headers: { "Cache-Control": "no-cache" },
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        console.log("✅ Development server is ready");
        globalServerReady = true;

        // Wait additional time for full initialization and hot reload stability
        await setTimeout(5000);
        return;
      }

      console.log(
        `Server response: ${response.status} (attempt ${attempts + 1}/${MAX_SERVER_START_ATTEMPTS})`,
      );
    } catch (e: any) {
      if (attempts % 10 === 0) {
        console.log(
          `Server not ready: ${e.message} (attempt ${attempts + 1}/${MAX_SERVER_START_ATTEMPTS})`,
        );
      }
    }

    await setTimeout(1000);
    attempts++;
  }

  throw new Error(
    `Development server failed to start after ${MAX_SERVER_START_ATTEMPTS} seconds`,
  );
}

async function startGlobalProductionServer(): Promise<void> {
  if (globalDevServer || globalServerReady) {
    return;
  }

  console.log("🏗️ Building project for E2E tests...");

  const path = await import("path");
  const frontendDir = path.resolve(process.cwd(), "frontend");

  // Step 1: Build the project
  const { spawn: spawnSync } = await import("child_process");
  const buildProcess = spawnSync("yarn", ["build"], {
    cwd: frontendDir,
    shell: true,
    stdio: ["ignore", "pipe", "pipe"],
  });

  let buildOutput = "";
  let buildError = "";

  buildProcess.stdout?.on("data", (data) => {
    const output = data.toString();
    buildOutput += output;
    if (output.includes("Built in") || output.includes("✓")) {
      console.log("Build:", output.trim());
    }
  });

  buildProcess.stderr?.on("data", (data) => {
    const error = data.toString();
    buildError += error;
    if (
      !error.includes("ExperimentalWarning") &&
      !error.includes("license field")
    ) {
      console.warn("Build warning:", error.trim());
    }
  });

  // Wait for build to complete
  await new Promise<void>((resolve, reject) => {
    buildProcess.on("exit", (code) => {
      if (code === 0) {
        console.log("✅ Project built successfully");
        resolve();
      } else {
        console.error("❌ Build failed:", buildError);
        reject(new Error(`Build failed with code ${code}: ${buildError}`));
      }
    });
  });

  console.log("🚀 Starting production server for E2E tests...");

  // Step 2: Find available port and start preview server
  const availablePort = await findAvailablePort();
  process.env.E2E_BASE_URL = `http://localhost:${availablePort}`;

  // Kill any existing process on the port
  try {
    const { execSync } = await import("child_process");
    execSync(`lsof -ti:${availablePort} | xargs kill -9`, { stdio: "ignore" });
    await setTimeout(2000); // Wait for cleanup
  } catch (e) {
    // Port was already free
  }

  globalDevServer = spawn(
    "yarn",
    ["preview", "--port", availablePort.toString(), "--host", "0.0.0.0"],
    {
      cwd: frontendDir,
      shell: true,
      detached: false,
      stdio: ["ignore", "pipe", "pipe"],
    },
  );

  let serverOutput = "";

  globalDevServer.stdout?.on("data", (data) => {
    const output = data.toString();
    serverOutput += output;
    if (output.includes("Local:") || output.includes("astro")) {
      console.log(`✅ Preview server ready on port ${availablePort}`);
    }
  });

  globalDevServer.stderr?.on("data", (data) => {
    const error = data.toString();
    if (
      !error.includes("ExperimentalWarning") &&
      !error.includes("license field")
    ) {
      console.warn("Preview server warning:", error.trim());
    }
  });

  // Wait for server to be ready
  let attempts = 0;
  console.log(
    `⏳ Waiting for production server at ${process.env.E2E_BASE_URL}...`,
  );

  while (attempts < MAX_SERVER_START_ATTEMPTS) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);

      const response = await fetch(process.env.E2E_BASE_URL, {
        signal: controller.signal,
        headers: { "Cache-Control": "no-cache" },
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        console.log("✅ Production server is ready");
        globalServerReady = true;

        // Wait additional time for full initialization
        await setTimeout(2000);
        return;
      }

      console.log(
        `Server response: ${response.status} (attempt ${attempts + 1}/${MAX_SERVER_START_ATTEMPTS})`,
      );
    } catch (e: any) {
      if (attempts % 15 === 0) {
        console.log(
          `Server not ready: ${e.message} (attempt ${attempts + 1}/${MAX_SERVER_START_ATTEMPTS})`,
        );
      }
    }

    await setTimeout(1000);
    attempts++;
  }

  throw new Error(
    `Production server failed to start after ${MAX_SERVER_START_ATTEMPTS} seconds`,
  );
}

export async function setup(): Promise<void> {
  if (isPhotoBoothDevelopmentMode) {
    console.log(
      "🔧 Setting up global E2E test environment (development mode)...",
    );

    try {
      // Start development server for PhotoBooth testing
      await startGlobalDevelopmentServer();

      // Set environment variable to signal readiness
      process.env.E2E_GLOBAL_SETUP_READY = "true";

      console.log(
        "✅ Global E2E setup complete (development server ready for PhotoBooth)",
      );
    } catch (error) {
      console.error("❌ Global E2E setup failed:", error);
      await teardown(); // Cleanup on failure
      throw error;
    }
  } else {
    console.log(
      "🔧 Setting up global E2E test environment (production build)...",
    );

    try {
      // Build and start production server
      await startGlobalProductionServer();

      // Set environment variable to signal readiness
      process.env.E2E_GLOBAL_SETUP_READY = "true";

      console.log("✅ Global E2E setup complete (production server ready)");
    } catch (error) {
      console.error("❌ Global E2E setup failed:", error);
      await teardown(); // Cleanup on failure
      throw error;
    }
  }
}

export async function teardown(): Promise<void> {
  const serverType = isPhotoBoothDevelopmentMode ? "development" : "production";
  console.log(`🧹 Cleaning up global E2E test environment (${serverType})...`);

  // Clear environment variable
  delete process.env.E2E_GLOBAL_SETUP_READY;

  // Stop dev server
  if (globalDevServer) {
    try {
      globalDevServer.kill("SIGTERM");

      // Wait for graceful shutdown
      await new Promise<void>((resolve) => {
        const timeout = setTimeout(() => {
          if (globalDevServer && !globalDevServer.killed) {
            console.warn(`Force killing ${serverType} server`);
            globalDevServer.kill("SIGKILL");
          }
          resolve();
        }, 5000);

        globalDevServer?.on("exit", () => {
          clearTimeout(timeout);
          resolve();
        });
      });

      globalDevServer = null;
      globalServerReady = false;
      console.log(
        `✅ ${serverType.charAt(0).toUpperCase() + serverType.slice(1)} server stopped`,
      );
    } catch (e) {
      console.warn(`Warning: Failed to stop ${serverType} server:`, e);
    }
  }

  console.log("✅ Global E2E teardown complete");
}

// Export server access functions
export function getGlobalBaseURL(): string {
  return process.env.E2E_BASE_URL || BASE_URL;
}

export function isGlobalServerReady(): boolean {
  return process.env.E2E_GLOBAL_SETUP_READY === "true";
}
