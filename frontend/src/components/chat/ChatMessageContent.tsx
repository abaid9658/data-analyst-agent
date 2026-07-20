"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import {
  Check,
  ChevronDown,
  ChevronUp,
  Copy,
  Download,
  Lightbulb,
  Play,
} from "lucide-react";
import type { ChatMessage } from "@/types/chat.types";

// Lazy-load Plotly to reduce initial bundle
const PlotlyChart = dynamic(() => import("@/components/charts/PlotlyChart"), {
  ssr: false,
  loading: () => (
    <div className="h-64 skeleton rounded-xl" />
  ),
});

interface ChatMessageContentProps {
  message: ChatMessage;
}

export function ChatMessageContent({ message }: ChatMessageContentProps) {
  return (
    <div className="space-y-4">
      {/* Plan steps (collapsed by default) */}
      {message.metadata?.plan_steps && (
        <PlanSteps steps={message.metadata.plan_steps} />
      )}

      {/* SQL block */}
      {message.metadata?.sql_query && (
        <SQLBlock sql={message.metadata.sql_query} />
      )}

      {/* Python code */}
      {message.metadata?.python_code && (
        <CodeBlock code={message.metadata.python_code} language="python" label="Python" />
      )}

      {/* Chart */}
      {message.metadata?.chart_spec && (
        <div className="chart-card overflow-hidden">
          <PlotlyChart spec={message.metadata.chart_spec} />
        </div>
      )}

      {/* Table data */}
      {message.metadata?.table_data && (
        <DataTable data={message.metadata.table_data} />
      )}

      {/* Main text content */}
      {message.content && (
        <div className="prose prose-invert prose-sm max-w-none">
          <ReactMarkdown
            components={{
              code({ node, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                return match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus as Record<string, React.CSSProperties>}
                    language={match[1]}
                    PreTag="div"
                    className="rounded-lg text-xs"
                    {...props}
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code className="bg-surface-elevated px-1.5 py-0.5 rounded text-xs font-mono text-primary-300" {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
      )}

      {/* Key Insights */}
      {message.metadata?.insights && message.metadata.insights.length > 0 && (
        <InsightsList insights={message.metadata.insights} />
      )}
    </div>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function PlanSteps({ steps }: { steps: string[] }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="rounded-lg border border-surface-border overflow-hidden">
      <button
        onClick={() => setExpanded((p) => !p)}
        className="w-full flex items-center justify-between px-4 py-2.5 text-xs text-gray-400 hover:text-gray-200 transition-colors"
        style={{ background: "rgba(37,37,64,0.5)" }}
      >
        <span className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-primary-400 animate-pulse" />
          Executed {steps.length} step{steps.length !== 1 ? "s" : ""}
        </span>
        {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>
      {expanded && (
        <div className="px-4 pb-3 pt-2 space-y-1.5">
          {steps.map((step, i) => (
            <div key={i} className="flex items-start gap-2.5 text-xs text-gray-400">
              <div className="w-5 h-5 rounded-full bg-surface-elevated flex items-center justify-center flex-shrink-0 mt-0.5">
                <Check className="w-3 h-3 text-green-400" />
              </div>
              {step}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function SQLBlock({ sql }: { sql: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="code-block">
      <div className="code-block-header">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-blue-400" />
          <span className="text-xs font-medium text-gray-300">SQL</span>
          <span className="badge badge-primary text-[10px] px-1.5 py-0">Generated & Safe</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 px-2 py-1 rounded transition-colors hover:bg-surface-elevated"
          >
            {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
            {copied ? "Copied" : "Copy"}
          </button>
        </div>
      </div>
      <SyntaxHighlighter
        style={vscDarkPlus as Record<string, React.CSSProperties>}
        language="sql"
        customStyle={{ background: "transparent", padding: "16px", margin: 0, fontSize: "12px" }}
      >
        {sql}
      </SyntaxHighlighter>
    </div>
  );
}

function CodeBlock({ code, language, label }: { code: string; language: string; label: string }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="code-block">
      <div className="code-block-header">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-400" />
          <span className="text-xs font-medium text-gray-300">{label}</span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-200 px-2 py-1 rounded transition-colors hover:bg-surface-elevated"
        >
          {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <SyntaxHighlighter
        style={vscDarkPlus as Record<string, React.CSSProperties>}
        language={language}
        customStyle={{ background: "transparent", padding: "16px", margin: 0, fontSize: "12px" }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

function DataTable({ data }: { data: { columns: string[]; rows: unknown[][] } }) {
  const [showAll, setShowAll] = useState(false);
  const displayRows = showAll ? data.rows : data.rows.slice(0, 10);

  return (
    <div className="rounded-xl border border-surface-border overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-surface-border" style={{ background: "rgba(37,37,64,0.4)" }}>
        <span className="text-xs font-medium text-gray-300">
          Results — {data.rows.length.toLocaleString()} rows
        </span>
        <button className="flex items-center gap-1 text-xs text-primary-400 hover:text-primary-300 transition-colors">
          <Download className="w-3 h-3" />
          Export CSV
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr style={{ background: "rgba(20,20,37,0.8)" }}>
              {data.columns.map((col) => (
                <th key={col} className="px-4 py-2.5 text-left text-gray-400 font-medium whitespace-nowrap border-b border-surface-border">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayRows.map((row, i) => (
              <tr
                key={i}
                className="border-b border-surface-border/50 hover:bg-surface-elevated transition-colors"
              >
                {(row as unknown[]).map((cell, j) => (
                  <td key={j} className="px-4 py-2.5 text-gray-300 whitespace-nowrap font-mono">
                    {cell === null ? <span className="text-gray-600">null</span> : String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.rows.length > 10 && !showAll && (
        <div className="px-4 py-2 text-center border-t border-surface-border">
          <button
            onClick={() => setShowAll(true)}
            className="text-xs text-primary-400 hover:text-primary-300 transition-colors"
          >
            Show all {data.rows.length.toLocaleString()} rows
          </button>
        </div>
      )}
    </div>
  );
}

function InsightsList({ insights }: { insights: string[] }) {
  return (
    <div className="rounded-xl border border-primary-500/20 p-4" style={{ background: "rgba(99,102,241,0.06)" }}>
      <div className="flex items-center gap-2 mb-3">
        <Lightbulb className="w-4 h-4 text-primary-400" />
        <span className="text-xs font-semibold text-primary-300 uppercase tracking-wide">Key Insights</span>
      </div>
      <ul className="space-y-2">
        {insights.map((insight, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
            <span className="text-primary-400 mt-0.5 flex-shrink-0">→</span>
            {insight}
          </li>
        ))}
      </ul>
    </div>
  );
}
