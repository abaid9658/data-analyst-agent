"use client";

import { ChartCard } from "@/components/charts/ChartCard";
import { KPIWidget } from "./KPIWidget";
import type { DashboardWidget as WidgetType } from "@/services/dashboard.service";

interface DashboardWidgetProps {
  widget: WidgetType;
}

export function DashboardWidget({ widget }: DashboardWidgetProps) {
  const config = widget.config || {};

  switch (widget.widget_type) {
    case "kpi":
      return (
        <KPIWidget
          title={widget.title || "KPI Metric"}
          value={String(config.value ?? "0")}
          change={config.change as string | number}
          changeType={config.changeType as "positive" | "negative" | "neutral"}
          className="h-full"
        />
      );
    case "chart":
      if (!config.plotly_spec) {
        return (
          <div className="h-full flex items-center justify-center border border-surface-border rounded-2xl text-xs text-gray-500">
            No chart spec available
          </div>
        );
      }
      return (
        <ChartCard
          spec={config.plotly_spec as any}
          title={widget.title || "Chart Visualization"}
          explanation={config.explanation as string}
          chartId={widget.chart_id || undefined}
        />
      );
    case "text":
      return (
        <div className="glass-card p-5 h-full overflow-y-auto space-y-2">
          {widget.title && <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide">{widget.title}</h4>}
          <p className="text-xs text-gray-300 leading-relaxed whitespace-pre-wrap">{String(config.text ?? "")}</p>
        </div>
      );
    case "table":
      const columns = (config.columns as string[]) || [];
      const rows = (config.rows as unknown[][]) || [];
      return (
        <div className="glass-card p-4 h-full flex flex-col justify-between overflow-hidden">
          {widget.title && <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">{widget.title}</h4>}
          <div className="overflow-auto flex-1 text-left">
            <table className="w-full text-[10px]">
              <thead>
                <tr className="border-b border-surface-border">
                  {columns.map((c) => (
                    <th key={c} className="p-1.5 font-medium text-gray-500">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr key={i} className="border-b border-surface-border/40">
                    {row.map((cell, j) => (
                      <td key={j} className="p-1.5 text-gray-300 font-mono">{String(cell)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    default:
      return null;
  }
}
