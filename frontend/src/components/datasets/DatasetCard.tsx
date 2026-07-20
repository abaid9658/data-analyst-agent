"use client";

import { motion } from "framer-motion";
import { Database, FileJson, FileSpreadsheet, FileText, MoreVertical, Trash2 } from "lucide-react";
import { useState } from "react";
import type { Dataset } from "@/types/dataset.types";
import { formatBytes, formatNumber, formatRelativeTime } from "@/lib/formatters";
import { useDeleteDataset } from "@/hooks/useDatasets";
import { ConfirmDialog } from "@/components/common/ConfirmDialog";
import { useChatStore } from "@/store/chat.store";
import { cn } from "@/lib/utils";

const FILE_ICONS: Record<string, React.ReactNode> = {
  csv: <FileText className="w-5 h-5 text-green-400" />,
  excel: <FileSpreadsheet className="w-5 h-5 text-emerald-400" />,
  json: <FileJson className="w-5 h-5 text-yellow-400" />,
  pdf: <FileText className="w-5 h-5 text-red-400" />,
};

const STATUS_BADGE: Record<string, string> = {
  ready: "badge-green",
  processing: "badge-primary",
  error: "badge-red",
};

interface DatasetCardProps {
  dataset: Dataset;
  onClick?: () => void;
}

export function DatasetCard({ dataset, onClick }: DatasetCardProps) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const { mutate: deleteDataset, isPending } = useDeleteDataset();
  const { selectedDatasetId, setSelectedDatasetId } = useChatStore();
  const isSelected = selectedDatasetId === dataset.id;

  return (
    <>
      <motion.div
        whileHover={{ y: -2 }}
        onClick={onClick}
        className={cn(
          "glass-card p-5 cursor-pointer transition-all group relative",
          isSelected && "ring-2 ring-primary-500/60"
        )}
      >
        {/* Header row */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-surface-elevated flex items-center justify-center flex-shrink-0">
              {FILE_ICONS[dataset.file_type ?? "csv"] ?? <Database className="w-5 h-5 text-gray-400" />}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-gray-200 truncate max-w-[180px]">{dataset.name}</p>
              <p className="text-xs text-gray-500">{dataset.original_filename}</p>
            </div>
          </div>

          {/* Menu trigger */}
          <div className="relative">
            <button
              onClick={(e) => { e.stopPropagation(); setMenuOpen((p) => !p); }}
              className="p-1.5 rounded-lg text-gray-500 hover:text-gray-300 hover:bg-surface-elevated opacity-0 group-hover:opacity-100 transition-all"
            >
              <MoreVertical className="w-4 h-4" />
            </button>
            {menuOpen && (
              <div
                className="absolute right-0 top-full mt-1 w-36 rounded-xl border border-surface-border py-1 z-10 shadow-card-lg"
                style={{ background: "#141425" }}
              >
                <button
                  onClick={(e) => { e.stopPropagation(); setSelectedDatasetId(dataset.id); setMenuOpen(false); }}
                  className="w-full text-left px-3 py-2 text-xs text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-colors"
                >
                  Use in Chat
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); setConfirmDelete(true); setMenuOpen(false); }}
                  className="w-full text-left px-3 py-2 text-xs text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-2"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  Delete
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Stats row */}
        <div className="flex items-center gap-3 text-xs text-gray-500 mb-3">
          {dataset.row_count != null && (
            <span>
              {formatNumber(dataset.row_count)}{" "}
              {dataset.file_type === "pdf" ? "chunks" : "rows"}
            </span>
          )}
          {dataset.column_count != null && dataset.file_type !== "pdf" && (
            <span>· {dataset.column_count} cols</span>
          )}
          {dataset.file_size_bytes != null && (
            <span>· {formatBytes(dataset.file_size_bytes)}</span>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between">
          <span className={`badge text-[10px] ${STATUS_BADGE[dataset.status] ?? "badge-primary"}`}>
            {dataset.status}
          </span>
          <span className="text-[10px] text-gray-600">{formatRelativeTime(dataset.created_at)}</span>
        </div>
      </motion.div>

      <ConfirmDialog
        open={confirmDelete}
        title="Delete Dataset"
        description={`This will permanently delete "${dataset.name}" and all associated analysis history.`}
        confirmLabel="Delete"
        danger
        onConfirm={() => { deleteDataset(dataset.id); setConfirmDelete(false); }}
        onCancel={() => setConfirmDelete(false)}
      />
    </>
  );
}
