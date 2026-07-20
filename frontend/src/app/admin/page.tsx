"use client";

import Link from "next/link";
import { Users, ShieldAlert } from "lucide-react";

export default function AdminPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">System Overview</h1>
        <p className="text-xs text-slate-400">Admin operations and auditing logs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link href="/admin/users">
          <div className="p-5 border border-slate-800 rounded-xl hover:bg-slate-800/40 transition-colors flex items-center gap-4 cursor-pointer">
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400">
              <Users className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">User Management</p>
              <p className="text-xs text-slate-500">Edit, activate, or disable user log entries</p>
            </div>
          </div>
        </Link>

        <Link href="/admin/audit-logs">
          <div className="p-5 border border-slate-800 rounded-xl hover:bg-slate-800/40 transition-colors flex items-center gap-4 cursor-pointer">
            <div className="w-10 h-10 rounded-lg bg-orange-500/10 flex items-center justify-center text-orange-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-200">Audit Logs</p>
              <p className="text-xs text-slate-500">Security audits, logins, and tool executions</p>
            </div>
          </div>
        </Link>
      </div>
    </div>
  );
}
