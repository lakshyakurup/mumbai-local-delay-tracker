import type {
  DelayRecord,
  DelaysListResponse,
  LinesStatusResponse,
  LineStationsResponse,
  StatsSummaryResponse,
  StatsTrendsResponse,
} from "@/lib/types";

const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
    cache: "no-store",
  });
  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`API request failed (${response.status}): ${text || response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export const fetchLineStatus = async (): Promise<LinesStatusResponse> => {
  return request<LinesStatusResponse>("/api/v2/lines/status");
};

export const fetchDelaysV2 = async (line?: string): Promise<DelaysListResponse> => {
  const qs = line ? `?line=${encodeURIComponent(line.toLowerCase())}` : "";
  return request<DelaysListResponse>(`/api/v2/delays${qs}`);
};

export const fetchDelays = async (line?: string): Promise<DelayRecord[]> => {
  const data = await fetchDelaysV2(line);
  return data.delays ?? [];
};

export const fetchSummary = async (): Promise<StatsSummaryResponse> => {
  return request<StatsSummaryResponse>("/api/v2/stats/summary");
};

export const fetchStats = fetchSummary;

export const fetchTrends = async (): Promise<StatsTrendsResponse> => {
  return request<StatsTrendsResponse>("/api/v2/stats/trends");
};

export const fetchStations = async (line: string): Promise<LineStationsResponse> => {
  return request<LineStationsResponse>(`/api/v2/lines/${encodeURIComponent(line.toLowerCase())}/stations`);
};
