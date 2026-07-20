"use client";

import { ShieldAlert } from "lucide-react";

export default function AdminAuditLogsPage() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <ShieldAlert className="w-5 h-5 text-orange-400" />
        <h1 className="text-xl font-bold text-slate-100">Audit Logs</h1>
      </div>
      <p className="text-xs text-slate-400">Security history audits and tool run logs</p>

      <div className="rounded-xl border border-slate-800 p-6 text-center text-xs text-slate-500">
        No log activities recorded
      </div>
    </div>
  );
}
