"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, ShieldAlert, Settings, HardHat } from "lucide-react";
import clsx from "clsx";

const links = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/violations", label: "Violations", icon: ShieldAlert },
  { href: "/settings", label: "Cameras & Settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 shrink-0 bg-gray-950 border-r border-gray-800 h-screen sticky top-0 flex flex-col">
      <div className="flex items-center gap-2 px-5 py-5 border-b border-gray-800">
        <HardHat className="text-warn" size={22} />
        <span className="font-semibold text-white text-sm">PPE Compliance</span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {links.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition",
              pathname === href
                ? "bg-gray-800 text-white"
                : "text-gray-400 hover:bg-gray-900 hover:text-gray-200"
            )}
          >
            <Icon size={18} />
            {label}
          </Link>
        ))}
      </nav>
      <div className="px-5 py-4 text-xs text-gray-600 border-t border-gray-800">
        Real-time PPE Detection v1.0
      </div>
    </aside>
  );
}
