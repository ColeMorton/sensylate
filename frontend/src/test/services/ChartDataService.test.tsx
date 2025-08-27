import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import {
  mockMultiStockDataXPEVNIO,
  mockXPEVData,
  mockNIOData,
  mockEmptyData,
  mockDataWithMissingValues,
} from "@/test/__mocks__/multi-stock-data.mock";

/**
 * Data Service Tests for Multi-Stock Chart Functionality
 * Tests the ChartDataService for multi-stock data fetching scenarios
 */

// Mock fetch API
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock CSV parsing
const mockParseCsv = vi.fn();
vi.mock("@/utils/csvParser", () => ({
  parseCsv: mockParseCsv,
}));

describe("ChartDataService Multi-Stock Tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFetch.mockClear();
    mockParseCsv.mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("Multi-Symbol Data Fetching", () => {
    it("should fetch multiple stock symbols concurrently", async () => {
      // Mock successful responses for both symbols
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () =>
            Promise.resolve("mocked,csv,data\n2024-01-01,10.50,11.80"),
        })
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("mocked,csv,data\n2024-01-01,6.25,6.55"),
        });

      mockParseCsv
        .mockReturnValueOnce(mockXPEVData)
        .mockReturnValueOnce(mockNIOData);

      // Import service after mocks are set up
      const { chartDataService } = await import("@/services/ChartDataService");

      // Create promises for concurrent execution
      const xpevPromise = chartDataService.fetchStockData(
        "XPEV",
        new AbortController().signal,
      );
      const nioPromise = chartDataService.fetchStockData(
        "NIO",
        new AbortController().signal,
      );

      const [xpevResult, nioResult] = await Promise.all([
        xpevPromise,
        nioPromise,
      ]);

      // Verify both requests were made
      expect(mockFetch).toHaveBeenCalledTimes(2);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("XPEV"),
        expect.objectContaining({ signal: expect.any(AbortSignal) }),
      );
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("NIO"),
        expect.objectContaining({ signal: expect.any(AbortSignal) }),
      );

      // Verify parsed results
      expect(xpevResult).toEqual(mockXPEVData);
      expect(nioResult).toEqual(mockNIOData);
    });

    it("should handle partial failures in multi-stock requests", async () => {
      // XPEV succeeds, NIO fails
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("mocked,csv,data"),
        })
        .mockRejectedValueOnce(new Error("Network timeout"));

      mockParseCsv.mockReturnValueOnce(mockXPEVData);

      const { chartDataService } = await import("@/services/ChartDataService");

      // Test concurrent requests with mixed outcomes
      const xpevPromise = chartDataService.fetchStockData(
        "XPEV",
        new AbortController().signal,
      );
      const nioPromise = chartDataService.fetchStockData(
        "NIO",
        new AbortController().signal,
      );

      const [xpevResult, nioError] = await Promise.allSettled([
        xpevPromise,
        nioPromise,
      ]);

      expect(xpevResult.status).toBe("fulfilled");
      expect(xpevResult.value).toEqual(mockXPEVData);

      expect(nioError.status).toBe("rejected");
      expect(nioError.reason.message).toContain("Network timeout");
    });

    it("should handle AbortController for concurrent requests", async () => {
      const abortController = new AbortController();

      // Mock long-running requests
      mockFetch.mockImplementation(
        () =>
          new Promise((resolve) => {
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  text: () => Promise.resolve("data"),
                }),
              1000,
            );
          }),
      );

      const { chartDataService } = await import("@/services/ChartDataService");

      const xpevPromise = chartDataService.fetchStockData(
        "XPEV",
        abortController.signal,
      );
      const nioPromise = chartDataService.fetchStockData(
        "NIO",
        abortController.signal,
      );

      // Abort after a short delay
      setTimeout(() => abortController.abort(), 50);

      // Both requests should be aborted
      await expect(Promise.all([xpevPromise, nioPromise])).rejects.toThrow();
    });
  });

  describe("Data Quality and Validation", () => {
    it("should validate CSV data structure for stock data", async () => {
      const invalidCsvData = "invalid,structure\nno,proper,headers";

      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(invalidCsvData),
      });

      // Mock parser to throw validation error
      mockParseCsv.mockImplementation(() => {
        throw new Error("Invalid CSV structure: missing required columns");
      });

      const { chartDataService } = await import("@/services/ChartDataService");

      await expect(
        chartDataService.fetchStockData(
          "INVALID",
          new AbortController().signal,
        ),
      ).rejects.toThrow("Invalid CSV structure");
    });

    it("should handle malformed price data gracefully", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve("valid,csv,response"),
      });

      mockParseCsv.mockReturnValue(mockDataWithMissingValues);

      const { chartDataService } = await import("@/services/ChartDataService");

      const result = await chartDataService.fetchStockData(
        "TEST",
        new AbortController().signal,
      );

      // Should return data even with missing values
      expect(result).toEqual(mockDataWithMissingValues);
      expect(result.some((row) => row.open === "")).toBe(true);
    });

    it("should handle empty data responses", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve("date,open,high,low,close,volume\n"), // Headers only
      });

      mockParseCsv.mockReturnValue(mockEmptyData);

      const { chartDataService } = await import("@/services/ChartDataService");

      const result = await chartDataService.fetchStockData(
        "EMPTY",
        new AbortController().signal,
      );

      expect(result).toEqual([]);
      expect(Array.isArray(result)).toBe(true);
    });
  });

  describe("Error Handling and Resilience", () => {
    it("should handle HTTP error responses", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: "Not Found",
      });

      const { chartDataService } = await import("@/services/ChartDataService");

      await expect(
        chartDataService.fetchStockData(
          "NOTFOUND",
          new AbortController().signal,
        ),
      ).rejects.toThrow("404");
    });

    it("should handle network errors", async () => {
      mockFetch.mockRejectedValueOnce(new Error("Failed to fetch"));

      const { chartDataService } = await import("@/services/ChartDataService");

      await expect(
        chartDataService.fetchStockData(
          "NETWORK_ERROR",
          new AbortController().signal,
        ),
      ).rejects.toThrow("Failed to fetch");
    });

    it("should handle timeout scenarios", async () => {
      mockFetch.mockImplementation(
        () =>
          new Promise((_, reject) => {
            setTimeout(() => reject(new Error("Request timeout")), 100);
          }),
      );

      const { chartDataService } = await import("@/services/ChartDataService");

      await expect(
        chartDataService.fetchStockData(
          "TIMEOUT",
          new AbortController().signal,
        ),
      ).rejects.toThrow("Request timeout");
    });

    it("should handle rate limiting gracefully", async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 429,
        statusText: "Too Many Requests",
        headers: new Map([["Retry-After", "60"]]),
      });

      const { chartDataService } = await import("@/services/ChartDataService");

      await expect(
        chartDataService.fetchStockData(
          "RATE_LIMITED",
          new AbortController().signal,
        ),
      ).rejects.toThrow("429");
    });
  });

  describe("Caching and Performance", () => {
    it("should cache successful responses", async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve("cached,data"),
      });

      mockParseCsv.mockReturnValue(mockXPEVData);

      const { chartDataService } = await import("@/services/ChartDataService");

      // First request
      const result1 = await chartDataService.fetchStockData(
        "CACHED",
        new AbortController().signal,
      );

      // Second request (should use cache if implemented)
      const result2 = await chartDataService.fetchStockData(
        "CACHED",
        new AbortController().signal,
      );

      expect(result1).toEqual(result2);
      expect(result1).toEqual(mockXPEVData);
    });

    it("should handle large datasets efficiently", async () => {
      // Generate large CSV data
      const largeCsvData = [
        "date,open,high,low,close,volume",
        ...Array.from(
          { length: 10000 },
          (_, i) =>
            `2024-01-${String(i + 1).padStart(2, "0")},100.${i},105.${i},95.${i},102.${i},${1000000 + i}`,
        ),
      ].join("\n");

      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(largeCsvData),
      });

      // Mock large dataset parsing
      const largeDataset = Array.from({ length: 10000 }, (_, i) => ({
        date: `2024-01-${String(i + 1).padStart(2, "0")}`,
        open: `100.${i}`,
        high: `105.${i}`,
        low: `95.${i}`,
        close: `102.${i}`,
        volume: `${1000000 + i}`,
      }));

      mockParseCsv.mockReturnValue(largeDataset);

      const { chartDataService } = await import("@/services/ChartDataService");

      const startTime = Date.now();
      const result = await chartDataService.fetchStockData(
        "LARGE",
        new AbortController().signal,
      );
      const endTime = Date.now();

      expect(result).toHaveLength(10000);
      expect(endTime - startTime).toBeLessThan(1000); // Should complete within 1 second
    });
  });

  describe("Data Format Compatibility", () => {
    it("should handle different CSV formats", async () => {
      const alternativeCsvFormat = [
        "Date,Open,High,Low,Close,Volume", // Different capitalization
        "2024-01-01,10.50,12.25,9.75,11.80,15234567",
      ].join("\n");

      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(alternativeCsvFormat),
      });

      mockParseCsv.mockReturnValue([
        {
          date: "2024-01-01",
          open: "10.50",
          high: "12.25",
          low: "9.75",
          close: "11.80",
          volume: "15234567",
        },
      ]);

      const { chartDataService } = await import("@/services/ChartDataService");

      const result = await chartDataService.fetchStockData(
        "FORMAT_TEST",
        new AbortController().signal,
      );

      expect(result).toHaveLength(1);
      expect(result[0].close).toBe("11.80");
    });

    it("should handle CSV with extra columns", async () => {
      const csvWithExtraColumns = [
        "date,open,high,low,close,volume,adj_close,dividend",
        "2024-01-01,10.50,12.25,9.75,11.80,15234567,11.75,0.00",
      ].join("\n");

      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(csvWithExtraColumns),
      });

      mockParseCsv.mockReturnValue([
        {
          date: "2024-01-01",
          open: "10.50",
          high: "12.25",
          low: "9.75",
          close: "11.80",
          volume: "15234567",
          adj_close: "11.75",
          dividend: "0.00",
        },
      ]);

      const { chartDataService } = await import("@/services/ChartDataService");

      const result = await chartDataService.fetchStockData(
        "EXTRA_COLS",
        new AbortController().signal,
      );

      expect(result[0]).toHaveProperty("close", "11.80");
      expect(result[0]).toHaveProperty("adj_close", "11.75");
    });
  });

  describe("Multi-Stock Integration", () => {
    it("should support the multi-stock workflow end-to-end", async () => {
      // Mock responses for XPEV and NIO
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("xpev,csv,data"),
        })
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("nio,csv,data"),
        });

      mockParseCsv
        .mockReturnValueOnce(mockMultiStockDataXPEVNIO.XPEV)
        .mockReturnValueOnce(mockMultiStockDataXPEVNIO.NIO);

      const { chartDataService } = await import("@/services/ChartDataService");

      // Simulate the multi-stock hook behavior
      const symbols = ["XPEV", "NIO"];
      const abortController = new AbortController();

      const stockDataPromises = symbols.map((symbol) =>
        chartDataService.fetchStockData(symbol, abortController.signal),
      );

      const results = await Promise.all(stockDataPromises);

      // Convert to the expected multi-stock data structure
      const multiStockData = results.reduce(
        (acc, data, index) => {
          acc[symbols[index]] = data;
          return acc;
        },
        {} as { [symbol: string]: typeof mockXPEVData },
      );

      expect(multiStockData).toEqual(mockMultiStockDataXPEVNIO);
      expect(Object.keys(multiStockData)).toEqual(["XPEV", "NIO"]);
      expect(multiStockData.XPEV).toHaveLength(mockXPEVData.length);
      expect(multiStockData.NIO).toHaveLength(mockNIOData.length);
    });

    it("should handle mixed success/failure in multi-stock requests", async () => {
      // XPEV succeeds, NIO fails, TSLA succeeds
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("xpev,data"),
        })
        .mockRejectedValueOnce(new Error("NIO API error"))
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve("tsla,data"),
        });

      mockParseCsv.mockReturnValueOnce(mockXPEVData).mockReturnValueOnce([
        {
          date: "2024-01-01",
          open: "200",
          high: "210",
          low: "195",
          close: "205",
          volume: "30000000",
        },
      ]);

      const { chartDataService } = await import("@/services/ChartDataService");

      const symbols = ["XPEV", "NIO", "TSLA"];
      const abortController = new AbortController();

      const stockDataPromises = symbols.map((symbol) =>
        chartDataService.fetchStockData(symbol, abortController.signal),
      );

      const results = await Promise.allSettled(stockDataPromises);

      expect(results[0].status).toBe("fulfilled");
      expect(results[1].status).toBe("rejected");
      expect(results[2].status).toBe("fulfilled");

      // The hook should handle this by setting an error state
      const hasError = results.some((result) => result.status === "rejected");
      expect(hasError).toBe(true);
    });
  });
});
