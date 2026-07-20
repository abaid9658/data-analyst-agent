"use client";

import { DashboardWidget } from "./DashboardWidget";
import type { DashboardWidget as WidgetType } from "@/services/dashboard.service";

interface DashboardGridProps {
  widgets: WidgetType[];
}

export function DashboardGrid({ widgets }: DashboardGridProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {widgets.map((widget) => (
        <div key={widget.id} className="min-h-72">
          <DashboardWidget widget={widget} />
        </div>
      ))}
    </div>
  );
}
