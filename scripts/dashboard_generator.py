#!/usr/bin/env python3
"""
Dashboard generator for creating scalable performance overview visualizations.

This script generates high-resolution dashboard images from historical trading
performance data, following Sensylate design system specifications.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Import our custom modules
from scripts.utils.config_loader import ConfigLoader
from scripts.utils.logging_setup import setup_logging
from scripts.utils.dashboard_parser import parse_dashboard_data, TradeData, MonthlyPerformance
from scripts.utils.theme_manager import create_theme_manager, ThemeManager
from scripts.utils.layout_manager import create_layout_manager, LayoutManager
from scripts.utils.chart_generators import create_chart_generator, AdvancedChartGenerator
from scripts.utils.scalability_manager import create_scalability_manager, ScalabilityManager
from scripts.utils.config_validator import validate_dashboard_config, validate_input_file, ConfigValidationError


class DashboardGenerator:
    """Main dashboard generation class."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize dashboard generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.theme_manager = create_theme_manager()
        
        # Configure font fallbacks for proper Heebo font integration
        self.theme_manager.configure_font_fallbacks()
        
        self.scalability_manager = create_scalability_manager(config)
        self.layout_manager = create_layout_manager(config)
        self.chart_generator = create_chart_generator(self.theme_manager, self.scalability_manager)
        
        # Validate theme colors
        if not self.theme_manager.validate_colors():
            raise ValueError("Invalid color configuration in theme manager")
    
    def generate_dashboard(self, input_file: Path, mode: str = 'light') -> Path:
        """
        Generate dashboard visualization.
        
        Args:
            input_file: Path to the input markdown file
            mode: 'light' or 'dark' mode
            
        Returns:
            Path to the generated dashboard image
        """
        self.logger.info(f"Generating {mode} mode dashboard from {input_file}")
        
        # Parse the input data
        data = parse_dashboard_data(str(input_file))
        
        # Set up matplotlib with theme
        self._setup_matplotlib(mode)
        
        # Create the dashboard
        fig = self._create_dashboard_figure(data, mode)
        
        # Save the output
        output_path = self._save_dashboard(fig, mode)
        
        plt.close(fig)
        
        self.logger.info(f"Dashboard saved to {output_path}")
        return output_path
    
    def _setup_matplotlib(self, mode: str):
        """Setup matplotlib with Sensylate theme."""
        style_config = self.theme_manager.get_matplotlib_style(mode)
        
        # Apply style configuration
        for key, value in style_config.items():
            plt.rcParams[key] = value
    
    def _create_dashboard_figure(self, data: Dict[str, Any], mode: str) -> plt.Figure:
        """
        Create the enhanced dashboard figure with Phase 2 features.
        
        Args:
            data: Parsed performance data
            mode: 'light' or 'dark' mode
            
        Returns:
            Matplotlib figure object
        """
        # Create enhanced layout
        fig, gs = self.layout_manager.create_dashboard_figure()
        
        # Get theme colors
        theme = self.theme_manager.get_theme_colors(mode)
        
        # Set figure background
        fig.patch.set_facecolor(theme.background)
        
        # Create enhanced subplots
        metrics_ax = self.layout_manager.create_metrics_row(fig, gs)
        monthly_ax = self.layout_manager.create_chart_subplot(fig, gs, (1, 0))
        quality_ax = self.layout_manager.create_chart_subplot(fig, gs, (1, 1))
        trades_ax = self.layout_manager.create_chart_subplot(fig, gs, (2, 0))
        duration_ax = self.layout_manager.create_chart_subplot(fig, gs, (2, 1))
        
        # Generate enhanced chart components
        self._create_enhanced_key_metrics(metrics_ax, data['performance_metrics'], mode)
        self.chart_generator.create_enhanced_monthly_bars(monthly_ax, data['monthly_performance'], mode)
        self.chart_generator.create_enhanced_donut_chart(quality_ax, data['quality_distribution'], mode)
        self.chart_generator.create_waterfall_chart(trades_ax, data['trades'], mode)
        self.chart_generator.create_enhanced_scatter(duration_ax, data['trades'], mode)
        
        # Add enhanced title and subtitle
        metadata = data.get('metadata', {})
        title = "Historical Trading Performance Dashboard"
        subtitle = metadata.get('date_range', '')
        
        self.layout_manager.add_title_and_subtitle(fig, title, subtitle, theme.__dict__)
        
        # Apply final layout optimizations
        self.layout_manager.finalize_layout(fig)
        
        return fig
    
    def _create_enhanced_key_metrics(self, ax: plt.Axes, metrics, mode: str):
        """Create enhanced key metrics display with Phase 2 features."""
        theme = self.theme_manager.get_theme_colors(mode)
        
        # Enhanced metrics data with indicators
        metrics_data = [
            {
                'label': 'Win Rate',
                'value': f"{metrics.win_rate:.1f}%",
                'indicator': 'positive' if metrics.win_rate > 50 else 'negative'
            },
            {
                'label': 'Total Return',
                'value': f"{metrics.total_return:+.2f}%",
                'indicator': 'positive' if metrics.total_return > 0 else 'negative'
            },
            {
                'label': 'Profit Factor',
                'value': f"{metrics.profit_factor:.2f}",
                'indicator': 'positive' if metrics.profit_factor > 1 else 'negative'
            },
            {
                'label': 'Total Trades',
                'value': f"{metrics.total_trades}",
                'indicator': 'neutral'
            }
        ]
        
        # Use enhanced layout manager for metric cards
        self.layout_manager.create_metric_cards(ax, metrics_data, theme.__dict__)
    
    
    def _save_dashboard(self, fig: plt.Figure, mode: str) -> Path:
        """Save the dashboard figure to file."""
        output_config = self.config.get('output', {})
        base_path = Path(output_config.get('base_path', 'data/outputs/dashboards'))
        
        # Ensure output directory exists
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d')
        if mode == 'light':
            filename = output_config.get('light_mode_file', 'dashboard-light-{timestamp}.png')
        else:
            filename = output_config.get('dark_mode_file', 'dashboard-dark-{timestamp}.png')
            
        filename = filename.format(timestamp=timestamp)
        output_path = base_path / filename
        
        # Save with high DPI
        dpi = output_config.get('dpi', 300)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                   facecolor=fig.get_facecolor(), edgecolor='none')
        
        return output_path


