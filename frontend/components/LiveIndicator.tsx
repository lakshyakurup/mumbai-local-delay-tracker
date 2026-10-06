export default function LiveIndicator() {
  return (
    <div className="flex items-center space-x-3 px-4 py-2 bg-neutral-950 border border-neutral-800 rounded-full shadow-2xl">
      <span className="relative flex h-3 w-3">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
      </span>
      <span className="text-xs font-mono tracking-widest text-neutral-300 uppercase">
        Live Feed • Mumbai Local
      </span>
    </div>
  );
}
