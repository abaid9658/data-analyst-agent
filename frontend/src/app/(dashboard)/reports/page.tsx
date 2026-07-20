"use client";

import { useQuery } from "@tanstack/react-query";
import { FileText, Download } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { formatBytes, formatRelativeTime } from "@/lib/formatters";

export default function ReportsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["reports"],
    queryFn: async () => {
      // Stub list of generated reports
      return { reports: [] };
    },
  });

  const reports = data?.reports ?? [];

  if (isLoading) {
    return (
      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-white">Generated Reports</h1>
        <TableSkeleton rows={4} cols={4} />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Generated Reports</h1>
        <p className="text-sm text-gray-500">Download previously compiled executive summary PDFs, slide decks, and spreadsheets</p>
      </div>

      {reports.length === 0 ? (
        <EmptyState
          icon={<FileText className="w-7 h-7" />}
          title="No reports generated"
          description="Type 'generate PDF report' in your active analysis conversation thread to build executive export files."
        />
      ) : (
        <div className="rounded-xl border border-surface-border overflow-hidden">
          <table className="w-full text-xs text-left">
            <thead>
              <tr style={{ background: "rgba(20,20,37,0.8)" }}>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Title</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Format</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Size</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Generated</th>
                <th className="px-4 py-2.5 border-b border-surface-border"></th>
              </tr>
            </thead>
            <tbody>
              {reports.map((rep: any) => (
                <tr key={rep.id} className="border-b border-surface-border/50 hover:bg-surface-elevated transition-colors">
                  <td className="px-4 py-2.5 text-gray-200 font-semibold">{rep.title}</td>
                  <td className="px-4 py-2.5 text-primary-300 uppercase">{rep.format}</td>
                  <td className="px-4 py-2.5 text-gray-400">{formatBytes(rep.file_size_bytes)}</td>
                  <td className="px-4 py-2.5 text-gray-500">{formatRelativeTime(rep.created_at)}</td>
                  <td className="px-4 py-2.5 text-right">
                    <a href={`/api/v1/report/${rep.id}/download`} download>
                      <button className="p-1.5 rounded-lg text-primary-400 hover:text-primary-300 hover:bg-surface-elevated">
                        <Download className="w-4 h-4" />
                      </button>
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
