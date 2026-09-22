"use client";

import { Violation } from "@/lib/types";
import { CheckCircle2 } from "lucide-react";

export default function ViolationsTable({
  violations,
  onResolve,
}: {
  violations: Violation[];
  onResolve: (id: number) => void;
}) {
  return (
    <div className="rounded-xl border border-gray-800 bg-panel overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-gray-900 text-gray-400">
          <tr>
            <th className="text-left px-4 py-2 font-medium">Type</th>
            <th className="text-left px-4 py-2 font-medium">Camera</th>
            <th className="text-left px-4 py-2 font-medium">Confidence</th>
            <th className="text-left px-4 py-2 font-medium">Time</th>
            <th className="text-left px-4 py-2 font-medium">Status</th>
            <th className="text-left px-4 py-2 font-medium"></th>
          </tr>
        </thead>
        <tbody>
          {violations.length === 0 && (
            <tr>
              <td colSpan={6} className="px-4 py-6 text-center text-gray-500">
                No violations recorded.
              </td>
            </tr>
          )}
          {violations.map((v) => (
            <tr key={v.id} className="border-t border-gray-800 text-gray-200">
              <td className="px-4 py-2 text-danger font-medium">{v.violation_type}</td>
              <td className="px-4 py-2">{v.camera_id ?? "—"}</td>
              <td className="px-4 py-2">{(v.confidence * 100).toFixed(0)}%</td>
              <td className="px-4 py-2">{new Date(v.timestamp).toLocaleString()}</td>
              <td className="px-4 py-2">
                {v.resolved ? (
                  <span className="text-safe text-xs">Resolved</span>
                ) : (
                  <span className="text-warn text-xs">Open</span>
                )}
              </td>
              <td className="px-4 py-2">
                {!v.resolved && (
                  <button
                    onClick={() => onResolve(v.id)}
                    className="flex items-center gap-1 text-xs text-gray-400 hover:text-safe transition"
                  >
                    <CheckCircle2 size={14} /> Resolve
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
