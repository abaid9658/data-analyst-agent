"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { Download, ZoomIn, ZoomOut } from "lucide-react";
import type { PlotlySpec } from "@/types/chart.types";

const PlotlyChart = dynamic(() => import("./PlotlyChart").then((m) => m.PlotlyChart), { ssr: false });

interface ChartCardProps {
  spec: PlotlySpec;
  title?: string;
  explanation?: string;
  chartId?: string;
}

export function ChartCard({ spec, title, explanation, chartId }: ChartCardProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-2xl border border-surface-border overflow-hidden" style={{ background: "rgba(20,20,37,0.8)" }}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-border">
        <span className="text-sm font-semibold text-gray-200 truncate">
          {title ?? "Data Visualization"}
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setExpanded((p) => !p)}
            className="p-1.5 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-colors"
            title={expanded ? "Collapse" : "Expand"}
          >
            {expanded ? <ZoomOut className="w-3.5 h-3.5" /> : <ZoomIn className="w-3.5 h-3.5" />}
          </button>
          {chartId && (
            <a
              href={`/api/v1/chart/${chartId}/download?format=png`}
              download
              className="p-1.5 rounded-lg text-gray-400 hover:text-primary-300 hover:bg-surface-elevated transition-colors"
              title="Download PNG"
            >
              <Download className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>

      {/* Chart body */}
      <div className={expanded ? "h-[480px]" : "h-72"}>
        <PlotlyChart spec={spec} />
      </div>

      {/* Explanation */}
      {explanation && (
        <div className="px-4 py-2.5 border-t border-surface-border text-xs text-gray-400 leading-relaxed">
          {explanation}
        </div>
      )}
    </div>
  );
}
