"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthStore } from "@/store/auth.store";
import { Loader2 } from "lucide-react";

import { Suspense } from "react";

function OAuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const setTokens = useAuthStore((s) => s.setTokens);

  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");

    if (accessToken && refreshToken) {
      setTokens(accessToken, refreshToken);
      router.replace("/chat");
    } else {
      router.replace("/login");
    }
  }, [searchParams, setTokens, router]);

  return (
    <div className="h-screen flex flex-col items-center justify-center space-y-4" style={{ background: "#0A0A0F" }}>
      <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
      <p className="text-sm text-gray-500">Completing login authorization…</p>
    </div>
  );
}

export default function OAuthCallbackPage() {
  return (
    <Suspense fallback={
      <div className="h-screen flex flex-col items-center justify-center space-y-4" style={{ background: "#0A0A0F" }}>
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
        <p className="text-sm text-gray-500">Completing login authorization…</p>
      </div>
    }>
      <OAuthCallbackContent />
    </Suspense>
  );
}
export const dynamic = "force-dynamic";
