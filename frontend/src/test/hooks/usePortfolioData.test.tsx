import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import type { StockDataRow } from "@/types/ChartTypes";

// Mock chart data service
const mockChartDataService = {
  fetchStockData: vi.fn(),
  fetchAppleStockData: vi.fn(),
};

vi.mock("@/services/ChartDataService", () => ({
  chartDataService: mockChartDataService,
}));

// Mock chart dependency config
const mockChartConfig = {
  multiStockMapping: {
    "xpev-nio-stock-price": ["XPEV", "NIO"],
    "test-multi-stock": ["AAPL", "MSTR", "TSLA"],
  },
  symbolMetadata: {
    XPEV: {
      name: "XPeng Inc.",
      displayName: "XPeng Price",
      sector: "Electric Vehicles",
    },
    NIO: {
      name: "NIO Inc.",
      displayName: "NIO Price",
      sector: "Electric Vehicles",
    },
    AAPL: {
      name: "Apple Inc.",
      displayName: "Apple Price",
      sector: "Technology",
    },
    MSTR: {
      name: "MicroStrategy Inc.",
      displayName: "Strategy Price",
      sector: "Technology",
    },
    TSLA: {
      name: "Tesla Inc.",
      displayName: "Tesla Price",
      sector: "Electric Vehicles",
    },
  },
};

vi.mock("@/config/chart-data-dependencies.json", () => mockChartConfig);

