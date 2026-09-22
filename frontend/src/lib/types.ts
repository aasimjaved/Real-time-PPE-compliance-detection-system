export interface Camera {
  id: number;
  name: string;
  location?: string;
  source: string;
  active: boolean;
  created_at: string;
}

export interface Violation {
  id: number;
  camera_id: number | null;
  violation_type: string;
  confidence: number;
  snapshot_path?: string;
  timestamp: string;
  resolved: boolean;
}

export interface StatsSummary {
  total_violations: number;
  violations_today: number;
  compliance_rate_24h: number;
  violations_by_type: Record<string, number>;
  violations_by_camera: Record<string, number>;
  trend_last_7_days: { date: string; violations: number }[];
}

export interface Detection {
  class_name: string;
  confidence: number;
  bbox: [number, number, number, number];
}

export interface LiveFrameMessage {
  type: "frame";
  image: string;
  detections: Detection[];
}

export interface LiveViolationMessage {
  type: "violation";
  violation_type: string;
  confidence: number;
  timestamp: string;
}

export type LiveMessage = LiveFrameMessage | LiveViolationMessage | { type: "error"; message: string };
