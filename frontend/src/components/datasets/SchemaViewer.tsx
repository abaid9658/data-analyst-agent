"use client";

import type { DatasetSchema } from "@/types/dataset.types";

interface SchemaViewerProps {
  schema: DatasetSchema | null;
}

export function SchemaViewer({ schema }: SchemaViewerProps) {
  if (!schema || !schema.columns || !schema.columns.length) {
    return (
      <div className="py-8 text-center text-sm text-gray-500">
        No schema details available
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-surface-border overflow-hidden">
      <table className="w-full text-xs text-left">
        <thead>
          <tr style={{ background: "rgba(20,20,37,0.8)" }}>
            <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">
              Column Name
            </th>
            <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">
              Data Type
            </th>
            <th className="px-4 py-2.5 text-gray-400 font-medium border-b border-surface-border">
              Nullable
            </th>
          </tr>
        </thead>
        <tbody>
          {schema.columns.map((col) => (
            <tr
              key={col.name}
              className="border-b border-surface-border/50 hover:bg-surface-elevated transition-colors"
            >
              <td className="px-4 py-2.5 text-gray-200 font-semibold font-mono">
                {col.name}
              </td>
              <td className="px-4 py-2.5 text-primary-300 font-mono">
                {col.type.toUpperCase()}
              </td>
              <td className="px-4 py-2.5 text-gray-400">
                {col.nullable ? (
                  <span className="text-yellow-500/80">Yes</span>
                ) : (
                  <span className="text-gray-600">No</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
