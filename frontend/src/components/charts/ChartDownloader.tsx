"use client";

import { Download } from "lucide-react";

interface ChartDownloaderProps {
  chartId: string;
}

export function ChartDownloader({ chartId }: ChartDownloaderProps) {
  const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

  const formats: { label: string; format: string; mime: string }[] = [
    { label: "PNG", format: "png", mime: "image/png" },
    { label: "SVG", format: "svg", mime: "image/svg+xml" },
    { label: "PDF", format: "pdf", mime: "application/pdf" },
  ];

  return (
    <div className="flex items-center gap-1">
      <span className="text-xs text-gray-500 mr-1">Export:</span>
      {formats.map(({ label, format }) => (
        <a
          key={format}
          href={`${BASE}/chart/${chartId}/download?format=${format}`}
          download={`chart.${format}`}
          className="px-2 py-0.5 text-[10px] rounded-md border border-surface-border text-gray-400 hover:text-primary-300 hover:border-primary-500/40 transition-colors"
        >
          {label}
        </a>
      ))}
    </div>
  );
}
