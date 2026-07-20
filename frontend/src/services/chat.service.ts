import { apiClient, streamSSE } from "@/lib/api-client";
import type { ConversationListResponse, MessageListResponse, SendMessageRequest, StreamChunk } from "@/types/chat.types";

export const chatService = {
  streamMessage: (request: SendMessageRequest): AsyncGenerator<StreamChunk> => {
    return streamSSE("/chat/message", request as Record<string, unknown>) as AsyncGenerator<StreamChunk>;
  },

  getSessions: async (): Promise<ConversationListResponse> => {
    const { data } = await apiClient.get<ConversationListResponse>("/chat/sessions");
    return data;
  },

  getMessages: async (sessionId: string): Promise<MessageListResponse> => {
    const { data } = await apiClient.get<MessageListResponse>(`/chat/sessions/${sessionId}/messages`);
    return data;
  },

  deleteSession: async (sessionId: string): Promise<void> => {
    await apiClient.delete(`/chat/sessions/${sessionId}`);
  },
};
