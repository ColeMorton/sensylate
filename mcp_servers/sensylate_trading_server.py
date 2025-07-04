#!/usr/bin/env python3
"""
Sensylate Trading MCP Server - Local development focused trading analysis tools
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not installed. Install with: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Initialize the MCP server
mcp = FastMCP("Sensylate Trading Server")

# Configure logging for local development
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensylateDataManager:
    """Manage Sensylate's local data and analysis workflows"""

    def __init__(self):
        self.base_path = Path(".")
        self.data_path = self.base_path / "data"
        self.outputs_path = self.data_path / "outputs"
        self.scripts_path = self.base_path / "scripts"

    def get_analysis_files(self, analysis_type: str = "fundamental_analysis") -> List[Dict[str, Any]]:
        """Get list of analysis files"""
        analysis_path = self.outputs_path / analysis_type
        if not analysis_path.exists():
            return []

        files = []
        for file_path in analysis_path.glob("*.md"):
            files.append({
                "file": file_path.name,
                "path": str(file_path),
                "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "size": file_path.stat().st_size
            })

        return sorted(files, key=lambda x: x["created"], reverse=True)

    def get_latest_analysis(self, ticker: str, analysis_type: str = "fundamental_analysis") -> Optional[str]:
        """Get latest analysis for a specific ticker"""
        analysis_path = self.outputs_path / analysis_type
        if not analysis_path.exists():
            return None

        # Look for files containing the ticker
        for file_path in analysis_path.glob(f"*{ticker.upper()}*.md"):
            with open(file_path, 'r') as f:
                return f.read()

        return None

    def get_trading_performance_data(self) -> Dict[str, Any]:
        """Get trading performance data from outputs"""
        perf_data = {
            "live_signals": [],
            "historical_analysis": [],
            "validation_results": []
        }

        # Check for live signals
        trade_history_path = self.outputs_path / "analysis_trade_history"
        if trade_history_path.exists():
            for json_file in trade_history_path.glob("**/*.json"):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                        perf_data["live_signals"].append({
                            "file": json_file.name,
                            "data": data,
                            "created": datetime.fromtimestamp(json_file.stat().st_mtime).isoformat()
                        })
                except (json.JSONDecodeError, Exception):
                    continue

        return perf_data

# Initialize data manager
data_manager = SensylateDataManager()

@mcp.tool
def get_fundamental_analysis(ticker: str) -> str:
    """Get the latest fundamental analysis for a specific ticker"""

    analysis = data_manager.get_latest_analysis(ticker, "fundamental_analysis")

    if analysis:
        return json.dumps({
            "ticker": ticker.upper(),
            "analysis_found": True,
            "content": analysis,
            "source": "local_analysis",
            "timestamp": datetime.now().isoformat()
        }, indent=2)
    else:
        return json.dumps({
            "ticker": ticker.upper(),
            "analysis_found": False,
            "message": f"No fundamental analysis found for {ticker.upper()}",
            "available_analyses": [f["file"] for f in data_manager.get_analysis_files("fundamental_analysis")],
            "timestamp": datetime.now().isoformat()
        }, indent=2)

@mcp.tool
def list_available_analyses(analysis_type: str = "fundamental_analysis") -> str:
    """List all available analysis files of a specific type"""

    files = data_manager.get_analysis_files(analysis_type)

    return json.dumps({
        "analysis_type": analysis_type,
        "total_files": len(files),
        "files": files,
        "timestamp": datetime.now().isoformat()
    }, indent=2)

@mcp.tool
def get_trading_performance() -> str:
    """Get trading performance data and live signals"""

    performance_data = data_manager.get_trading_performance_data()

    return json.dumps({
        "performance_summary": {
            "live_signals_count": len(performance_data["live_signals"]),
            "historical_analyses": len(performance_data["historical_analysis"]),
            "validation_results": len(performance_data["validation_results"])
        },
        "data": performance_data,
        "timestamp": datetime.now().isoformat()
    }, indent=2)

@mcp.tool
def generate_blog_content(ticker: str, content_type: str = "fundamental_analysis") -> str:
    """Generate blog content from existing analysis data"""

    analysis = data_manager.get_latest_analysis(ticker, content_type)

    if not analysis:
        return json.dumps({
            "error": f"No analysis found for {ticker.upper()}",
            "available_tickers": [f["file"].split("_")[0] for f in data_manager.get_analysis_files(content_type)]
        })

    # Extract key insights for blog post
    lines = analysis.split('\n')
    title_line = next((line for line in lines if line.startswith('#')), f"# {ticker.upper()} Analysis")

    # Generate blog frontmatter
    blog_content = f"""---
title: "{title_line.lstrip('#').strip()}"
meta_title: "{ticker.upper()} Trading Analysis - Sensylate"
description: "Comprehensive fundamental analysis of {ticker.upper()} with trading insights and market evaluation"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: ["Trading Analysis", "Fundamental Analysis"]
tags: ["{ticker.upper()}", "Trading", "Analysis"]
draft: false
---

{analysis}

---

*This analysis was generated using Sensylate's automated trading analysis pipeline. For more insights and analysis, explore our [trading blog](/blog/).*
"""

    # Suggest filename
    suggested_filename = f"{ticker.lower()}-fundamental-analysis-{datetime.now().strftime('%Y%m%d')}.md"
    blog_path = Path("frontend/src/content/blog") / suggested_filename

    return json.dumps({
        "ticker": ticker.upper(),
        "content_generated": True,
        "suggested_filename": suggested_filename,
        "suggested_path": str(blog_path),
        "content": blog_content,
        "word_count": len(blog_content.split()),
        "timestamp": datetime.now().isoformat()
    }, indent=2)

