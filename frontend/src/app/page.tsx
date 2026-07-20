"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  BarChart2,
  Brain,
  Database,
  FileText,
  MessageSquare,
  Sparkles,
  TrendingUp,
  Upload,
  Zap,
  ChevronRight,
  Check,
} from "lucide-react";

// ─── Landing Page ─────────────────────────────────────────────────────────────

export default function LandingPage() {
  return (
    <main className="min-h-screen overflow-x-hidden" style={{ background: "#0A0A0F" }}>
      {/* ─── Navbar ─────────────────────────────────────────────────── */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-surface-border backdrop-blur-xl"
           style={{ background: "rgba(10,10,15,0.8)" }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg text-white">DataAnalyst AI</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm text-gray-400 hover:text-white transition-colors">Features</a>
            <a href="#how-it-works" className="text-sm text-gray-400 hover:text-white transition-colors">How it works</a>
            <a href="#pricing" className="text-sm text-gray-400 hover:text-white transition-colors">Pricing</a>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-sm text-gray-400 hover:text-white transition-colors px-4 py-2">
              Sign in
            </Link>
            <Link href="/register">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="btn-primary text-sm px-5 py-2"
              >
                Get Started Free
              </motion.button>
            </Link>
          </div>
        </div>
      </nav>

      {/* ─── Hero ───────────────────────────────────────────────────── */}
      <section className="pt-32 pb-24 px-6 relative overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[800px] h-[400px] rounded-full opacity-10"
             style={{ background: "radial-gradient(ellipse, #6366F1, transparent)" }} />
        <div className="absolute top-40 left-1/4 w-[300px] h-[300px] rounded-full opacity-5"
             style={{ background: "radial-gradient(ellipse, #06B6D4, transparent)" }} />

        <div className="max-w-4xl mx-auto text-center relative">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 badge badge-primary mb-8 text-sm"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Powered by GPT-4o + LangGraph
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl md:text-7xl font-black mb-6 leading-tight tracking-tight"
          >
            <span className="text-white">Talk to your</span>{" "}
            <span style={{
              background: "linear-gradient(135deg, #818CF8, #06B6D4)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}>
              data
            </span>
            <br />
            <span className="text-white">like a</span>{" "}
            <span style={{
              background: "linear-gradient(135deg, #6366F1, #4F46E5)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}>
              data scientist
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed"
          >
            Upload any dataset, connect any database, and ask questions in plain English.
            Get instant SQL queries, Python analysis, interactive charts, and ML predictions.
          </motion.p>

          {/* CTA buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex items-center justify-center gap-4 flex-wrap"
          >
            <Link href="/register">
              <motion.button
                whileHover={{ scale: 1.03, boxShadow: "0 0 30px rgba(99,102,241,0.5)" }}
                whileTap={{ scale: 0.97 }}
                className="btn-primary px-8 py-3.5 text-base flex items-center gap-2"
              >
                Start Analyzing Free
                <ChevronRight className="w-4 h-4" />
              </motion.button>
            </Link>
            <Link href="/login">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="btn-ghost px-8 py-3.5 text-base"
              >
                Sign in
              </motion.button>
            </Link>
          </motion.div>

          {/* Trust indicators */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-10 flex items-center justify-center gap-6 text-sm text-gray-500"
          >
            {["No credit card required", "500MB free uploads", "All major databases"].map((item) => (
              <div key={item} className="flex items-center gap-1.5">
                <Check className="w-3.5 h-3.5 text-green-400" />
                {item}
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ─── Chat Preview ────────────────────────────────────────────── */}
      <section className="pb-24 px-6">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="glass-card p-6 relative overflow-hidden"
            style={{ boxShadow: "0 0 60px rgba(99,102,241,0.15)" }}
          >
            {/* Window chrome */}
            <div className="flex items-center gap-2 mb-4 pb-4 border-b border-surface-border">
              <div className="w-3 h-3 rounded-full bg-red-500/60" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
              <div className="w-3 h-3 rounded-full bg-green-500/60" />
              <span className="ml-3 text-xs text-gray-500 font-mono">DataAnalyst AI — sales_2025.csv</span>
            </div>

            {/* Demo conversation */}
            <div className="space-y-4">
              {/* User message */}
              <div className="flex justify-end">
                <div className="msg-user">
                  Show me monthly revenue trend and predict next 3 months 📈
                </div>
              </div>

              {/* AI response */}
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-primary flex-shrink-0 flex items-center justify-center">
                  <Brain className="w-4 h-4 text-white" />
                </div>
                <div className="flex-1 space-y-3">
                  <div className="msg-assistant">
                    <p className="text-gray-200 mb-3">Here&apos;s the monthly revenue analysis with a 3-month forecast:</p>

                    {/* Fake SQL block */}
                    <div className="code-block mb-3">
                      <div className="code-block-header">
                        <span className="text-xs text-gray-400">SQL</span>
                        <span className="text-xs text-gray-500">Generated & Executed</span>
                      </div>
                      <pre className="p-4 text-xs text-green-300 font-mono overflow-x-auto">
{`SELECT DATE_TRUNC('month', order_date) AS month,
       SUM(revenue) AS total_revenue
FROM orders
WHERE order_date >= '2025-01-01'
GROUP BY 1 ORDER BY 1`}
                      </pre>
                    </div>

                    {/* Fake chart placeholder */}
                    <div className="rounded-lg border border-surface-border p-4 mb-3"
                         style={{ background: "rgba(99,102,241,0.05)", minHeight: "120px" }}>
                      <div className="flex items-end gap-2 h-16 px-4">
                        {[40, 55, 45, 70, 65, 85, 78, 92, 88, 110, 105, 130].map((h, i) => (
                          <motion.div
                            key={i}
                            initial={{ height: 0 }}
                            whileInView={{ height: `${h}%` }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.05, duration: 0.4 }}
                            className="flex-1 rounded-sm"
                            style={{
                              background: i >= 9
                                ? "rgba(6,182,212,0.6)"   // Forecast - cyan
                                : "rgba(99,102,241,0.8)", // Actual - indigo
                            }}
                          />
                        ))}
                      </div>
                      <div className="flex justify-between text-xs text-gray-500 mt-2 px-2">
                        <span>Jan</span><span>Mar</span><span>Jun</span>
                        <span>Sep</span><span className="text-cyan-400">Oct-Dec (Forecast)</span>
                      </div>
                    </div>

                    {/* Insights */}
                    <div className="space-y-2">
                      {[
                        "📈 Revenue grew 23% YoY — strongest Q4 on record",
                        "🎯 Forecast: +18% growth expected in next quarter",
                        "⚠️ August dip aligns with summer slowdown pattern",
                      ].map((insight) => (
                        <div key={insight} className="flex items-start gap-2 text-sm text-gray-300">
                          <span className="flex-shrink-0">{insight.charAt(0)}</span>
                          <span>{insight.slice(2)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ─── Features ─────────────────────────────────────────────────── */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Everything you need to analyze data
            </h2>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              A complete data science platform powered by AI agents that think, plan, and execute.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ translateY: -4 }}
                className="glass-card p-6 group"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-all group-hover:scale-110"
                  style={{ background: feature.gradient }}
                >
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Data Sources ─────────────────────────────────────────────── */}
      <section className="py-24 px-6 border-t border-surface-border">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Connect any data source
          </h2>
          <p className="text-gray-400 mb-12">
            Upload files or connect directly to your databases. We handle the rest.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {DATA_SOURCES.map((source) => (
              <motion.div
                key={source}
                whileHover={{ scale: 1.05 }}
                className="glass-card p-4 flex items-center justify-center text-sm font-medium text-gray-300"
              >
                <Database className="w-4 h-4 mr-2 text-primary-400" />
                {source}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── CTA ──────────────────────────────────────────────────────── */}
      <section className="py-24 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="glass-card p-12"
            style={{ boxShadow: "0 0 60px rgba(99,102,241,0.2)" }}
          >
            <Zap className="w-12 h-12 text-primary-400 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to analyze smarter?
            </h2>
            <p className="text-gray-400 mb-8">
              Join thousands of analysts who use DataAnalyst AI every day.
            </p>
            <Link href="/register">
              <motion.button
                whileHover={{ scale: 1.03, boxShadow: "0 0 40px rgba(99,102,241,0.5)" }}
                whileTap={{ scale: 0.97 }}
                className="btn-primary px-10 py-4 text-base"
              >
                Start for Free — No credit card needed
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ─── Footer ───────────────────────────────────────────────────── */}
      <footer className="py-8 px-6 border-t border-surface-border text-center text-sm text-gray-500">
        <p>© 2026 DataAnalyst AI. Built with Next.js, FastAPI, and LangGraph.</p>
      </footer>
    </main>
  );
}

// ─── Data ──────────────────────────────────────────────────────────────────

const FEATURES = [
  {
    title: "Natural Language to SQL",
    description: "Ask questions in plain English. Get optimized, explained SQL instantly.",
    icon: MessageSquare,
    gradient: "linear-gradient(135deg, #6366F1, #4338CA)",
  },
  {
    title: "Auto Visualizations",
    description: "AI picks the best chart type. Interactive Plotly charts for any data.",
    icon: BarChart2,
    gradient: "linear-gradient(135deg, #06B6D4, #0891B2)",
  },
  {
    title: "Machine Learning",
    description: "Auto ML pipeline: regression, classification, clustering, and forecasting.",
    icon: Brain,
    gradient: "linear-gradient(135deg, #8B5CF6, #6D28D9)",
  },
  {
    title: "Trend Analysis",
    description: "Time series analysis, forecasting, and seasonality detection with Prophet.",
    icon: TrendingUp,
    gradient: "linear-gradient(135deg, #10B981, #059669)",
  },
  {
    title: "Upload Any File",
    description: "CSV, Excel, JSON. Auto schema detection and data profiling on upload.",
    icon: Upload,
    gradient: "linear-gradient(135deg, #F59E0B, #D97706)",
  },
  {
    title: "PDF/PPT Reports",
    description: "Generate professional reports with insights, charts, and recommendations.",
    icon: FileText,
    gradient: "linear-gradient(135deg, #EF4444, #DC2626)",
  },
];

const DATA_SOURCES = [
  "CSV Files",
  "Excel",
  "JSON",
  "PostgreSQL",
  "MySQL",
  "SQLite",
  "SQL Server",
  "MongoDB",
];
