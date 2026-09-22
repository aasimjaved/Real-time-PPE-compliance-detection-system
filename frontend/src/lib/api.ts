import { Camera, Violation, StatsSummary } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

export const api = {
  getCameras: () => request<Camera[]>("/api/cameras"),
  createCamera: (data: Omit<Camera, "id" | "created_at">) =>
    request<Camera>("/api/cameras", { method: "POST", body: JSON.stringify(data) }),
  deleteCamera: (id: number) => request(`/api/cameras/${id}`, { method: "DELETE" }),
  toggleCamera: (id: number) => request<Camera>(`/api/cameras/${id}/toggle`, { method: "PATCH" }),

  getViolations: (params?: { camera_id?: number; violation_type?: string; resolved?: boolean }) => {
    const qs = new URLSearchParams();
    if (params?.camera_id !== undefined) qs.set("camera_id", String(params.camera_id));
    if (params?.violation_type) qs.set("violation_type", params.violation_type);
    if (params?.resolved !== undefined) qs.set("resolved", String(params.resolved));
    const query = qs.toString() ? `?${qs.toString()}` : "";
    return request<Violation[]>(`/api/violations${query}`);
  },
  resolveViolation: (id: number) =>
    request<Violation>(`/api/violations/${id}/resolve`, { method: "PATCH" }),

  getStatsSummary: () => request<StatsSummary>("/api/stats/summary"),
};

export function wsUrl(cameraId: string, source: string, name: string) {
  const base = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
  const params = new URLSearchParams({ source, name });
  return `${base}/ws/live/${cameraId}?${params.toString()}`;
}
