export interface DashboardChart {
  title: string;
  category?: string;
  description?: string;
  chartType: string;
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
      "2x2_grid": "grid grid-cols-1 gap-6 lg:grid-cols-2",
      "1x3_stack": "grid grid-cols-1 gap-6",
      "3x1_row": "grid grid-cols-1 gap-6 lg:grid-cols-3",
      "1x2_column": "grid grid-cols-1 gap-6 lg:grid-cols-2",
    };

    return layoutMappings[layout] || "grid grid-cols-1 gap-6";
  }
}
