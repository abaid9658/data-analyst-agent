"use client";

import { useQuery } from "@tanstack/react-query";
import { LayoutDashboard, Eye } from "lucide-react";
import { EmptyState } from "@/components/common/EmptyState";
import { CardSkeleton } from "@/components/common/LoadingSkeleton";
import Link from "next/link";

export default function DashboardsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboards"],
    queryFn: async () => {
      // Mock or fetch dashboard items from backend settings/dashboards
      return { dashboards: [] };
    },
  });

  const dashboards = data?.dashboards ?? [];

  if (isLoading) {
    return (
      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-white">Dashboards</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <CardSkeleton />
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboards</h1>
          <p className="text-sm text-gray-500">View and customize interactive dashboards</p>
        </div>
      </div>

      {dashboards.length === 0 ? (
        <EmptyState
          icon={<LayoutDashboard className="w-7 h-7" />}
          title="No dashboards yet"
          description="Ask the AI Analyst to 'generate a dashboard' inside any conversation thread to automatically synthesize your visualizations."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {dashboards.map((dash: any) => (
            <div key={dash.id} className="glass-card p-5 space-y-3">
              <h3 className="text-sm font-semibold text-gray-200">{dash.title}</h3>
              <p className="text-xs text-gray-500">{dash.description}</p>
              <div className="flex justify-end pt-2">
                <Link href={`/dashboards/${dash.id}`}>
                  <button className="btn-primary text-xs flex items-center gap-1 px-3 py-1.5">
                    <Eye className="w-3.5 h-3.5" />
                    Open
                  </button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
