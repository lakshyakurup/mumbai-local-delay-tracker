"use client";

import { useEffect, useState } from "react";
import { DelayChart } from "@/components/DelayChart";
import { fetchSummary, fetchTrends } from "@/lib/api";
import type { StatsSummary, TrendItem } from "@/lib/types";

export default function AnalyticsPage() {
  const [summary, setSummary] = useState<StatsSummary | null>(null);
  const [trends, setTrends] = useState<TrendItem[]>([]);

  useEffect(() => {
    void Promise.all([fetchSummary(), fetchTrends()])
      .then(([summaryRes, trendsRes]) => {
        setSummary(summaryRes.summary ?? null);
        setTrends(trendsRes.trends ?? []);
      })
      .catch(() => {
        setSummary(null);
        setTrends([]);
      });
  }, []);

  const chartData = trends.map((t) => ({
    date: typeof t.period === "string" ? t.period : new Date(t.period).toISOString().slice(0, 10),
    average_delay_minutes: t.avg_delay_minutes,
    observations: t.delay_count,
  }));

  return (
    <main className="page-shell content-page">
      <header className="page-heading">
        <p className="eyebrow">Commuter telemetry / 02</p>
        <h1>
          Patterns worth
          <br />
          <em>paying attention to.</em>
        </h1>
      </header>

      <section className="analytics-layout">
        <div className="panel chart-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Rolling window</p>
              <h2>Delay pressure</h2>
            </div>
            <span>{summary?.measurement_period_hours ?? 24}h</span>
          </div>
          <DelayChart data={chartData} />
        </div>

        <div className="panel insight-panel">
          <p className="eyebrow">Readout</p>
          <h2>
            {summary?.peak_hour
              ? `Pressure peaks at ${summary.peak_hour}`
              : "No peak detected"}
          </h2>
          <p>
            Average observed delay across the network is{" "}
            <b>{(summary?.avg_delay_minutes_all_lines ?? 0).toFixed(1)} minutes</b>.
          </p>
          <div className="line-summary">
            <div>
              <span>On-time rate</span>
              <b>{summary?.on_time_percentage ?? 0}%</b>
            </div>
            <div>
              <span>Most delayed</span>
              <b>
                {summary?.most_delayed_station?.name ?? "—"}{" "}
                ({summary?.most_delayed_station?.avg_delay?.toFixed(1) ?? "0"}m)
              </b>
            </div>
            <div>
              <span>Total readings</span>
              <b>{summary?.total_delays_24h ?? 0}</b>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
