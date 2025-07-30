#!/usr/bin/env python3
"""
Photo Booth Dashboard Screenshot Generator

This script generates high-resolution dashboard screenshots using Puppeteer
via Node.js subprocess calls for web-based dashboard rendering.
"""

import argparse
import asyncio
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.logging_setup import setup_logging


class PhotoBoothGenerator:
    """Main photo booth screenshot generation class."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize photo booth generator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_url = config.get("base_url", "http://localhost:4321")
        self.output_dir = Path(config.get("output", {}).get("directory", "data/outputs/photo-booth"))
        self.screenshot_settings = config.get("screenshot_settings", {})
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_screenshot(
        self, 
        dashboard_id: str, 
        mode: str = "light",
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Generate a single dashboard screenshot.

        Args:
            dashboard_id: ID of the dashboard to screenshot
            mode: Theme mode ('light' or 'dark')
            custom_config: Optional custom screenshot configuration

        Returns:
            Path to the generated screenshot
        """
        self.logger.info(f"Generating {mode} mode screenshot for dashboard: {dashboard_id}")

        # Build URL with parameters
        url = f"{self.base_url}/photo-booth?dashboard={dashboard_id}&mode={mode}"
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_template = self.config.get("output", {}).get("filename_template", "{dashboard_id}_{mode}_{timestamp}.png")
        filename = filename_template.format(
            dashboard_id=dashboard_id,
            mode=mode,
            timestamp=timestamp
        )
        output_path = self.output_dir / filename

        # Merge screenshot settings
        settings = {**self.screenshot_settings}
        if custom_config:
            settings.update(custom_config)

        # Create Node.js script for Puppeteer
        puppeteer_script = self._create_puppeteer_script(url, str(output_path), settings)
        
        try:
            # Execute Puppeteer script
            self._execute_puppeteer_script(puppeteer_script)
            
            if output_path.exists():
                self.logger.info(f"Screenshot saved to: {output_path}")
                return output_path
            else:
                raise RuntimeError(f"Screenshot generation failed: {output_path} not created")
                
        except Exception as e:
            self.logger.error(f"Failed to generate screenshot: {e}")
            raise

    def generate_all_dashboards(
        self, 
        dashboards: Optional[List[str]] = None,
        modes: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Generate screenshots for multiple dashboards.

        Args:
            dashboards: List of dashboard IDs to generate (default: all active)
            modes: List of modes to generate (default: from config)

        Returns:
            List of generated screenshot paths
        """
        # Load photo booth config
        photo_booth_config_path = project_root / "frontend/src/config/photo-booth.json"
        with open(photo_booth_config_path) as f:
            photo_booth_config = json.load(f)

        # Determine dashboards to generate
        if dashboards is None:
            active_dashboards = [d["id"] for d in photo_booth_config["active_dashboards"] if d["enabled"]]
        else:
            active_dashboards = dashboards

        # Determine modes to generate
        if modes is None:
            modes = photo_booth_config.get("output", {}).get("modes", ["light", "dark"])

        generated_files = []
        
        for dashboard_id in active_dashboards:
            for mode in modes:
                try:
                    output_path = self.generate_screenshot(dashboard_id, mode)
                    generated_files.append(output_path)
                except Exception as e:
                    self.logger.error(f"Failed to generate {mode} screenshot for {dashboard_id}: {e}")
                    continue

        self.logger.info(f"Generated {len(generated_files)} screenshots")
        return generated_files

    def _create_puppeteer_script(self, url: str, output_path: str, settings: Dict[str, Any]) -> str:
        """Create Node.js Puppeteer script for screenshot generation."""
        viewport = settings.get("viewport", {"width": 1920, "height": 1080})
        device_scale_factor = settings.get("device_scale_factor", 2)
        timeout = settings.get("timeout", 30000)
        wait_for_selector = settings.get("wait_for_selector", ".photo-booth-ready")
        
        script = f'''
const puppeteer = require('puppeteer');

(async () => {{
  const browser = await puppeteer.launch({{
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  }});
  
  try {{
    const page = await browser.newPage();
    
    // Set viewport and device scale factor
    await page.setViewport({{
      width: {viewport["width"]},
      height: {viewport["height"]},
      deviceScaleFactor: {device_scale_factor}
    }});
    
    // Navigate to the page
    console.log('Navigating to:', '{url}');
    await page.goto('{url}', {{ waitUntil: 'networkidle0', timeout: {timeout} }});
    
    // Wait for dashboard to be ready
    console.log('Waiting for dashboard to be ready...');
    await page.waitForSelector('{wait_for_selector}', {{ timeout: {timeout} }});
    
    // Additional wait for charts to render
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Take screenshot
    console.log('Taking screenshot...');
    await page.screenshot({{
      path: '{output_path}',
      fullPage: {str(settings.get("full_page", True)).lower()},
      type: '{settings.get("format", "png")}',
      quality: {settings.get("quality", 95) if settings.get("format") == "jpeg" else "undefined"}
    }});
    
    console.log('Screenshot saved to:', '{output_path}');
    
  }} catch (error) {{
    console.error('Screenshot generation failed:', error);
    process.exit(1);
  }} finally {{
    await browser.close();
  }}
}})();
'''
        return script

    def _execute_puppeteer_script(self, script: str) -> None:
        """Execute the Puppeteer script using Node.js."""
        # Write script to temporary file with .cjs extension for CommonJS compatibility
        script_path = self.output_dir / f"puppeteer_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.cjs"
        
        try:
            with open(script_path, 'w') as f:
                f.write(script)
            
            # Execute with Node.js from frontend directory
            frontend_dir = project_root / "frontend"
            result = subprocess.run(
                ["node", str(script_path)],
                cwd=str(frontend_dir),
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Puppeteer script failed: {result.stderr}")
            
            self.logger.debug(f"Puppeteer output: {result.stdout}")
            
        finally:
            # Clean up temporary script
            if script_path.exists():
                script_path.unlink()

    def cleanup_old_screenshots(self) -> None:
        """Clean up old screenshots based on configuration."""
        cleanup_config = self.config.get("output", {}).get("auto_cleanup", {})
        
        if not cleanup_config.get("enabled", False):
            return
            
        keep_latest = cleanup_config.get("keep_latest", 5)
        older_than_days = cleanup_config.get("older_than_days", 30)
        
        # Implementation for cleanup logic
        # This is a placeholder - would implement file age checking and deletion
        self.logger.info(f"Cleanup: keeping latest {keep_latest}, removing files older than {older_than_days} days")


def load_config() -> Dict[str, Any]:
    """Load configuration from photo-booth config file."""
    config_path = project_root / "frontend/src/config/photo-booth.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Photo booth config not found: {config_path}")
    
    with open(config_path) as f:
        return json.load(f)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dashboard",
        help="Dashboard ID to generate (default: all active dashboards)"
    )
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Theme mode to generate"
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:4321",
        help="Base URL for the Astro development server"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory override (default from config)"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up old screenshots after generation"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )

    args = parser.parse_args()

    try:
        # Setup logging
        setup_logging(level=args.log_level)
        
        # Load configuration
        config = load_config()
        
        # Override base URL if provided
        config["base_url"] = args.base_url
        
        # Override output directory if provided
        if args.output_dir:
            config["output"]["directory"] = args.output_dir

        # Create generator
        generator = PhotoBoothGenerator(config)
        
        # Determine modes to generate
        modes = ["light", "dark"] if args.mode == "both" else [args.mode]
        
        # Generate screenshots
        if args.dashboard:
            generated_files = []
            for mode in modes:
                output_path = generator.generate_screenshot(args.dashboard, mode)
                generated_files.append(output_path)
        else:
            generated_files = generator.generate_all_dashboards(modes=modes)
        
        # Cleanup if requested
        if args.cleanup:
            generator.cleanup_old_screenshots()
        
        # Print results
        print(f"✅ Generated {len(generated_files)} screenshot(s):")
        for path in generated_files:
            print(f"  - {path}")

    except Exception as e:
        logging.error(f"Photo booth generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()