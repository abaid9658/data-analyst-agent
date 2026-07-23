"use client";

import { Bell, Database, Moon, Search, Sun, Upload } from "lucide-react";
import { useTheme } from "next-themes";
import { useChatStore } from "@/store/chat.store";
import { useDatasets } from "@/hooks/useDatasets";
import { useEffect, useState } from "react";

export function Header() {
  const { theme, setTheme } = useTheme();
  const { selectedDatasetId, setSelectedDatasetId } = useChatStore();
  const { data: datasetsData } = useDatasets();
  const datasets = datasetsData?.datasets ?? [];
  const [showDatasetPicker, setShowDatasetPicker] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const selectedDataset = datasets.find((d) => d.id === selectedDatasetId);

  return (
    <header
      className="h-14 flex items-center justify-between px-4 border-b border-surface-border flex-shrink-0"
      style={{ background: "rgba(10,10,15,0.9)", backdropFilter: "blur(12px)" }}
    >
      {/* Left — Dataset selector */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <button
            onClick={() => setShowDatasetPicker((p) => !p)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-surface-border text-sm text-gray-400 hover:text-gray-200 hover:border-primary-500/50 transition-all"
            style={{ background: "rgba(37,37,64,0.5)" }}
          >
            <Database className="w-3.5 h-3.5" />
            <span className="max-w-[160px] truncate">
              {selectedDataset?.name ?? "No dataset selected"}
            </span>
          </button>

          {showDatasetPicker && (
            <div
              className="absolute top-full left-0 mt-2 w-72 rounded-xl border border-surface-border z-50 py-1 shadow-card-lg"
              style={{ background: "#141425" }}
            >
              <div className="px-3 py-2 border-b border-surface-border">
                <p className="text-xs font-medium text-gray-400">Select dataset</p>
              </div>
              <div className="max-h-48 overflow-y-auto">
                <button
                  onClick={() => { setSelectedDatasetId(null); setShowDatasetPicker(false); }}
                  className="w-full text-left px-3 py-2 text-sm text-gray-400 hover:bg-surface-elevated hover:text-gray-200 transition-colors"
                >
                  None
                </button>
                {datasets.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => { setSelectedDatasetId(d.id); setShowDatasetPicker(false); }}
                    className="w-full text-left px-3 py-2 text-sm hover:bg-surface-elevated transition-colors"
                  >
                    <p className="text-gray-200 truncate">{d.name}</p>
                    <p className="text-xs text-gray-500">
                      {d.row_count?.toLocaleString()} rows · {d.file_type?.toUpperCase()}
                    </p>
                  </button>
                ))}
              </div>
              <div className="border-t border-surface-border px-3 py-2">
                <a href="/datasets" className="flex items-center gap-2 text-xs text-primary-400 hover:text-primary-300 transition-colors">
                  <Upload className="w-3 h-3" />
                  Upload new dataset
                </a>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Right — Actions */}
      <div className="flex items-center gap-1">
        {/* Search (placeholder) */}
        <button className="p-2 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-all">
          <Search className="w-4 h-4" />
        </button>

        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="p-2 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-all"
        >
          {!mounted ? (
            <div className="w-4 h-4" />
          ) : theme === "dark" ? (
            <Sun className="w-4 h-4" />
          ) : (
            <Moon className="w-4 h-4" />
          )}
        </button>

        {/* Notifications */}
        <button className="p-2 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-all relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-primary-500" />
        </button>
      </div>
    </header>
  );
}
