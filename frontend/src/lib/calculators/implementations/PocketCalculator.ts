import {
  BaseCalculator,
  type CalculatorMetadata,
  type CalculatorSchema,
  type CalculatorResult,
} from "../core/Calculator.ts";

export class PocketCalculator extends BaseCalculator {
  readonly metadata: CalculatorMetadata = {
    id: "pocket-calculator",
    name: "Pocket Calculator",
    description: "Basic arithmetic calculator with standard operations",
    category: "math",
    version: "1.0.0",
    author: "Cole Morton",
    tags: ["arithmetic", "basic", "math"],
  };

  readonly schema: CalculatorSchema = {
    inputs: [
      {
        name: "expression",
        type: "text",
        label: "Expression",
        required: true,
        placeholder: "e.g., 2 + 3 * 4",
        validation: (value: string) => {
          if (!value || typeof value !== "string") {
            return "Expression is required";
          }
          if (!/^[0-9+\-*/.() ]+$/.test(value)) {
            return "Expression contains invalid characters";
          }
          return null;
        },
      },
    ],
    outputs: [
      {
        name: "result",
        type: "number",
        label: "Result",
      },
      {
        name: "formattedResult",
        type: "text",
        label: "Formatted Result",
      },
    ],
  };

  calculate(inputs: Record<string, unknown>): CalculatorResult {
    const startTime = performance.now();

    const validationErrors = this.validateInputs(inputs);
    if (validationErrors.length > 0) {
      return {
        success: false,
        error: validationErrors.join(", "),
      };
    }

    try {
      const expression = inputs.expression.trim();

      // Security: Only allow safe mathematical expressions
      const sanitizedExpression = expression.replace(/[^0-9+\-*/.() ]/g, "");

      if (sanitizedExpression !== expression) {
        return {
          success: false,
          error: "Expression contains invalid characters",
        };
      }

      // Evaluate the expression safely
      const result = this.evaluateExpression(sanitizedExpression);

      if (!isFinite(result)) {
        return {
          success: false,
          error: "Result is not a finite number",
        };
      }

      const formattedResult = this.formatNumber(result);
      const calculationTime = performance.now() - startTime;

      return {
        success: true,
        data: {
          result,
          formattedResult,
        },
        metadata: {
          calculationTime,
          timestamp: new Date(),
          version: this.metadata.version,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Calculation failed",
      };
    }
  }

  private evaluateExpression(expression: string): number {
    // Simple expression evaluator - in production, consider using a proper math parser
    try {
      // Remove spaces and validate parentheses
      const cleaned = expression.replace(/\s/g, "");
      if (!this.validateParentheses(cleaned)) {
        throw new Error("Mismatched parentheses");
      }

      // Use Function constructor for safe evaluation (better than eval)
      // This is still not completely safe - consider using a proper math parser library
      const result = Function(`"use strict"; return (${cleaned})`)();
      return Number(result);
    } catch {
      throw new Error("Invalid expression");
    }
  }

  private validateParentheses(expression: string): boolean {
    let count = 0;
    for (const char of expression) {
      if (char === "(") {
        count++;
      }
      if (char === ")") {
        count--;
      }
      if (count < 0) {
        return false;
      }
    }
    return count === 0;
  }

  private formatNumber(num: number): string {
    if (Number.isInteger(num)) {
      return num.toLocaleString();
    }

    // Round to reasonable precision and remove trailing zeros
    const rounded = Number(num.toPrecision(10));
    return rounded.toLocaleString();
  }
}
