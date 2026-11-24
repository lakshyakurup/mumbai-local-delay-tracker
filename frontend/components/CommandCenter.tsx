"use client";

import { useAppContext } from "@/context/AppContext";
import LineCard from "@/components/LineCard";
import LiveIndicator from "@/components/LiveIndicator";
import { LiveTicker } from "@/components/LiveTicker";
import { formatDelay, severityLabel, severityTone } from "@/utils/formatters";

export function CommandCenter() {
  const { delays, statuses, summary, error, isLoading, refresh } = useAppContext();

  const tickerMessages = delays
    .filter((d) => d.notes || d.station)
    .slice(0, 3)
    .map((d) => d.notes || `${d.station} · ${d.delay_minutes} min`);

  return (
    <main className="page-shell">
      <LiveTicker messages={tickerMessages} />
      <header className="hero">
        <div>
          <LiveIndicator />
          <p className="eyebrow">Suburban rail intelligence / 01</p>
          <h1>
            Know the city
            <br />
            <em>between stations.</em>
          </h1>
          <p className="hero-copy">
            A live operational read on Mumbai's Central, Western, and Harbour corridors.
          </p>
        </div>
        <button className="refresh-button" onClick={() => void refresh()} disabled={isLoading}>
          {isLoading ? "Syncing" : "Sync now"}
          <span>↗</span>
        </button>
      </header>

      <section className="status-grid">
        {statuses.length ? (
          statuses.map((status) => (
            <LineCard
              key={status.line_id}
              name={status.line_name}
              status={status.status}
              delayTime={formatDelay(status.avg_delay_minutes)}
              lineColorClass={severityTone(status.status.toLowerCase())}
            />
          ))
        ) : (
          <p className="empty-state">{error ?? "Waiting for the first network reading..."}</p>
        )}
      </section>

      <section className="signal-row">
        <div>
          <span className="metric-label">Network average</span>
          <strong>{formatDelay(summary?.avg_delay_minutes_all_lines ?? 0)}</strong>
        </div>
        <div>
          <span className="metric-label">Readings logged</span>
          <strong>{summary?.total_delays_24h ?? 0}</strong>
        </div>
        <div>
          <span className="metric-label">Peak pressure</span>
          <strong>{summary?.peak_hour ?? "--"}</strong>
        </div>
      </section>

      <section className="incident-list">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Latest observations</p>
            <h2>On the ground</h2>
          </div>
          <span>{delays.length} signals</span>
        </div>
        {delays.slice(0, 8).map((delay) => (
          <article className="incident-row" key={delay.id}>
            <span className={`severity-dot ${delay.severity}`} />
            <div>
              <strong>{delay.station}</strong>
              <span>
                {delay.line} · {delay.direction ?? "—"}
              </span>
            </div>
            <b>{formatDelay(delay.delay_minutes)}</b>
            <time>
              {new Date(delay.created_at).toLocaleTimeString("en-IN", {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </time>
          </article>
        ))}
      </section>
    </main>
  );
}
