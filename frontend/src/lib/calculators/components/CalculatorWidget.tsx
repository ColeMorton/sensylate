import React, { useState, useEffect } from "react";
import type { BaseCalculator, CalculatorConfig } from "../core/Calculator.ts";
import { defaultTheme, type CalculatorTheme } from "../core/UIRenderer.ts";
import { calculatorRegistry } from "../registry/CalculatorRegistry.ts";
import { FieldRenderer } from "./FieldRenderer.tsx";

interface CalculatorWidgetProps {
  calculatorId: string;
  config?: CalculatorConfig;
  theme?: CalculatorTheme;
  onResult?: (result: any) => void;
  onError?: (error: string) => void;
}

export const CalculatorWidget: React.FC<CalculatorWidgetProps> = ({
  calculatorId,
  config = {},
  theme = defaultTheme,
  onResult,
  onError,
}) => {
  const [calculator, setCalculator] = useState<BaseCalculator | null>(null);
  const [inputs, setInputs] = useState<Record<string, any>>({});
  const [outputs, setOutputs] = useState<Record<string, any>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isCalculating, setIsCalculating] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);

  // Initialize calculator on client side
  useEffect(() => {
    try {
      if (!calculatorRegistry) {
        setErrors({ general: "Calculator registry not available" });
        return;
      }

      const calcInstance = calculatorRegistry.get(calculatorId);
      if (calcInstance) {
        setCalculator(calcInstance);
        try {
          const defaultInputs = calcInstance.getDefaultInputs();
          setInputs(defaultInputs || {});
        } catch (error) {
          console.error("Error getting default inputs:", error);
          setInputs({});
        }
        // Clear any previous errors
        setErrors({});
      } else {
        setErrors({ general: `Calculator "${calculatorId}" not found` });
      }
    } catch (error) {
      console.error("Error initializing calculator:", error);
      setErrors({ general: "Failed to initialize calculator" });
    }
  }, [calculatorId]);

  const handleInputChange = (name: string, value: any) => {
    setInputs((prev) => ({ ...prev, [name]: value }));

    // Clear field error when user starts typing
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleCalculate = async () => {
    if (!calculator) {
      setErrors({ general: "Calculator not available" });
      return;
    }

    setIsCalculating(true);
    setErrors({});

    try {
      const result = await Promise.resolve(calculator.calculate(inputs));

      if (result.success) {
        setOutputs(result.data || {});
        setLastResult(result);
        onResult?.(result);
      } else {
        const errorMessage = result.error || "Calculation failed";
        setErrors({ general: errorMessage });
        onError?.(errorMessage);
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unexpected error";
      setErrors({ general: errorMessage });
      onError?.(errorMessage);
    } finally {
      setIsCalculating(false);
    }
  };

  const handleReset = () => {
    if (calculator) {
      setInputs(calculator.getDefaultInputs());
    } else {
      setInputs({});
    }
    setOutputs({});
    setErrors({});
    setLastResult(null);
  };

  const hasRequiredInputs =
    calculator && calculator.schema?.inputs
      ? calculator.schema.inputs
          .filter((field) => field.required)
          .every((field) => {
            const value = inputs[field.name];
            return value !== undefined && value !== null && value !== "";
          })
      : false;

  const containerStyle = {
    backgroundColor: theme.colors.background,
    color: theme.colors.text,
    fontFamily: theme.typography.fontFamily,
    borderRadius: theme.borderRadius,
    boxShadow: theme.shadow,
    padding: theme.spacing.lg,
    border: `1px solid ${theme.colors.border}`,
  };

  const buttonStyle = {
    backgroundColor: theme.colors.primary,
    color: theme.colors.background,
    padding: `${theme.spacing.sm} ${theme.spacing.md}`,
    borderRadius: theme.borderRadius,
    border: "none",
    fontSize: theme.typography.fontSize.md,
    fontWeight: theme.typography.fontWeight.medium,
    cursor: "pointer",
    opacity: !hasRequiredInputs || isCalculating ? 0.6 : 1,
    transition: "opacity 0.2s",
  };

  const sectionStyle = {
    marginBottom: theme.spacing.lg,
  };

  const titleStyle = {
    fontSize: theme.typography.fontSize.xl,
    fontWeight: theme.typography.fontWeight.bold,
    marginBottom: theme.spacing.sm,
    color: theme.colors.text,
  };

  const descriptionStyle = {
    fontSize: theme.typography.fontSize.sm,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  };

  const errorStyle = {
    color: theme.colors.error,
    fontSize: theme.typography.fontSize.sm,
    marginTop: theme.spacing.xs,
  };

  // Show loading state while calculator is initializing
  if (!calculator) {
    return (
      <div style={containerStyle} data-testid="calculator-widget">
        {errors.general ? (
          <div style={errorStyle} data-testid="error" role="alert">
            {errors.general}
          </div>
        ) : (
          <div style={{ textAlign: "center", padding: theme.spacing.lg }}>
            <p style={{ color: theme.colors.textSecondary }}>
              Loading calculator...
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={containerStyle} data-testid="calculator-widget">
      {config.showMetadata !== false && (
        <div style={sectionStyle}>
          <h3 style={titleStyle}>{calculator.metadata.name}</h3>
          <p style={descriptionStyle}>{calculator.metadata.description}</p>
        </div>
      )}

      {/* General Error */}
      {errors.general && (
        <div style={errorStyle} data-testid="error" role="alert">
          {errors.general}
        </div>
      )}

      {/* Input Fields */}
      <div style={sectionStyle}>
        <h4
          style={{
            fontSize: theme.typography.fontSize.lg,
            fontWeight: theme.typography.fontWeight.medium,
            marginBottom: theme.spacing.md,
            color: theme.colors.text,
          }}
        >
          Inputs
        </h4>

        <div
          style={{
            display: "grid",
            gap: theme.spacing.md,
            gridTemplateColumns:
              config.layout === "horizontal"
                ? "repeat(auto-fit, minmax(200px, 1fr))"
                : "1fr",
          }}
        >
          {calculator.schema?.inputs?.map((field) => (
            <FieldRenderer
              key={field.name}
              field={field}
              value={inputs[field.name]}
              error={errors[field.name]}
              onChange={(value) => handleInputChange(field.name, value)}
              theme={theme}
              disabled={isCalculating}
            />
          ))}
        </div>
      </div>

      {/* Calculate Button */}
      <div style={{ ...sectionStyle, textAlign: "center" }}>
        <button
          onClick={handleCalculate}
          disabled={!hasRequiredInputs || isCalculating}
          style={buttonStyle}
          data-testid="calculate-button"
          type="submit"
        >
          {isCalculating ? "Calculating..." : "Calculate"}
        </button>

        {Object.keys(outputs).length > 0 && (
          <button
            onClick={handleReset}
            style={{
              ...buttonStyle,
              backgroundColor: theme.colors.secondary,
              marginLeft: theme.spacing.sm,
            }}
            data-testid="reset-button"
            type="reset"
          >
            Reset
          </button>
        )}
      </div>

      {/* Output Fields */}
      {Object.keys(outputs).length > 0 && (
        <div style={sectionStyle}>
          <h4
            style={{
              fontSize: theme.typography.fontSize.lg,
              fontWeight: theme.typography.fontWeight.medium,
              marginBottom: theme.spacing.md,
              color: theme.colors.text,
            }}
          >
            Results
          </h4>

          <div
            style={{
              display: "grid",
              gap: theme.spacing.sm,
              gridTemplateColumns:
                config.layout === "horizontal"
                  ? "repeat(auto-fit, minmax(200px, 1fr))"
                  : "1fr",
            }}
            data-testid="results-container"
          >
            {calculator.schema?.outputs?.map((field) => {
              const value = outputs[field.name];
              if (value === undefined || value === null) {
                return null;
              }

              const formattedValue =
                field.type === "number"
                  ? typeof value === "number"
                    ? value.toLocaleString()
                    : value
                  : value;

              return (
                <div
                  key={field.name}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: theme.spacing.sm,
                    backgroundColor: theme.colors.surface,
                    borderRadius: theme.borderRadius,
                    border: `1px solid ${theme.colors.border}`,
                  }}
                  data-testid={`result-${field.name}`}
                >
                  <span
                    style={{
                      fontSize: theme.typography.fontSize.sm,
                      color: theme.colors.textSecondary,
                    }}
                  >
                    {field.label}:
                  </span>
                  <span
                    style={{
                      fontSize: theme.typography.fontSize.md,
                      fontWeight: theme.typography.fontWeight.medium,
                      color: theme.colors.text,
                    }}
                    data-testid={`result-value-${field.name}`}
                  >
                    {formattedValue}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Metadata */}
          {lastResult?.metadata && config.showMetadata !== false && (
            <div
              style={{
                marginTop: theme.spacing.md,
                padding: theme.spacing.sm,
                backgroundColor: theme.colors.surface,
                borderRadius: theme.borderRadius,
                fontSize: theme.typography.fontSize.xs,
                color: theme.colors.textSecondary,
              }}
            >
              Calculated in {lastResult.metadata.calculationTime?.toFixed(2)}ms
              {lastResult.warnings && lastResult.warnings.length > 0 && (
                <div
                  style={{
                    color: theme.colors.error,
                    marginTop: theme.spacing.xs,
                  }}
                >
                  ⚠️ {lastResult.warnings.join(", ")}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