@mcp.tool
def run_analysis_script(script_name: str, ticker: str = "", **kwargs) -> str:
    """Run a Sensylate analysis script with specified parameters"""

    script_path = data_manager.scripts_path / f"{script_name}.py"

    if not script_path.exists():
        available_scripts = [f.stem for f in data_manager.scripts_path.glob("*.py")]
        return json.dumps({
            "error": f"Script {script_name} not found",
            "available_scripts": available_scripts
        })

    # Prepare command
    command_parts = ["python", str(script_path)]

    if ticker:
        command_parts.extend(["--ticker", ticker])

    # Add any additional parameters
    for key, value in kwargs.items():
        command_parts.extend([f"--{key}", str(value)])

    return json.dumps({
        "script": script_name,
        "command": " ".join(command_parts),
        "parameters": {"ticker": ticker, **kwargs},
        "status": "command_prepared",
        "note": "Execute this command in your terminal to run the analysis",
        "timestamp": datetime.now().isoformat()
    }, indent=2)

@mcp.resource("config://sensylate-paths")
def get_sensylate_paths() -> str:
    """Get Sensylate project paths and structure"""
    return json.dumps({
        "base_path": str(data_manager.base_path.absolute()),
        "data_path": str(data_manager.data_path.absolute()),
        "outputs_path": str(data_manager.outputs_path.absolute()),
        "scripts_path": str(data_manager.scripts_path.absolute()),
        "frontend_path": str((data_manager.base_path / "frontend").absolute()),
        "blog_content_path": str((data_manager.base_path / "frontend/src/content/blog").absolute()),
        "structure_validated": all(p.exists() for p in [
            data_manager.data_path,
            data_manager.outputs_path,
            data_manager.scripts_path
        ])
    }, indent=2)

@mcp.resource("analytics://recent-activity")
def get_recent_activity() -> str:
    """Get recent analysis activity and file changes"""

    recent_files = []

    # Get recent analysis files
    for analysis_type in ["fundamental_analysis", "twitter_post_strategy", "analysis_trade_history"]:
        analysis_path = data_manager.outputs_path / analysis_type
        if analysis_path.exists():
            for file_path in analysis_path.glob("*.md"):
                if datetime.fromtimestamp(file_path.stat().st_mtime) > datetime.now().replace(hour=0, minute=0, second=0).timestamp():
                    recent_files.append({
                        "file": file_path.name,
                        "type": analysis_type,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })

    return json.dumps({
        "recent_activity": {
            "today_files": len(recent_files),
            "files": sorted(recent_files, key=lambda x: x["modified"], reverse=True)
        },
        "analysis_types_active": list(set(f["type"] for f in recent_files)),
        "last_updated": datetime.now().isoformat()
    }, indent=2)

@mcp.resource("status://mcp-integration")
def get_mcp_integration_status() -> str:
    """Get status of MCP integration with Sensylate workflows"""
    return json.dumps({
        "mcp_server_status": "active",
        "local_development_mode": True,
        "static_site_deployment": "netlify",
        "data_pipeline_integration": "active",
        "content_generation": "automated",
        "analysis_workflows": "mcp_enabled",
        "team_workspace_integration": "active",
        "last_health_check": datetime.now().isoformat()
    }, indent=2)

@mcp.prompt("generate-trading-blog-post")
def trading_blog_post_prompt(ticker: str, analysis_type: str = "fundamental") -> str:
    """Generate a comprehensive trading blog post from analysis data"""
    return f"""You are a professional financial content writer creating a blog post about {ticker.upper()}.

Using the fundamental analysis data available, create a comprehensive blog post that includes:

1. **Executive Summary** - Key investment thesis in 2-3 sentences
2. **Financial Highlights** - Key metrics and ratios
3. **Strengths & Opportunities** - What makes this stock attractive
4. **Risks & Concerns** - Potential downside factors
5. **Technical Analysis** - Chart patterns and price action
6. **Investment Recommendation** - Clear guidance for investors

**Writing Style:**
- Professional but accessible
- Data-driven with specific numbers
- Balanced perspective (pros and cons)
- Clear actionable insights

**SEO Optimization:**
- Include {ticker.upper()} naturally throughout
- Use relevant financial keywords
- Structure with clear headings
- Include a compelling meta description

**Compliance:**
- Educational content only
- Not personalized investment advice
- Include appropriate disclaimers

Generate content suitable for publication on a trading analysis blog."""

if __name__ == "__main__":
    mcp.run()
