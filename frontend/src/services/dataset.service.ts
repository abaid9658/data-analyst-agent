import { apiClient } from "@/lib/api-client";
import type { Dataset, DatasetListResponse, UploadResponse } from "@/types/dataset.types";

export const datasetService = {
  /** Upload CSV / Excel / JSON file */
  uploadFile: async (formData: FormData): Promise<UploadResponse> => {
    const { data } = await apiClient.post<UploadResponse>("/upload/file", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },

  /** Poll background task status */
  getUploadStatus: async (taskId: string): Promise<{ task_id: string; status: string; result: unknown }> => {
    const { data } = await apiClient.get(`/upload/status/${taskId}`);
    return data;
  },

  /** List all datasets */
  listDatasets: async (page = 1, limit = 50): Promise<DatasetListResponse> => {
    const { data } = await apiClient.get<DatasetListResponse>("/upload/datasets", {
      params: { page, limit },
    });
    return data;
  },

  /** Get single dataset details */
  getDataset: async (datasetId: string): Promise<Dataset> => {
    const { data } = await apiClient.get<Dataset>(`/upload/datasets/${datasetId}`);
    return data;
  },

  /** Delete a dataset */
  deleteDataset: async (datasetId: string): Promise<void> => {
    await apiClient.delete(`/upload/datasets/${datasetId}`);
  },
};
