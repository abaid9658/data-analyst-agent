"use client";

import { Brain } from "lucide-react";

export function ThinkingIndicator() {
  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-primary flex-shrink-0 flex items-center justify-center shadow-glow-primary">
        <Brain className="w-4 h-4 text-white" />
      </div>

      {/* Bubble */}
      <div className="msg-assistant py-3.5 px-4 flex items-center gap-3">
        {/* Animated dots */}
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="thinking-dot"
              style={{ animationDelay: `${i * 0.2}s` }}
            />
          ))}
        </div>
        <span className="text-sm text-gray-400">Analyzing your data...</span>
      </div>
    </div>
  );
}
