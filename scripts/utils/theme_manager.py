#!/usr/bin/env python3
"""
Theme manager for Sensylate design system integration.

This module provides color palette and theme management for dashboard generation,
ensuring consistency with the Sensylate brand guidelines.
"""

import yaml
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ColorPalette:
    """Represents the Sensylate color palette."""
    
    # Primary chart colors
    primary_data: str = "#26c6da"      # Cyan
    secondary_data: str = "#7e57c2"    # Purple
    tertiary_data: str = "#3179f5"     # Blue
    
    # Extended palette
    quaternary: str = "#ff7043"        # Orange
    quinary: str = "#66bb6a"           # Green
    senary: str = "#ec407a"            # Pink
    
    def get_extended_palette(self) -> list:
        """Get the full extended color palette as a list."""
        return [
            self.primary_data,
            self.secondary_data,
            self.tertiary_data,
            self.quaternary,
            self.quinary,
            self.senary
        ]


@dataclass
class ThemeColors:
    """Represents theme-specific colors (light/dark mode)."""
    background: str
    card_backgrounds: str
    primary_text: str
    body_text: str
    muted_text: str
    borders: str


@dataclass
class Typography:
    """Represents typography settings."""
    primary_family: str = "Heebo"
    regular_weight: int = 400
    semibold_weight: int = 600
    fallback: str = "sans-serif"


