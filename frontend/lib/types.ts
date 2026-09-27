export const RAILWAY_LINES = ["Western", "Central", "Harbour"] as const;

export type RailwayLine = (typeof RAILWAY_LINES)[number];
export type Direction = "UP" | "DN";
export type Priority = "Minor" | "Major" | "Severe";

export interface DelayIncident {
  id: number;
  line: RailwayLine;
  direction: Direction;
  station: string;
  affected_stretch: string;
  delay_minutes: number;
  priority: Priority;
  announcement_text: string;
  created_at: string;
}

export interface DelayStats {
  total_active_delays: number;
  average_delay_minutes: number;
  worst_affected_line: RailwayLine | null;
  most_affected_stretch: string | null;
}

export interface ApiErrorPayload {
  detail?: string;
}
