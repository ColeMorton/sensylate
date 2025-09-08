/**
 * Bitcoin Price Chart Data Adapter
 *
 * Handles data fetching and processing specific to BTC price chart.
 * Colocated with chart component to follow GenContentOps principles.
 */

import type { StockDataRow } from "@/types/ChartTypes";
import type { ChartDataAdapter } from "@/services/UnifiedChartDataService";

export interface BTCPriceDataAdapter extends ChartDataAdapter<StockDataRow> {
  fetchData(signal?: AbortSignal, _params?: unknown): Promise<StockDataRow[]>;
}

export class BTCPriceDataAdapterImpl implements BTCPriceDataAdapter {
  private cache: StockDataRow[] | null = null;
  private lastFetched: number | null = null;
  private readonly cacheDuration = 5 * 60 * 1000; // 5 minutes

  async fetchData(signal?: AbortSignal, _params?: unknown): Promise<StockDataRow[]> {
    // Check cache validity
    if (
      this.cache &&
      this.lastFetched &&
      Date.now() - this.lastFetched < this.cacheDuration
    ) {
      return this.cache;
    }

    try {
      const response = await fetch("/data/raw/stocks/BTC-USD/daily.csv", {
        signal,
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch BTC data: ${response.status}`);
      }

      const csvText = await response.text();
      const data = this.parseCSV(csvText);

      // Update cache
      this.cache = data;
      this.lastFetched = Date.now();

      return data;
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        throw error;
      }
      throw new Error(
        `BTC data fetch failed: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  private parseCSV(csvText: string): StockDataRow[] {
    const lines = csvText.trim().split("\n");
    const headers = lines[0].split(",");

    return lines.slice(1).map((line) => {
      const values = line.split(",");
      const row: StockDataRow = {} as StockDataRow;
      headers.forEach((header, index) => {
        row[header.trim()] = values[index]?.trim() || "";
      });
      return row;
    });
  }
}

// Export singleton instance
export const btcPriceDataAdapter = new BTCPriceDataAdapterImpl();
