import type { FundamentalAnalysisData } from "@/types/ChartTypes";

export const mockFundamentalData: Record<string, FundamentalAnalysisData> = {
  GOOGL: {
    company: {
      name: "Alphabet",
      ticker: "GOOGL",
      logo: "/images/logos/googl.svg",
      brandColor: "#EA4335",
    },
    keyMetrics: {
      stockReturn: { value: 18, period: "YoY" },
      grossMargin: 58,
      fcfMargin: 20,
      fairPrice: 183,
      currentPrice: 150,
    },
    financialData: {
      revenue: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [
          182527000000, 257637000000, 282836000000, 307394000000, 328284000000,
        ],
      },
      fcf: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [
          42843000000, 67012000000, 60010000000, 69495000000, 73584000000,
        ],
      },
      revenueSource: {
        categories: ["Search", "YouTube", "Cloud", "Subscriptions"],
        values: [63.3, 11.1, 12.2, 13.3],
        colors: ["#EA4335", "#FBBC05", "#34A853", "#4285F4"],
      },
      geography: {
        regions: ["US", "EMEA", "APAC", "Other"],
        values: [46, 31, 15, 8],
      },
    },
    qualityMetrics: {
      management: 4.0,
      productReviews: 4.5,
      employees: 4.4,
      moat: 5.0,
    },
    financialHealth: {
      revenueGrowth: 12,
      fcfGrowth: 13,
      cashPosition: 72,
      debtToEquity: 0.3,
    },
    prosCons: {
      pros: [
        "Massive product presence",
        "Very strong moat",
        "Dominant in search and ads",
        "Growing cloud business",
      ],
      cons: [
        "Regulatory risks",
        "Ad revenue concentration",
        "AI disrupting search",
        "Multiple strong competitors",
      ],
    },
    valuation: {
      peRatio: 27,
      pegRatio: 1.5,
      evToRevenue: 5.2,
      dcfValue: 195,
      analystTarget: 183,
    },
    balanceSheet: {
      assets: {
        years: [2021, 2022, 2023, 2024],
        values: [359268000000, 365264000000, 402392000000, 430253000000],
      },
      liabilities: {
        years: [2021, 2022, 2023, 2024],
        values: [107633000000, 109120000000, 115371000000, 119013000000],
      },
      equity: {
        years: [2021, 2022, 2023, 2024],
        values: [251635000000, 256144000000, 287021000000, 311240000000],
      },
    },
  },
  NVDA: {
    company: {
      name: "NVIDIA",
      ticker: "NVDA",
      logo: "/images/logos/nvda.svg",
      brandColor: "#76B900",
    },
    keyMetrics: {
      stockReturn: { value: 76, period: "YoY" },
      grossMargin: 70,
      fcfMargin: 48,
      fairPrice: 152,
      currentPrice: 140,
    },
    financialData: {
      revenue: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [
          16675000000, 26914000000, 60922000000, 60922000000, 79774000000,
        ],
      },
      fcf: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [5822000000, 8132000000, 25048000000, 8132000000, 35704000000],
      },
      revenueSource: {
        categories: ["Gaming & Other", "Data Center", "Datacenter", "Other"],
        values: [23, 87, 0, 0],
        colors: ["#76B900", "#228B22", "#32CD32", "#90EE90"],
      },
      geography: {
        regions: ["US", "China", "Taiwan", "Other"],
        values: [21, 20, 24, 35],
      },
    },
    qualityMetrics: {
      management: 5.0,
      productReviews: 4.0,
      employees: 4.4,
      moat: 5.0,
    },
    financialHealth: {
      revenueGrowth: 70,
      fcfGrowth: 75,
      cashPosition: 43,
      debtToEquity: 0.2,
    },
    prosCons: {
      pros: [
        "Well positioned industry leader",
        "Visionary leadership",
        "AI market dominance",
        "Strong R&D capabilities",
      ],
      cons: [
        "Cyclicality",
        "Competitive sector",
        "High valuation",
        "China export restrictions",
      ],
    },
    valuation: {
      peRatio: 65,
      pegRatio: 1.2,
      evToRevenue: 22.5,
      dcfValue: 160,
      analystTarget: 152,
    },
    balanceSheet: {
      assets: {
        years: [2021, 2022, 2023, 2024],
        values: [44187000000, 41182000000, 49579000000, 65728000000],
      },
      liabilities: {
        years: [2021, 2022, 2023, 2024],
        values: [17574000000, 15632000000, 19077000000, 22683000000],
      },
      equity: {
        years: [2021, 2022, 2023, 2024],
        values: [26613000000, 25550000000, 30502000000, 43045000000],
      },
    },
  },
  ASML: {
    company: {
      name: "ASML",
      ticker: "ASML",
      logo: "/images/logos/asml.svg",
      brandColor: "#0066CC",
    },
    keyMetrics: {
      stockReturn: { value: 16, period: "YoY" },
      grossMargin: 52,
      fcfMargin: 30,
      fairPrice: 938,
      currentPrice: 850,
    },
    financialData: {
      revenue: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [
          14000000000, 18611000000, 21173000000, 27564000000, 31200000000,
        ],
      },
      fcf: {
        years: [2020, 2021, 2022, 2023, 2024],
        values: [3500000000, 4200000000, 4800000000, 6500000000, 8800000000],
      },
      revenueSource: {
        categories: ["EUV", "DUV", "Service", "Other"],
        values: [55, 25, 15, 5],
        colors: ["#0066CC", "#4D94FF", "#80B3FF", "#CCE0FF"],
      },
      geography: {
        regions: ["South Korea", "Taiwan", "China", "US"],
        values: [35, 30, 20, 15],
      },
    },
    qualityMetrics: {
      management: 4.5,
      productReviews: 5.4,
      employees: 4.1,
      moat: 5.0,
    },
    financialHealth: {
      revenueGrowth: 46,
      fcfGrowth: 52,
      cashPosition: 5,
      debtToEquity: 0.1,
    },
    prosCons: {
      pros: [
        "Incredibly strong moat",
        "Critical player in the industry",
        "High barriers to entry",
        "Technological leadership",
      ],
      cons: [
        "Prone to geopolitical tension",
        "Cyclicality",
        "China exposure risk",
        "Supply chain complexity",
      ],
    },
    valuation: {
      peRatio: 45,
      pegRatio: 2.1,
      evToRevenue: 12.8,
      dcfValue: 950,
      analystTarget: 938,
    },
    balanceSheet: {
      assets: {
        years: [2021, 2022, 2023, 2024],
        values: [28500000000, 32100000000, 36700000000, 41200000000],
      },
      liabilities: {
        years: [2021, 2022, 2023, 2024],
        values: [12400000000, 13800000000, 15200000000, 16900000000],
      },
      equity: {
        years: [2021, 2022, 2023, 2024],
        values: [16100000000, 18300000000, 21500000000, 24300000000],
      },
    },
  },
};

// Export function to get mock data for a specific ticker
export const getFundamentalMockData = (
  ticker: string,
): FundamentalAnalysisData => {
  return mockFundamentalData[ticker.toUpperCase()] || mockFundamentalData.GOOGL;
};

// Export function to get list of available tickers
export const getAvailableTickers = (): string[] => {
  return Object.keys(mockFundamentalData);
};

// Export default mock data (GOOGL)
export default mockFundamentalData.GOOGL;
