"use client";

import { useUIStore } from "@/store/ui.store";
import { Sidebar } from "./Sidebar";
import { Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function MobileNav() {
  const { mobileNavOpen, setMobileNavOpen } = useUIStore();

  return (
    <div className="md:hidden">
      {/* Trigger Button */}
      <button
        onClick={() => setMobileNavOpen(true)}
        className="p-2 text-gray-400 hover:text-gray-200"
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Drawer */}
      <AnimatePresence>
        {mobileNavOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileNavOpen(false)}
              className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
            />

            {/* Sidebar content drawer */}
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "tween", duration: 0.3 }}
              className="fixed top-0 bottom-0 left-0 w-64 z-50 flex flex-col"
            >
              <div className="absolute top-4 right-4 z-50">
                <button
                  onClick={() => setMobileNavOpen(false)}
                  className="p-1 rounded-lg bg-surface-elevated text-gray-400"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <Sidebar />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
