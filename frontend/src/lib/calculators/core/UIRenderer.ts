import type {
  CalculatorField,
  CalculatorMetadata,
  CalculatorConfig,
} from "./Calculator.ts";

export interface ThemeColors {
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  error: string;
  success: string;
}

export interface ThemeSpacing {
  xs: string;
  sm: string;
  md: string;
  lg: string;
  xl: string;
}

export interface ThemeTypography {
  fontFamily: string;
  fontSize: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  fontWeight: {
    normal: string;
    medium: string;
    bold: string;
  };
}

export interface CalculatorTheme {
  name: string;
  colors: ThemeColors;
  spacing: ThemeSpacing;
  typography: ThemeTypography;
  borderRadius: string;
  shadow: string;
}

export interface UIComponentProps {
  field: CalculatorField;
  value: unknown;
  error?: string;
  onChange: (value: unknown) => void;
  theme: CalculatorTheme;
  disabled?: boolean;
}

export interface CalculatorUIProps {
  metadata: CalculatorMetadata;
  schema: { inputs: CalculatorField[]; outputs: CalculatorField[] };
  config: CalculatorConfig;
  theme: CalculatorTheme;
  inputs: Record<string, unknown>;
  outputs: Record<string, unknown>;
  errors: Record<string, string>;
  isCalculating: boolean;
  onInputChange: (name: string, value: unknown) => void;
  onCalculate: () => void;
  onReset: () => void;
}

export const defaultTheme: CalculatorTheme = {
  name: "default",
  colors: {
    primary: "#3b82f6",
    secondary: "#6b7280",
    background: "#ffffff",
    surface: "#f9fafb",
    text: "#111827",
    textSecondary: "#6b7280",
    border: "#d1d5db",
    error: "#ef4444",
    success: "#10b981",
  },
  spacing: {
    xs: "0.25rem",
    sm: "0.5rem",
    md: "1rem",
    lg: "1.5rem",
    xl: "2rem",
  },
  typography: {
    fontFamily: "system-ui, -apple-system, sans-serif",
    fontSize: {
      xs: "0.75rem",
      sm: "0.875rem",
      md: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
    },
    fontWeight: {
      normal: "400",
      medium: "500",
      bold: "700",
    },
  },
  borderRadius: "0.375rem",
  shadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
};

export const darkTheme: CalculatorTheme = {
  ...defaultTheme,
  name: "dark",
  colors: {
    primary: "#60a5fa",
    secondary: "#9ca3af",
    background: "#111827",
    surface: "#1f2937",
    text: "#f9fafb",
    textSecondary: "#9ca3af",
    border: "#374151",
    error: "#f87171",
    success: "#34d399",
  },
};
