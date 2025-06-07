import React from "react";
import type { CalculatorField } from "../core/Calculator.ts";
import type { CalculatorTheme } from "../core/UIRenderer.ts";

interface FieldRendererProps {
  field: CalculatorField;
  value: any;
  error?: string;
  onChange: (value: any) => void;
  theme: CalculatorTheme;
  disabled?: boolean;
}

export const FieldRenderer: React.FC<FieldRendererProps> = ({
  field,
  value,
  error,
  onChange,
  theme,
  disabled = false,
}) => {
  const baseInputStyle = {
    width: "100%",
    padding: theme.spacing.sm,
    border: `1px solid ${error ? theme.colors.error : theme.colors.border}`,
    borderRadius: theme.borderRadius,
    fontSize: theme.typography.fontSize.md,
    backgroundColor: disabled ? theme.colors.surface : theme.colors.background,
    color: theme.colors.text,
    fontFamily: theme.typography.fontFamily,
    outline: "none",
    transition: "border-color 0.2s",
    opacity: disabled ? 0.6 : 1,
  };

  const labelStyle = {
    display: "block",
    marginBottom: theme.spacing.xs,
    fontSize: theme.typography.fontSize.sm,
    fontWeight: theme.typography.fontWeight.medium,
    color: theme.colors.text,
  };

  const errorStyle = {
    color: theme.colors.error,
    fontSize: theme.typography.fontSize.xs,
    marginTop: theme.spacing.xs,
  };

  const requiredStyle = {
    color: theme.colors.error,
    marginLeft: theme.spacing.xs,
  };

  const handleChange = (
    event: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >,
  ) => {
    let newValue: any = event.target.value;

    if (field.type === "number") {
      newValue = newValue === "" ? undefined : Number(newValue);
    } else if (field.type === "boolean") {
      newValue = (event.target as HTMLInputElement).checked;
    }

    onChange(newValue);
  };

  const renderField = () => {
    switch (field.type) {
      case "number":
        return (
          <input
            type="number"
            value={value ?? ""}
            onChange={handleChange}
            placeholder={field.placeholder}
            min={field.min}
            max={field.max}
            step={field.step}
            disabled={disabled}
            style={baseInputStyle}
          />
        );

      case "text":
        return (
          <input
            type="text"
            value={value ?? ""}
            onChange={handleChange}
            placeholder={field.placeholder}
            disabled={disabled}
            style={baseInputStyle}
          />
        );

      case "date":
        return (
          <input
            type="date"
            value={value ?? ""}
            onChange={handleChange}
            disabled={disabled}
            style={baseInputStyle}
          />
        );

      case "boolean":
        return (
          <label
            style={{
              display: "flex",
              alignItems: "center",
              cursor: disabled ? "not-allowed" : "pointer",
              opacity: disabled ? 0.6 : 1,
            }}
          >
            <input
              type="checkbox"
              checked={value ?? false}
              onChange={handleChange}
              disabled={disabled}
              style={{
                marginRight: theme.spacing.sm,
                accentColor: theme.colors.primary,
              }}
            />
            <span
              style={{
                fontSize: theme.typography.fontSize.sm,
                color: theme.colors.text,
              }}
            >
              {field.label}
            </span>
          </label>
        );

      case "select":
        return (
          <select
            value={value ?? ""}
            onChange={handleChange}
            disabled={disabled}
            style={{
              ...baseInputStyle,
              cursor: disabled ? "not-allowed" : "pointer",
            }}
          >
            <option value="">Select an option...</option>
            {field.options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );

      default:
        return (
          <input
            type="text"
            value={value ?? ""}
            onChange={handleChange}
            placeholder={field.placeholder}
            disabled={disabled}
            style={baseInputStyle}
          />
        );
    }
  };

  if (field.type === "boolean") {
    return (
      <div>
        {renderField()}
        {error && <div style={errorStyle}>{error}</div>}
      </div>
    );
  }

  return (
    <div>
      <label style={labelStyle}>
        {field.label}
        {field.required && <span style={requiredStyle}>*</span>}
      </label>
      {renderField()}
      {error && <div style={errorStyle}>{error}</div>}
    </div>
  );
};
