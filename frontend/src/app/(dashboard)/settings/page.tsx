"use client";

import { useQuery, useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { useForm } from "react-hook-form";
import { Loader2, Settings, User } from "lucide-react";
import { useState } from "react";

export default function SettingsPage() {
  const [saveSuccess, setSaveSuccess] = useState(false);

  const { data: profile, isLoading } = useQuery({
    queryKey: ["profile"],
    queryFn: async () => {
      const { data } = await apiClient.get("/settings/profile");
      return data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: async (payload: { full_name: string; preferences: any }) => {
      const { data } = await apiClient.put("/settings/profile", payload);
      return data;
    },
    onSuccess: () => {
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    },
  });

  const { register, handleSubmit } = useForm({
    values: {
      full_name: profile?.full_name ?? "",
      theme: profile?.preferences?.theme ?? "dark",
      language: profile?.preferences?.language ?? "en",
    },
  });

  const onSubmit = (values: any) => {
    updateMutation.mutate({
      full_name: values.full_name,
      preferences: {
        theme: values.theme,
        language: values.language,
      },
    });
  };

  if (isLoading) {
    return (
      <div className="p-6 max-w-2xl mx-auto flex justify-center py-20">
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-sm text-gray-500">Configure your profile details and analysis preferences</p>
      </div>

      <div className="glass-card p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="text-xs text-gray-400 block mb-1">Full Name</label>
            <input
              {...register("full_name")}
              type="text"
              className="input-field text-sm"
            />
          </div>

          <div>
            <label className="text-xs text-gray-400 block mb-1">Email Address</label>
            <input
              type="email"
              disabled
              value={profile?.email ?? ""}
              className="input-field text-sm opacity-50 cursor-not-allowed"
            />
            <span className="text-[10px] text-gray-500 mt-1 block">Email address cannot be changed</span>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-gray-400 block mb-1">UI Theme</label>
              <select {...register("theme")} className="input-field text-sm">
                <option value="dark">Dark Theme</option>
                <option value="light">Light Theme</option>
                <option value="system">System Default</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-gray-400 block mb-1">Language</label>
              <select {...register("language")} className="input-field text-sm">
                <option value="en">English (US)</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
              </select>
            </div>
          </div>

          {saveSuccess && (
            <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-xl text-xs text-green-400">
              Preferences saved successfully!
            </div>
          )}

          <div className="flex justify-end pt-4 border-t border-surface-border">
            <button
              type="submit"
              disabled={updateMutation.isPending}
              className="btn-primary flex items-center gap-1 text-xs px-4 py-2"
            >
              {updateMutation.isPending && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
              Save Preferences
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
