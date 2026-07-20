import { apiClient } from "@/lib/api-client";
import type { PlotlySpec } from "@/types/chart.types";

export interface GenerateChartRequest {
  dataset_id: string;
  chart_type?: string;
  x_column?: string;
  y_column?: string;
  color_column?: string;
  title?: string;
}

export interface GenerateChartResponse {
  chart_id: string;
  chart_type: string;
  plotly_spec: PlotlySpec;
  explanation: string;
  download_urls: { png: string; svg: string; pdf: string };
}

export const chartService = {
  generateChart: async (body: GenerateChartRequest): Promise<GenerateChartResponse> => {
    const { data } = await apiClient.post<GenerateChartResponse>("/chart/generate", body);
    return data;
  },

  getDownloadUrl: (chartId: string, format: "png" | "svg" | "pdf"): string => {
    return `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}/chart/${chartId}/download?format=${format}`;
  },
};