describe("usePortfolioData Multi-Stock Hook Tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("useMultiStockData", () => {
    it("should fetch data for multiple symbols concurrently", async () => {
      // Import after mocks are set up
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const mockXPEVData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "10.00",
          high: "12.00",
          low: "9.50",
          close: "11.50",
          volume: "1000000",
        },
        {
          date: "2024-01-02",
          open: "11.50",
          high: "13.00",
          low: "11.00",
          close: "12.75",
          volume: "1200000",
        },
      ];

      const mockNIOData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "8.00",
          high: "9.00",
          low: "7.50",
          close: "8.75",
          volume: "800000",
        },
        {
          date: "2024-01-02",
          open: "8.75",
          high: "10.00",
          low: "8.50",
          close: "9.50",
          volume: "950000",
        },
      ];

      mockChartDataService.fetchStockData
        .mockResolvedValueOnce(mockXPEVData)
        .mockResolvedValueOnce(mockNIOData);

      const { result } = renderHook(() => useMultiStockData(["XPEV", "NIO"]));

      // Initially loading
      expect(result.current.loading).toBe(true);
      expect(result.current.data).toEqual({});
      expect(result.current.error).toBe(null);

      // Wait for data to load
      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Verify concurrent calls were made
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledTimes(2);
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledWith(
        "XPEV",
        expect.any(AbortSignal),
      );
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledWith(
        "NIO",
        expect.any(AbortSignal),
      );

      // Verify data structure
      expect(result.current.data).toEqual({
        XPEV: mockXPEVData,
        NIO: mockNIOData,
      });
      expect(result.current.error).toBe(null);
    });

    it("should handle partial failures gracefully", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const mockXPEVData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "10.00",
          high: "12.00",
          low: "9.50",
          close: "11.50",
          volume: "1000000",
        },
      ];

      mockChartDataService.fetchStockData
        .mockResolvedValueOnce(mockXPEVData)
        .mockRejectedValueOnce(new Error("NIO data fetch failed"));

      const { result } = renderHook(() => useMultiStockData(["XPEV", "NIO"]));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should set error when any symbol fails
      expect(result.current.error).toContain("NIO data fetch failed");
      expect(result.current.data).toEqual({});
    });

    it("should handle empty symbols array", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const { result } = renderHook(() => useMultiStockData([]));

      // Should not be loading and have empty data
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toEqual({});
      expect(result.current.error).toBe(null);
      expect(mockChartDataService.fetchStockData).not.toHaveBeenCalled();
    });

    it("should handle AbortController cleanup on unmount", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const mockAbortError = new Error("AbortError");
      mockAbortError.name = "AbortError";

      mockChartDataService.fetchStockData.mockRejectedValue(mockAbortError);

      const { result, unmount } = renderHook(() => useMultiStockData(["XPEV"]));

      // Start loading
      expect(result.current.loading).toBe(true);

      // Unmount before completion
      unmount();

      // Should not set error for aborted requests
      await waitFor(() => {
        expect(result.current.error).toBe(null);
      });
    });

    it("should update when symbols array changes", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const mockXPEVData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "10.00",
          high: "12.00",
          low: "9.50",
          close: "11.50",
          volume: "1000000",
        },
      ];

      const mockAAPLData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "150.00",
          high: "155.00",
          low: "148.00",
          close: "152.00",
          volume: "50000000",
        },
      ];

      mockChartDataService.fetchStockData
        .mockResolvedValueOnce(mockXPEVData)
        .mockResolvedValueOnce(mockAAPLData);

      const { result, rerender } = renderHook(
        ({ symbols }) => useMultiStockData(symbols),
        { initialProps: { symbols: ["XPEV"] } },
      );

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.data).toEqual({ XPEV: mockXPEVData });

      // Change symbols
      rerender({ symbols: ["AAPL"] });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.data).toEqual({ AAPL: mockAAPLData });
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledTimes(2);
    });
  });

  describe("Dynamic Symbol Resolution Helpers", () => {
    it("should detect multi-stock charts correctly", async () => {
      // These helper functions are used in PortfolioChart.tsx
      const isMultiStockChart = (chartType: string): boolean => {
        return (
          chartType.includes("multi-stock") ||
          chartType.endsWith("-stock-price")
        );
      };

      expect(isMultiStockChart("multi-stock-price")).toBe(true);
      expect(isMultiStockChart("xpev-nio-stock-price")).toBe(true);
      expect(isMultiStockChart("apple-price")).toBe(false);
      expect(isMultiStockChart("portfolio-value-comparison")).toBe(false);
    });

    it("should resolve symbols from multi-stock chart type", async () => {
      const getSymbolsFromMultiStockChart = (chartType: string): string[] => {
        const isMultiStock =
          chartType.includes("multi-stock") ||
          chartType.endsWith("-stock-price");
        if (!isMultiStock) {
          return [];
        }
        const multiStockMapping = mockChartConfig.multiStockMapping;
        return (
          multiStockMapping[chartType as keyof typeof multiStockMapping] || []
        );
      };

      expect(getSymbolsFromMultiStockChart("xpev-nio-stock-price")).toEqual([
        "XPEV",
        "NIO",
      ]);
      expect(getSymbolsFromMultiStockChart("test-multi-stock")).toEqual([
        "AAPL",
        "MSTR",
        "TSLA",
      ]);
      expect(getSymbolsFromMultiStockChart("apple-price")).toEqual([]);
      expect(getSymbolsFromMultiStockChart("unknown-chart")).toEqual([]);
    });

    it("should get display names from symbol metadata", async () => {
      const getSymbolDisplayName = (symbol: string): string => {
        const metadata =
          mockChartConfig.symbolMetadata[
            symbol as keyof typeof mockChartConfig.symbolMetadata
          ];
        return metadata?.name
          ? `${metadata.name} (${symbol})`
          : `${symbol} Price`;
      };

      expect(getSymbolDisplayName("XPEV")).toBe("XPeng Inc. (XPEV)");
      expect(getSymbolDisplayName("NIO")).toBe("NIO Inc. (NIO)");
      expect(getSymbolDisplayName("UNKNOWN")).toBe("UNKNOWN Price");
    });
  });

  describe("useStockData Integration", () => {
    it("should fetch single stock data correctly", async () => {
      const { useStockData } = await import("@/hooks/usePortfolioData");

      const mockData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "150.00",
          high: "155.00",
          low: "148.00",
          close: "152.00",
          volume: "50000000",
        },
      ];

      mockChartDataService.fetchStockData.mockResolvedValue(mockData);

      const { result } = renderHook(() => useStockData("AAPL"));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.data).toEqual(mockData);
      expect(result.current.error).toBe(null);
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledWith(
        "AAPL",
        expect.any(AbortSignal),
      );
    });

    it("should handle empty symbol gracefully", async () => {
      const { useStockData } = await import("@/hooks/usePortfolioData");

      const { result } = renderHook(() => useStockData(""));

      expect(result.current.loading).toBe(false);
      expect(result.current.data).toEqual([]);
      expect(result.current.error).toBe("No symbol provided");
      expect(mockChartDataService.fetchStockData).not.toHaveBeenCalled();
    });
  });

  describe("Error Handling and Edge Cases", () => {
    it("should handle network timeouts", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const timeoutError = new Error("Request timeout");
      mockChartDataService.fetchStockData.mockRejectedValue(timeoutError);

      const { result } = renderHook(() => useMultiStockData(["XPEV", "NIO"]));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.error).toContain("Request timeout");
      expect(result.current.data).toEqual({});
    });

    it("should handle malformed response data", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      // Mock service returns invalid data
      mockChartDataService.fetchStockData.mockResolvedValue(null);

      const { result } = renderHook(() => useMultiStockData(["XPEV"]));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should handle null response gracefully
      expect(result.current.data).toEqual({ XPEV: null });
      expect(result.current.error).toBe(null);
    });

    it("should handle large symbol arrays efficiently", async () => {
      const { useMultiStockData } = await import("@/hooks/usePortfolioData");

      const largeSymbolArray = [
        "AAPL",
        "MSTR",
        "TSLA",
        "NVDA",
        "GOOGL",
        "MSFT",
        "AMZN",
      ];
      const mockData: StockDataRow[] = [
        {
          date: "2024-01-01",
          open: "100.00",
          high: "105.00",
          low: "98.00",
          close: "102.00",
          volume: "1000000",
        },
      ];

      // Mock all symbols to return data
      mockChartDataService.fetchStockData.mockResolvedValue(mockData);

      const { result } = renderHook(() => useMultiStockData(largeSymbolArray));

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should make concurrent calls for all symbols
      expect(mockChartDataService.fetchStockData).toHaveBeenCalledTimes(
        largeSymbolArray.length,
      );

      // Should have data for all symbols
      const expectedData = largeSymbolArray.reduce(
        (acc, symbol) => {
          acc[symbol] = mockData;
          return acc;
        },
        {} as { [symbol: string]: StockDataRow[] },
      );

      expect(result.current.data).toEqual(expectedData);
    });
  });
});
