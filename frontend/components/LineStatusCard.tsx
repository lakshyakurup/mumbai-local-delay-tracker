import type { LineStatus } from "@/lib/types";
import { formatDelay, severityLabel, severityTone } from "@/utils/formatters";

export function LineStatusCard({ status }: { status: LineStatus }) { return <article className={`line-card ${severityTone(status.status)}`}><div className="line-card-top"><span className="line-name">{status.line}</span><span className="severity-badge">{severityLabel(status.status)}</span></div><div className="delay-number">{formatDelay(status.average_delay_minutes)}</div><div className="line-card-meta"><span>{status.active_incidents} active observations</span><span>Updated {new Date(status.updated_at).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}</span></div></article>; }
