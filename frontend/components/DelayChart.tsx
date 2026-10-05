"use client";

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TrendPoint } from "@/lib/types";
import { formatDate } from "@/utils/formatters";

export function DelayChart({ data }: { data: TrendPoint[] }) { return <div className="chart-frame"><ResponsiveContainer width="100%" height={280}><AreaChart data={data}><defs><linearGradient id="delay-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#f3b562" stopOpacity={0.45} /><stop offset="100%" stopColor="#f3b562" stopOpacity={0} /></linearGradient></defs><XAxis dataKey="date" tickFormatter={formatDate} stroke="#708092" tickLine={false} axisLine={false} /><YAxis stroke="#708092" tickLine={false} axisLine={false} unit="m" /><Tooltip contentStyle={{ background: "#18232d", border: "1px solid #30404b", borderRadius: 2 }} /><Area type="monotone" dataKey="average_delay_minutes" stroke="#f3b562" fill="url(#delay-fill)" strokeWidth={2} /></AreaChart></ResponsiveContainer></div>; }
