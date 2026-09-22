"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

export default function ComplianceChart({
  data,
}: {
  data: { date: string; violations: number }[];
}) {
  return (
    <div className="rounded-xl border border-gray-800 bg-panel p-4">
      <h3 className="text-sm font-medium text-gray-300 mb-3">Violations — Last 7 Days</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
          <XAxis dataKey="date" stroke="#6b7280" fontSize={12} />
          <YAxis stroke="#6b7280" fontSize={12} allowDecimals={false} />
          <Tooltip
            contentStyle={{ background: "#111827", border: "1px solid #1f2937", borderRadius: 8 }}
          />
          <Line type="monotone" dataKey="violations" stroke="#dc2626" strokeWidth={2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
