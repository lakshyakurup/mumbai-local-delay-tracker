interface LineCardProps {
  name: string;
  status: string;
  delayTime: string;
  lineColorClass: string;
}

export default function LineCard({ name, status, delayTime }: LineCardProps) {
  return (
    <div className="group relative p-6 bg-neutral-950/80 backdrop-blur-md border border-neutral-800 hover:border-neutral-600 transition-all duration-300 rounded-2xl shadow-xl">
      <div className="absolute inset-0 bg-gradient-to-br from-white/[0.03] to-transparent rounded-2xl pointer-events-none" />

      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-bold text-white tracking-tight">{name} Line</h3>
        <span className="px-2.5 py-1 text-[10px] font-mono uppercase tracking-wider bg-neutral-900 border border-neutral-700 text-neutral-300 rounded-md">
          {status}
        </span>
      </div>

      <div className="flex items-baseline space-x-2">
        <span className="text-3xl font-extrabold font-mono text-white tracking-tighter">{delayTime}</span>
        <span className="text-xs text-neutral-500">avg delay</span>
      </div>
    </div>
  );
}
