// ─── Chat Types ───────────────────────────────────────────────────────────────

export type MessageRole = "user" | "assistant" | "system";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  created_at: string;
  metadata?: MessageMetadata;
  processing_time_ms?: number;
  isStreaming?: boolean;
}

export interface MessageMetadata {
  sql_query?: string;
  sql_explanation?: string;
  python_code?: string;
  code_explanation?: string;
  chart_spec?: PlotlySpec;
  table_data?: TableData;
  insights?: string[];
  recommendations?: string[];
  plan_steps?: string[];
  model_used?: string;
  // RAG — PDF document answers
  rag_answer?: string;
  rag_sources?: number[];   // page numbers
  [key: string]: unknown;
}

export interface TableData {
  columns: string[];
  rows: unknown[][];
  row_count: number;
}

export interface PlotlySpec {
  data: PlotlyTrace[];
  layout?: Record<string, unknown>;
  config?: Record<string, unknown>;
}

export interface PlotlyTrace {
  type: string;
  x?: unknown[];
  y?: unknown[];
  name?: string;
  [key: string]: unknown;
}

export interface StreamChunk {
  type:
    | "thinking"
    | "intent"
    | "plan"
    | "sql"
    | "code"
    | "text"
    | "chart"
    | "table"
    | "analysis"
    | "insights"
    | "rag_answer"
    | "done"
    | "error";
  content: unknown;
}

// ─── Conversation Types ───────────────────────────────────────────────────────

export interface Conversation {
  id: string;
  title: string | null;
  message_count: number;
  dataset_id: string | null;
  data_source_id: string | null;
  created_at: string;
  updated_at: string;
  is_pinned: boolean;
}

export interface ConversationListResponse {
  sessions: Conversation[];
}

export interface MessageListResponse {
  session_id: string;
  messages: ChatMessage[];
}

export interface SendMessageRequest {
  message: string;
  session_id?: string;
  dataset_id?: string;
  connection_id?: string;
  stream?: boolean;
}
