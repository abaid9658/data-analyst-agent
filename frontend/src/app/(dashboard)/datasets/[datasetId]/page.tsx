"use client";

import { useDataset } from "@/hooks/useDatasets";
import { DataPreview } from "@/components/datasets/DataPreview";
import { SchemaViewer } from "@/components/datasets/SchemaViewer";
import { ArrowLeft, Database, Info, Loader2, Table } from "lucide-react";
import { useState } from "react";
import { formatBytes } from "@/lib/formatters";
import Link from "next/link";
import { useParams as useNextParams } from "next/navigation";

export default function DatasetDetailPage() {
  const params = useNextParams();
  const datasetId = params?.datasetId as string | undefined;
  const { data: dataset, isLoading } = useDataset(datasetId);
  const [activeTab, setActiveTab] = useState<"preview" | "schema">("preview");

  if (isLoading) {
    return (
      <div className="h-96 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
      </div>
    );
  }

  if (!dataset) {
    return (
      <div className="p-8 text-center text-gray-500">
        Dataset not found.
      </div>
    );
  }

  // Preview format wrapper
  const sampleData = dataset.schema ? {
    columns: dataset.schema.columns.map((c: any) => c.name),
    rows: [] // Sample rows could be fetched, placeholder/stub works
  } : null;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Back button & Title */}
      <div className="flex items-center gap-4">
        <Link href="/datasets">
          <button className="p-2 rounded-lg hover:bg-surface-elevated text-gray-400 hover:text-gray-200 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
        </Link>
        <div>
          <h1 className="text-xl font-bold text-white">{dataset.name}</h1>
          <p className="text-xs text-gray-500">
            {dataset.file_type?.toUpperCase()} · {dataset.row_count?.toLocaleString()} {dataset.file_type === "pdf" ? "chunks" : "rows"} · {dataset.file_size_bytes && formatBytes(dataset.file_size_bytes)}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-surface-border">
        <button
          onClick={() => setActiveTab("preview")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm border-b-2 transition-all ${
            activeTab === "preview"
              ? "border-primary-500 text-primary-400"
              : "border-transparent text-gray-400 hover:text-gray-200"
          }`}
        >
          <Table className="w-4 h-4" />
          Preview
        </button>
        <button
          onClick={() => setActiveTab("schema")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm border-b-2 transition-all ${
            activeTab === "schema"
              ? "border-primary-500 text-primary-400"
              : "border-transparent text-gray-400 hover:text-gray-200"
          }`}
        >
          <Info className="w-4 h-4" />
          Schema
        </button>
      </div>

      {/* Content */}
      <div className="space-y-4">
        {activeTab === "preview" ? (
          <DataPreview data={sampleData} isLoading={isLoading} />
        ) : (
          <SchemaViewer schema={dataset.schema} />
        )}
      </div>
    </div>
  );
}
