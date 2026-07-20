"use client";

import { Lightbulb, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

interface MessageInsightsProps {
  insights: string[];
  recommendations?: string[];
}

export function MessageInsights({ insights, recommendations }: MessageInsightsProps) {
  return (
    <div className="space-y-3 max-w-2xl">
      {/* Key Insights */}
      {insights.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-emerald-500/20 overflow-hidden"
          style={{ background: "rgba(16,185,129,0.05)" }}
        >
          <div className="flex items-center gap-2 px-4 py-2.5 border-b border-emerald-500/10">
            <Lightbulb className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-xs font-semibold text-emerald-400">Key Insights</span>
          </div>
          <ul className="px-4 py-3 space-y-2">
            {insights.map((insight, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 flex-shrink-0 mt-1.5" />
                {insight}
              </li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-xl border border-blue-500/20 overflow-hidden"
          style={{ background: "rgba(59,130,246,0.05)" }}
        >
          <div className="flex items-center gap-2 px-4 py-2.5 border-b border-blue-500/10">
            <TrendingUp className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-xs font-semibold text-blue-400">Recommendations</span>
          </div>
          <ul className="px-4 py-3 space-y-2">
            {recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
                <span className="w-4 h-4 rounded-full bg-blue-500/20 text-blue-400 text-[10px] flex-shrink-0 flex items-center justify-center font-bold">
                  {i + 1}
                </span>
                {rec}
              </li>
            ))}
          </ul>
        </motion.div>
      )}
    </div>
  );
}
