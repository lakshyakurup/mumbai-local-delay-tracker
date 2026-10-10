import type { DelayRecord, LineStatus, RailwayLine, StatsSummary, StationMetric, TrendPoint } from "@/lib/types";

const DEFAULT_API_ORIGIN = "http://localhost:8000";
const V2_PREFIX = "/api/v2";
const API_V2_BASE = resolveApiV2Base(process.env.NEXT_PUBLIC_API_URL ?? DEFAULT_API_ORIGIN);

type ApiLine = "central" | "western" | "harbour";
type ApiDelayRecord = Omit<DelayRecord, "line"> & { line: ApiLine };
type ApiLineStatus = Omit<LineStatus, "line"> & { line: ApiLine };
type ApiStationMetric = Omit<StationMetric, "line"> & { line: ApiLine };
type ApiStatsSummary = Omit<StatsSummary, "by_line"> & { by_line: Record<ApiLine, number> };

function resolveApiV2Base(rawValue: string): string {
  const trimmed = rawValue.trim();
  try {
    const url = new URL(trimmed || DEFAULT_API_ORIGIN);
    const normalizedPath = url.pathname.replace(/\/+$/, "");
    const basePath = normalizedPath.endsWith(V2_PREFIX) ? normalizedPath : `${normalizedPath === "/" ? "" : normalizedPath}${V2_PREFIX}`;
    return `${url.origin}${basePath}`;
  } catch {
    return `${DEFAULT_API_ORIGIN}${V2_PREFIX}`;
  }
}

function asRailwayLine(line: ApiLine): RailwayLine {
  return `${line.charAt(0).toUpperCase()}${line.slice(1)}` as RailwayLine;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const response = await fetch(`${API_V2_BASE}${normalizedPath}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`API request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function fetchLineStatus(): Promise<LineStatus[]> {
  const rows = await request<ApiLineStatus[]>("/lines/status");
  return rows.map((row) => ({ ...row, line: asRailwayLine(row.line) }));
}

export async function fetchDelaysV2(line?: string): Promise<DelayRecord[]> {
  const query = line ? `?line=${line.toLowerCase()}` : "";
  const rows = await request<ApiDelayRecord[]>(`/delays${query}`);
  return rows.map((row) => ({ ...row, line: asRailwayLine(row.line) }));
}

export async function fetchSummary(): Promise<StatsSummary> {
  const summary = await request<ApiStatsSummary>("/stats/summary");
  return {
    ...summary,
    by_line: Object.fromEntries(
      Object.entries(summary.by_line).map(([line, minutes]) => [asRailwayLine(line as ApiLine), minutes]),
    ),
  };
}

export const fetchTrends = () => request<TrendPoint[]>("/stats/trends");

export async function fetchStations(line: string): Promise<StationMetric[]> {
  const rows = await request<ApiStationMetric[]>(`/lines/${line.toLowerCase()}/stations`);
  return rows.map((row) => ({ ...row, line: asRailwayLine(row.line) }));
}

export const fetchDelays = (line?: string) => fetchDelaysV2(line);
export const fetchStats = () => fetchSummary();
