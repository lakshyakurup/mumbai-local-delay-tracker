export const RAILWAY_LINES = ["Central", "Western", "Harbour"] as const;
export type RailwayLine = (typeof RAILWAY_LINES)[number];
export type Severity = "normal" | "minor" | "major" | "severe";
export interface DelayRecord { id: number; line: string; station: string; direction: string; delay_minutes: number; severity: Severity; announcement?: string; recorded_at: string; }
export interface LineStatus { line: RailwayLine; status: Severity; average_delay_minutes: number; active_incidents: number; updated_at: string; }
export interface StationMetric { line: RailwayLine; station: string; average_delay_minutes: number; trains_observed: number; reliability_percent: number; measured_at: string; }
export interface StatsSummary { window_hours: number; total_records: number; average_delay_minutes: number; peak_hour: number | null; by_line: Record<string, number>; }
export interface TrendPoint { date: string; average_delay_minutes: number; observations: number; }
export interface DelayIncident { id: number; line: RailwayLine; direction: "UP" | "DN"; station: string; affected_stretch: string; delay_minutes: number; priority: "Minor" | "Major" | "Severe"; announcement_text: string; created_at: string; }
export interface DelayStats { total_active_delays: number; average_delay_minutes: number; worst_affected_line: RailwayLine | null; most_affected_stretch: string | null; }
export interface ApiErrorPayload { detail?: string; }
