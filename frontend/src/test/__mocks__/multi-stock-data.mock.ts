import type { StockDataRow } from "@/types/ChartTypes";

/**
 * Mock data for multi-stock chart testing
 * Contains realistic stock price data for various test scenarios
 */

// XPEV (XPeng) mock data - Chinese EV company with higher volatility
export const mockXPEVData: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "10.50",
    high: "12.25",
    low: "9.75",
    close: "11.80",
    volume: "15234567",
  },
  {
    date: "2024-01-02",
    open: "11.80",
    high: "13.10",
    low: "11.40",
    close: "12.65",
    volume: "18765432",
  },
  {
    date: "2024-01-03",
    open: "12.65",
    high: "13.90",
    low: "12.20",
    close: "13.45",
    volume: "22341234",
  },
  {
    date: "2024-01-04",
    open: "13.45",
    high: "14.20",
    low: "12.85",
    close: "13.90",
    volume: "19876543",
  },
  {
    date: "2024-01-05",
    open: "13.90",
    high: "15.30",
    low: "13.60",
    close: "14.75",
    volume: "25432198",
  },
  {
    date: "2024-01-08",
    open: "14.75",
    high: "15.80",
    low: "14.20",
    close: "15.25",
    volume: "21987654",
  },
  {
    date: "2024-01-09",
    open: "15.25",
    high: "16.10",
    low: "14.90",
    close: "15.60",
    volume: "18234567",
  },
  {
    date: "2024-01-10",
    open: "15.60",
    high: "16.75",
    low: "15.20",
    close: "16.30",
    volume: "24567890",
  },
];

// NIO mock data - Chinese EV company with different price range
export const mockNIOData: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "6.25",
    high: "6.80",
    low: "6.10",
    close: "6.55",
    volume: "45678912",
  },
  {
    date: "2024-01-02",
    open: "6.55",
    high: "7.20",
    low: "6.40",
    close: "6.95",
    volume: "52134567",
  },
  {
    date: "2024-01-03",
    open: "6.95",
    high: "7.45",
    low: "6.75",
    close: "7.20",
    volume: "48976543",
  },
  {
    date: "2024-01-04",
    open: "7.20",
    high: "7.60",
    low: "6.90",
    close: "7.35",
    volume: "43218765",
  },
  {
    date: "2024-01-05",
    open: "7.35",
    high: "7.90",
    low: "7.15",
    close: "7.65",
    volume: "56789123",
  },
  {
    date: "2024-01-08",
    open: "7.65",
    high: "8.20",
    low: "7.40",
    close: "7.95",
    volume: "49876543",
  },
  {
    date: "2024-01-09",
    open: "7.95",
    high: "8.35",
    low: "7.70",
    close: "8.10",
    volume: "41234567",
  },
  {
    date: "2024-01-10",
    open: "8.10",
    high: "8.50",
    low: "7.85",
    close: "8.25",
    volume: "38765432",
  },
];

// AAPL (Apple) mock data - Large cap tech stock with lower volatility
export const mockAAPLData: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "185.25",
    high: "189.80",
    low: "184.90",
    close: "188.45",
    volume: "67890123",
  },
  {
    date: "2024-01-02",
    open: "188.45",
    high: "192.30",
    low: "187.60",
    close: "191.75",
    volume: "72134567",
  },
  {
    date: "2024-01-03",
    open: "191.75",
    high: "194.20",
    low: "190.85",
    close: "193.60",
    volume: "65432198",
  },
  {
    date: "2024-01-04",
    open: "193.60",
    high: "196.40",
    low: "192.80",
    close: "195.20",
    volume: "69876543",
  },
  {
    date: "2024-01-05",
    open: "195.20",
    high: "198.75",
    low: "194.50",
    close: "197.90",
    volume: "74321098",
  },
  {
    date: "2024-01-08",
    open: "197.90",
    high: "200.60",
    low: "196.80",
    close: "199.35",
    volume: "71234567",
  },
  {
    date: "2024-01-09",
    open: "199.35",
    high: "201.90",
    low: "198.20",
    close: "200.85",
    volume: "68765432",
  },
  {
    date: "2024-01-10",
    open: "200.85",
    high: "203.40",
    low: "199.70",
    close: "202.15",
    volume: "73456789",
  },
];

