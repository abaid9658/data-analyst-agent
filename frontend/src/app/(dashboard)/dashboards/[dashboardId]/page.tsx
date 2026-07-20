"use client";

import { useQuery } from "@tanstack/react-query";
import { DashboardGrid } from "@/components/dashboard/DashboardGrid";
import { DashboardToolbar } from "@/components/dashboard/DashboardToolbar";
import { ArrowLeft, Loader2 } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function DashboardDetailPage() {
  const params = useParams();
  const dashboardId = params?.dashboardId as string | undefined;

  const { data: dashboard, isLoading } = useQuery({
    queryKey: ["dashboard", dashboardId],
    queryFn: async () => {
      // Fetch details of dashboard by ID, mock fallback for now
      return {
        dashboard_id: dashboardId,
        title: "Executive Metrics Dashboard",
        description: "Interactive report insights summary view",
        widgets: [],
      };
    },
    enabled: !!dashboardId,
  });

  if (isLoading) {
    return (
      <div className="h-96 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="p-8 text-center text-gray-500">
        Dashboard not found.
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Back link */}
      <div className="flex items-center gap-3">
        <Link href="/dashboards">
          <button className="p-2 rounded-lg hover:bg-surface-elevated text-gray-400 hover:text-gray-200 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
        </Link>
        <span className="text-xs text-gray-500">Back to Dashboards</span>
      </div>

      {/* Toolbar */}
      <DashboardToolbar
        title={dashboard.title}
        onShare={() => alert("Share link copied to clipboard!")}
        onExport={() => window.print()}
      />

      {/* Dashboard Widgets Grid */}
      {dashboard.widgets.length === 0 ? (
        <div className="py-20 text-center text-sm text-gray-500 border border-dashed border-surface-border rounded-2xl">
          No widgets have been generated on this dashboard yet.
        </div>
      ) : (
        <DashboardGrid widgets={dashboard.widgets as any} />
      )}
    </div>
  );
}
