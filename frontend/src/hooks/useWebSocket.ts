"use client";

import { useEffect, useRef, useState } from "react";
import { LiveMessage } from "@/lib/types";

export function useLiveFeed(url: string | null) {
  const [lastMessage, setLastMessage] = useState<LiveMessage | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!url) return;

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as LiveMessage;
        setLastMessage(data);
      } catch {
        // ignore malformed frames
      }
    };

    // keep-alive ping every 15s so the backend's receive_text() doesn't hang forever
    const ping = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) ws.send("ping");
    }, 15000);

    return () => {
      clearInterval(ping);
      ws.close();
    };
  }, [url]);

  return { lastMessage, connected };
}
