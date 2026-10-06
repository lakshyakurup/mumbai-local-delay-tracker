import type { DelayRecord, LineStatus, StatsSummary, StationMetric, TrendPoint } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, headers: { "Content-Type": "application/json", ...init?.headers }, cache: "no-store" });
  if (!response.ok) throw new Error(`API request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export const fetchLineStatus = () => request<LineStatus[]>("/api/v2/lines/status");
export const fetchDelaysV2 = (line?: string) => request<DelayRecord[]>(`/api/v2/delays${line ? `?line=${line.toLowerCase()}` : ""}`);
export const fetchSummary = () => request<StatsSummary>("/api/v2/stats/summary");
export const fetchTrends = () => request<TrendPoint[]>("/api/v2/stats/trends");
export const fetchStations = (line: string) => request<StationMetric[]>(`/api/v2/lines/${line.toLowerCase()}/stations`);
export const fetchDelays = (line?: string) => fetchDelaysV2(line);
export const fetchStats = () => fetchSummary();
