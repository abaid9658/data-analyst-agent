"use client";

import { useState } from "react";
import { Check, ChevronDown, ChevronUp, Copy, Database } from "lucide-react";

interface MessageSQLBlockProps {
  sql: string;
  explanation?: string;
}

export function MessageSQLBlock({ sql, explanation }: MessageSQLBlockProps) {
  const [expanded, setExpanded] = useState(true);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-primary-500/20 overflow-hidden max-w-2xl">
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-2.5"
        style={{ background: "rgba(79,70,229,0.1)" }}
      >
        <div className="flex items-center gap-2 text-xs font-medium text-primary-300">
          <Database className="w-3.5 h-3.5" />
          Generated SQL
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? "Copied" : "Copy"}
          </button>
          <button
            onClick={() => setExpanded((p) => !p)}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* SQL code */}
      {expanded && (
        <pre
          className="px-4 py-3 text-xs font-mono text-green-300 overflow-x-auto leading-relaxed"
          style={{ background: "#0D0D1A" }}
        >
          <code>{sql}</code>
        </pre>
      )}

      {/* Explanation */}
      {explanation && (
        <div className="px-4 py-2 border-t border-primary-500/10 text-xs text-gray-400">
          {explanation}
        </div>
      )}
    </div>
  );
}
