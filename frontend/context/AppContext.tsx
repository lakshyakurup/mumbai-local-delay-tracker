"use client";

import { createContext, useContext, type ReactNode } from "react";
import { useLiveDelays } from "@/hooks/useLiveDelays";

type AppContextValue = ReturnType<typeof useLiveDelays>;
const AppContext = createContext<AppContextValue | null>(null);

export function AppProvider({ children }: { children: ReactNode }) { return <AppContext.Provider value={useLiveDelays()}>{children}</AppContext.Provider>; }
export function useAppContext(): AppContextValue { const context = useContext(AppContext); if (!context) throw new Error("useAppContext must be used inside AppProvider"); return context; }
