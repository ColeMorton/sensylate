#!/usr/bin/env python3
"""
Dashboard Configuration Generator

Reads from Astro content collection (frontend/src/content/dashboards/*.mdx)
and generates static JSON configuration for production builds.

DevContentOps Pipeline Integration:
- Called by data_pipeline_manager.py during build process
- Outputs to frontend/public/data/dashboards.json
- Eliminates runtime API dependency for static deployment
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DashboardConfigGenerator:
    """Generates dashboard configurations from content collection"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.content_dir = project_root / "frontend" / "src" / "content" / "dashboards"
        self.output_dir = project_root / "frontend" / "public" / "data"
        
        # Chart configurations mapped from content
        self.chart_configs = {
            "trading_performance": [
                {
                    "title": "Bitcoin Portfolio Value Comparison",
                    "category": "Bitcoin Performance",
                    "description": "Multi-strategy Bitcoin trading vs buy-and-hold approach from 2014-2025. Active strategy: $1,000 → $113,312 (11,231% return).",
                    "chartType": "portfolio-value-comparison"
                },
                {
                    "title": "Bitcoin Returns Comparison", 
                    "category": "Bitcoin Performance",
                    "description": "Daily returns comparison: multi-strategy Bitcoin trading vs passive buy-and-hold showing day-to-day percentage changes over 3,960 days of market data.",
                    "chartType": "returns-comparison"
                },
                {
                    "title": "Bitcoin Portfolio Drawdown Analysis",
                    "category": "Bitcoin Risk Analysis", 
                    "description": "Bitcoin portfolio risk analysis showing drawdown periods. Maximum drawdown: 53.23% with 839-day recovery duration.",
                    "chartType": "portfolio-drawdowns"
                },
                {
                    "title": "Live Signals Equity Curve",
                    "category": "Live Trading Performance",
                    "description": "Comprehensive live trading analysis showing equity curve, MFE (Maximum Favorable Excursion), and MAE (Maximum Adverse Excursion). Real-time performance from April to August 2025 with risk management insights.",
                    "chartType": "live-signals-equity-curve"
                }
            ],
            "portfolio_analysis": [
                {
                    "title": "Live Signals Equity Curve",
                    "category": "Live Trading Performance", 
                    "description": "Comprehensive live trading analysis showing equity curve, MFE (Maximum Favorable Excursion), and MAE (Maximum Adverse Excursion). Real-time performance from April to August 2025 with risk management insights.",
                    "chartType": "live-signals-equity-curve"
                },
                {
                    "title": "Live Signals Drawdown Analysis",
                    "category": "Live Trading Risk",
                    "description": "Live portfolio drawdown periods showing risk management during real trading. Peak drawdown of $69.23 with successful recovery to profitability.",
                    "chartType": "live-signals-drawdowns"
                },
                {
                    "title": "Closed Position PnL Waterfall",
                    "category": "Live Trading Individual Trades",
                    "description": "Waterfall chart showing individual trade profits and losses from closed positions, sorted from highest to lowest PnL. Visualizes contribution of each trade to overall portfolio performance.",
                    "chartType": "trade-pnl-waterfall"
                },
                {
                    "title": "Open Positions Cumulative PnL Time Series",
                    "category": "Live Trading Open Positions",
                    "description": "Multi-line time series showing cumulative PnL for each open position, indexed to $0 at entry date. Track real-time performance across the live portfolio with individual lines for each ticker.",
                    "chartType": "open-positions-pnl-timeseries"
                }
            ],
            "portfolio_history_portrait": [
                {
                    "title": "Closed Position PnL Waterfall",
                    "category": "Trading Performance",
                    "description": "Waterfall chart showing individual trade profits and losses from closed positions, sorted from highest to lowest PnL. Visualizes contribution of each trade to overall portfolio performance.", 
                    "chartType": "trade-pnl-waterfall"
                },
                {
                    "title": "Closed Position PnL Performance",
                    "category": "Trading Performance",
                    "description": "Multi-line time series showing cumulative PnL for each closed position, indexed to $0 at entry date. Track performance progression across the closed portfolio with individual lines for each ticker.",
                    "chartType": "closed-positions-pnl-timeseries"
                }
            ],
            "fundamental_analysis": [
                {
                    "title": "Revenue & FCF",
                    "category": "Financial Performance", 
                    "description": "Revenue and free cash flow trends over time",
                    "chartType": "fundamental-revenue-fcf"
                },
                {
                    "title": "Revenue Source",
                    "category": "Revenue Breakdown",
                    "description": "Revenue distribution by business segment",
                    "chartType": "fundamental-revenue-source"
                },
                {
                    "title": "Geography",
                    "category": "Geographic Distribution",
                    "description": "Revenue distribution by geographic region", 
                    "chartType": "fundamental-geography"
                },
                {
                    "title": "Key Metrics",
                    "category": "Growth Analysis",
                    "description": "Key growth metrics and performance indicators",
                    "chartType": "fundamental-key-metrics"
                },
                {
                    "title": "Quality", 
                    "category": "Quality Assessment",
                    "description": "Quality ratings across multiple dimensions",
                    "chartType": "fundamental-quality-rating"
                },
                {
                    "title": "Financials",
                    "category": "Financial Health",
                    "description": "Revenue growth, FCF growth, and cash position",
                    "chartType": "fundamental-financial-health"
                },
                {
                    "title": "Pros & Cons",
                    "category": "Investment Analysis",
                    "description": "Key investment advantages and risks",
                    "chartType": "fundamental-pros-cons"
                },
                {
                    "title": "Valuation",
                    "category": "Valuation Analysis",
                    "description": "Multiple valuation methodologies and fair value estimates",
                    "chartType": "fundamental-valuation"
                },
                {
                    "title": "Balance Sheet",
                    "category": "Financial Position", 
                    "description": "Balance sheet metrics and financial stability",
                    "chartType": "fundamental-balance-sheet"
                }
            ],
            "bitcoin_cycle_intelligence": [
                {
                    "title": "Bitcoin Price - 210 Day History",
                    "category": "Bitcoin Analysis",
                    "description": "Interactive Bitcoin (BTC-USD) price chart showing the last 210 days of market data. Displays daily open, high, low, close prices with volume data for cycle intelligence analysis.",
                    "chartType": "btc-price"
                }
            ]
        }
    
    def discover_dashboards(self) -> List[Dict[str, Any]]:
        """Discover dashboard configurations from content collection"""
        dashboards = []
        
        if not self.content_dir.exists():
            logger.warning(f"Content directory not found: {self.content_dir}")
            return dashboards
            
        # Scan for .mdx files
        for mdx_file in self.content_dir.glob("*.mdx"):
            try:
                dashboard_config = self._process_dashboard_file(mdx_file)
                if dashboard_config and dashboard_config.get("enabled", True):
                    dashboards.append(dashboard_config)
                    logger.info(f"✅ Processed dashboard: {dashboard_config['id']}")
                else:
                    logger.info(f"⏭️  Skipped disabled dashboard: {mdx_file.stem}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to process {mdx_file}: {e}")
                continue
                
        logger.info(f"📊 Discovered {len(dashboards)} enabled dashboards")
        return dashboards
    
    def _process_dashboard_file(self, mdx_file: Path) -> Optional[Dict[str, Any]]:
        """Process individual MDX file and extract dashboard configuration"""
        try:
            with open(mdx_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
            # Convert filename to dashboard ID (hyphenated to underscore)
            dashboard_id = mdx_file.stem.replace('-', '_')
            
            # Extract frontmatter data
            metadata = post.metadata
            
            # Get chart configurations for this dashboard
            charts = self.chart_configs.get(dashboard_id, [])
            
            # Auto-detect optimal layout based on chart count if not explicitly specified
            chart_count = len(charts)
            if chart_count == 1:
                default_layout = "1x1"  # Full-width single chart
            elif chart_count == 2:
                default_layout = "2x1_stack"  # Vertical stack
            else:
                default_layout = "2x2_grid"  # Multi-chart grid
            
            # Build dashboard configuration
            config = {
                "id": dashboard_id,
                "title": metadata.get("title", mdx_file.stem.replace('-', ' ').title()),
                "description": metadata.get("description", ""),
                "layout": metadata.get("layout", default_layout),
                "mode": metadata.get("mode", "both"), 
                "enabled": metadata.get("enabled", True),
                "charts": charts,
                "export_defaults": metadata.get("export_defaults", {})
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Error processing {mdx_file}: {e}")
            return None
    
    def generate_static_config(self) -> Dict[str, Any]:
        """Generate complete static dashboard configuration"""
        dashboards = self.discover_dashboards()
        
        # Filter only enabled dashboards
        enabled_dashboards = [d for d in dashboards if d.get("enabled", True)]
        
        config = {
            "success": True,
            "dashboards": enabled_dashboards,
            "timestamp": "build-time",
            "source": "static_generation",
            "generator": "dashboard_config_generator.py"
        }
        
        return config
    
    def write_static_config(self, config: Dict[str, Any]) -> bool:
        """Write static configuration to public directory"""
        try:
            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = self.output_dir / "dashboards.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            logger.info(f"✅ Generated static config: {output_file}")
            logger.info(f"📊 Included {len(config['dashboards'])} dashboards")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to write static config: {e}")
            return False


def main():
    """Main entry point for dashboard config generation"""
    # Find project root (assuming script is in scripts/ directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    logger.info("🔨 Starting dashboard configuration generation...")
    logger.info(f"📁 Project root: {project_root}")
    
    # Initialize generator
    generator = DashboardConfigGenerator(project_root)
    
    # Generate configuration
    config = generator.generate_static_config()
    
    # Write to static file
    success = generator.write_static_config(config)
    
    if success:
        logger.info("✅ Dashboard configuration generation completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Dashboard configuration generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()