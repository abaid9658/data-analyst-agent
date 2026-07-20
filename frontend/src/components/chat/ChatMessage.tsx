"use client";

import { motion } from "framer-motion";
import { Brain } from "lucide-react";
import { ChatMessageContent } from "./ChatMessageContent";
import type { ChatMessage as ChatMessageType } from "@/types/chat.types";
import { formatDistanceToNow } from "date-fns";
import { cn } from "@/lib/utils";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[70%]">
          <div className="msg-user">{message.content}</div>
          <p className="text-right text-[10px] text-gray-600 mt-1 pr-1">
            {formatDistanceToNow(new Date(message.created_at ?? Date.now()), { addSuffix: true })}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-primary flex-shrink-0 flex items-center justify-center mt-1 shadow-glow-primary">
        <Brain className="w-4 h-4 text-white" />
      </div>

      {/* Message bubble */}
      <div className="flex-1 min-w-0">
        <div className="msg-assistant">
          <ChatMessageContent message={message} />
        </div>
        <div className="flex items-center gap-3 mt-1 pl-1">
          <p className="text-[10px] text-gray-600">
            {formatDistanceToNow(new Date(message.created_at ?? Date.now()), { addSuffix: true })}
          </p>
          {message.metadata?.model_used && (
            <p className="text-[10px] text-gray-600">· {message.metadata.model_used}</p>
          )}
          {message.processing_time_ms && (
            <p className="text-[10px] text-gray-600">· {(message.processing_time_ms / 1000).toFixed(1)}s</p>
          )}
        </div>
      </div>
    </div>
  );
}
