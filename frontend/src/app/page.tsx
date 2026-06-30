"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const formData = new FormData(e.currentTarget);
    const endpoint = isLogin ? "/login" : "/register";

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Authentication failed");
      }

      // Store user info in localStorage for simplicity
      localStorage.setItem("user", JSON.stringify(data.user));
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--background)' }}>
      <div className="glass-card animate-fade-in" style={{ width: '100%', maxWidth: '400px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem', color: 'var(--primary)' }}>👁️ OcuVisionAI</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Detect Early. Save Vision.</p>
        
        <div style={{ display: 'flex', marginBottom: '1.5rem', borderBottom: '1px solid var(--border)' }}>
          <button 
            style={{ flex: 1, padding: '10px', background: 'none', border: 'none', borderBottom: isLogin ? '2px solid var(--primary)' : '2px solid transparent', fontWeight: isLogin ? 700 : 500, color: isLogin ? 'var(--primary)' : 'var(--text-muted)' }}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button 
            style={{ flex: 1, padding: '10px', background: 'none', border: 'none', borderBottom: !isLogin ? '2px solid var(--primary)' : '2px solid transparent', fontWeight: !isLogin ? 700 : 500, color: !isLogin ? 'var(--primary)' : 'var(--text-muted)' }}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>

        {error && <div style={{ background: '#fef2f2', color: '#dc2626', padding: '10px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.9rem' }}>{error}</div>}

        <form onSubmit={handleSubmit} style={{ textAlign: 'left' }}>
          {!isLogin && (
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input type="text" name="name" className="form-input" placeholder="Dr. Priya Sharma" required={!isLogin} />
            </div>
          )}
          
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input type="email" name="email" className="form-input" placeholder="you@example.com" required />
          </div>
          
          <div className="form-group">
            <label className="form-label">Password</label>
            <input type="password" name="password" className="form-input" placeholder="••••••••" required />
          </div>
          
          <button type="submit" className="btn-primary" style={{ marginTop: '1rem' }} disabled={loading}>
            {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account')}
          </button>
        </form>
      </div>
    </div>
  );
}
