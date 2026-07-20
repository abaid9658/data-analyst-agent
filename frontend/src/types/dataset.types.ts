// ─── Dataset Types ────────────────────────────────────────────────────────────

export interface Dataset {
  id: string;
  name: string;
  description: string | null;
  original_filename: string | null;
  file_type: "csv" | "excel" | "json" | "pdf" | null;
  file_size_bytes: number | null;
  row_count: number | null;
  column_count: number | null;
  schema: DatasetSchema | null;
  status: "processing" | "ready" | "error";
  error_message: string | null;
  created_at: string;
  updated_at: string;
  profile?: DatasetProfile;
}

export interface DatasetColumn {
  name: string;
  type: string;
  nullable: boolean;
  sample_values?: unknown[];
}

export interface DatasetSchema {
  columns: DatasetColumn[];
}

export interface DatasetProfile {
  missing_values: Record<string, number>;
  duplicate_rows: number;
  data_types: Record<string, string>;
  numeric_stats: Record<string, NumericStats>;
  categorical_stats: Record<string, CategoricalStats>;
}

export interface NumericStats {
  mean: number;
  std: number;
  min: number;
  max: number;
  p25: number;
  p50: number;
  p75: number;
}

export interface CategoricalStats {
  unique_count: number;
  top_values: Array<{ value: string; count: number }>;
}

export interface DatasetListResponse {
  datasets: Dataset[];
  total: number;
}

export interface UploadResponse {
  dataset_id: string;
  name: string;
  status: string;
  task_id: string;
  message: string;
}

// ─── Connection Types ─────────────────────────────────────────────────────────

export type ConnectionType = "postgresql" | "mysql" | "sqlite" | "sqlserver" | "mongodb";

export interface DatabaseConnection {
  id: string;
  name: string;
  type: ConnectionType;
  status: "active" | "error" | "disabled";
  last_connected: string | null;
}

export interface ConnectionListResponse {
  connections: DatabaseConnection[];
}

// ─── Chart Types ──────────────────────────────────────────────────────────────

export interface PlotlySpec {
  data: unknown[];
  layout?: Record<string, unknown>;
  config?: Record<string, unknown>;
}
