"use client";

import { useState } from "react";
import { Check, ChevronDown, ChevronUp, Code, Copy } from "lucide-react";

interface MessageCodeBlockProps {
  code: string;
  language?: string;
  explanation?: string;
}

export function MessageCodeBlock({ code, language = "python", explanation }: MessageCodeBlockProps) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-yellow-500/20 overflow-hidden max-w-2xl">
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-2.5"
        style={{ background: "rgba(234,179,8,0.07)" }}
      >
        <div className="flex items-center gap-2 text-xs font-medium text-yellow-400/80">
          <Code className="w-3.5 h-3.5" />
          {language.toUpperCase()} Code
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

      {/* Code body — collapsed by default (click to expand) */}
      {expanded && (
        <pre
          className="px-4 py-3 text-xs font-mono text-blue-200 overflow-x-auto leading-relaxed max-h-64 overflow-y-auto"
          style={{ background: "#0D0D1A" }}
        >
          <code>{code}</code>
        </pre>
      )}

      {!expanded && (
        <button
          onClick={() => setExpanded(true)}
          className="w-full px-4 py-2 text-xs text-gray-500 hover:text-gray-300 text-left transition-colors"
          style={{ background: "#0D0D1A" }}
        >
          {code.split("\n").length} lines · click to expand
        </button>
      )}

      {/* Explanation */}
      {explanation && (
        <div className="px-4 py-2 border-t border-yellow-500/10 text-xs text-gray-400">
          {explanation}
        </div>
      )}
    </div>
  );
}
