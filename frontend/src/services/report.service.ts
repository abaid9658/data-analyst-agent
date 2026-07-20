import { apiClient } from "@/lib/api-client";

export interface GenerateReportRequest {
  session_id: string;
  format: "pdf" | "docx" | "pptx" | "xlsx" | "markdown";
  title: string;
  include_sections?: string[];
}

export interface GenerateReportResponse {
  report_id: string;
  status: string;
  task_id: string;
}

export interface ReportStatus {
  report_id: string;
  status: "generating" | "ready" | "error";
  format: string;
  title: string;
  download_url: string | null;
  created_at: string;
  expires_at: string | null;
}

export const reportService = {
  generateReport: async (body: GenerateReportRequest): Promise<GenerateReportResponse> => {
    const { data } = await apiClient.post<GenerateReportResponse>("/report/generate", body);
    return data;
  },

  getReportStatus: async (reportId: string): Promise<ReportStatus> => {
    const { data } = await apiClient.get<ReportStatus>(`/report/${reportId}`);
    return data;
  },

  getDownloadUrl: (reportId: string): string =>
    `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}/report/${reportId}/download`,
};
