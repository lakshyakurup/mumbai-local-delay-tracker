import type { Severity } from "@/lib/types";

export function formatDelay(minutes: number): string { return minutes === 0 ? "On time" : `${Math.round(minutes)} min late`; }
export function formatUpdated(value?: string): string { return value ? new Intl.DateTimeFormat("en-IN", { hour: "2-digit", minute: "2-digit" }).format(new Date(value)) : "Awaiting signal"; }
export function formatDate(value: string): string { return new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short" }).format(new Date(value)); }
export function severityLabel(severity: Severity): string { return { normal: "Normal", minor: "Minor delay", major: "Major disruption", severe: "Severe disruption" }[severity]; }
export function severityTone(severity: Severity): string { return { normal: "normal", minor: "minor", major: "major", severe: "severe" }[severity]; }
