import type { ThemeColors } from "@/types/ChartTypes";
import themeConfig from "@/config/theme.json";

// Extract colors from theme configuration
export function getThemeColors(isDarkMode: boolean): ThemeColors {
  const theme = isDarkMode
    ? themeConfig.colors.darkmode
    : themeConfig.colors.default;
  const dataColors = themeConfig.colors.data;

  return {
    primary: theme.theme_color.primary,
    body: theme.theme_color.body,
    border: theme.theme_color.border,
    light: theme.theme_color.light,
    dark: theme.theme_color.dark,
    text: theme.text_color.text,
    textDark: theme.text_color["text-dark"],
    textLight: theme.text_color["text-light"],
    primaryData: dataColors.primary_data,
    secondaryData: dataColors.secondary_data,
    tertiaryData: dataColors.tertiary_data,
    quaternary: dataColors.quaternary,
    neutralData: dataColors.neutral_data,
  };
}

// Get chart-specific color palette
export function getChartColors(isDarkMode: boolean) {
  const colors = getThemeColors(isDarkMode);

  return {
    multiStrategy: colors.primaryData, // #00BCD4 - Cyan for multi-strategy
    buyHold: colors.secondaryData, // #9575CD - Purple for buy-and-hold
    drawdown: colors.quaternary, // #FF7043 - Orange for drawdowns/risk
    tertiary: colors.tertiaryData, // #4285F4 - Blue for additional data
    neutral: colors.neutralData, // #90A4AE - Gray for neutral/reference
    text: colors.text,
    textDark: colors.textDark,
    textLight: colors.textLight,
    grid: isDarkMode ? "rgba(156, 163, 175, 0.2)" : "rgba(0, 0, 0, 0.1)",
    tick: isDarkMode ? "#9CA3AF" : "#6B7280",
  };
}

// Generate Plotly layout colors based on theme
export function getPlotlyThemeColors(isDarkMode: boolean) {
  const colors = getThemeColors(isDarkMode);

  return {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: {
      family: '"Inter", ui-sans-serif, system-ui, -apple-system, sans-serif',
      size: 12,
      color: colors.text,
    },
    titleFont: {
      size: 16,
      color: colors.textDark,
    },
    legendBgColor: isDarkMode
      ? "rgba(31, 41, 55, 0.8)"
      : "rgba(255, 255, 255, 0.8)",
    legendBorderColor: isDarkMode
      ? "rgba(156, 163, 175, 0.3)"
      : "rgba(0, 0, 0, 0.2)",
    gridColor: isDarkMode ? "rgba(156, 163, 175, 0.2)" : "rgba(0, 0, 0, 0.1)",
    tickColor: isDarkMode ? "#9CA3AF" : "#6B7280",
  };
}
