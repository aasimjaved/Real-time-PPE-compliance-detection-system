"use client";

import { useEffect, useState } from "react";
import { Plus, Trash2, Power } from "lucide-react";
import { api } from "@/lib/api";
import { Camera } from "@/lib/types";

export default function SettingsPage() {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [form, setForm] = useState({ name: "", location: "", source: "0" });

  const load = () => api.getCameras().then(setCameras).catch(() => {});

  useEffect(() => {
    load();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.source) return;
    await api.createCamera({ ...form, active: true });
    setForm({ name: "", location: "", source: "0" });
    load();
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-semibold text-white">Cameras & Settings</h1>
        <p className="text-sm text-gray-400">
          Add camera sources — a webcam index (e.g. <code>0</code>), a video file path, or an
          RTSP/HTTP stream URL.
        </p>
      </div>

      <form onSubmit={handleAdd} className="rounded-xl border border-gray-800 bg-panel p-4 space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <input
            placeholder="Camera name (e.g. Main Gate)"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-200 col-span-2"
          />
          <input
            placeholder="Location (optional)"
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            className="bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-200"
          />
          <input
            placeholder="Source (0, rtsp://..., /path/to.mp4)"
            value={form.source}
            onChange={(e) => setForm({ ...form, source: e.target.value })}
            className="bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-200"
          />
        </div>
        <button
          type="submit"
          className="flex items-center gap-2 bg-white text-gray-900 text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-200 transition"
        >
          <Plus size={16} /> Add Camera
        </button>
      </form>

      <div className="space-y-2">
        {cameras.map((cam) => (
          <div
            key={cam.id}
            className="flex items-center justify-between rounded-xl border border-gray-800 bg-panel px-4 py-3"
          >
            <div>
              <p className="text-sm text-gray-200 font-medium">{cam.name}</p>
              <p className="text-xs text-gray-500">
                {cam.location || "No location"} · source: {cam.source}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => api.toggleCamera(cam.id).then(load)}
                className={`flex items-center gap-1 text-xs px-2 py-1 rounded-lg ${
                  cam.active ? "text-safe" : "text-gray-500"
                }`}
              >
                <Power size={14} /> {cam.active ? "Active" : "Inactive"}
              </button>
              <button
                onClick={() => api.deleteCamera(cam.id).then(load)}
                className="text-gray-500 hover:text-danger transition"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-gray-800 bg-panel p-4 text-xs text-gray-500">
        Alert channels (email/Slack webhook) and model path are configured via the backend&apos;s
        <code className="mx-1 text-gray-400">.env</code> file — see <code>backend/.env.example</code>.
      </div>
    </div>
  );
}