// MSTR (MicroStrategy) mock data - Volatile Bitcoin proxy stock
export const mockMSTRData: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "520.75",
    high: "545.20",
    low: "515.60",
    close: "538.90",
    volume: "1234567",
  },
  {
    date: "2024-01-02",
    open: "538.90",
    high: "565.40",
    low: "532.80",
    close: "559.30",
    volume: "1456789",
  },
  {
    date: "2024-01-03",
    open: "559.30",
    high: "582.60",
    low: "550.20",
    close: "575.85",
    volume: "1678912",
  },
  {
    date: "2024-01-04",
    open: "575.85",
    high: "598.70",
    low: "568.40",
    close: "592.15",
    volume: "1543210",
  },
  {
    date: "2024-01-05",
    open: "592.15",
    high: "615.90",
    low: "585.30",
    close: "608.45",
    volume: "1789123",
  },
  {
    date: "2024-01-08",
    open: "608.45",
    high: "632.80",
    low: "601.70",
    close: "625.20",
    volume: "1621098",
  },
  {
    date: "2024-01-09",
    open: "625.20",
    high: "648.50",
    low: "618.90",
    close: "641.75",
    volume: "1432156",
  },
  {
    date: "2024-01-10",
    open: "641.75",
    high: "665.30",
    low: "635.40",
    close: "658.90",
    volume: "1789432",
  },
];

// TSLA (Tesla) mock data - High volatility EV leader
export const mockTSLAData: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "238.45",
    high: "248.90",
    low: "235.20",
    close: "245.75",
    volume: "89123456",
  },
  {
    date: "2024-01-02",
    open: "245.75",
    high: "255.60",
    low: "242.30",
    close: "252.40",
    volume: "94567890",
  },
  {
    date: "2024-01-03",
    open: "252.40",
    high: "262.85",
    low: "249.70",
    close: "259.20",
    volume: "87654321",
  },
  {
    date: "2024-01-04",
    open: "259.20",
    high: "268.50",
    low: "255.80",
    close: "265.90",
    volume: "91234567",
  },
  {
    date: "2024-01-05",
    open: "265.90",
    high: "275.30",
    low: "262.40",
    close: "272.15",
    volume: "96789123",
  },
  {
    date: "2024-01-08",
    open: "272.15",
    high: "281.70",
    low: "268.50",
    close: "278.85",
    volume: "89876543",
  },
  {
    date: "2024-01-09",
    open: "278.85",
    high: "288.20",
    low: "275.60",
    close: "285.40",
    volume: "85432198",
  },
  {
    date: "2024-01-10",
    open: "285.40",
    high: "294.90",
    low: "282.70",
    close: "291.65",
    volume: "92345678",
  },
];

// Edge case data for testing
export const mockEmptyData: StockDataRow[] = [];

export const mockSingleDataPoint: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "100.00",
    high: "105.00",
    low: "98.00",
    close: "102.50",
    volume: "1000000",
  },
];

export const mockDataWithMissingValues: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "100.00",
    high: "105.00",
    low: "98.00",
    close: "102.50",
    volume: "1000000",
  },
  {
    date: "2024-01-02",
    open: "",
    high: "107.00",
    low: "101.00",
    close: "105.25",
    volume: "1100000",
  },
  {
    date: "2024-01-03",
    open: "105.25",
    high: "",
    low: "103.50",
    close: "104.75",
    volume: "",
  },
];

export const mockDataWithZeroValues: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "100.00",
    high: "105.00",
    low: "98.00",
    close: "102.50",
    volume: "1000000",
  },
  {
    date: "2024-01-02",
    open: "0",
    high: "107.00",
    low: "101.00",
    close: "0",
    volume: "1100000",
  },
  {
    date: "2024-01-03",
    open: "105.25",
    high: "108.00",
    low: "0",
    close: "106.75",
    volume: "0",
  },
];

export const mockDataWithOutliers: StockDataRow[] = [
  {
    date: "2024-01-01",
    open: "100.00",
    high: "105.00",
    low: "98.00",
    close: "102.50",
    volume: "1000000",
  },
  {
    date: "2024-01-02",
    open: "102.50",
    high: "999999.99",
    low: "101.00",
    close: "103.25",
    volume: "1100000",
  },
  {
    date: "2024-01-03",
    open: "103.25",
    high: "108.00",
    low: "0.01",
    close: "106.75",
    volume: "999999999",
  },
];

// Multi-stock data combinations for different test scenarios
export const mockMultiStockDataXPEVNIO = {
  XPEV: mockXPEVData,
  NIO: mockNIOData,
};

export const mockMultiStockDataThreeSymbols = {
  AAPL: mockAAPLData,
  MSTR: mockMSTRData,
  TSLA: mockTSLAData,
};

export const mockMultiStockDataPartial = {
  XPEV: mockXPEVData,
  NIO: [], // Empty NIO data to test partial scenarios
};

export const mockMultiStockDataWithErrors = {
  XPEV: mockDataWithMissingValues,
  NIO: mockDataWithZeroValues,
};

// Chart configuration mocks
export const mockMultiStockMapping = {
  "xpev-nio-stock-price": ["XPEV", "NIO"],
  "tech-giants-comparison": ["AAPL", "MSTR", "TSLA"],
  "ev-leaders-comparison": ["XPEV", "NIO", "TSLA"],
  "single-symbol-test": ["AAPL"],
  "empty-symbols-test": [],
};

