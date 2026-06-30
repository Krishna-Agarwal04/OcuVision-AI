"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";

export default function SidebarLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<{name: string, email: string} | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("user");
    if (!stored) {
      router.push("/");
    } else {
      setUser(JSON.parse(stored));
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("user");
    router.push("/");
  };

  if (!user) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>;

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div>
          <h2>👁️ OcuVisionAI</h2>
          <p style={{ fontSize: '0.8rem', opacity: 0.75, marginBottom: '24px', padding: '0 12px' }}>Retinal Screening System</p>
          
          <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '8px', padding: '12px', marginBottom: '24px' }}>
            <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>Logged in as</div>
            <strong style={{ display: 'block', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user.name}</strong>
          </div>
        </div>

        <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Link href="/dashboard" className={`sidebar-nav-item ${pathname === '/dashboard' ? 'active' : ''}`}>
            📊 Dashboard
          </Link>
          <Link href="/new-scan" className={`sidebar-nav-item ${pathname === '/new-scan' ? 'active' : ''}`}>
            🔬 New Scan
          </Link>
          <Link href="/history" className={`sidebar-nav-item ${pathname === '/history' ? 'active' : ''}`}>
            📜 History
          </Link>
        </nav>

        <button onClick={handleLogout} className="btn-secondary" style={{ marginTop: 'auto', background: 'rgba(255,255,255,0.1)', color: 'white', border: 'none' }}>
          🚪 Logout
        </button>
      </aside>
      
      <main className="main-content">
        <div className="container animate-fade-in">
          {children}
        </div>
      </main>
    </div>
  );
}
