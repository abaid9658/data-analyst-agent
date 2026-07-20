import { apiClient } from "@/lib/api-client";

export interface GenerateDashboardRequest {
  session_id: string;
  title: string;
}

export interface DashboardWidget {
  id: string;
  widget_type: "kpi" | "chart" | "table" | "text";
  title: string | null;
  config: Record<string, unknown>;
  grid_x: number;
  grid_y: number;
  grid_w: number;
  grid_h: number;
  chart_id: string | null;
  query_id: string | null;
}

export interface Dashboard {
  dashboard_id: string;
  title: string;
  description: string | null;
  widgets: DashboardWidget[];
  layout: unknown | null;
}

export const dashboardService = {
  autoGenerate: async (body: GenerateDashboardRequest): Promise<Dashboard> => {
    const { data } = await apiClient.post<Dashboard>("/dashboard/auto-generate", body);
    return data;
  },
};
