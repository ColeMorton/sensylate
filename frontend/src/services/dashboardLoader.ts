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
}
