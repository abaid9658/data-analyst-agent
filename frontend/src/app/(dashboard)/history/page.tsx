"use client";

import { useQuery } from "@tanstack/react-query";
import { History, Search, Terminal } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { useState } from "react";
import { useDebounce } from "@/hooks/useDebounce";
import { apiClient } from "@/lib/api-client";
import { formatDate } from "@/lib/formatters";

export default function HistoryPage() {
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 350);

  const { data, isLoading } = useQuery({
    queryKey: ["history", debouncedSearch],
    queryFn: async () => {
      const { data } = await apiClient.get("/history", {
        params: { search: debouncedSearch || undefined },
      });
      return data;
    },
  });

  const items = data?.items ?? [];

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header + Search */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Analysis History</h1>
          <p className="text-sm text-gray-500">Track and review past SQL queries, code executions, and questions</p>
        </div>

        {/* Search Input */}
        <div className="relative max-w-xs w-full">
          <Search className="w-4 h-4 text-gray-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search past queries…"
            className="input-field text-sm pl-10 w-full"
          />
        </div>
      </div>

      {isLoading ? (
        <TableSkeleton rows={8} cols={4} />
      ) : items.length === 0 ? (
        <EmptyState
          icon={<History className="w-7 h-7" />}
          title="No history items"
          description="Your analytical query runs and generated SQL statements will show up here."
        />
      ) : (
        <div className="rounded-xl border border-surface-border overflow-hidden">
          <table className="w-full text-xs text-left">
            <thead>
              <tr style={{ background: "rgba(20,20,37,0.8)" }}>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Question</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">SQL/Code Preview</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Source</th>
                <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">Date</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item: any) => (
                <tr key={item.id} className="border-b border-surface-border/50 hover:bg-surface-elevated transition-colors">
                  <td className="px-4 py-2.5 text-gray-200 font-medium max-w-xs truncate">{item.question}</td>
                  <td className="px-4 py-2.5 text-gray-300 font-mono max-w-sm truncate text-[11px]">{item.dataset_name}</td>
                  <td className="px-4 py-2.5">
                    <span className="badge badge-primary text-[10px] uppercase">{item.type}</span>
                  </td>
                  <td className="px-4 py-2.5 text-gray-500">{formatDate(item.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
