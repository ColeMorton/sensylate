import type { APIRoute } from "astro";
import { spawn } from "child_process";
import path from "path";

interface ExportRequest {
  dashboard_id: string;
  mode: "light" | "dark";
  aspect_ratio: "16:9" | "4:3" | "3:4";
  format: "png" | "svg" | "both";
  dpi: 150 | 300 | 600;
  scale_factor: 2 | 3 | 4;
}

interface ExportResponse {
  success: boolean;
  message: string;
  files?: string[];
  error?: string;
}

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = (await request.json()) as ExportRequest;

    // Validate required fields
    if (
      !body.dashboard_id ||
      !body.mode ||
      !body.aspect_ratio ||
      !body.format ||
      !body.dpi ||
      !body.scale_factor
    ) {
      return new Response(
        JSON.stringify({
          success: false,
          message: "Missing required parameters",
          error: "All export parameters are required",
        } as ExportResponse),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    // Build Python script arguments
    const scriptPath = path.resolve(
      process.cwd(),
      "..",
      "scripts",
      "photo_booth_generator.py",
    );
    const args = [
      scriptPath,
      "--dashboard",
      body.dashboard_id,
      "--mode",
      body.mode,
      "--aspect-ratio",
      body.aspect_ratio,
      "--format",
      body.format,
      "--dpi",
      body.dpi.toString(),
      "--scale-factor",
      body.scale_factor.toString(),
      "--base-url",
      "http://localhost:4321",
    ];

    // Execute Python script
    const pythonProcess = spawn("python3", args, {
      cwd: path.resolve(process.cwd(), ".."),
      stdio: ["pipe", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    pythonProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    const exitCode = await new Promise<number>((resolve) => {
      pythonProcess.on("close", resolve);
    });

    if (exitCode === 0) {
      // Parse generated files from stdout
      const files = stdout
        .split("\n")
        .filter(
          (line) => line.includes("screenshot(s):") || line.includes("- "),
        )
        .map((line) => line.replace(/^.*- /, "").trim())
        .filter(Boolean);

      return new Response(
        JSON.stringify({
          success: true,
          message: `Successfully exported dashboard "${body.dashboard_id}"`,
          files: files,
        } as ExportResponse),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        },
      );
    } else {
      console.error("Python script failed:", stderr);
      return new Response(
        JSON.stringify({
          success: false,
          message: "Export generation failed",
          error: stderr || "Unknown Python script error",
        } as ExportResponse),
        {
          status: 500,
          headers: { "Content-Type": "application/json" },
        },
      );
    }
  } catch (error) {
    console.error("Export API error:", error);

    const errorMessage =
      error instanceof Error ? error.message : "Unknown server error";

    return new Response(
      JSON.stringify({
        success: false,
        message: "Export request failed",
        error: errorMessage,
      } as ExportResponse),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
};
