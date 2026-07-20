"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { reportService } from "@/services/report.service";
import { FileText, Loader2, ArrowRight } from "lucide-react";

interface ReportDownloaderProps {
  sessionId: string;
}

export function ReportDownloader({ sessionId }: ReportDownloaderProps) {
  const [format, setFormat] = useState<"pdf" | "docx" | "pptx" | "xlsx" | "markdown">("pdf");
  const [title, setTitle] = useState("Executive Data Analysis Summary");
  const [reportId, setReportId] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () =>
      reportService.generateReport({
        session_id: sessionId,
        format,
        title,
      }),
    onSuccess: (data) => {
      setReportId(data.report_id);
    },
  });

  return (
    <div className="glass-card p-5 space-y-4">
      <div className="flex items-center gap-2">
        <FileText className="w-5 h-5 text-primary-400" />
        <h3 className="text-sm font-semibold text-gray-200">Compile Executive Report</h3>
      </div>

      <div className="space-y-3">
        <div>
          <label className="text-[10px] text-gray-500 uppercase tracking-wider block mb-1">Report Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="input-field text-xs w-full"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-[10px] text-gray-500 uppercase tracking-wider block mb-1">Export Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value as any)}
              className="input-field text-xs w-full"
            >
              <option value="pdf">PDF Document</option>
              <option value="docx">Word Document</option>
              <option value="pptx">PowerPoint Slides</option>
              <option value="xlsx">Excel Sheet</option>
              <option value="markdown">Markdown Summary</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={() => mutation.mutate()}
              disabled={mutation.isPending}
              className="btn-primary w-full flex items-center justify-center gap-1.5 text-xs py-2 h-[34px]"
            >
              {mutation.isPending ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <>
                  Compile
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {reportId && (
        <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-xl text-xs text-green-400 flex items-center justify-between">
          <span>Report compilation started!</span>
          <a
            href={reportService.getDownloadUrl(reportId)}
            download
            className="underline hover:text-green-300 font-semibold"
          >
            Check Status
          </a>
        </div>
      )}

      {mutation.isError && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-400">
          Failed to queue report generation.
        </div>
      )}
    </div>
  );
}
