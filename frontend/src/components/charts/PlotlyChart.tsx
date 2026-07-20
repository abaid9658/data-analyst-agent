"use client";

import { useEffect, useRef } from "react";
import type { PlotlySpec } from "@/types/chart.types";

interface PlotlyChartProps {
  spec: PlotlySpec;
  className?: string;
}

export function PlotlyChart({ spec, className }: PlotlyChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let mounted = true;

    const renderChart = async () => {
      const Plotly = await import("plotly.js-dist-min");
      if (!mounted || !containerRef.current) return;

      const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ["sendDataToCloud", "editInChartStudio"] as string[],
        displaylogo: false,
        toImageButtonOptions: {
          format: "png",
          scale: 2,
        },
      };

      const layout = {
        ...spec.layout,
        autosize: true,
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { family: "Inter, sans-serif", color: "#C4C6D0", size: 12 },
        margin: { l: 50, r: 20, t: 50, b: 50 },
        legend: {
          bgcolor: "rgba(28,28,46,0.8)",
          bordercolor: "#252540",
          borderwidth: 1,
        },
        xaxis: { ...(spec.layout?.xaxis ?? {}), gridcolor: "#252540", zerolinecolor: "#3A3A60" },
        yaxis: { ...(spec.layout?.yaxis ?? {}), gridcolor: "#252540", zerolinecolor: "#3A3A60" },
      };

      await Plotly.newPlot(containerRef.current, spec.data || [], layout, config);
    };

    renderChart();

    return () => {
      mounted = false;
      if (containerRef.current) {
        import("plotly.js-dist-min").then((Plotly) => {
          if (containerRef.current) Plotly.purge(containerRef.current);
        });
      }
    };
  }, [spec]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{ minHeight: 320, width: "100%" }}
    />
  );
}

export default PlotlyChart;
