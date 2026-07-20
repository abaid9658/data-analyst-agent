import { apiClient } from "@/lib/api-client";
import type { DatabaseConnection, ConnectionListResponse } from "@/types/dataset.types";

export interface ConnectRequest {
  name: string;
  type: string;
  config: {
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
    ssl: boolean;
  };
}

export interface TestConnectionResponse {
  status: string;
  latency_ms: number;
  tables_count: number;
}

export const databaseService = {
  /** Test connection without saving */
  testConnection: async (body: { type: string; config: ConnectRequest["config"] }): Promise<TestConnectionResponse> => {
    const { data } = await apiClient.post<TestConnectionResponse>("/database/test", body);
    return data;
  },

  /** Save a new connection */
  connect: async (body: ConnectRequest): Promise<DatabaseConnection> => {
    const { data } = await apiClient.post<DatabaseConnection>("/database/connect", body);
    return data;
  },

  /** List all saved connections */
  listConnections: async (): Promise<ConnectionListResponse> => {
    const { data } = await apiClient.get<ConnectionListResponse>("/database/connections");
    return data;
  },

  /** Delete a connection */
  deleteConnection: async (connectionId: string): Promise<void> => {
    await apiClient.delete(`/database/connections/${connectionId}`);
  },
};
