"use client";

import { useCallback, useEffect, useState } from "react";

import { fetchDelays, fetchStats } from "@/lib/api";
import { DelayIncident, DelayStats, RailwayLine } from "@/lib/types";

const LINES: Array<RailwayLine | "All Lines"> = ["All Lines", "Western", "Central", "Harbour"];
const lineColors: Record<RailwayLine, string> = {
  Western: "border-amber-400/40 bg-amber-400/10 text-amber-200",
  Central: "border-sky-400/40 bg-sky-400/10 text-sky-200",
  Harbour: "border-teal-400/40 bg-teal-400/10 text-teal-200",
};

function timeAgo(value: string): string {
  const minutes = Math.max(0, Math.floor((Date.now() - new Date(value).getTime()) / 60000));
  return minutes < 1 ? "Just now" : `${minutes} min ago`;
}

function priorityClass(priority: DelayIncident["priority"]): string {
  if (priority === "Severe") return "border-rose-400/40 bg-rose-400/10 text-rose-200";
  if (priority === "Major") return "border-orange-400/40 bg-orange-400/10 text-orange-200";
  return "border-lime-400/40 bg-lime-400/10 text-lime-200";
}

export function Dashboard() {
  const [line, setLine] = useState<RailwayLine | "All Lines">("All Lines");
  const [delays, setDelays] = useState<DelayIncident[]>([]);
  const [stats, setStats] = useState<DelayStats | null>(null);
  const [updatedAt, setUpdatedAt] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [nextDelays, nextStats] = await Promise.all([
        fetchDelays(line === "All Lines" ? undefined : line),
        fetchStats(),
      ]);
      setDelays(nextDelays);
      setStats(nextStats);
      setUpdatedAt(new Date().toISOString());
      setError("");
    } catch {
      setError("Could not connect to the delay service. Is FastAPI running on port 8000?");
    } finally {
      setLoading(false);
    }
  }, [line]);

  useEffect(() => {
    loadData();
    const timer = setInterval(loadData, 30000);
    return () => clearInterval(timer);
  }, [loadData]);

  return (
    <main className="min-h-screen bg-rail-bg text-rail-text">
      <section className="mx-auto flex max-w-6xl flex-col gap-7 px-4 py-8 md:px-8">
        <header className="flex flex-col gap-5 border-b border-white/10 pb-7 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-teal-300">Mumbai suburban rail</p>
            <h1 className="text-3xl font-semibold tracking-tight md:text-5xl">Delay Control Room</h1>
            <p className="mt-2 max-w-xl text-sm text-rail-muted">A live view of service interruptions across the city&apos;s three busiest lines.</p>
          </div>
          <button onClick={loadData} disabled={loading} className="rounded-lg border border-white/15 bg-white/5 px-4 py-2 text-sm font-medium transition hover:bg-white/10 disabled:opacity-50">
            {loading ? "Refreshing..." : "Refresh Data"}
          </button>
        </header>

        <section className="grid gap-3 md:grid-cols-3">
          {[
            ["Active disruptions", stats?.total_active_delays ?? 0, "incidents currently tracked"],
            ["Average delay", `${stats?.average_delay_minutes.toFixed(1) ?? "0.0"} min`, "across all lines"],
            ["Most affected stretch", stats?.most_affected_stretch ?? "No active disruption", stats?.worst_affected_line ?? "Awaiting data"],
          ].map(([label, value, detail]) => (
            <article key={label} className="border-l-2 border-teal-300/70 bg-rail-panel px-5 py-4 shadow-card">
              <p className="text-xs uppercase tracking-wider text-rail-muted">{label}</p>
              <p className="mt-2 text-2xl font-semibold">{value}</p>
              <p className="mt-1 text-xs text-rail-muted">{detail}</p>
            </article>
          ))}
        </section>

        <nav className="flex flex-wrap gap-2" aria-label="Filter by railway line">
          {LINES.map((option) => (
            <button key={option} onClick={() => setLine(option)} className={`rounded-full border px-4 py-2 text-sm transition ${line === option ? option === "All Lines" ? "border-white bg-white text-slate-900" : lineColors[option] : "border-white/15 text-rail-muted hover:border-white/35 hover:text-white"}`}>
              {option}
            </button>
          ))}
        </nav>

        <section className="border border-white/10 bg-rail-panel p-5 shadow-card">
          <div className="mb-5 flex items-center justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold">Live incident feed</h2>
              <p className="mt-1 text-xs text-rail-muted">{updatedAt ? `Last checked ${new Date(updatedAt).toLocaleTimeString()}` : "Connecting to service"}</p>
            </div>
            <span className="flex items-center gap-2 text-xs text-teal-200"><span className="h-2 w-2 animate-pulse rounded-full bg-teal-300" />Live</span>
          </div>
          {error ? <p className="text-sm text-rose-300">{error}</p> : null}
          {!loading && !error && delays.length === 0 ? <p className="text-sm text-rail-muted">No disruptions found for this line.</p> : null}
          <div className="space-y-3">
            {delays.map((incident) => (
              <article key={incident.id} className="border border-white/10 bg-[#0d1527] p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`rounded-md border px-2 py-1 text-xs font-medium ${lineColors[incident.line]}`}>{incident.line}</span>
                      <span className={`rounded-md border px-2 py-1 text-xs font-medium ${priorityClass(incident.priority)}`}>{incident.priority}</span>
                      <span className="rounded-md bg-white/10 px-2 py-1 text-xs text-white/80">{incident.direction}</span>
                      <span className="rounded-md bg-white/10 px-2 py-1 text-xs text-white/80">{incident.delay_minutes} min</span>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-white/90">{incident.announcement_text}</p>
                    <div className="mt-3 flex flex-wrap gap-2 text-xs text-rail-muted"><span className="rounded-full border border-white/10 px-2 py-1">{incident.affected_stretch}</span><span className="rounded-full border border-white/10 px-2 py-1">Reported at {incident.station}</span></div>
                  </div>
                  <time className="shrink-0 text-xs text-rail-muted">{timeAgo(incident.created_at)}</time>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