def main(config: Dict[str, Any], input_file: Path, mode: str = 'both', 
         output_dir: Optional[Path] = None) -> List[Path]:
    """
    Main execution function.
    
    Args:
        config: Configuration dictionary
        input_file: Input historical performance markdown file
        mode: Dashboard mode ('light', 'dark', or 'both')
        output_dir: Optional output directory override
        
    Returns:
        List of generated dashboard file paths
    """
    generator = DashboardGenerator(config)
    
    # Override output directory if provided
    if output_dir:
        config['output']['directory'] = str(output_dir)
    
    modes_to_generate = ['light', 'dark'] if mode == 'both' else [mode]
    generated_files = []
    
    for dashboard_mode in modes_to_generate:
        output_file = generator.generate_dashboard(input_file, dashboard_mode)
        generated_files.append(output_file)
        print(f"Generated {dashboard_mode} mode dashboard: {output_file}")
    
    # Print Make-compatible output for pipeline integration
    if len(generated_files) == 1:
        print(f"OUTPUT_FILE={generated_files[0]}")
    else:
        for i, file_path in enumerate(generated_files):
            print(f"OUTPUT_FILE_{i+1}={file_path}")
    
    return generated_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", 
        default="configs/dashboard_generation.yaml",
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "--input", 
        required=True, 
        help="Input historical performance markdown file"
    )
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Dashboard mode to generate"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory override (default from config)"
    )
    parser.add_argument(
        "--env",
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment configuration"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate configuration and input, don't generate dashboards"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-essential output (useful for Make integration)"
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.load_with_environment(args.config, args.env)

        # Setup logging
        if args.quiet:
            # Suppress INFO and lower for quiet mode
            logging.getLogger().setLevel(logging.WARNING)
        else:
            setup_logging(
                level=args.log_level, 
                log_file=config.get("logging", {}).get("file")
            )

        # Validate configuration
        try:
            validation_summary = validate_dashboard_config(config)
            if not args.quiet:
                if validation_summary['warning_count'] > 0:
                    print(f"⚠️  Configuration validation passed with {validation_summary['warning_count']} warning(s)")
        except ConfigValidationError as e:
            print(f"❌ Configuration validation failed: {e}")
            sys.exit(1)
        
        # Validate input file
        input_path = Path(args.input)
        try:
            validate_input_file(input_path)
        except ConfigValidationError as e:
            print(f"❌ Input file validation failed: {e}")
            sys.exit(1)
        
        output_dir = Path(args.output_dir) if args.output_dir else None
        
        if args.validate_only:
            if not args.quiet:
                print("✅ Configuration and input validation successful")
            sys.exit(0)

        # Generate dashboards
        generated_files = main(config, input_path, args.mode, output_dir)
        
        if not args.quiet:
            print(f"✅ Successfully generated {len(generated_files)} dashboard file(s)")

    except Exception as e:
        logging.error(f"Dashboard generation failed: {e}")
        sys.exit(1)