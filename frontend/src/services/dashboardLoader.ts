import type { ChartType } from "@/types/ChartTypes";

export interface DashboardChart {
  title: string;
  category?: string;
  description?: string;
  chartType: ChartType;
}

export interface DashboardConfig {
  id: string;
  title: string;
  description?: string;
  layout: string;
  mode: string;
  enabled: boolean;
  charts: DashboardChart[];
}

export class DashboardLoader {
  static async getAllDashboards(): Promise<DashboardConfig[]> {
    try {
      const response = await fetch("/api/dashboards.json");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.success ? data.dashboards : [];
    } catch (error) {
      console.error("Failed to load dashboards:", error);
      return [];
    }
  }

  static async getDashboard(id: string): Promise<DashboardConfig | null> {
    const dashboards = await this.getAllDashboards();
    return dashboards.find((dashboard) => dashboard.id === id) || null;
  }

  static getLayoutClasses(layout: string): string {
    const layoutMappings: Record<string, string> = {
      "2x2_grid": "grid grid-cols-1 gap-6 lg:grid-cols-2 h-full",
      "1x3_stack": "flex flex-col gap-6 h-full",
      "2x1_stack": "flex flex-col h-full",
      "3x1_row": "grid grid-cols-1 gap-6 lg:grid-cols-3 h-full",
      "1x2_column": "grid grid-cols-1 gap-6 lg:grid-cols-2 h-full",
      fundamental_3x3: "fundamental-dashboard-grid",
    };

    return layoutMappings[layout] || "flex flex-col gap-6 h-full";
  }
}
