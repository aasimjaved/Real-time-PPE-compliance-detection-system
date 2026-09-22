"use client";

import { useEffect, useState } from "react";
import ViolationsTable from "@/components/ViolationsTable";
import { api } from "@/lib/api";
import { Violation } from "@/lib/types";

export default function ViolationsPage() {
  const [violations, setViolations] = useState<Violation[]>([]);
  const [filter, setFilter] = useState<"all" | "open" | "resolved">("all");

  const load = () => {
    const params = filter === "all" ? undefined : { resolved: filter === "resolved" };
    api.getViolations(params).then(setViolations).catch(() => {});
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  const handleResolve = async (id: number) => {
    await api.resolveViolation(id);
    load();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-white">Violation Log</h1>
          <p className="text-sm text-gray-400">All detected PPE compliance violations</p>
        </div>
        <div className="flex gap-2">
          {(["all", "open", "resolved"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs capitalize transition ${
                filter === f
                  ? "bg-white text-gray-900"
                  : "bg-gray-900 text-gray-400 hover:text-gray-200"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <ViolationsTable violations={violations} onResolve={handleResolve} />
    </div>
  );
}
