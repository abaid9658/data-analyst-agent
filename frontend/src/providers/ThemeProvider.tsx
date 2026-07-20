"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";
import React from "react";

/** Wraps next-themes ThemeProvider with forced dark mode as default */
export function ThemeProvider({ children, ...props }: React.ComponentProps<typeof NextThemesProvider>) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem
      disableTransitionOnChange={false}
      {...props}
    >
      {children}
    </NextThemesProvider>
  );
}
