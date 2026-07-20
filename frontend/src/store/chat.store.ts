import { create } from "zustand";
import type { ChatMessage } from "@/types/chat.types";

interface ChatState {
  messages: ChatMessage[];
  selectedDatasetId: string | null;
  selectedConnectionId: string | null;

  addMessage: (message: ChatMessage) => void;
  updateLastAssistantMessage: (id: string, updates: Partial<ChatMessage>) => void;
  clearMessages: () => void;
  setSelectedDatasetId: (id: string | null) => void;
  setSelectedConnectionId: (id: string | null) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  selectedDatasetId: null,
  selectedConnectionId: null,

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  updateLastAssistantMessage: (id, updates) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.id === id ? { ...m, ...updates } : m
      ),
    })),

  clearMessages: () => set({ messages: [] }),

  setSelectedDatasetId: (id) => set({ selectedDatasetId: id }),
  setSelectedConnectionId: (id) => set({ selectedConnectionId: id }),
}));
