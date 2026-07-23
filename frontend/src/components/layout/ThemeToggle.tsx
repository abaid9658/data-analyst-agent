"use client";

import { useTheme } from "@/hooks/useTheme";
import { Moon, Sun } from "lucide-react";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const { isDark, toggleTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-surface-elevated transition-all"
      title={isDark ? "Activate Light Mode" : "Activate Dark Mode"}
    >
      {!mounted ? (
        <div className="w-4 h-4" />
      ) : isDark ? (
        <Sun className="w-4 h-4" />
      ) : (
        <Moon className="w-4 h-4" />
      )}
    </button>
  );
}
