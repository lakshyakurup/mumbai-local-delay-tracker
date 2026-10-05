import Link from "next/link";

export function Navbar() { return <nav className="nav-shell"><Link href="/" className="brand-mark"><span className="brand-dot" />MUMBAI / RAILWATCH</Link><div className="nav-links"><Link href="/">Command center</Link><Link href="/analytics">Analytics</Link><Link href="/lines">Lines</Link></div><div className="network-state"><span className="pulse-dot" />Live network</div></nav>; }
