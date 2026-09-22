"use client";

import { useState } from "react";
import { useLiveFeed } from "@/hooks/useWebSocket";
import { wsUrl } from "@/lib/api";
import { LiveFrameMessage, LiveViolationMessage } from "@/lib/types";

export default function LiveFeed({
  cameraId,
  source,
  name,
}: {
  cameraId: string;
  source: string;
  name: string;
}) {
  const [recentAlert, setRecentAlert] = useState<LiveViolationMessage | null>(null);
  const { lastMessage, connected } = useLiveFeed(wsUrl(cameraId, source, name));

  const frame = lastMessage?.type === "frame" ? (lastMessage as LiveFrameMessage) : null;

  if (lastMessage?.type === "violation") {
    const v = lastMessage as LiveViolationMessage;
    if (v.timestamp !== recentAlert?.timestamp) setRecentAlert(v);
  }

  const violationCount = frame?.detections.filter((d) =>
    d.class_name.startsWith("NO-")
  ).length ?? 0;

  return (
    <div className="rounded-xl overflow-hidden border border-gray-800 bg-panel">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900">
        <div className="flex items-center gap-2">
          <span
            className={`h-2.5 w-2.5 rounded-full ${connected ? "bg-safe" : "bg-gray-600"}`}
          />
          <span className="text-sm font-medium text-gray-200">{name}</span>
        </div>
        <span
          className={`text-xs px-2 py-0.5 rounded-full ${
            violationCount > 0 ? "bg-danger/20 text-danger" : "bg-safe/20 text-safe"
          }`}
        >
          {violationCount > 0 ? `${violationCount} violation(s)` : "Compliant"}
        </span>
      </div>

      <div className="relative aspect-video bg-black flex items-center justify-center">
        {frame ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={`data:image/jpeg;base64,${frame.image}`}
            alt={`Live feed for ${name}`}
            className="w-full h-full object-contain"
          />
        ) : (
          <span className="text-gray-500 text-sm">
            {connected ? "Waiting for frames…" : "Connecting to camera…"}
          </span>
        )}
      </div>

      {recentAlert && (
        <div className="px-4 py-2 bg-danger/10 border-t border-danger/30 text-danger text-xs">
          🚨 {recentAlert.violation_type} detected ({(recentAlert.confidence * 100).toFixed(0)}%
          confidence) at {new Date(recentAlert.timestamp).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
}
