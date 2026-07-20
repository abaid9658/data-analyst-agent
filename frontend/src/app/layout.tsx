import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
import { QueryProvider } from "@/providers/QueryProvider";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AI Data Analyst Agent",
  description:
    "Production-ready AI Data Analyst — upload datasets, connect databases, ask questions in plain English, and get intelligent insights, SQL, visualizations, and ML predictions automatically.",
  keywords: [
    "AI Data Analyst",
    "Data Analysis",
    "SQL Generator",
    "Machine Learning",
    "Data Visualization",
    "Business Intelligence",
  ],
  authors: [{ name: "AI Data Analyst Team" }],
  openGraph: {
    title: "AI Data Analyst Agent",
    description: "Talk to your data. Get instant insights.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased" style={{ backgroundColor: "#0A0A0F" }}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false}
          disableTransitionOnChange
        >
          <QueryProvider>{children}</QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
