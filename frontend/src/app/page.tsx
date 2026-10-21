'use client';

import React, { useState } from 'react';

interface LineData {
  code: string;
  name: string;
  status: string;
  delay: string;
  ping: string;
  health: string;
  stationsCount: number;
  terminals: string;
}

export default function Home() {
  const [lastSync, setLastSync] = useState<string>('JUST NOW');
  const [networkLatency, setNetworkLatency] = useState<number>(18);

  const lines: LineData[] = [
    { 
      code: 'WR', 
      name: 'Western Line', 
      status: 'ON TIME', 
      delay: '0 mins', 
      ping: '12ms', 
      health: '99.4%',
      stationsCount: 37,
      terminals: 'Churchgate ↔ Dahanu Road'
    },
    { 
      code: 'CR', 
      name: 'Central Line (Main)', 
      status: 'MINOR DELAY', 
      delay: '+6 mins', 
      ping: '24ms', 
      health: '91.8%',
      stationsCount: 62,
      terminals: 'CSMT ↔ Kasara / Khopoli'
    },
    { 
      code: 'HR', 
      name: 'Harbour Line', 
      status: 'OPERATIONAL', 
      delay: '+2 mins', 
      ping: '19ms', 
      health: '96.2%',
      stationsCount: 38,
      terminals: 'CSMT ↔ Panvel / Goregaon'
    },
    { 
      code: 'TH', 
      name: 'Trans-Harbour Line', 
      status: 'ON TIME', 
      delay: '0 mins', 
      ping: '15ms', 
      health: '98.1%',
      stationsCount: 14,
      terminals: 'Thane ↔ Panvel / Vashi'
    }
  ];

  return (
    <div className="min-h-screen bg-[#050508] text-slate-100 font-mono relative overflow-hidden selection:bg-cyan-500 selection:text-black">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293d15_1px,transparent_1px),linear-gradient(to_bottom,#1f293d15_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[250px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none" />

      <header className="border-b border-slate-800/80 bg-[#08090d]/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
          <span className="text-xs tracking-[0.25em] text-cyan-400 font-semibold uppercase">
            MUMBAI_LOCAL // RAIL_COMMAND_v2.0
          </span>
        </div>
        <div className="flex items-center space-x-6 text-xs text-slate-400">
          <div className="flex items-center space-x-2">
            <span className="text-slate-600">SYS_STATUS:</span>
            <span className="text-emerald-400 font-bold">ONLINE</span>
          </div>
          <div className="hidden sm:flex items-center space-x-2">
            <span className="text-slate-600">PULSE:</span>
            <span className="text-cyan-300">{networkLatency}ms</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10 relative z-10 space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between border-b border-slate-800/60 pb-8 gap-6">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-xs tracking-wider mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
              <span>SUBURBAN TRANSIT TELEMETRY</span>
            </div>
            <h1 className="text-3xl md:text-5xl font-black tracking-tight text-white uppercase">
              Know the city <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">between stations.</span>
            </h1>
            <p className="text-slate-400 text-sm mt-2 max-w-xl">
              Real-time operational intelligence across Western, Central, Harbour & Trans-Harbour suburban rail corridors.
            </p>
          </div>

          <button 
            onClick={() => {
              setLastSync('JUST NOW');
              setNetworkLatency(Math.floor(Math.random() * 10) + 12);
            }}
            className="self-start md:self-end px-5 py-2.5 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/40 hover:border-cyan-400 text-cyan-300 text-xs font-semibold uppercase tracking-widest transition-all duration-200 rounded-sm flex items-center space-x-2"
          >
            <span>SYNC TELEMETRY ({lastSync})</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-[#0b0d14] border border-slate-800 p-6 rounded-lg relative overflow-hidden group hover:border-cyan-500/50 transition-colors">
            <div className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-2">Network Average Delay</div>
            <div className="text-3xl font-bold text-white flex items-baseline space-x-2">
              <span>+2.1</span>
              <span className="text-xs font-normal text-slate-400">mins network-wide</span>
            </div>
          </div>
          <div className="bg-[#0b0d14] border border-slate-800 p-6 rounded-lg relative overflow-hidden group hover:border-cyan-500/50 transition-colors">
            <div className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-2">Tracked Stations</div>
            <div className="text-3xl font-bold text-white flex items-baseline space-x-2">
              <span>135+</span>
              <span className="text-xs font-normal text-slate-400">active stations</span>
            </div>
          </div>
          <div className="bg-[#0b0d14] border border-slate-800 p-6 rounded-lg relative overflow-hidden group hover:border-cyan-500/50 transition-colors">
            <div className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-2">Major Interchanges</div>
            <div className="text-3xl font-bold text-white flex items-baseline space-x-2">
              <span>DADAR / KURLA</span>
            </div>
          </div>
        </div>

        <div className="bg-[#0b0d14] border border-slate-800 rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-800/80 flex items-center justify-between bg-[#0e1018]">
            <span className="text-xs tracking-wider text-slate-300 font-bold uppercase">
              MUMBAI_SUBURBAN_NETWORK_STATUS
            </span>
          </div>
          <div className="divide-y divide-slate-800/60">
            {lines.map((line) => (
              <div key={line.code} className="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-900/40 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 rounded bg-slate-900 border border-slate-800 flex items-center justify-center text-cyan-400 font-bold text-sm">
                    {line.code}
                  </div>
                  <div>
                    <div className="text-base font-bold text-white">{line.name}</div>
                    <div className="text-xs text-slate-500">{line.terminals} • {line.stationsCount} Stations</div>
                  </div>
                </div>
                <div className="flex items-center space-x-8">
                  <div className="text-right">
                    <div className="text-xs text-slate-500">AVG DELAY</div>
                    <div className="text-sm font-bold text-cyan-300">{line.delay}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-slate-500">STATUS</div>
                    <span className="inline-block px-2.5 py-1 text-[10px] font-bold rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 tracking-wider uppercase">
                      {line.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
