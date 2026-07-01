"use client";

import { useEffect, useState } from "react";
import SidebarLayout from "../../components/SidebarLayout";

export default function HistoryPage() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const stored = localStorage.getItem("user");
        if (!stored) return;
        const user = JSON.parse(stored);
        
        const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiBase}/history/${user.id}`);
        const data = await res.json();
        setHistory(data);
      } catch (error) {
        console.error("Error fetching history:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistory();
  }, []);

  return (
    <SidebarLayout>
      <h1 className="page-title">Scan History</h1>
      <p className="page-subtitle">All your past retinal scans and AI diagnoses</p>

      <div className="glass-card">
        {loading ? <p>Loading history...</p> : history.length === 0 ? (
          <p style={{ color: 'var(--text-muted)' }}>No scan history found. Run your first scan to get started.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {history.map(scan => (
              <div key={scan.id} className="animate-fade-in" style={{ background: 'rgba(255,255,255,0.8)', border: '1px solid var(--border)', borderRadius: '12px', padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '8px' }}>
                    🗓️ {new Date(scan.created_at).toLocaleString()}
                  </div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 600 }}>
                    File: {scan.image_path}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <span className="badge" style={{ background: scan.prediction === 'No DR' ? 'var(--success)' : scan.prediction.includes('Mild') ? 'var(--warning)' : 'var(--danger)', fontSize: '1rem', padding: '6px 16px' }}>
                      {scan.prediction}
                    </span>
                  </div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    Confidence: <strong>{scan.confidence.toFixed(1)}%</strong>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </SidebarLayout>
  );
}
