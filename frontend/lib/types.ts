export const RAILWAY_LINES = ["Central", "Western", "Harbour"] as const;
export type RailwayLine = (typeof RAILWAY_LINES)[number];

export type Severity = "normal" | "minor" | "moderate" | "severe";
export type LineStatusCode = "ON_TIME" | "DELAYED" | "CRITICAL" | "UNKNOWN";

export interface DelayRecord {
  id: string;
  line: string;
  station: string;
  delay_minutes: number;
  direction?: string | null;
  severity: Severity;
  source?: string;
  created_at: string;
  updated_at?: string;
}

export interface DelaysListResponse {
  delays: DelayRecord[];
  count: number;
  total_records: number;
  page: number;
  limit: number;
}

export interface LineStatusItem {
  line_id: string;
  line_name: string;
  status: LineStatusCode;
  avg_delay_minutes: number;
  delay_percentage: number;
  last_updated: string;
  station_count: number;
  delayed_stations: number;
}

export interface LinesStatusResponse {
  lines: LineStatusItem[];
  timestamp: string;
}

export interface StationMetric {
  station_id: string;
  name: string;
  order: number;
  avg_delay_minutes: number;
  incidents_7d: number;
  on_time_percentage: number;
  last_delay?: string | null;
  passenger_volume_estimate?: number | null;
}

export interface LineStationsResponse {
  line: string;
  stations: StationMetric[];
}

export interface MostDelayedStation {
  name: string;
  line: string;
  avg_delay: number;
}

export interface StatsSummary {
  avg_delay_minutes_all_lines: number;
  peak_hour: string;
  peak_hour_avg_delay: number;
  total_delays_24h: number;
  most_delayed_station: MostDelayedStation;
  on_time_percentage: number;
  measurement_period_hours: number;
}

export interface StatsSummaryResponse {
  summary: StatsSummary;
  timestamp: string;
}

export interface LineBreakdownDetail {
  avg_delay: number;
  count: number;
}

export interface TrendItem {
  period: string;
  avg_delay_minutes: number;
  delay_count: number;
  line_breakdown: Record<string, LineBreakdownDetail>;
}

export interface StatsTrendsResponse {
  trends: TrendItem[];
  granularity: "hourly" | "daily" | "weekly";
}

// Backwards-compatible aliases used by older components
export type LineStatus = LineStatusItem;
export type TrendPoint = TrendItem;
export type DelayIncident = DelayRecord;
