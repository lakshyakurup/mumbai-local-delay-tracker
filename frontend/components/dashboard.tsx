"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchDelays, fetchStatus } from "@/lib/api";
import { DelayIncident, LineStatus, RailwayLine } from "@/lib/types";

const LINE_OPTIONS: RailwayLine[] = ["Western", "Central", "Harbour"];

function statusChipClass(status: LineStatus["status"]): string {
  if (status === "Normal") {
    return "border-emerald-400/40 bg-emerald-500/10 text-emerald-300";
  }
  if (status === "Minor Delays") {
    return "border-amber-400/40 bg-amber-500/10 text-amber-200";
  }
  return "border-rose-400/40 bg-rose-500/10 text-rose-200";
}

export function Dashboard() {
  const [delays, setDelays] = useState<DelayIncident[]>([]);
  const [status, setStatus] = useState<LineStatus[]>([]);
  const [selectedLine, setSelectedLine] = useState<string>("");
  const [stationFilter, setStationFilter] = useState<string>("");
  const [lastUpdated, setLastUpdated] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function loadData() {
      try {
        setIsLoading(true);
        const [nextDelays, nextStatus] = await Promise.all([
          fetchDelays(selectedLine || undefined),
          fetchStatus(),
        ]);
        setDelays(nextDelays);
        setStatus(nextStatus.lines);
        setLastUpdated(nextStatus.updated_at);
        setError("");
      } catch {
        setError("Could not connect to backend API. Is FastAPI running on port 8000?");
      } finally {
        setIsLoading(false);
      }
    }

    loadData();
    const timer = setInterval(loadData, 15000);
    return () => clearInterval(timer);
  }, [selectedLine]);

  const filteredDelays = useMemo(() => {
    const query = stationFilter.trim().toLowerCase();
    if (!query) {
      return delays;
    }
    return delays.filter((incident) =>
      incident.station.toLowerCase().includes(query),
    );
  }, [delays, stationFilter]);

  const cardData = useMemo(
    () =>
      LINE_OPTIONS.map((line) => {
        const lineStatus = status.find((entry) => entry.line === line);
        return {
          line,
          status: lineStatus?.status ?? "Normal",
          avgDelay: lineStatus?.avg_delay_minutes ?? 0,
          incidents: lineStatus?.incident_count ?? 0,
        };
      }),
    [status],
  );

  return (
    <main className="min-h-screen bg-rail-bg text-rail-text">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -top-32 left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-cyan-400/15 blur-3xl" />
        <div className="absolute bottom-0 left-0 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />
      </div>

      <section className="relative mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-8 md:px-8">
        <header className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-rail-panel/90 p-6 shadow-card backdrop-blur md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">
              Mumbai Local Delay Tracker
            </h1>
            <p className="text-sm text-rail-muted">
              Real-time incident intelligence across Central, Western, and Harbour lines
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-300" />
            Live Feed
          </div>
        </header>

        <div className="grid gap-4 md:grid-cols-3">
          {cardData.map((entry) => (
            <article
              key={entry.line}
              className="rounded-2xl border border-white/10 bg-rail-panelSoft p-4 shadow-card"
            >
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-lg font-semibold">{entry.line} Line</h2>
                <span
                  className={`rounded-full border px-3 py-1 text-xs font-medium ${statusChipClass(entry.status)}`}
                >
                  {entry.status}
                </span>
              </div>
              <p className="text-sm text-rail-muted">
                {entry.avgDelay.toFixed(1)} min avg delay
              </p>
              <p className="mt-1 text-xs text-rail-muted">
                {entry.incidents} active incidents tracked
              </p>
            </article>
          ))}
        </div>

        <section className="rounded-2xl border border-white/10 bg-rail-panel p-4 shadow-card">
          <div className="grid gap-3 md:grid-cols-3">
            <label className="text-sm">
              <span className="mb-1 block text-rail-muted">Railway line</span>
              <select
                className="w-full rounded-lg border border-white/15 bg-[#0c1220] px-3 py-2 text-sm outline-none ring-cyan-300 transition focus:ring-2"
                value={selectedLine}
                onChange={(event) => setSelectedLine(event.target.value)}
              >
                <option value="">All Lines</option>
                {LINE_OPTIONS.map((line) => (
                  <option key={line} value={line}>
                    {line}
                  </option>
                ))}
              </select>
            </label>

            <label className="text-sm md:col-span-2">
              <span className="mb-1 block text-rail-muted">Station search</span>
              <input
                value={stationFilter}
                onChange={(event) => setStationFilter(event.target.value)}
                placeholder="Type station name, e.g., Dadar"
                className="w-full rounded-lg border border-white/15 bg-[#0c1220] px-3 py-2 text-sm outline-none ring-cyan-300 transition focus:ring-2"
              />
            </label>
          </div>
        </section>

        <section className="rounded-2xl border border-white/10 bg-rail-panel p-4 shadow-card">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-lg font-semibold">Live Delay Feed</h3>
            {lastUpdated ? (
              <p className="text-xs text-rail-muted">
                Updated {new Date(lastUpdated).toLocaleTimeString()}
              </p>
            ) : null}
          </div>

          {isLoading ? <p className="text-sm text-rail-muted">Loading incidents...</p> : null}
          {error ? <p className="text-sm text-rose-300">{error}</p> : null}

          {!isLoading && !error && filteredDelays.length === 0 ? (
            <p className="text-sm text-rail-muted">No delays found for this filter.</p>
          ) : null}

          <div className="space-y-3">
            {filteredDelays.map((incident) => (
              <article
                key={incident.id}
                className="flex flex-col gap-2 rounded-xl border border-white/10 bg-[#0d1527] p-3 md:flex-row md:items-start md:justify-between"
              >
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-md bg-cyan-500/15 px-2 py-1 text-xs font-medium text-cyan-200">
                      {incident.line}
                    </span>
                    <span className="rounded-md bg-white/10 px-2 py-1 text-xs font-medium text-white/80">
                      {incident.station}
                    </span>
                    <span className="rounded-md bg-amber-500/15 px-2 py-1 text-xs font-medium text-amber-200">
                      {incident.delay_minutes} min
                    </span>
                  </div>
                  <p className="text-sm text-rail-text">{incident.announcement_text}</p>
                </div>
                <p className="text-xs text-rail-muted md:whitespace-nowrap">
                  {new Date(incident.created_at).toLocaleString()}
                </p>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
