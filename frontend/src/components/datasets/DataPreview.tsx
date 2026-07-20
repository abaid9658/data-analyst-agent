"use client";

import { useState } from "react";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { Download } from "lucide-react";

interface DataPreviewProps {
  data: {
    columns: string[];
    rows: unknown[][];
  } | null;
  isLoading?: boolean;
}

export function DataPreview({ data, isLoading = false }: DataPreviewProps) {
  const [page, setPage] = useState(1);
  const rowsPerPage = 10;

  if (isLoading) {
    return <TableSkeleton rows={10} cols={5} />;
  }

  if (!data || !data.rows.length) {
    return (
      <div className="py-8 text-center text-sm text-gray-500">
        No preview data available
      </div>
    );
  }

  const totalPages = Math.ceil(data.rows.length / rowsPerPage);
  const startIndex = (page - 1) * rowsPerPage;
  const pageRows = data.rows.slice(startIndex, startIndex + rowsPerPage);

  const handleExportCSV = () => {
    const headers = data.columns.join(",");
    const csvRows = data.rows.map((row) =>
      row.map((val) => `"${String(val ?? "").replace(/"/g, '""')}"`).join(",")
    );
    const blob = new Blob([[headers, ...csvRows].join("\n")], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.setAttribute("href", url);
    a.setAttribute("download", "data_preview.csv");
    a.click();
  };

  return (
    <div className="rounded-xl border border-surface-border overflow-hidden">
      {/* Header toolbar */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-surface-border" style={{ background: "rgba(37,37,64,0.4)" }}>
        <span className="text-xs font-medium text-gray-300">
          Showing {startIndex + 1}-{Math.min(startIndex + rowsPerPage, data.rows.length)} of {data.rows.length.toLocaleString()} rows
        </span>
        <button
          onClick={handleExportCSV}
          className="flex items-center gap-1 text-xs text-primary-400 hover:text-primary-300 transition-colors"
        >
          <Download className="w-3 h-3" />
          Export CSV
        </button>
      </div>

      {/* Table grid */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead>
            <tr style={{ background: "rgba(20,20,37,0.8)" }}>
              {data.columns.map((col) => (
                <th key={col} className="px-4 py-2.5 text-gray-400 font-medium whitespace-nowrap border-b border-surface-border">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pageRows.map((row, i) => (
              <tr key={i} className="border-b border-surface-border/50 hover:bg-surface-elevated transition-colors">
                {row.map((cell, j) => (
                  <td key={j} className="px-4 py-2.5 text-gray-300 font-mono whitespace-nowrap">
                    {cell === null ? <span className="text-gray-600">null</span> : String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-2.5 border-t border-surface-border">
          <button
            onClick={() => setPage((p) => Math.max(p - 1, 1))}
            disabled={page === 1}
            className="text-xs text-gray-400 hover:text-gray-200 disabled:opacity-40"
          >
            Previous
          </button>
          <span className="text-xs text-gray-500">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
            disabled={page === totalPages}
            className="text-xs text-gray-400 hover:text-gray-200 disabled:opacity-40"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
