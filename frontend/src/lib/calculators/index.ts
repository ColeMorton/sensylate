// Core types and interfaces
export type {
  CalculatorField,
  CalculatorSchema,
  CalculatorMetadata,
  CalculatorConfig,
  CalculatorResult,
} from "./core/Calculator.ts";

export { BaseCalculator } from "./core/Calculator.ts";

// UI and theming
export type {
  CalculatorTheme,
  ThemeColors,
  ThemeSpacing,
  ThemeTypography,
  CalculatorUIProps,
  UIComponentProps,
} from "./core/UIRenderer.ts";

export { defaultTheme, darkTheme } from "./core/UIRenderer.ts";

// Calculator implementations
export { PocketCalculator } from "./implementations/PocketCalculator.ts";
export { MortgageCalculator } from "./implementations/MortgageCalculator.ts";
export { DCACalculator } from "./implementations/DCACalculator.ts";

// Registry
export type { CalculatorRegistryEntry } from "./registry/CalculatorRegistry.ts";
export {
  CalculatorRegistry,
  calculatorRegistry,
} from "./registry/CalculatorRegistry.ts";

// UI Components
export { CalculatorWidget } from "./components/CalculatorWidget.tsx";
export { FieldRenderer } from "./components/FieldRenderer.tsx";
