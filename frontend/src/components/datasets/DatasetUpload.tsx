"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, CloudUpload, FileSpreadsheet, FileText, Loader2, XCircle } from "lucide-react";
import { useUploadDataset, useUploadStatus } from "@/hooks/useDatasets";
import { formatBytes } from "@/lib/formatters";
import { cn } from "@/lib/utils";

const ACCEPT = {
  "text/csv": [".csv"],
  "application/vnd.ms-excel": [".xls"],
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
  "application/json": [".json"],
  "application/pdf": [".pdf"],
};

interface DatasetUploadProps {
  onSuccess?: (datasetId: string) => void;
}

export function DatasetUpload({ onSuccess }: DatasetUploadProps) {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [droppedFile, setDroppedFile] = useState<File | null>(null);
  const { mutateAsync: uploadFile, isPending, isError, error } = useUploadDataset();
  const { data: statusData } = useUploadStatus(taskId ?? undefined);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (!acceptedFiles.length) return;
      const file = acceptedFiles[0];
      setDroppedFile(file);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("name", file.name.replace(/\.[^.]+$/, ""));

      try {
        const res = await uploadFile(formData);
        setTaskId(res.task_id);
        if (onSuccess) onSuccess(res.dataset_id);
      } catch {
        // Error handled by mutation state
      }
    },
    [uploadFile, onSuccess]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: ACCEPT,
    maxFiles: 1,
    maxSize: 100 * 1024 * 1024, // 100MB
    disabled: isPending,
  });

  const uploadStatus = statusData?.status;
  const isDone = uploadStatus === "SUCCESS";
  const isFailed = uploadStatus === "FAILURE" || isError;

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        {...getRootProps()}
        className={cn(
          "relative rounded-2xl border-2 border-dashed p-10 text-center cursor-pointer transition-all duration-200",
          isDragActive && !isDragReject && "border-primary-500 bg-primary-500/5",
          isDragReject && "border-red-400 bg-red-500/5",
          !isDragActive && !isDragReject && "border-surface-border hover:border-primary-500/50 hover:bg-surface-elevated",
          isPending && "pointer-events-none opacity-60"
        )}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center gap-3">
          {isPending ? (
            <Loader2 className="w-10 h-10 text-primary-400 animate-spin" />
          ) : isFailed ? (
            <XCircle className="w-10 h-10 text-red-400" />
          ) : isDone ? (
            <CheckCircle2 className="w-10 h-10 text-green-400" />
          ) : isDragActive ? (
            <CloudUpload className="w-10 h-10 text-primary-400" />
          ) : (
            <div className="w-14 h-14 rounded-2xl bg-primary-500/10 flex items-center justify-center">
              {droppedFile?.type === "application/pdf" ? (
                <FileText className="w-7 h-7 text-red-400" />
              ) : (
                <FileSpreadsheet className="w-7 h-7 text-primary-400" />
              )}
            </div>
          )}

          <div>
            {isPending ? (
              <p className="text-sm text-gray-400">Uploading {droppedFile?.name}…</p>
            ) : isFailed ? (
              <p className="text-sm text-red-400">Upload failed. Drop another file to retry.</p>
            ) : isDone ? (
              <p className="text-sm text-green-400">Upload complete — processing in background</p>
            ) : isDragActive ? (
              <p className="text-sm text-primary-300">Drop to upload</p>
            ) : (
              <>
                <p className="text-sm font-medium text-gray-300">
                  Drag & drop your dataset here
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  CSV, Excel (.xlsx / .xls), JSON, PDF · Max 100 MB
                </p>
              </>
            )}
          </div>

          {!isPending && !isDone && (
            <button
              type="button"
              className="btn-primary text-xs px-4 py-2 mt-1"
            >
              Browse Files
            </button>
          )}
        </div>
      </div>

      {/* Dropped file info */}
      <AnimatePresence>
        {droppedFile && !isFailed && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-3 glass-card px-4 py-3"
          >
            <FileSpreadsheet className="w-5 h-5 text-primary-400 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-200 truncate font-medium">{droppedFile.name}</p>
              <p className="text-xs text-gray-500">{formatBytes(droppedFile.size)}</p>
            </div>
            {isPending && (
              <div className="flex items-center gap-1.5 text-xs text-primary-400">
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                Uploading…
              </div>
            )}
            {isDone && <span className="badge badge-green text-xs">Processing</span>}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
