"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { databaseService } from "@/services/database.service";
import { dbConnectionSchema, type DbConnectionFormData } from "@/lib/validators";
import { useState } from "react";
import { Loader2 } from "lucide-react";

export function ConnectionForm() {
  const queryClient = useQueryClient();
  const [testResult, setTestResult] = useState<{ status: string; latency_ms?: number } | null>(null);
  const [testError, setTestError] = useState<string | null>(null);
  const [testing, setTesting] = useState(false);

  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<DbConnectionFormData>({
    resolver: zodResolver(dbConnectionSchema),
    defaultValues: {
      port: 5432,
      type: "postgresql",
      ssl: false,
    },
  });

  const saveMutation = useMutation({
    mutationFn: (data: DbConnectionFormData) =>
      databaseService.connect({
        name: data.name,
        type: data.type,
        config: {
          host: data.host,
          port: data.port,
          database: data.database,
          username: data.username,
          password: data.password,
          ssl: data.ssl,
        },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["connections"] });
      setTestResult({ status: "Saved Successfully" });
      setTestError(null);
    },
    onError: (err: any) => {
      setTestError(err.response?.data?.detail ?? "Failed to save connection");
    },
  });

  const handleTestConnection = async () => {
    setTesting(true);
    setTestResult(null);
    setTestError(null);
    const vals = getValues();
    try {
      const res = await databaseService.testConnection({
        type: vals.type,
        config: {
          host: vals.host,
          port: Number(vals.port),
          database: vals.database,
          username: vals.username,
          password: vals.password,
          ssl: vals.ssl,
        },
      });
      setTestResult(res);
    } catch (err: any) {
      setTestError(err.response?.data?.detail ?? "Connection test failed");
    } finally {
      setTesting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit((d) => saveMutation.mutate(d))} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs text-gray-400 block mb-1">Connection Name</label>
          <input
            {...register("name")}
            placeholder="e.g. Analytics DB"
            className="input-field text-sm"
          />
          {errors.name && <p className="text-xs text-red-400 mt-1">{errors.name.message}</p>}
        </div>

        <div>
          <label className="text-xs text-gray-400 block mb-1">Database Type</label>
          <select {...register("type")} className="input-field text-sm">
            <option value="postgresql">PostgreSQL</option>
            <option value="mysql">MySQL</option>
            <option value="sqlite">SQLite</option>
            <option value="sqlserver">SQL Server</option>
            <option value="mongodb">MongoDB</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2">
          <label className="text-xs text-gray-400 block mb-1">Host</label>
          <input
            {...register("host")}
            placeholder="127.0.0.1"
            className="input-field text-sm"
          />
          {errors.host && <p className="text-xs text-red-400 mt-1">{errors.host.message}</p>}
        </div>
        <div>
          <label className="text-xs text-gray-400 block mb-1">Port</label>
          <input
            type="number"
            {...register("port", { valueAsNumber: true })}
            className="input-field text-sm"
          />
          {errors.port && <p className="text-xs text-red-400 mt-1">{errors.port.message}</p>}
        </div>
      </div>

      <div>
        <label className="text-xs text-gray-400 block mb-1">Database Name</label>
        <input
          {...register("database")}
          placeholder="production_db"
          className="input-field text-sm"
        />
        {errors.database && <p className="text-xs text-red-400 mt-1">{errors.database.message}</p>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs text-gray-400 block mb-1">Username</label>
          <input
            {...register("username")}
            placeholder="db_user"
            className="input-field text-sm"
          />
          {errors.username && <p className="text-xs text-red-400 mt-1">{errors.username.message}</p>}
        </div>
        <div>
          <label className="text-xs text-gray-400 block mb-1">Password</label>
          <input
            type="password"
            {...register("password")}
            placeholder="••••••••"
            className="input-field text-sm"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <input type="checkbox" {...register("ssl")} id="ssl" className="rounded" />
        <label htmlFor="ssl" className="text-xs text-gray-400">Require SSL</label>
      </div>

      {testResult && (
        <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-xl text-xs text-green-400">
          Connected! Status: {testResult.status}{testResult.latency_ms && ` · Latency: ${testResult.latency_ms}ms`}
        </div>
      )}

      {testError && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-400">
          {testError}
        </div>
      )}

      <div className="flex justify-end gap-2 pt-2 border-t border-surface-border">
        <button
          type="button"
          onClick={handleTestConnection}
          disabled={testing}
          className="btn-ghost flex items-center gap-1 text-xs px-4 py-2"
        >
          {testing && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
          Test Connection
        </button>
        <button
          type="submit"
          disabled={saveMutation.isPending}
          className="btn-primary flex items-center gap-1 text-xs px-4 py-2"
        >
          {saveMutation.isPending && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
          Save Connection
        </button>
      </div>
    </form>
  );
}
