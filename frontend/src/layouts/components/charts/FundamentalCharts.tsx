import React from "react";
import type { Data, Layout } from "plotly.js";
import ChartRenderer from "./ChartRenderer";
import ChartContainer from "./ChartContainer";
import MetricCard from "../fundamentals/MetricCard";
import QualityRating from "../fundamentals/QualityRating";
import ProgressBar from "../fundamentals/ProgressBar";
import ProsCons from "../fundamentals/ProsCons";
import type { ChartType, FundamentalAnalysisData } from "@/types/ChartTypes";
import {
  IconTrendingUp,
  IconChartPie3,
  IconPercentage,
  IconCurrencyDollar,
} from "@tabler/icons-react";

interface FundamentalChartProps {
  chartType: ChartType;
  data: FundamentalAnalysisData;
  title?: string;
  className?: string;
}

const FundamentalChart: React.FC<FundamentalChartProps> = ({
  chartType,
  data,
  title,
  className = "",
}) => {
  // Basic validation
  if (!data) {
    return (
      <ChartContainer title={title || "Chart"} className={className}>
        <div className="flex h-full items-center justify-center">
          <p className="text-gray-500">No data available</p>
        </div>
      </ChartContainer>
    );
  }

  console.log(`FundamentalChart [${chartType}] debug:`, {
    chartType,
    title,
    companyName: data?.company?.name,
    ticker: data?.company?.ticker,
  });
  const baseLayoutConfig: Partial<Layout> = {
    autosize: true,
    margin: { l: 50, r: 20, t: 30, b: 40 },
    font: {
      family: '"Inter", ui-sans-serif, system-ui, -apple-system, sans-serif',
      size: 12,
    },
    paper_bgcolor: "rgba(255,255,255,0)",
    plot_bgcolor: "rgba(255,255,255,0)",
    showlegend: true,
    legend: {
      x: 0,
      y: 1,
      xanchor: "left",
      yanchor: "top",
      bgcolor: "rgba(255,255,255,0.9)",
      bordercolor: "rgba(0,0,0,0.1)",
      borderwidth: 1,
      font: { size: 11 },
    },
  };

  switch (chartType) {
    case "fundamental-revenue-fcf": {
      const revenueData = data?.financialData?.revenue;
      const fcfData = data?.financialData?.fcf;

      if (
        !revenueData?.years?.length ||
        !revenueData?.values?.length ||
        !fcfData?.years?.length ||
        !fcfData?.values?.length
      ) {
        return (
          <ChartContainer
            title={title || "Revenue & FCF"}
            className={className}
          >
            <div className="flex h-full items-center justify-center">
              <p className="text-gray-500">No revenue/FCF data available</p>
            </div>
          </ChartContainer>
        );
      }

      // Comprehensive data validation and sanitization
      const validateAndSanitizeData = (
        years: number[],
        values: number[],
        label: string,
      ) => {
        console.log(`${label} Raw Data:`, { years, values });

        if (years.length !== values.length) {
          console.error(`${label}: Years and values length mismatch`, {
            yearsLength: years.length,
            valuesLength: values.length,
          });
          return null;
        }

        const cleanValues = values.map((v, i) => {
          if (typeof v !== "number" || !isFinite(v)) {
            console.error(`${label}: Invalid value at index ${i}:`, v);
            return 0;
          }
          return v;
        });

        const cleanYears = years.map((y, i) => {
          if (typeof y !== "number" || !isFinite(y)) {
            console.error(`${label}: Invalid year at index ${i}:`, y);
            return 2020 + i; // Fallback
          }
          return y;
        });

        console.log(`${label} Clean Data:`, {
          years: cleanYears,
          values: cleanValues,
        });
        return { years: cleanYears, values: cleanValues };
      };

      const cleanRevenue = validateAndSanitizeData(
        revenueData.years,
        revenueData.values,
        "Revenue",
      );
      const cleanFCF = validateAndSanitizeData(
        fcfData.years,
        fcfData.values,
        "FCF",
      );

      if (!cleanRevenue || !cleanFCF) {
        return (
          <ChartContainer
            title={title || "Revenue & FCF"}
            className={className}
          >
            <div className="flex h-full items-center justify-center">
              <p className="text-red-500">Data validation failed</p>
            </div>
          </ChartContainer>
        );
      }

      // Convert to billions with validation
      const revenueBillions = cleanRevenue.values.map((v) => {
        const billions = v / 1e9;
        if (!isFinite(billions)) {
          console.error(
            "Revenue billions conversion failed:",
            v,
            "->",
            billions,
          );
          return 0;
        }
        return billions;
      });

      const fcfBillions = cleanFCF.values.map((v) => {
        const billions = v / 1e9;
        if (!isFinite(billions)) {
          console.error("FCF billions conversion failed:", v, "->", billions);
          return 0;
        }
        return billions;
      });

      console.log("Revenue & FCF Billions Data:", {
        revenueBillions,
        fcfBillions,
      });

      const chartData: Data[] = [
        {
          type: "scatter",
          mode: "lines+markers",
          name: "Revenue",
          x: cleanRevenue.years,
          y: revenueBillions,
          line: { color: "#FF5252", shape: "spline", width: 3 },
          marker: { size: 6 },
        },
        {
          type: "scatter",
          mode: "lines+markers",
          name: "Free cash flow",
          x: cleanFCF.years,
          y: fcfBillions,
          line: { color: "#2196F3", shape: "spline", width: 3 },
          marker: { size: 6 },
        },
      ];

      console.log("Revenue & FCF Final Chart Data:", chartData);

      // Minimal layout configuration for debugging
      const layout: Partial<Layout> = {
        autosize: true,
        showlegend: false, // Remove legend as requested
        margin: { l: 40, r: 20, t: 20, b: 40 }, // Tighter margins for export
        font: { family: "Arial, sans-serif", size: 12 },
        paper_bgcolor: "rgba(255,255,255,0.1)", // Slight visibility for debugging
        plot_bgcolor: "rgba(255,255,255,0.1)",
        xaxis: {
          title: "Year",
          gridcolor: "rgba(0,0,0,0.1)",
        },
        yaxis: {
          title: "Billions ($)",
          gridcolor: "rgba(0,0,0,0.1)",
        },
      };

      console.log("Revenue & FCF Layout Config:", layout);

      // Configuration for ChartRenderer
      const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false,
      };

      return (
        <ChartContainer title={title || "Revenue & FCF"} className={className}>
          <ChartRenderer
            data={chartData}
            layout={layout}
            config={config}
            loading={false}
            error={null}
          />
        </ChartContainer>
      );
    }

    case "fundamental-revenue-source": {
      const revenueSourceData = data?.financialData?.revenueSource;

      if (
        !revenueSourceData?.categories?.length ||
        !revenueSourceData?.values?.length
      ) {
        return (
          <ChartContainer
            title={title || "Revenue Source"}
            className={className}
          >
            <div className="flex h-full items-center justify-center">
              <p className="text-gray-500">No revenue source data available</p>
            </div>
          </ChartContainer>
        );
      }

      console.log("Revenue Source Raw Data:", {
        categories: revenueSourceData.categories,
        values: revenueSourceData.values,
        colors: revenueSourceData.colors,
      });

      // Validate pie chart data
      if (
        revenueSourceData.categories.length !== revenueSourceData.values.length
      ) {
        console.error("Revenue Source: Categories and values length mismatch");
        return (
          <ChartContainer
            title={title || "Revenue Source"}
            className={className}
          >
            <div className="flex h-full items-center justify-center">
              <p className="text-red-500">Data length mismatch</p>
            </div>
          </ChartContainer>
        );
      }

      // Validate and clean values
      const cleanValues = revenueSourceData.values.map((v, i) => {
        if (typeof v !== "number" || !isFinite(v) || v < 0) {
          console.error(`Revenue Source: Invalid value at index ${i}:`, v);
          return 0;
        }
        return v;
      });

      console.log("Revenue Source Clean Values:", cleanValues);

      const chartData: Data[] = [
        {
          type: "pie",
          labels: revenueSourceData.categories,
          values: cleanValues,
          hole: 0.4, // Reduced hole size for better visibility
          textposition: "auto",
          textinfo: "label+percent",
          marker: {
            colors: revenueSourceData.colors || [
              "#FF5252",
              "#FFC107",
              "#4CAF50",
              "#2196F3",
              "#9C27B0",
            ],
            line: { color: "#FFFFFF", width: 2 },
          },
        },
      ];

      console.log("Revenue Source Final Chart Data:", chartData);

      const layout: Partial<Layout> = {
        autosize: true,
        margin: { l: 20, r: 20, t: 20, b: 20 }, // Tighter margins for export
        font: { family: "Arial, sans-serif", size: 12 },
        paper_bgcolor: "rgba(255,255,255,0.1)",
        showlegend: false,
      };

      console.log("Revenue Source Layout Config:", layout);

      // Configuration for ChartRenderer
      const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false,
      };

      return (
        <ChartContainer title={title || "Revenue Source"} className={className}>
          <ChartRenderer
            data={chartData}
            layout={layout}
            config={config}
            loading={false}
            error={null}
          />
        </ChartContainer>
      );
    }

    case "fundamental-geography": {
      const geographyData = data?.financialData?.geography;

      if (!geographyData?.regions?.length || !geographyData?.values?.length) {
        return (
          <ChartContainer title={title || "Geography"} className={className}>
            <div className="flex h-full items-center justify-center">
              <p className="text-gray-500">No geography data available</p>
            </div>
          </ChartContainer>
        );
      }

      console.log("Geography Raw Data:", {
        regions: geographyData.regions,
        values: geographyData.values,
      });

      // Validate data lengths match
      if (geographyData.regions.length !== geographyData.values.length) {
        console.error("Geography: Regions and values length mismatch");
        return (
          <ChartContainer title={title || "Geography"} className={className}>
            <div className="flex h-full items-center justify-center">
              <p className="text-red-500">Geography data mismatch</p>
            </div>
          </ChartContainer>
        );
      }

      // Clean and validate values
      const cleanValues = geographyData.values.map((v, i) => {
        if (typeof v !== "number" || !isFinite(v) || v < 0) {
          console.error(`Geography: Invalid value at index ${i}:`, v);
          return 1; // Minimum size for visibility
        }
        return Math.max(1, v); // Ensure positive values
      });

      const numRegions = geographyData.regions.length;
      const positions = {
        x: [0.25, 0.75, 0.25, 0.75].slice(0, numRegions),
        y: [0.75, 0.75, 0.25, 0.25].slice(0, numRegions),
      };

      console.log("Geography Clean Data:", {
        cleanValues,
        positions,
        numRegions,
      });

      const chartData: Data[] = [
        {
          type: "scatter",
          mode: "markers+text",
          x: positions.x,
          y: positions.y,
          text: geographyData.regions.map(
            (region, i) => `${region}<br>${cleanValues[i]}%`,
          ),
          textposition: "middle center",
          textfont: { size: 12, color: "#FFFFFF" },
          marker: {
            size: cleanValues.map((v) => Math.max(30, v * 1.5)), // Ensure minimum visibility
            sizemode: "diameter",
            color: ["#FF5252", "#FFC107", "#4CAF50", "#2196F3"].slice(
              0,
              numRegions,
            ),
            opacity: 0.8,
            line: { color: "#FFFFFF", width: 2 },
          },
          showlegend: false,
        },
      ];

      console.log("Geography Final Chart Data:", chartData);

      const layout: Partial<Layout> = {
        autosize: true,
        margin: { l: 10, r: 10, t: 20, b: 10 }, // Very tight margins for bubble chart
        font: { family: "Arial, sans-serif", size: 12 },
        paper_bgcolor: "rgba(255,255,255,0.1)",
        xaxis: {
          visible: false,
          range: [0, 1],
          fixedrange: true,
        },
        yaxis: {
          visible: false,
          range: [0, 1],
          fixedrange: true,
        },
      };

      console.log("Geography Layout Config:", layout);

      // Configuration for ChartRenderer
      const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false,
      };

      return (
        <ChartContainer title={title || "Geography"} className={className}>
          <ChartRenderer
            data={chartData}
            layout={layout}
            config={config}
            loading={false}
            error={null}
          />
        </ChartContainer>
      );
    }

    case "fundamental-key-metrics": {
      // This is handled by MetricCard components for header - 4 metrics in horizontal row
      return (
        <div className={`grid grid-cols-4 gap-6 ${className}`}>
          <MetricCard
            icon={IconTrendingUp}
            value={`${data.keyMetrics.stockReturn.value > 0 ? "+" : ""}${data.keyMetrics.stockReturn.value}%`}
            label={`${data.keyMetrics.stockReturn.period} stock return`}
            trend={data.keyMetrics.stockReturn.value > 0 ? "up" : "down"}
          />
          <MetricCard
            icon={IconChartPie3}
            value={`${data.keyMetrics.grossMargin}%`}
            label="Gross margin"
            trend="neutral"
          />
          <MetricCard
            icon={IconPercentage}
            value={`${data.keyMetrics.fcfMargin}%`}
            label="FCF margin"
            trend="neutral"
          />
          <MetricCard
            icon={IconCurrencyDollar}
            value={`$${data.keyMetrics.fairPrice}`}
            label="Est. Fair price"
            trend={
              data.keyMetrics.fairPrice > data.keyMetrics.currentPrice
                ? "up"
                : "down"
            }
          />
        </div>
      );
    }

    case "fundamental-key-metrics-expanded": {
      // Expanded key metrics section for the main grid
      return (
        <ChartContainer title={title || "Key metrics"} className={className}>
          <div className="space-y-3">
            <ProgressBar
              label="Cloud growth"
              value={28}
              color="green"
              suffix="%"
            />
            <ProgressBar
              label="YouTube ad revenue"
              value={10}
              color="green"
              suffix="%"
            />
            <ProgressBar
              label="Search revenue"
              value={10}
              color="green"
              suffix="%"
            />
          </div>
        </ChartContainer>
      );
    }

    case "fundamental-quality-rating": {
      return (
        <ChartContainer title={title || "Quality"} className={className}>
          <div className="space-y-3">
            <QualityRating
              category="Management"
              rating={data.qualityMetrics.management}
            />
            <QualityRating
              category="Product reviews"
              rating={data.qualityMetrics.productReviews}
            />
            <QualityRating
              category="Employees"
              rating={data.qualityMetrics.employees}
            />
            <QualityRating category="Moat" rating={data.qualityMetrics.moat} />
          </div>
        </ChartContainer>
      );
    }

    case "fundamental-financial-health": {
      return (
        <ChartContainer title={title || "Financials"} className={className}>
          <div className="space-y-1">
            <ProgressBar
              label="Revenue growth"
              value={data.financialHealth.revenueGrowth}
              color={data.financialHealth.revenueGrowth > 0 ? "green" : "red"}
            />
            <ProgressBar
              label="Free cash flow growth"
              value={data.financialHealth.fcfGrowth}
              color={data.financialHealth.fcfGrowth > 0 ? "green" : "red"}
            />
            <ProgressBar
              label="Cash and investments"
              value={data.financialHealth.cashPosition}
              color="blue"
              suffix="bn"
              showPercentage={false}
            />
          </div>
        </ChartContainer>
      );
    }

    case "fundamental-pros-cons": {
      return (
        <ChartContainer title={title || "Pros & Cons"} className={className}>
          <ProsCons pros={data.prosCons.pros} cons={data.prosCons.cons} />
        </ChartContainer>
      );
    }

    case "fundamental-valuation": {
      const chartData: Data[] = [
        {
          type: "bar",
          x: ["P/E", "PEG", "EV/Rev", "DCF", "Analyst"],
          y: [
            data.valuation.peRatio,
            data.valuation.pegRatio,
            data.valuation.evToRevenue,
            data.valuation.dcfValue,
            data.valuation.analystTarget,
          ],
          marker: {
            color: ["#2196F3", "#4CAF50", "#FFC107", "#9C27B0", "#FF5252"],
          },
        },
      ];

      const layout: Partial<Layout> = {
        ...baseLayoutConfig,
        title: { text: title || "Valuation", font: { size: 16 } },
        xaxis: { gridcolor: "rgba(0,0,0,0.05)" },
        yaxis: {
          title: "Value ($)",
          gridcolor: "rgba(0,0,0,0.05)",
          tickformat: "$,.0f",
        },
        showlegend: false,
      };

      // Configuration for ChartRenderer
      const config = {
        responsive: true,
        displayModeBar: false,
        displaylogo: false,
      };

      return (
        <ChartContainer title={title || "Valuation"} className={className}>
          <ChartRenderer
            data={chartData}
            layout={layout}
            config={config}
            loading={false}
            error={null}
          />
        </ChartContainer>
      );
    }

    case "fundamental-valuation-a": {
      return (
        <ChartContainer title={title || "Valuation A"} className={className}>
          <div className="space-y-4">
            <div className="text-center">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Based on future FCF growth at a discount rate of 8.5%
              </p>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Next 10y FCF growth:</span>
                <span className="font-bold">11%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Terminal multiple:</span>
                <span className="font-bold">15x</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Discount rate:</span>
                <span className="font-bold">8.5%</span>
              </div>
            </div>
            <div className="border-t pt-2">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">$183</div>
                <div className="text-sm text-gray-600">Fair value</div>
              </div>
            </div>
          </div>
        </ChartContainer>
      );
    }

    case "fundamental-valuation-b": {
      return (
        <ChartContainer title={title || "Valuation B"} className={className}>
          <div className="space-y-4">
            <div className="text-center">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Based on avg industry multiple over the next 10 years
              </p>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Next 10y EPS growth:</span>
                <span className="font-bold">11%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Terminal multiple:</span>
                <span className="font-bold">20x</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Discount rate:</span>
                <span className="font-bold">8.5%</span>
              </div>
            </div>
            <div className="border-t pt-2">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">$183</div>
                <div className="text-sm text-gray-600">Fair value</div>
              </div>
            </div>
          </div>
        </ChartContainer>
      );
    }

    default:
      return (
        <ChartContainer title="Unknown Chart" className={className}>
          <div className="flex h-full items-center justify-center">
            <p className="text-gray-500">
              Chart type not implemented: {chartType}
            </p>
          </div>
        </ChartContainer>
      );
  }
};

export default FundamentalChart;
