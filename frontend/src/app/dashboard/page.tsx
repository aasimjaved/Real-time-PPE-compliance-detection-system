"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, ShieldCheck, Activity, CalendarClock } from "lucide-react";
import StatsCard from "@/components/StatsCard";
import ComplianceChart from "@/components/ComplianceChart";
import LiveFeed from "@/components/LiveFeed";
import { api } from "@/lib/api";
import { Camera, StatsSummary } from "@/lib/types";

export default function DashboardPage() {
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [cameras, setCameras] = useState<Camera[]>([]);

  useEffect(() => {
    const load = () => {
      api.getStatsSummary().then(setStats).catch(() => {});
      api.getCameras().then(setCameras).catch(() => {});
    };
    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-white">Site Safety Overview</h1>
        <p className="text-sm text-gray-400">Live PPE compliance monitoring across all cameras</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          label="Compliance Rate (24h)"
          value={stats ? `${stats.compliance_rate_24h.toFixed(0)}%` : "—"}
          icon={ShieldCheck}
          tone="safe"
        />
        <StatsCard
          label="Violations Today"
          value={stats?.violations_today ?? "—"}
          icon={AlertTriangle}
          tone="danger"
        />
        <StatsCard
          label="Total Violations Logged"
          value={stats?.total_violations ?? "—"}
          icon={Activity}
          tone="warn"
        />
        <StatsCard
          label="Active Cameras"
          value={cameras.filter((c) => c.active).length}
          icon={CalendarClock}
        />
      </div>

      {stats && <ComplianceChart data={stats.trend_last_7_days} />}

      <div>
        <h2 className="text-sm font-medium text-gray-300 mb-3">Live Camera Feeds</h2>
        {cameras.length === 0 ? (
          <p className="text-sm text-gray-500">
            No cameras configured yet. Add one from the Settings page to start monitoring.
          </p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {cameras
              .filter((c) => c.active)
              .map((cam) => (
                <LiveFeed
                  key={cam.id}
                  cameraId={String(cam.id)}
                  source={cam.source}
                  name={cam.name}
                />
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
