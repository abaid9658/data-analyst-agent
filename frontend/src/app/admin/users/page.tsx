"use client";

import { Users } from "lucide-react";

export default function AdminUsersPage() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Users className="w-5 h-5 text-indigo-400" />
        <h1 className="text-xl font-bold text-slate-100">User Management</h1>
      </div>
      <p className="text-xs text-slate-400">View and update system users details here.</p>

      <div className="rounded-xl border border-slate-800 p-6 text-center text-xs text-slate-500">
        No additional users registered
      </div>
    </div>
  );
}
