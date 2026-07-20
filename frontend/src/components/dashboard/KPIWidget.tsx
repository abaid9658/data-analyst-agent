"use client";

import { cn } from "@/lib/utils";

interface KPIWidgetProps {
  title: string;
  value: string | number;
  change?: string | number;
  changeType?: "positive" | "negative" | "neutral";
  className?: string;
}

export function KPIWidget({ title, value, change, changeType = "neutral", className }: KPIWidgetProps) {
  return (
    <div className={cn("glass-card p-5 space-y-2 flex flex-col justify-between", className)}>
      <p className="text-xs text-gray-500 font-medium uppercase tracking-wider">{title}</p>
      <div className="flex items-baseline justify-between">
        <span className="text-2xl font-bold text-gray-200">{value}</span>
        {change && (
          <span
            className={cn(
              "text-xs font-semibold px-2 py-0.5 rounded-full",
              changeType === "positive" && "bg-green-500/15 text-green-400",
              changeType === "negative" && "bg-red-500/15 text-red-400",
              changeType === "neutral" && "bg-gray-500/15 text-gray-400"
            )}
          >
            {changeType === "positive" ? "+" : ""}
            {change}%
          </span>
        )}
      </div>
    </div>
  );
}
