"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { User } from "lucide-react";
import { useAuthStore } from "@/store/auth.store";
import { cn } from "@/lib/utils";

interface ChatMessageUserProps {
  content: string;
  className?: string;
}

export function ChatMessageUser({ content, className }: ChatMessageUserProps) {
  const user = useAuthStore((s) => s.user);

  return (
    <motion.div
      initial={{ opacity: 0, x: 12 }}
      animate={{ opacity: 1, x: 0 }}
      className={cn("flex items-end gap-3 justify-end", className)}
    >
      <div
        className="max-w-[80%] rounded-2xl rounded-br-md px-4 py-3 text-sm leading-relaxed"
        style={{
          background: "linear-gradient(135deg, #7C3AED, #4F46E5)",
          color: "#fff",
        }}
      >
        <p className="whitespace-pre-wrap break-words">{content}</p>
      </div>

      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-primary-600 flex-shrink-0 flex items-center justify-center overflow-hidden relative">
        {user?.avatar_url ? (
          <Image
            src={user.avatar_url}
            alt="You"
            fill
            className="object-cover"
            unoptimized
          />
        ) : (
          <User className="w-4 h-4 text-white" />
        )}
      </div>
    </motion.div>
  );
}
