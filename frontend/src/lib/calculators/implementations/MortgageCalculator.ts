import {
  BaseCalculator,
  type CalculatorMetadata,
  type CalculatorSchema,
  type CalculatorResult,
} from "../core/Calculator.ts";

export class MortgageCalculator extends BaseCalculator {
  readonly metadata: CalculatorMetadata = {
    id: "mortgage-calculator",
    name: "Mortgage Payment Calculator",
    description:
      "Calculate monthly mortgage payments with principal, interest, taxes, and insurance",
    category: "finance",
    version: "1.0.0",
    author: "Sensylate",
    tags: ["mortgage", "loan", "finance", "payment"],
  };

  readonly schema: CalculatorSchema = {
    inputs: [
      {
        name: "loanAmount",
        type: "number",
        label: "Loan Amount ($)",
        required: true,
        min: 1000,
        max: 10000000,
        step: 1000,
        defaultValue: 300000,
        placeholder: "300,000",
      },
      {
        name: "interestRate",
        type: "number",
        label: "Annual Interest Rate (%)",
        required: true,
        min: 0.1,
        max: 30,
        step: 0.01,
        defaultValue: 6.5,
        placeholder: "6.5",
      },
      {
        name: "loanTermYears",
        type: "select",
        label: "Loan Term (Years)",
        required: true,
        defaultValue: 30,
        options: [
          { value: 15, label: "15 years" },
          { value: 20, label: "20 years" },
          { value: 25, label: "25 years" },
          { value: 30, label: "30 years" },
        ],
      },
      {
        name: "propertyTaxAnnual",
        type: "number",
        label: "Annual Property Tax ($)",
        required: false,
        min: 0,
        max: 100000,
        step: 100,
        defaultValue: 0,
        placeholder: "3,600",
      },
      {
        name: "homeInsuranceAnnual",
        type: "number",
        label: "Annual Home Insurance ($)",
        required: false,
        min: 0,
        max: 50000,
        step: 50,
        defaultValue: 0,
        placeholder: "1,200",
      },
      {
        name: "pmiMonthly",
        type: "number",
        label: "Monthly PMI ($)",
        required: false,
        min: 0,
        max: 1000,
        step: 10,
        defaultValue: 0,
        placeholder: "250",
      },
    ],
    outputs: [
      {
        name: "monthlyPrincipalInterest",
        type: "number",
        label: "Monthly Principal & Interest",
      },
      {
        name: "monthlyPropertyTax",
        type: "number",
        label: "Monthly Property Tax",
      },
      {
        name: "monthlyInsurance",
        type: "number",
        label: "Monthly Insurance",
      },
      {
        name: "monthlyPMI",
        type: "number",
        label: "Monthly PMI",
      },
      {
        name: "totalMonthlyPayment",
        type: "number",
        label: "Total Monthly Payment",
      },
      {
        name: "totalInterestPaid",
        type: "number",
        label: "Total Interest Over Life of Loan",
      },
      {
        name: "totalAmountPaid",
        type: "number",
        label: "Total Amount Paid",
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
      const {
        loanAmount,
        interestRate,
        loanTermYears,
        propertyTaxAnnual = 0,
        homeInsuranceAnnual = 0,
        pmiMonthly = 0,
      } = inputs;

      // Convert to monthly values
      const monthlyInterestRate = interestRate / 100 / 12;
      const numberOfPayments = loanTermYears * 12;

      // Calculate monthly principal and interest using mortgage formula
      let monthlyPrincipalInterest = 0;
      if (monthlyInterestRate > 0) {
        monthlyPrincipalInterest =
          (loanAmount *
            (monthlyInterestRate *
              Math.pow(1 + monthlyInterestRate, numberOfPayments))) /
          (Math.pow(1 + monthlyInterestRate, numberOfPayments) - 1);
      } else {
        // If no interest, just divide principal by number of payments
        monthlyPrincipalInterest = loanAmount / numberOfPayments;
      }

      // Calculate other monthly costs
      const monthlyPropertyTax = propertyTaxAnnual / 12;
      const monthlyInsurance = homeInsuranceAnnual / 12;

      // Calculate totals
      const totalMonthlyPayment =
        monthlyPrincipalInterest +
        monthlyPropertyTax +
        monthlyInsurance +
        pmiMonthly;
      const totalAmountPaid =
        monthlyPrincipalInterest * numberOfPayments +
        propertyTaxAnnual * loanTermYears +
        homeInsuranceAnnual * loanTermYears +
        pmiMonthly * numberOfPayments;
      const totalInterestPaid =
        monthlyPrincipalInterest * numberOfPayments - loanAmount;

      const calculationTime = performance.now() - startTime;

      return {
        success: true,
        data: {
          monthlyPrincipalInterest:
            Math.round(monthlyPrincipalInterest * 100) / 100,
          monthlyPropertyTax: Math.round(monthlyPropertyTax * 100) / 100,
          monthlyInsurance: Math.round(monthlyInsurance * 100) / 100,
          monthlyPMI: pmiMonthly,
          totalMonthlyPayment: Math.round(totalMonthlyPayment * 100) / 100,
          totalInterestPaid: Math.round(totalInterestPaid * 100) / 100,
          totalAmountPaid: Math.round(totalAmountPaid * 100) / 100,
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
}
