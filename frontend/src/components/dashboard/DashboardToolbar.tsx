"use client";

import { Share2, FileDown, Plus } from "lucide-react";

interface DashboardToolbarProps {
  title: string;
  onShare?: () => void;
  onExport?: () => void;
}

export function DashboardToolbar({ title, onShare, onExport }: DashboardToolbarProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 py-3 border-b border-surface-border">
      <h2 className="text-lg font-bold text-gray-200">{title}</h2>
      <div className="flex items-center gap-2">
        <button
          onClick={onShare}
          className="btn-ghost flex items-center gap-1.5 text-xs px-3.5 py-2"
        >
          <Share2 className="w-3.5 h-3.5" />
          Share Link
        </button>
        <button
          onClick={onExport}
          className="btn-primary flex items-center gap-1.5 text-xs px-3.5 py-2"
        >
          <FileDown className="w-3.5 h-3.5" />
          Export PDF
        </button>
      </div>
    </div>
  );
}
