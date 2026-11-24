import type { Severity } from "@/lib/types";

export function formatDelay(minutes: number): string {
  if (!minutes || minutes === 0) return "On time";
  return `${Math.round(minutes)} min late`;
}

export function formatUpdated(value?: string): string {
  return value
    ? new Intl.DateTimeFormat("en-IN", { hour: "2-digit", minute: "2-digit" }).format(new Date(value))
    : "Awaiting signal";
}

export function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short" }).format(new Date(value));
}

export function severityLabel(status: string): string {
  const map: Record<string, string> = {
    normal: "Normal",
    minor: "Minor delay",
    moderate: "Moderate delay",
    major: "Major disruption",
    severe: "Severe disruption",
    on_time: "On time",
    delayed: "Delayed",
    critical: "Critical",
    unknown: "Unknown",
  };
  return map[status.toLowerCase()] ?? status;
}

export function severityTone(status: string): string {
  const map: Record<string, string> = {
    normal: "normal",
    minor: "minor",
    moderate: "major",
    major: "major",
    severe: "severe",
    on_time: "normal",
    delayed: "major",
    critical: "severe",
    unknown: "minor",
  };
  return map[status.toLowerCase()] ?? "minor";
}
