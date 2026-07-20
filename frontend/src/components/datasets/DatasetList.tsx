"use client";

import { useDatasets } from "@/hooks/useDatasets";
import { DatasetCard } from "./DatasetCard";
import { EmptyState } from "@/components/common/EmptyState";
import { CardSkeleton } from "@/components/common/LoadingSkeleton";
import { Database } from "lucide-react";
import { useRouter } from "next/navigation";

export function DatasetList() {
  const { data, isLoading } = useDatasets();
  const datasets = data?.datasets ?? [];
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => <CardSkeleton key={i} />)}
      </div>
    );
  }

  if (!datasets.length) {
    return (
      <EmptyState
        icon={<Database className="w-7 h-7" />}
        title="No datasets yet"
        description="Upload a CSV, Excel, or JSON file to start analyzing your data with AI."
      />
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {datasets.map((dataset) => (
        <DatasetCard
          key={dataset.id}
          dataset={dataset}
          onClick={() => router.push(`/datasets/${dataset.id}`)}
        />
      ))}
    </div>
  );
}
