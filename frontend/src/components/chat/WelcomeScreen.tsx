"use client";

import { motion } from "framer-motion";
import {
  BarChart2,
  Brain,
  Database,
  FileText,
  Sparkles,
  TrendingUp,
  Upload,
} from "lucide-react";

const SUGGESTION_GROUPS = [
  {
    label: "Explore",
    icon: BarChart2,
    color: "#6366F1",
    suggestions: [
      "Show top 10 products by revenue",
      "What are the key statistics of this dataset?",
      "Find the most correlated columns",
    ],
  },
  {
    label: "Visualize",
    icon: TrendingUp,
    color: "#06B6D4",
    suggestions: [
      "Generate a monthly revenue trend chart",
      "Create a heatmap of correlations",
      "Show sales distribution by region",
    ],
  },
  {
    label: "Predict",
    icon: Brain,
    color: "#8B5CF6",
    suggestions: [
      "Forecast next quarter's revenue",
      "Predict customer churn probability",
      "Detect anomalies in the data",
    ],
  },
  {
    label: "Report",
    icon: FileText,
    color: "#10B981",
    suggestions: [
      "Generate an executive summary",
      "Create a full PDF report",
      "List business recommendations",
    ],
  },
];

interface WelcomeScreenProps {
  onSuggestionClick: (text: string) => void;
}

export function WelcomeScreen({ onSuggestionClick }: WelcomeScreenProps) {
  return (
    <div className="py-12 px-4 max-w-3xl mx-auto">
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-primary mb-5 shadow-glow-primary">
          <Brain className="w-9 h-9 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-white mb-3">
          What do you want to analyze?
        </h1>
        <p className="text-gray-400 text-base max-w-lg mx-auto">
          Upload a dataset or connect a database, then ask anything in plain English.
          I&apos;ll handle the SQL, Python, charts, and insights automatically.
        </p>
      </motion.div>

      {/* Upload / Connect CTA */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="flex items-center justify-center gap-3 mb-10"
      >
        <a href="/datasets">
          <button className="btn-primary flex items-center gap-2 px-5 py-2.5 text-sm">
            <Upload className="w-4 h-4" />
            Upload Dataset
          </button>
        </a>
        <a href="/datasets#connect">
          <button className="btn-ghost flex items-center gap-2 px-5 py-2.5 text-sm">
            <Database className="w-4 h-4" />
            Connect Database
          </button>
        </a>
      </motion.div>

      {/* Suggestion groups */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="flex items-center gap-2 mb-4 justify-center">
          <Sparkles className="w-4 h-4 text-primary-400" />
          <span className="text-sm text-gray-400">Try asking...</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {SUGGESTION_GROUPS.map((group, gi) => (
            <motion.div
              key={group.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + gi * 0.07 }}
              className="glass-card p-4"
            >
              <div className="flex items-center gap-2 mb-3">
                <div
                  className="w-6 h-6 rounded-lg flex items-center justify-center"
                  style={{ background: `${group.color}30` }}
                >
                  <group.icon className="w-3.5 h-3.5" style={{ color: group.color }} />
                </div>
                <span className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                  {group.label}
                </span>
              </div>
              <div className="space-y-1.5">
                {group.suggestions.map((s) => (
                  <button
                    key={s}
                    onClick={() => onSuggestionClick(s)}
                    className="w-full text-left text-sm text-gray-400 hover:text-gray-200 px-3 py-2 rounded-lg hover:bg-surface-elevated transition-all group"
                  >
                    <span className="text-primary-400 group-hover:text-primary-300 transition-colors mr-2">→</span>
                    {s}
                  </button>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