export const mockMultiStockMetadata = {
  "xpev-nio-stock-price": {
    displayName: "XPEV vs NIO Comparison",
    description: "Chinese EV stocks price comparison over 1 year",
    sector: "Electric Vehicles",
    comparisonType: "peer_analysis",
  },
  "tech-giants-comparison": {
    displayName: "Tech Giants Comparison",
    description: "Large cap technology stocks comparison",
    sector: "Technology",
    comparisonType: "sector_analysis",
  },
  "ev-leaders-comparison": {
    displayName: "EV Leaders Comparison",
    description: "Top electric vehicle companies comparison",
    sector: "Electric Vehicles",
    comparisonType: "sector_analysis",
  },
};

export const mockSymbolMetadata = {
  XPEV: {
    name: "XPeng Inc.",
    displayName: "XPeng Price",
    chartType: "xpev-price",
    sector: "Electric Vehicles",
    description: "XPeng Inc. stock price data from Yahoo Finance",
    dataYears: 4,
  },
  NIO: {
    name: "NIO Inc.",
    displayName: "NIO Price",
    chartType: "nio-price",
    sector: "Electric Vehicles",
    description: "NIO Inc. stock price data from Yahoo Finance",
    dataYears: 6,
  },
  AAPL: {
    name: "Apple Inc.",
    displayName: "Apple Price",
    chartType: "apple-price",
    sector: "Technology",
    description: "Apple Inc. stock price data from Yahoo Finance",
    dataYears: 15,
  },
  MSTR: {
    name: "MicroStrategy Inc.",
    displayName: "Strategy Price",
    chartType: "mstr-price",
    sector: "Technology",
    description: "MicroStrategy Inc. stock price data from Yahoo Finance",
    dataYears: 6,
  },
  TSLA: {
    name: "Tesla Inc.",
    displayName: "Tesla Price",
    chartType: "tsla-price",
    sector: "Electric Vehicles",
    description: "Tesla Inc. stock price data from Yahoo Finance",
    dataYears: 10,
  },
};

// Performance testing data (larger datasets)
export const mockLargeDataset: StockDataRow[] = Array.from(
  { length: 1000 },
  (_, i) => {
    const date = new Date(2023, 0, 1);
    date.setDate(date.getDate() + i);
    const basePrice = 100;
    const volatility = 0.02;
    const trend = 0.0001;

    const previousClose =
      i === 0
        ? basePrice
        : basePrice +
          i * trend * basePrice +
          (Math.random() - 0.5) * volatility * basePrice;
    const open = previousClose * (1 + (Math.random() - 0.5) * 0.01);
    const close = open * (1 + (Math.random() - 0.5) * volatility);
    const high = Math.max(open, close) * (1 + Math.random() * 0.005);
    const low = Math.min(open, close) * (1 - Math.random() * 0.005);
    const volume = Math.floor(Math.random() * 100000000 + 10000000);

    return {
      date: date.toISOString().split("T")[0],
      open: open.toFixed(2),
      high: high.toFixed(2),
      low: low.toFixed(2),
      close: close.toFixed(2),
      volume: volume.toString(),
    };
  },
);

// Helper function to create custom mock data
export function createMockStockData(
  symbol: string,
  startDate: string,
  days: number,
  basePrice: number,
  volatility: number = 0.02,
): StockDataRow[] {
  const data: StockDataRow[] = [];
  const start = new Date(startDate);

  for (let i = 0; i < days; i++) {
    const date = new Date(start);
    date.setDate(date.getDate() + i);

    const open = basePrice * (1 + (Math.random() - 0.5) * volatility);
    const close = open * (1 + (Math.random() - 0.5) * volatility);
    const high = Math.max(open, close) * (1 + Math.random() * 0.01);
    const low = Math.min(open, close) * (1 - Math.random() * 0.01);
    const volume = Math.floor(Math.random() * 50000000 + 5000000);

    data.push({
      date: date.toISOString().split("T")[0],
      open: open.toFixed(2),
      high: high.toFixed(2),
      low: low.toFixed(2),
      close: close.toFixed(2),
      volume: volume.toString(),
    });
  }

  return data;
}

// Mock API response helpers
export function createMockApiResponse<T>(
  data: T,
  delay: number = 0,
): Promise<T> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(data), delay);
  });
}

export function createMockApiError(
  message: string,
  delay: number = 0,
): Promise<never> {
  return new Promise((_, reject) => {
    setTimeout(() => reject(new Error(message)), delay);
  });
}

export function createMockAbortError(): Promise<never> {
  return new Promise((_, reject) => {
    const error = new Error("AbortError");
    error.name = "AbortError";
    setTimeout(() => reject(error), 0);
  });
}
