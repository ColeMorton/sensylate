import {
  BaseCalculator,
  type CalculatorMetadata,
  type CalculatorSchema,
  type CalculatorResult,
} from "../core/Calculator.ts";

export class DCACalculator extends BaseCalculator {
  readonly metadata: CalculatorMetadata = {
    id: "dca-calculator",
    name: "Dollar Cost Averaging Calculator",
    description:
      "Calculate Bitcoin DCA strategy returns and statistics over time",
    category: "crypto",
    version: "1.0.0",
    author: "Sensylate",
    tags: ["bitcoin", "dca", "investment", "crypto", "dollar-cost-averaging"],
  };

  readonly schema: CalculatorSchema = {
    inputs: [
      {
        name: "weeklyAmount",
        type: "number",
        label: "Weekly Investment Amount ($)",
        required: true,
        min: 1,
        max: 10000,
        step: 1,
        defaultValue: 100,
        placeholder: "100",
      },
      {
        name: "startDate",
        type: "date",
        label: "Start Date",
        required: true,
        defaultValue: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000)
          .toISOString()
          .split("T")[0], // 1 year ago
      },
      {
        name: "endDate",
        type: "date",
        label: "End Date",
        required: true,
        defaultValue: new Date().toISOString().split("T")[0], // Today
      },
      {
        name: "currentBTCPrice",
        type: "number",
        label: "Current BTC Price ($)",
        required: true,
        min: 1,
        max: 1000000,
        step: 0.01,
        defaultValue: 45000,
        placeholder: "45,000",
      },
      {
        name: "avgBTCPrice",
        type: "number",
        label: "Average BTC Price During Period ($)",
        required: true,
        min: 1,
        max: 1000000,
        step: 0.01,
        defaultValue: 35000,
        placeholder: "35,000",
      },
    ],
    outputs: [
      {
        name: "totalInvested",
        type: "number",
        label: "Total Amount Invested",
      },
      {
        name: "totalBTCAccumulated",
        type: "number",
        label: "Total BTC Accumulated",
      },
      {
        name: "currentValue",
        type: "number",
        label: "Current Portfolio Value",
      },
      {
        name: "totalReturn",
        type: "number",
        label: "Total Return ($)",
      },
      {
        name: "totalReturnPercent",
        type: "number",
        label: "Total Return (%)",
      },
      {
        name: "averageCostBasis",
        type: "number",
        label: "Average Cost Basis per BTC",
      },
      {
        name: "weeklyInvestments",
        type: "number",
        label: "Number of Weekly Investments",
      },
      {
        name: "annualizedReturn",
        type: "number",
        label: "Annualized Return (%)",
      },
    ],
  };

  calculate(inputs: Record<string, any>): CalculatorResult {
    const startTime = performance.now();

    const validationErrors = this.validateInputs(inputs);
    if (validationErrors.length > 0) {
      return {
        success: false,
        error: validationErrors.join(", "),
      };
    }

    try {
      const { weeklyAmount, startDate, endDate, currentBTCPrice, avgBTCPrice } =
        inputs;

      const start = new Date(startDate);
      const end = new Date(endDate);

      // Validate date range
      if (start >= end) {
        return {
          success: false,
          error: "End date must be after start date",
        };
      }

      if (end > new Date()) {
        return {
          success: false,
          error: "End date cannot be in the future",
        };
      }

      // Calculate number of weeks between dates
      const timeDiffMs = end.getTime() - start.getTime();
      const weeksDiff = Math.floor(timeDiffMs / (7 * 24 * 60 * 60 * 1000));
      const weeklyInvestments = weeksDiff + 1; // Include start week

      if (weeklyInvestments <= 0) {
        return {
          success: false,
          error: "Investment period must be at least one week",
        };
      }

      // Calculate DCA metrics
      const totalInvested = weeklyAmount * weeklyInvestments;
      const totalBTCAccumulated = totalInvested / avgBTCPrice;
      const currentValue = totalBTCAccumulated * currentBTCPrice;
      const totalReturn = currentValue - totalInvested;
      const totalReturnPercent = (totalReturn / totalInvested) * 100;
      const averageCostBasis = avgBTCPrice;

      // Calculate annualized return
      const yearsInvested = weeklyInvestments / 52.14; // Average weeks per year
      let annualizedReturn = 0;
      if (yearsInvested > 0 && totalInvested > 0) {
        annualizedReturn =
          (Math.pow(currentValue / totalInvested, 1 / yearsInvested) - 1) * 100;
      }

      const calculationTime = performance.now() - startTime;

      return {
        success: true,
        data: {
          totalInvested: Math.round(totalInvested * 100) / 100,
          totalBTCAccumulated:
            Math.round(totalBTCAccumulated * 100000000) / 100000000, // 8 decimal places
          currentValue: Math.round(currentValue * 100) / 100,
          totalReturn: Math.round(totalReturn * 100) / 100,
          totalReturnPercent: Math.round(totalReturnPercent * 100) / 100,
          averageCostBasis: Math.round(averageCostBasis * 100) / 100,
          weeklyInvestments,
          annualizedReturn: Math.round(annualizedReturn * 100) / 100,
        },
        warnings:
          yearsInvested < 1
            ? ["Results may be less accurate for periods under 1 year"]
            : undefined,
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
}
