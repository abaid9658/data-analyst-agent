import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { datasetService } from "@/services/dataset.service";

/**
 * Fetch all datasets for the current user.
 */
export function useDatasets() {
  return useQuery({
    queryKey: ["datasets"],
    queryFn: () => datasetService.listDatasets(),
    staleTime: 60 * 1000,
  });
}

/**
 * Fetch a single dataset by ID.
 */
export function useDataset(datasetId: string | undefined) {
  return useQuery({
    queryKey: ["datasets", datasetId],
    queryFn: () => datasetService.getDataset(datasetId!),
    enabled: !!datasetId,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Upload a file and trigger background profiling.
 */
export function useUploadDataset() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (formData: FormData) => datasetService.uploadFile(formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["datasets"] });
    },
  });
}

/**
 * Delete a dataset by ID.
 */
export function useDeleteDataset() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (datasetId: string) => datasetService.deleteDataset(datasetId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["datasets"] });
    },
  });
}

/**
 * Poll upload task status.
 */
export function useUploadStatus(taskId: string | undefined) {
  return useQuery({
    queryKey: ["upload-status", taskId],
    queryFn: () => datasetService.getUploadStatus(taskId!),
    enabled: !!taskId,
    refetchInterval: (data) => {
      const status = (data as { status?: string } | undefined)?.status;
      return status === "SUCCESS" || status === "FAILURE" ? false : 2000;
    },
  });
}
