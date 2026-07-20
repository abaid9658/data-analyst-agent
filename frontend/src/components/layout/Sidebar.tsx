"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  BarChart2,
  Brain,
  Database,
  FileText,
  History,
  LayoutDashboard,
  LogOut,
  MessageSquare,
  Plus,
  Settings,
  Upload,
  ChevronRight,
  Pin,
} from "lucide-react";
import { useAuthStore } from "@/store/auth.store";
import { useChatStore } from "@/store/chat.store";
import { useConversations } from "@/hooks/useChat";
import { formatDistanceToNow } from "date-fns";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/chat", icon: MessageSquare, label: "Chat" },
  { href: "/datasets", icon: Upload, label: "Datasets" },
  { href: "/dashboards", icon: LayoutDashboard, label: "Dashboards" },
  { href: "/reports", icon: FileText, label: "Reports" },
  { href: "/history", icon: History, label: "History" },
];

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { data: conversationsData } = useConversations();
  const conversations = conversationsData?.sessions ?? [];

  const handleNewChat = () => {
    router.push("/chat");
  };

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <aside
      className="w-60 flex-shrink-0 flex flex-col border-r border-surface-border h-full"
      style={{ background: "#0F0F1A" }}
    >
      {/* Logo */}
      <div className="px-4 py-4 border-b border-surface-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center flex-shrink-0">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold text-sm text-white">DataAnalyst AI</span>
            <div className="badge badge-primary text-[10px] px-1.5 py-0 ml-1">Beta</div>
          </div>
        </div>
      </div>

      {/* New Chat Button */}
      <div className="px-3 py-3">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleNewChat}
          className="w-full btn-primary py-2 text-sm flex items-center justify-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Analysis
        </motion.button>
      </div>

      {/* Navigation */}
      <nav className="px-3 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link key={item.href} href={item.href}>
              <div className={cn("sidebar-item", isActive && "active")}>
                <item.icon className="w-4 h-4 flex-shrink-0" />
                <span>{item.label}</span>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Divider */}
      <div className="mx-3 my-3 h-px bg-surface-border" />

      {/* Recent Conversations */}
      <div className="flex-1 overflow-y-auto px-3 min-h-0">
        <p className="text-[11px] text-gray-500 font-medium uppercase tracking-wider px-2 mb-2">
          Recent
        </p>
        <div className="space-y-0.5">
          {conversations.slice(0, 10).map((conv) => {
            const isActive = pathname === `/chat/${conv.id}`;
            return (
              <Link key={conv.id} href={`/chat/${conv.id}`}>
                <div
                  className={cn(
                    "sidebar-item group relative",
                    isActive && "active"
                  )}
                >
                  <MessageSquare className="w-3.5 h-3.5 flex-shrink-0 opacity-60" />
                  <div className="flex-1 min-w-0">
                    <p className="truncate text-xs leading-tight">
                      {conv.title || "Untitled Analysis"}
                    </p>
                    <p className="text-[10px] text-gray-500 mt-0.5">
                      {formatDistanceToNow(new Date(conv.updated_at ?? Date.now()), { addSuffix: true })}
                    </p>
                  </div>
                </div>
              </Link>
            );
          })}

          {conversations.length === 0 && (
            <p className="text-xs text-gray-600 px-2 py-2">No conversations yet</p>
          )}
        </div>
      </div>

      {/* Bottom section */}
      <div className="border-t border-surface-border px-3 py-3 space-y-0.5">
        <Link href="/settings">
          <div className={cn("sidebar-item", pathname === "/settings" && "active")}>
            <Settings className="w-4 h-4 flex-shrink-0" />
            <span>Settings</span>
          </div>
        </Link>

        {/* User */}
        <div className="flex items-center gap-3 px-3 py-2 mt-1">
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #6366F1, #4F46E5)" }}
          >
            {user?.full_name?.[0]?.toUpperCase() ?? "U"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-gray-200 truncate">{user?.full_name}</p>
            <p className="text-[10px] text-gray-500 truncate">{user?.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="text-gray-500 hover:text-red-400 transition-colors p-1"
            title="Logout"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </aside>
  );
}
