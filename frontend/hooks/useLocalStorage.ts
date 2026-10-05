"use client";

import { useEffect, useState } from "react";

export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(initialValue);
  useEffect(() => { try { const stored = window.localStorage.getItem(key); if (stored) setValue(JSON.parse(stored) as T); } catch { /* storage is optional */ } }, [key]);
  const update = (next: T) => { setValue(next); try { window.localStorage.setItem(key, JSON.stringify(next)); } catch { /* storage is optional */ } };
  return [value, update];
}
