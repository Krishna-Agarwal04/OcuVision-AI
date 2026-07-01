"use client";

import { useEffect, useState } from "react";
import SidebarLayout from "../../components/SidebarLayout";
import Link from "next/link";

export default function Dashboard() {
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

  const totalScans = history.length;
  const lastScan = totalScans > 0 ? new Date(history[0].created_at).toLocaleDateString() : "—";
  const lastDiagnosis = totalScans > 0 ? history[0].prediction : "—";

  return (
    <SidebarLayout>
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">Here's your retinal screening summary</p>

      {totalScans > 0 && ['Severe', 'Proliferative DR'].includes(history[0].prediction) && (
        <div style={{ background: '#fef2f2', border: '2px solid #dc2626', borderRadius: '10px', padding: '16px 20px', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ fontSize: '2rem' }}>🚨</span>
          <div>
            <strong style={{ color: '#dc2626', fontSize: '1.1rem' }}>High-Risk Result Detected</strong>
            <p style={{ color: '#7f1d1d', margin: '4px 0 0 0', fontSize: '0.9rem' }}>Your most recent scan was classified as <strong>{history[0].prediction}</strong>. Please seek immediate ophthalmology consultation.</p>
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px', marginBottom: '40px' }}>
        <div className="glass-card">
          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 600 }}>Total Scans</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary)' }}>{totalScans}</div>
        </div>
        <div className="glass-card">
          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 600 }}>Last Scan Date</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary)' }}>{lastScan}</div>
        </div>
        <div className="glass-card">
          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: 600 }}>Last Diagnosis</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)', marginTop: '8px' }}>{lastDiagnosis}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        <div className="glass-card">
          <h3 style={{ marginBottom: '16px', color: 'var(--primary)' }}>Recent Scans</h3>
          {loading ? <p>Loading...</p> : totalScans === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No scans yet. Start a new scan to see results here.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {history.slice(0, 5).map(scan => (
                <div key={scan.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 16px', background: 'rgba(255,255,255,0.5)', borderRadius: '8px', border: '1px solid var(--border)' }}>
                  <div>
                    <strong style={{ display: 'block' }}>{new Date(scan.created_at).toLocaleString()}</strong>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{scan.image_path}</span>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <span className="badge" style={{ background: scan.prediction === 'No DR' ? 'var(--success)' : scan.prediction.includes('Mild') ? 'var(--warning)' : 'var(--danger)', marginBottom: '4px' }}>
                      {scan.prediction}
                    </span>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Conf: {scan.confidence.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div>
          <div className="glass-card" style={{ marginBottom: '24px' }}>
            <h3 style={{ marginBottom: '16px', color: 'var(--primary)' }}>Quick Start</h3>
            <Link href="/new-scan" style={{ display: 'block', marginBottom: '12px' }}>
              <button className="btn-primary">🔬 Start New Scan</button>
            </Link>
            <Link href="/history" style={{ display: 'block' }}>
              <button className="btn-secondary">📜 View Full History</button>
            </Link>
          </div>
          
          <div style={{ background: '#eff6ff', borderLeft: '4px solid #3b82f6', padding: '16px', borderRadius: '8px', fontSize: '0.9rem' }}>
            <strong>ℹ️ How it works</strong><br/>
            Upload a retinal fundus image. Our AI classifies diabetic retinopathy severity in seconds.
          </div>
        </div>
      </div>
    </SidebarLayout>
  );
}
