export interface CalculatorField {
  name: string;
  type: "number" | "text" | "select" | "boolean" | "date";
  label: string;
  required?: boolean;
  placeholder?: string;
  min?: number;
  max?: number;
  step?: number;
  options?: { value: string | number; label: string }[];
  defaultValue?: any;
  validation?: (value: any) => string | null;
}

export interface CalculatorSchema {
  inputs: CalculatorField[];
  outputs: CalculatorField[];
}

export interface CalculatorMetadata {
  id: string;
  name: string;
  description: string;
  category: string;
  version: string;
  author?: string;
  tags?: string[];
}

export interface CalculatorConfig {
  theme?: string;
  layout?: "vertical" | "horizontal" | "grid";
  showMetadata?: boolean;
  customStyles?: Record<string, any>;
}

export interface CalculatorResult {
  success: boolean;
  data?: Record<string, any>;
  error?: string;
  warnings?: string[];
  metadata?: {
    calculationTime?: number;
    timestamp?: Date;
    version?: string;
  };
}

export abstract class BaseCalculator {
  abstract readonly metadata: CalculatorMetadata;
  abstract readonly schema: CalculatorSchema;

  abstract calculate(
    inputs: Record<string, any>,
  ): Promise<CalculatorResult> | CalculatorResult;

  validateInputs(inputs: Record<string, any>): string[] {
    const errors: string[] = [];

    for (const field of this.schema.inputs) {
      const value = inputs[field.name];

      if (
        field.required &&
        (value === undefined || value === null || value === "")
      ) {
        errors.push(`${field.label} is required`);
        continue;
      }

      if (value !== undefined && value !== null && value !== "") {
        if (field.type === "number") {
          const numValue = Number(value);
          if (isNaN(numValue)) {
            errors.push(`${field.label} must be a number`);
          } else {
            if (field.min !== undefined && numValue < field.min) {
              errors.push(`${field.label} must be at least ${field.min}`);
            }
            if (field.max !== undefined && numValue > field.max) {
              errors.push(`${field.label} must be at most ${field.max}`);
            }
          }
        }

        if (field.validation) {
          const validationError = field.validation(value);
          if (validationError) {
            errors.push(validationError);
          }
        }
      }
    }

    return errors;
  }

  getDefaultInputs(): Record<string, any> {
    const defaults: Record<string, any> = {};
    for (const field of this.schema.inputs) {
      if (field.defaultValue !== undefined) {
        defaults[field.name] = field.defaultValue;
      }
    }
    return defaults;
  }
}
