import type { APIRoute } from "astro";
import { writeFileSync, existsSync, mkdirSync } from "fs";
import path from "path";

interface ExportMetadata {
  dashboard_id: string;
  mode: "light" | "dark";
  aspect_ratio: "16:9" | "4:3" | "3:4";
  format: "png" | "svg" | "both";
  dpi: 150 | 300 | 600;
  scale_factor: 2 | 3 | 4;
}

interface ProcessExportResponse {
  success: boolean;
  file?: string;
  message: string;
  error?: string;
}

export const POST: APIRoute = async ({ request }) => {
  try {
    const formData = await request.formData();
    const imageFile = formData.get("image") as File;
    const metadataStr = formData.get("metadata") as string;

    // Validate required data
    if (!imageFile || !metadataStr) {
      return new Response(
        JSON.stringify({
          success: false,
          message: "Missing required data",
          error: "Both image file and metadata are required",
        } as ProcessExportResponse),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    // Parse metadata
    let metadata: ExportMetadata;
    try {
      metadata = JSON.parse(metadataStr);
    } catch {
      return new Response(
        JSON.stringify({
          success: false,
          message: "Invalid metadata format",
          error: "Failed to parse metadata JSON",
        } as ProcessExportResponse),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    const { dashboard_id, mode, aspect_ratio, format, dpi, scale_factor } =
      metadata;

    // Validate metadata fields
    if (
      !dashboard_id ||
      !mode ||
      !aspect_ratio ||
      !format ||
      !dpi ||
      !scale_factor
    ) {
      return new Response(
        JSON.stringify({
          success: false,
          message: "Incomplete metadata",
          error: "All metadata fields are required",
        } as ProcessExportResponse),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    // Setup output directory and filename
    const projectRoot = path.resolve(process.cwd(), "..");
    const outputDir = path.join(projectRoot, "data", "outputs", "photo-booth");

    // Ensure output directory exists
    if (!existsSync(outputDir)) {
      mkdirSync(outputDir, { recursive: true });
    }

    // Generate filename using same convention as Python script
    const timestamp = new Date()
      .toISOString()
      .replace(/[-:]/g, "")
      .replace(/\..+/, "")
      .replace(/T/, "_")
      .substring(0, 15); // Format: 20250807_123456

    const aspectRatioStr = aspect_ratio.replace(":", "x");
    const filename = `${dashboard_id}_${mode}_${aspectRatioStr}_${format}_${dpi}dpi_${timestamp}.png`;
    const outputPath = path.join(outputDir, filename);

    // Convert image file to buffer and save
    const imageBuffer = Buffer.from(await imageFile.arrayBuffer());
    writeFileSync(outputPath, imageBuffer);

    console.log(`Client-side export saved to: ${outputPath}`);

    return new Response(
      JSON.stringify({
        success: true,
        file: outputPath,
        message: `Successfully exported dashboard "${dashboard_id}" to ${filename}`,
      } as ProcessExportResponse),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      },
    );
  } catch (error) {
    console.error("Export processing error:", error);

    const errorMessage =
      error instanceof Error ? error.message : "Unknown processing error";

    return new Response(
      JSON.stringify({
        success: false,
        message: "Export processing failed",
        error: errorMessage,
      } as ProcessExportResponse),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
};
