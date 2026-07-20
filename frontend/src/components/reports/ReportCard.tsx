"use client";

import { FileText, Calendar, Download } from "lucide-react";
import { formatRelativeTime } from "@/lib/formatters";
import type { ReportStatus } from "@/services/report.service";

interface ReportCardProps {
  report: ReportStatus;
  onDownload?: () => void;
}

export function ReportCard({ report, onDownload }: ReportCardProps) {
  const isReady = report.status === "ready";

  return (
    <div
      className="glass-card p-5 flex flex-col justify-between h-44 relative overflow-hidden border border-surface-border"
    >
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-400 flex-shrink-0">
          <FileText className="w-5 h-5" />
        </div>
        <div className="min-w-0">
          <h4 className="text-sm font-semibold text-gray-200 truncate">{report.title}</h4>
          <span className="text-[10px] text-primary-300 uppercase font-mono tracking-wider">{report.format}</span>
        </div>
      </div>

      <div className="space-y-2 mt-4">
        <div className="flex items-center gap-1.5 text-xs text-gray-500">
          <Calendar className="w-3.5 h-3.5" />
          <span>{formatRelativeTime(report.created_at)}</span>
        </div>
      </div>

      <div className="flex items-center justify-between pt-3 border-t border-surface-border/50">
        <span className={`text-[10px] px-2 py-0.5 rounded-full ${isReady ? "bg-green-500/10 text-green-400" : "bg-yellow-500/10 text-yellow-400"}`}>
          {report.status}
        </span>
        {isReady && (
          <button
            onClick={onDownload}
            className="flex items-center gap-1 text-xs text-primary-400 hover:text-primary-300 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            Download
          </button>
        )}
      </div>
    </div>
  );
}
