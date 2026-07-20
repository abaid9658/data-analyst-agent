"use client";

import { useEffect, useState } from "react";

interface StreamingTextProps {
  text: string;
  isStreaming?: boolean;
}

/**
 * StreamingText — animates text in character-by-character when streaming is active,
 * then renders the complete text when streaming is done.
 */
export function StreamingText({ text, isStreaming }: StreamingTextProps) {
  const [displayed, setDisplayed] = useState(isStreaming ? "" : text);

  useEffect(() => {
    if (!isStreaming) {
      setDisplayed(text);
      return;
    }
    // Animate last chunk arrival
    setDisplayed(text);
  }, [text, isStreaming]);

  return (
    <span className="whitespace-pre-wrap break-words">
      {displayed}
      {isStreaming && (
        <span className="inline-block w-0.5 h-4 bg-primary-400 ml-0.5 animate-pulse align-middle" />
      )}
    </span>
  );
}
