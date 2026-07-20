"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { databaseService } from "@/services/database.service";
import { Database, Trash2 } from "lucide-react";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { useState } from "react";
import { ConfirmDialog } from "@/components/common/ConfirmDialog";

export function ConnectionList() {
  const queryClient = useQueryClient();
  const [selectedConnectionId, setSelectedConnectionId] = useState<string | null>(null);

  const { data: connectionsData, isLoading } = useQuery({
    queryKey: ["connections"],
    queryFn: () => databaseService.listConnections(),
  });

  const deleteMutation = useMutation({
    mutationFn: (connectionId: string) => databaseService.deleteConnection(connectionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["connections"] });
      setSelectedConnectionId(null);
    },
  });

  const connections = connectionsData?.connections ?? [];

  if (isLoading) {
    return <TableSkeleton rows={3} cols={4} />;
  }

  if (connections.length === 0) {
    return (
      <div className="py-8 text-center text-sm text-gray-500">
        No active database connections. Use the form below to connect.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {connections.map((conn) => (
        <div
          key={conn.id}
          className="flex items-center justify-between p-4 rounded-xl border border-surface-border"
          style={{ background: "rgba(37,37,64,0.3)" }}
        >
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary-500/10 flex items-center justify-center text-primary-400">
              <Database className="w-4 h-4" />
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-200">{conn.name}</p>
              <p className="text-xs text-gray-500">
                {conn.type.toUpperCase()} · Status:{" "}
                <span className="text-green-400">{conn.status}</span>
              </p>
            </div>
          </div>

          <button
            onClick={() => setSelectedConnectionId(conn.id)}
            className="p-1.5 rounded-lg text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      ))}

      <ConfirmDialog
        open={selectedConnectionId !== null}
        title="Remove Database Connection"
        description="Are you sure you want to delete this database connection? This cannot be undone."
        confirmLabel="Remove"
        danger
        onConfirm={() => {
          if (selectedConnectionId) {
            deleteMutation.mutate(selectedConnectionId);
          }
        }}
        onCancel={() => setSelectedConnectionId(null)}
      />
    </div>
  );
}
