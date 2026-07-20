"use client";

import { BookOpen } from "lucide-react";
import { motion } from "framer-motion";

interface MessageRAGAnswerProps {
  /** The LLM-synthesized answer text (supports Markdown) */
  answer: string;
  /** List of PDF page numbers cited as sources */
  sources?: number[];
}

export function MessageRAGAnswer({ answer, sources }: MessageRAGAnswerProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-amber-500/20 overflow-hidden max-w-2xl"
      style={{ background: "rgba(245,158,11,0.04)" }}
    >
      {/* Header */}
      <div
        className="flex items-center gap-2 px-4 py-2.5 border-b border-amber-500/10"
        style={{ background: "rgba(245,158,11,0.08)" }}
      >
        <BookOpen className="w-3.5 h-3.5 text-amber-400" />
        <span className="text-xs font-semibold text-amber-400">
          Document Answer
        </span>
        {sources && sources.length > 0 && (
          <span className="ml-auto text-[10px] text-amber-400/70 font-mono">
            Source page{sources.length > 1 ? "s" : ""}:{" "}
            {sources.map((p) => `p.${p}`).join(", ")}
          </span>
        )}
      </div>

      {/* Answer body */}
      <div className="px-4 py-3 text-sm text-gray-200 leading-relaxed whitespace-pre-wrap">
        {answer}
      </div>
    </motion.div>
  );
}
