"use client";

interface ChatContainerProps {
  children: React.ReactNode;
}

export function ChatContainer({ children }: ChatContainerProps) {
  return (
    <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      {children}
    </div>
  );
}
