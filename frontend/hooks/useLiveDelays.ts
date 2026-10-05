"use client";

import { useCallback, useEffect, useState } from "react";
import { fetchDelaysV2, fetchLineStatus, fetchSummary } from "@/lib/api";
import type { DelayRecord, LineStatus, StatsSummary } from "@/lib/types";

export function useLiveDelays() {
  const [delays, setDelays] = useState<DelayRecord[]>([]);
  const [statuses, setStatuses] = useState<LineStatus[]>([]);
  const [summary, setSummary] = useState<StatsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const refresh = useCallback(async () => { try { const [nextDelays, nextStatuses, nextSummary] = await Promise.all([fetchDelaysV2(), fetchLineStatus(), fetchSummary()]); setDelays(nextDelays); setStatuses(nextStatuses); setSummary(nextSummary); setError(null); } catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to reach the delay service"); } finally { setIsLoading(false); } }, []);
  useEffect(() => { void refresh(); const timer = window.setInterval(() => void refresh(), 30_000); return () => window.clearInterval(timer); }, [refresh]);
  return { delays, statuses, summary, error, isLoading, refresh };
}
