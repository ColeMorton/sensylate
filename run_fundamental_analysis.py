#!/usr/bin/env python3
"""
Execute Fundamental Analysis Script for MU

This script properly sets up the environment and executes the fundamental analysis
script for generating Twitter content from existing fundamental analysis data.
"""

import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from script_config import ScriptConfig
from script_registry import ScriptRegistry
from base_scripts.fundamental_analysis_script import FundamentalAnalysisScript


def main():
    """Execute fundamental analysis script for MU"""

    # Set up configuration
    base_path = Path(__file__).parent
    config = ScriptConfig.from_environment(base_path)

    print(f"Base path: {config.base_path}")
    print(f"Data outputs path: {config.data_outputs_path}")
    print(f"Twitter outputs path: {config.twitter_outputs_path}")

    # Create script registry and register fundamental analysis script
    registry = ScriptRegistry(config)
    registry.register_script(FundamentalAnalysisScript, "fundamental_analysis")

    # Parameters for execution
    ticker = "MU"
    date = "20250730"
    data_path = str(config.data_outputs_path / "fundamental_analysis" / f"{ticker}_{date}.json")
    output_path = str(config.twitter_outputs_path / "fundamental_analysis" / f"{ticker}_{date}.md")

    print(f"Ticker: {ticker}")
    print(f"Date: {date}")
    print(f"Data path: {data_path}")
    print(f"Output path: {output_path}")

    # Verify data file exists
    if not Path(data_path).exists():
        print(f"ERROR: Data file not found at {data_path}")
        print("Please ensure the markdown file has been converted to JSON format.")
        return 1

    # Execute the script
    print("\nExecuting fundamental analysis script...")

    try:
        result = registry.execute_script(
            "fundamental_analysis",
            ticker=ticker,
            date=date,
            data_path=data_path,
            output_path=output_path,
            validate_content=True
        )

        if result.success:
            print(f"✅ SUCCESS: Content generated successfully")
            print(f"Output saved to: {result.output_path}")
            print(f"Processing time: {result.processing_time:.2f} seconds")

            if hasattr(result, 'validation_score') and result.validation_score:
                print(f"Validation score: {result.validation_score}/10.0")

            # Print generated content preview
            if result.content:
                print("\n--- Generated Content Preview ---")
                preview = result.content[:500] + "..." if len(result.content) > 500 else result.content
                print(preview)
                print("--- End Preview ---")

            return 0

        else:
            print(f"❌ FAILED: {result.error}")
            if hasattr(result, 'error_context') and result.error_context:
                print(f"Error context: {result.error_context}")
            return 1

    except Exception as e:
        print(f"❌ EXECUTION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
