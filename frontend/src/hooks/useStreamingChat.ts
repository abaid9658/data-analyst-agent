import { useState, useCallback, useRef } from "react";
import { chatService } from "@/services/chat.service";
import { useChatStore } from "@/store/chat.store";
import type { ChatMessage, StreamChunk } from "@/types/chat.types";
const uuidv4 = () =>
  typeof window !== "undefined" && window.crypto?.randomUUID
    ? window.crypto.randomUUID()
    : Math.random().toString(36).substring(2, 15);

export function useStreamingChat(sessionId?: string) {
  const [isLoading, setIsLoading] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const { messages, addMessage, updateLastAssistantMessage } = useChatStore();
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (
      text: string,
      currentSessionId?: string,
      datasetId?: string,
      connectionId?: string
    ) => {
      if (!text.trim() || isLoading) return;

      // Abort any previous request
      abortRef.current?.abort();
      abortRef.current = new AbortController();

      // Add user message immediately
      const userMsg: ChatMessage = {
        id: uuidv4(),
        role: "user",
        content: text,
        created_at: new Date().toISOString(),
      };
      addMessage(userMsg);

      setIsLoading(true);
      setIsThinking(true);

      // Placeholder assistant message
      const assistantId = uuidv4();
      const assistantMsg: ChatMessage = {
        id: assistantId,
        role: "assistant",
        content: "",
        created_at: new Date().toISOString(),
        metadata: {},
        isStreaming: true,
      };
      addMessage(assistantMsg);

      try {
        const stream = chatService.streamMessage({
          message: text,
          session_id: currentSessionId,
          dataset_id: datasetId,
          connection_id: connectionId,
          stream: true,
        });

        let textContent = "";
        const meta: Record<string, unknown> = {};

        for await (const chunk of stream) {
          if (abortRef.current?.signal.aborted) break;

          const typedChunk = chunk as StreamChunk;

          switch (typedChunk.type) {
            case "thinking":
              setIsThinking(true);
              break;

            case "plan":
              setIsThinking(false);
              meta.plan_steps = (typedChunk.content as { steps: string[] }).steps;
              break;

            case "text":
              setIsThinking(false);
              textContent += typedChunk.content || "";
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: meta,
                isStreaming: true,
              });
              break;

            case "sql":
              meta.sql_query = typedChunk.content;
              break;

            case "code":
              meta.python_code = typedChunk.content;
              break;

            case "chart":
              meta.chart_spec = typedChunk.content;
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: { ...meta },
                isStreaming: true,
              });
              break;

            case "table":
              meta.table_data = typedChunk.content;
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: { ...meta },
                isStreaming: true,
              });
              break;

            case "insights":
              meta.insights = typedChunk.content;
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: { ...meta },
                isStreaming: false,
              });
              break;

            case "rag_answer": {
              const ragPayload = typedChunk.content as {
                answer: string;
                sources: number[];
                retrieved_chunks: number;
              };
              // Use the RAG answer as the primary displayed text
              textContent = ragPayload.answer || "";
              meta.rag_answer = ragPayload.answer;
              meta.rag_sources = ragPayload.sources;
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: { ...meta },
                isStreaming: true,
              });
              break;
            }

            case "done":
              updateLastAssistantMessage(assistantId, {
                content: textContent,
                metadata: { ...meta },
                isStreaming: false,
              });
              break;

            case "error":
              updateLastAssistantMessage(assistantId, {
                content: `Error: ${typedChunk.content}`,
                isStreaming: false,
              });
              break;
          }
        }
      } catch (error) {
        if ((error as Error).name !== "AbortError") {
          updateLastAssistantMessage(assistantId, {
            content: "Sorry, I encountered an error. Please try again.",
            isStreaming: false,
          });
        }
      } finally {
        setIsLoading(false);
        setIsThinking(false);
      }
    },
    [isLoading, addMessage, updateLastAssistantMessage]
  );

  const stopGeneration = useCallback(() => {
    abortRef.current?.abort();
    setIsLoading(false);
    setIsThinking(false);
  }, []);

  return {
    messages,
    isLoading,
    isThinking,
    sendMessage,
    stopGeneration,
  };
}
