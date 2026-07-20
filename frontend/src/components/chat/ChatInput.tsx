"use client";

import { useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowUp, Paperclip, Sparkles, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
}

const QUICK_SUGGESTIONS = [
  "Show top 10 products by revenue",
  "Find anomalies in the data",
  "Predict next month's sales",
  "Generate a monthly revenue chart",
  "What are the key trends?",
  "Cluster customers by behavior",
];

export function ChatInput({ onSend, isLoading = false }: ChatInputProps) {
  const [value, setValue] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setValue("");
    // Reset height
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  }, [value, isLoading, onSend]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
    // Auto-resize
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 200) + "px";
    }
  };

  return (
    <div className="space-y-2">
      {/* Quick suggestions */}
      <AnimatePresence>
        {showSuggestions && value.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className="flex flex-wrap gap-2"
          >
            {QUICK_SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => {
                  setValue(s);
                  setShowSuggestions(false);
                  textareaRef.current?.focus();
                }}
                className="text-xs px-3 py-1.5 rounded-full border border-surface-border text-gray-400 hover:text-gray-200 hover:border-primary-500/40 transition-all"
                style={{ background: "rgba(37,37,64,0.5)" }}
              >
                {s}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input box */}
      <div
        className="flex items-end gap-3 rounded-2xl border border-surface-border p-3 transition-all focus-within:border-primary-500/60 focus-within:shadow-glow-primary"
        style={{ background: "rgba(37,37,64,0.6)" }}
      >
        {/* Suggestions toggle */}
        <button
          onClick={() => setShowSuggestions((p) => !p)}
          className={cn(
            "flex-shrink-0 p-2 rounded-lg transition-colors",
            showSuggestions
              ? "text-primary-400 bg-primary-500/10"
              : "text-gray-500 hover:text-gray-300 hover:bg-surface-elevated"
          )}
          title="Quick suggestions"
        >
          <Sparkles className="w-4 h-4" />
        </button>

        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleTextareaChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(false)}
          disabled={isLoading}
          placeholder="Ask anything about your data — e.g. 'Show monthly revenue trend' or 'Find top customers'"
          className="flex-1 bg-transparent text-sm text-gray-200 placeholder-gray-600 resize-none outline-none leading-relaxed min-h-[24px] max-h-[200px]"
          rows={1}
        />

        {/* Character count for long messages */}
        {value.length > 200 && (
          <span className="flex-shrink-0 text-xs text-gray-600 self-center">
            {value.length}
          </span>
        )}

        {/* Send button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          disabled={!value.trim() || isLoading}
          className={cn(
            "flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-all",
            value.trim() && !isLoading
              ? "bg-gradient-primary shadow-glow-primary text-white"
              : "bg-surface-elevated text-gray-600"
          )}
        >
          <ArrowUp className="w-4 h-4" />
        </motion.button>
      </div>

      <p className="text-center text-[10px] text-gray-600">
        AI can make mistakes. Always verify critical analysis.
      </p>
    </div>
  );
}