class ThemeManager:
    """Manages theme configuration and color palettes for dashboard generation."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize theme manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize palettes
        self.color_palette = self._create_color_palette()
        self.light_theme = self._create_light_theme()
        self.dark_theme = self._create_dark_theme()
        self.typography = self._create_typography()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path:
            # Use default configuration
            return self._get_default_config()
            
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                self.logger.warning(f"Config file not found: {self.config_path}, using defaults")
                return self._get_default_config()
                
            with open(config_file, 'r') as file:
                return yaml.safe_load(file)
                
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default Sensylate theme configuration."""
        return {
            'design_system': {
                'colors': {
                    'primary_data': '#26c6da',
                    'secondary_data': '#7e57c2',
                    'tertiary_data': '#3179f5',
                    'extended_palette': {
                        'quaternary': '#ff7043',
                        'quinary': '#66bb6a',
                        'senary': '#ec407a'
                    }
                },
                'light_mode': {
                    'background': '#fff',
                    'card_backgrounds': '#f6f6f6',
                    'primary_text': '#121212',
                    'body_text': '#444444',
                    'muted_text': '#717171',
                    'borders': '#eaeaea'
                },
                'dark_mode': {
                    'background': '#202124',
                    'card_backgrounds': '#222222',
                    'primary_text': '#fff',
                    'body_text': '#B4AFB6',
                    'muted_text': '#B4AFB6',
                    'borders': '#3E3E3E'
                },
                'fonts': {
                    'primary_family': 'Heebo',
                    'weights': {
                        'regular': 400,
                        'semibold': 600
                    },
                    'fallback': 'sans-serif'
                }
            }
        }
    
    def _create_color_palette(self) -> ColorPalette:
        """Create color palette from configuration."""
        colors_config = self.config.get('design_system', {}).get('colors', {})
        extended = colors_config.get('extended_palette', {})
        
        return ColorPalette(
            primary_data=colors_config.get('primary_data', '#26c6da'),
            secondary_data=colors_config.get('secondary_data', '#7e57c2'),
            tertiary_data=colors_config.get('tertiary_data', '#3179f5'),
            quaternary=extended.get('quaternary', '#ff7043'),
            quinary=extended.get('quinary', '#66bb6a'),
            senary=extended.get('senary', '#ec407a')
        )
    
    def _create_light_theme(self) -> ThemeColors:
        """Create light mode theme colors."""
        light_config = self.config.get('design_system', {}).get('light_mode', {})
        
        return ThemeColors(
            background=light_config.get('background', '#fff'),
            card_backgrounds=light_config.get('card_backgrounds', '#f6f6f6'),
            primary_text=light_config.get('primary_text', '#121212'),
            body_text=light_config.get('body_text', '#444444'),
            muted_text=light_config.get('muted_text', '#717171'),
            borders=light_config.get('borders', '#eaeaea')
        )
    
    def _create_dark_theme(self) -> ThemeColors:
        """Create dark mode theme colors."""
        dark_config = self.config.get('design_system', {}).get('dark_mode', {})
        
        return ThemeColors(
            background=dark_config.get('background', '#202124'),
            card_backgrounds=dark_config.get('card_backgrounds', '#222222'),
            primary_text=dark_config.get('primary_text', '#fff'),
            body_text=dark_config.get('body_text', '#B4AFB6'),
            muted_text=dark_config.get('muted_text', '#B4AFB6'),
            borders=dark_config.get('borders', '#3E3E3E')
        )
    
    def _create_typography(self) -> Typography:
        """Create typography configuration."""
        fonts_config = self.config.get('design_system', {}).get('fonts', {})
        weights = fonts_config.get('weights', {})
        
        return Typography(
            primary_family=fonts_config.get('primary_family', 'Heebo'),
            regular_weight=weights.get('regular', 400),
            semibold_weight=weights.get('semibold', 600),
            fallback=fonts_config.get('fallback', 'sans-serif')
        )
    
    def get_theme_colors(self, mode: str = 'light') -> ThemeColors:
        """
        Get theme colors for specified mode.
        
        Args:
            mode: 'light' or 'dark'
            
        Returns:
            ThemeColors object for the specified mode
        """
        if mode.lower() == 'dark':
            return self.dark_theme
        return self.light_theme
    
    def get_quality_colors(self) -> Dict[str, str]:
        """
        Get color mapping for trade quality categories.
        
        Returns:
            Dictionary mapping quality categories to colors
        """
        return {
            'Excellent': self.color_palette.primary_data,      # Cyan
            'Good': self.color_palette.tertiary_data,          # Blue
            'Poor': self.color_palette.secondary_data,         # Purple
            'Failed': self.color_palette.quaternary,           # Orange
            'Poor Setup': self.color_palette.quinary           # Green
        }
    
    def get_performance_colors(self) -> Dict[str, str]:
        """
        Get color mapping for performance indicators.
        
        Returns:
            Dictionary mapping performance types to colors
        """
        return {
            'positive': self.color_palette.primary_data,       # Cyan for gains
            'negative': self.color_palette.secondary_data,     # Purple for losses
            'neutral': self.color_palette.tertiary_data        # Blue for neutral
        }
    
    def get_monthly_colors(self) -> list:
        """
        Get colors for monthly performance charts.
        
        Returns:
            List of colors for monthly data series
        """
        return [
            self.color_palette.secondary_data,    # Purple
            self.color_palette.primary_data,      # Cyan
            self.color_palette.tertiary_data      # Blue
        ]
    
    def get_matplotlib_style(self, mode: str = 'light') -> Dict[str, Any]:
        """
        Get matplotlib style configuration for the specified mode.
        
        Args:
            mode: 'light' or 'dark'
            
        Returns:
            Dictionary of matplotlib style parameters
        """
        theme = self.get_theme_colors(mode)
        
        return {
            'figure.facecolor': theme.background,
            'axes.facecolor': theme.background,
            'axes.edgecolor': theme.borders,
            'axes.labelcolor': theme.body_text,
            'text.color': theme.body_text,
            'xtick.color': theme.body_text,
            'ytick.color': theme.body_text,
            'grid.color': theme.borders,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.grid': True,
            'font.family': self._get_font_list(),
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        }
    
    def validate_colors(self) -> bool:
        """
        Validate that all required colors are properly defined.
        
        Returns:
            True if all colors are valid, False otherwise
        """
        try:
            # Check primary colors
            colors_to_check = [
                self.color_palette.primary_data,
                self.color_palette.secondary_data,
                self.color_palette.tertiary_data
            ]
            
            # Check extended palette
            colors_to_check.extend(self.color_palette.get_extended_palette())
            
            # Check theme colors
            for theme in [self.light_theme, self.dark_theme]:
                colors_to_check.extend([
                    theme.background,
                    theme.primary_text,
                    theme.body_text,
                    theme.borders
                ])
            
            # Validate hex color format
            for color in colors_to_check:
                if not color.startswith('#'):
                    self.logger.error(f"Invalid color format: {color}")
                    return False
                
                # Accept both #RGB and #RRGGBB formats
                hex_part = color[1:]
                if len(hex_part) not in [3, 6]:
                    self.logger.error(f"Invalid color format: {color}")
                    return False
                    
                # Check if it's a valid hex color
                int(hex_part, 16)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Color validation failed: {e}")
            return False
    
    def _get_font_list(self) -> List[str]:
        """
        Get prioritized font list with fallbacks.
        
        Returns:
            List of font families in priority order
        """
        fonts = [self.typography.primary_family]
        
        # Add common system fallbacks
        if self.typography.primary_family.lower() == 'heebo':
            fonts.extend([
                'Helvetica Neue',
                'Arial',
                'DejaVu Sans',
                'Liberation Sans',
                'sans-serif'
            ])
        else:
            fonts.append(self.typography.fallback)
            
        return fonts
    
    def configure_font_fallbacks(self) -> None:
        """Configure font fallbacks and attempt to load Heebo font."""
        import matplotlib.font_manager as fm
        import matplotlib.pyplot as plt
        import requests
        import tempfile
        import os
        from zipfile import ZipFile
        
        # Refresh font cache to ensure up-to-date font list
        fm.fontManager.__init__()
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        
        # Check if Heebo is already available
        if self.typography.primary_family in available_fonts:
            self.logger.info(f"Font '{self.typography.primary_family}' is available")
            plt.rcParams['font.family'] = self._get_font_list()
            return
        
        self.logger.warning(f"Font '{self.typography.primary_family}' not found, attempting to download")
        
        # Try to download and install Heebo font from Google Fonts
        try:
            self._download_and_install_heebo()
            
            # Refresh font manager after installation
            fm.fontManager.__init__()
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            if self.typography.primary_family in available_fonts:
                self.logger.info(f"Successfully installed and configured '{self.typography.primary_family}' font")
                plt.rcParams['font.family'] = self._get_font_list()
                return
                
        except Exception as e:
            self.logger.warning(f"Failed to download Heebo font: {e}")
        
        # Fall back to best available system font
        preferred_fallbacks = ['Helvetica Neue', 'Arial', 'DejaVu Sans', 'Liberation Sans']
        selected_fallback = 'sans-serif'  # Ultimate fallback
        
        for fallback in preferred_fallbacks:
            if fallback in available_fonts:
                selected_fallback = fallback
                break
                
        self.logger.info(f"Using fallback font: {selected_fallback}")
        fallback_fonts = [selected_fallback] + self._get_font_list()[1:]
        plt.rcParams['font.family'] = fallback_fonts
    
    def _download_and_install_heebo(self) -> None:
        """Download and install Heebo font from Google Fonts."""
        import tempfile
        import requests
        import matplotlib.font_manager as fm
        from zipfile import ZipFile
        import os
        
        # Google Fonts download URL for Heebo (all weights)
        font_url = "https://fonts.google.com/download?family=Heebo"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the font zip file
            response = requests.get(font_url, timeout=10)
            response.raise_for_status()
            
            zip_path = os.path.join(temp_dir, "heebo.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract font files
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find and install TTF files
            font_files = []
            for file in os.listdir(temp_dir):
                if file.endswith('.ttf') and 'Heebo' in file:
                    font_path = os.path.join(temp_dir, file)
                    font_files.append(font_path)
                    
                    # Add font to matplotlib font manager
                    fm.fontManager.addfont(font_path)
                    self.logger.debug(f"Added font file: {file}")
            
            if font_files:
                self.logger.info(f"Successfully downloaded and installed {len(font_files)} Heebo font files")
            else:
                raise ValueError("No Heebo font files found in downloaded archive")
    
    def get_title_style(self, mode: str = 'light') -> Dict[str, Any]:
        """
        Get standardized title styling for all charts.
        
        Args:
            mode: 'light' or 'dark'
            
        Returns:
            Dictionary of title styling parameters
        """
        theme = self.get_theme_colors(mode)
        
        return {
            'fontsize': 12,
            'fontweight': 'bold',
            'color': theme.primary_text,
            'pad': 20,
            'fontfamily': self._get_font_list()
        }
    
    def apply_title_style(self, ax, title: str, mode: str = 'light') -> None:
        """
        Apply standardized title styling to an axes object.
        
        Args:
            ax: Matplotlib axes object
            title: Title text
            mode: 'light' or 'dark'
        """
        style = self.get_title_style(mode)
        ax.set_title(title, **style)


def create_theme_manager(config_path: Optional[str] = None) -> ThemeManager:
    """
    Factory function to create a ThemeManager instance.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Configured ThemeManager instance
    """
    return ThemeManager(config_path)


if __name__ == "__main__":
    # Test theme manager
    theme_manager = create_theme_manager()
    
    print("Color Palette:")
    print(f"  Primary: {theme_manager.color_palette.primary_data}")
    print(f"  Secondary: {theme_manager.color_palette.secondary_data}")
    print(f"  Tertiary: {theme_manager.color_palette.tertiary_data}")
    
    print("\nLight Theme:")
    light = theme_manager.light_theme
    print(f"  Background: {light.background}")
    print(f"  Text: {light.primary_text}")
    
    print("\nDark Theme:")
    dark = theme_manager.dark_theme
    print(f"  Background: {dark.background}")
    print(f"  Text: {dark.primary_text}")
    
    print(f"\nColor validation: {theme_manager.validate_colors()}")