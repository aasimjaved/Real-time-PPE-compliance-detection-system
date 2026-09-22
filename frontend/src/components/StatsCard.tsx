import { LucideIcon } from "lucide-react";
import clsx from "clsx";

export default function StatsCard({
  label,
  value,
  icon: Icon,
  tone = "neutral",
}: {
  label: string;
  value: string | number;
  icon: LucideIcon;
  tone?: "neutral" | "danger" | "safe" | "warn";
}) {
  const toneClasses = {
    neutral: "text-gray-200 bg-gray-800",
    danger: "text-danger bg-danger/10",
    safe: "text-safe bg-safe/10",
    warn: "text-warn bg-warn/10",
  }[tone];

  return (
    <div className="rounded-xl border border-gray-800 bg-panel p-4 flex items-center gap-4">
      <div className={clsx("p-3 rounded-lg", toneClasses)}>
        <Icon size={22} />
      </div>
      <div>
        <p className="text-xs text-gray-400">{label}</p>
        <p className="text-2xl font-semibold text-white">{value}</p>
      </div>
    </div>
  );
}
