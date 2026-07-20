"use client";

import { X } from "lucide-react";
import { ConnectionList } from "./ConnectionList";
import { ConnectionForm } from "./ConnectionForm";
import { motion, AnimatePresence } from "framer-motion";

interface DatabaseWizardProps {
  open: boolean;
  onClose: () => void;
}

export function DatabaseWizard({ open, onClose }: DatabaseWizardProps) {
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Modal content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
          >
            <div
              className="w-full max-w-2xl rounded-2xl border border-surface-border shadow-card-lg overflow-hidden flex flex-col max-h-[85vh]"
              style={{ background: "#141425" }}
            >
              {/* Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-surface-border">
                <div>
                  <h3 className="text-base font-semibold text-gray-200">Database Connection Wizard</h3>
                  <p className="text-xs text-gray-500">Connect your PostgreSQL, MySQL, SQL Server, or MongoDB databases</p>
                </div>
                <button
                  onClick={onClose}
                  className="text-gray-500 hover:text-gray-300 transition-colors p-1"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Scrollable body content split into List and Form */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                <div>
                  <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Active Connections</h4>
                  <ConnectionList />
                </div>

                <div className="border-t border-surface-border/50 pt-5">
                  <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">Add New Connection</h4>
                  <ConnectionForm />
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
