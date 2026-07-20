import { useTheme as useNextTheme } from "next-themes";

/**
 * useTheme hook — wraps next-themes for consistent dark/light mode control.
 */
export function useTheme() {
  const { theme, setTheme, resolvedTheme, systemTheme } = useNextTheme();

  const isDark = resolvedTheme === "dark";
  const toggleTheme = () => setTheme(isDark ? "light" : "dark");

  return { theme, resolvedTheme, systemTheme, isDark, setTheme, toggleTheme };
}
