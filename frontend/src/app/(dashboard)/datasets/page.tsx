"use client";

import { useState } from "react";
import { DatasetUpload } from "@/components/datasets/DatasetUpload";
import { DatasetList } from "@/components/datasets/DatasetList";
import { DatabaseWizard } from "@/components/database/DatabaseWizard";
import { Database, Plus, Upload } from "lucide-react";
import { motion } from "framer-motion";

export default function DatasetsPage() {
  const [wizardOpen, setWizardOpen] = useState(false);

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dataset Manager</h1>
          <p className="text-sm text-gray-500">Upload dataset files or connect to live SQL databases</p>
        </div>
        <button
          onClick={() => setWizardOpen(true)}
          className="btn-ghost flex items-center gap-2 text-sm px-4 py-2"
        >
          <Database className="w-4 h-4" />
          Connect Database
        </button>
      </div>

      {/* Upload card */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-4">Ingest New Dataset</h3>
        <DatasetUpload />
      </div>

      {/* Dataset Grid List */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">Available Datasets</h3>
        <DatasetList />
      </div>

      {/* Database Connection wizard */}
      <DatabaseWizard open={wizardOpen} onClose={() => setWizardOpen(false)} />
    </div>
  );
}
