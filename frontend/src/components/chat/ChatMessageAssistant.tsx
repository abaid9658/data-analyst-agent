"use client";

import { motion } from "framer-motion";
import { Brain } from "lucide-react";
import { StreamingText } from "./StreamingText";
import { MessageSQLBlock } from "./MessageSQLBlock";
import { MessageCodeBlock } from "./MessageCodeBlock";
import { MessageInsights } from "./MessageInsights";
import { MessageRAGAnswer } from "./MessageRAGAnswer";
import { PlotlyChart } from "@/components/charts/PlotlyChart";
import type { ChatMessage } from "@/types/chat.types";
import { cn } from "@/lib/utils";

interface ChatMessageAssistantProps {
  message: ChatMessage;
  isStreaming?: boolean;
  className?: string;
}

export function ChatMessageAssistant({ message, isStreaming, className }: ChatMessageAssistantProps) {
  const meta = message.metadata ?? {};

  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      className={cn("flex items-start gap-3", className)}
    >
      {/* AI Avatar */}
      <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-gradient-to-br from-violet-600 to-indigo-600 shadow-glow-sm">
        <Brain className="w-4 h-4 text-white" />
      </div>

      <div className="flex-1 min-w-0 space-y-3">
        {/* Main text content */}
        {message.content && (
          <div
            className="rounded-2xl rounded-tl-md px-4 py-3 text-sm leading-relaxed text-gray-200 max-w-[90%]"
            style={{ background: "rgba(37,37,64,0.6)", border: "1px solid rgba(99,102,241,0.15)" }}
          >
            <StreamingText text={message.content} isStreaming={isStreaming} />
          </div>
        )}

        {/* SQL block */}
        {meta.sql_query && <MessageSQLBlock sql={meta.sql_query} explanation={meta.sql_explanation} />}

        {/* Code block */}
        {meta.python_code && <MessageCodeBlock code={meta.python_code} language="python" explanation={meta.code_explanation} />}

        {/* Chart */}
        {meta.chart_spec && (
          <div className="max-w-2xl">
            <PlotlyChart spec={meta.chart_spec} />
          </div>
        )}

        {/* RAG Answer (PDF document response) */}
        {meta.rag_answer && (
          <MessageRAGAnswer
            answer={meta.rag_answer as string}
            sources={meta.rag_sources as number[] | undefined}
          />
        )}

        {/* Insights */}
        {meta.insights && meta.insights.length > 0 && (
          <MessageInsights insights={meta.insights} recommendations={meta.recommendations} />
        )}
      </div>
    </motion.div>
  );
}
