"use client";

import { useState } from "react";
import SidebarLayout from "../../components/SidebarLayout";

export default function NewScan() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setLoading(true);
    try {
      const stored = localStorage.getItem("user");
      if (!stored) return;
      const user = JSON.parse(stored);

      const formData = new FormData();
      formData.append("file", file);
      formData.append("user_id", user.id.toString());

      const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiBase}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Analysis failed");
      
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error analyzing image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SidebarLayout>
      <h1 className="page-title">New Retinal Scan</h1>
      <p className="page-subtitle">Upload a fundus image for AI-powered diabetic retinopathy screening</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
        <div className="glass-card">
          <h3 style={{ marginBottom: '16px' }}>📤 Upload Image</h3>
          
          <div style={{ border: '2px dashed var(--border)', borderRadius: '12px', padding: '32px', textAlign: 'center', marginBottom: '24px', background: 'white' }}>
            {preview ? (
              <img src={preview} alt="Preview" style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px' }} />
            ) : (
              <div style={{ color: 'var(--text-muted)' }}>
                <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📷</div>
                <p>Drag & drop or browse</p>
                <p style={{ fontSize: '0.8rem' }}>Supported formats: JPG, JPEG, PNG</p>
              </div>
            )}
            <input type="file" accept="image/*" onChange={handleFileChange} style={{ marginTop: '16px' }} />
          </div>

          <button 
            className="btn-primary" 
            onClick={handleAnalyze} 
            disabled={!file || loading}
          >
            {loading ? "🧠 Analyzing..." : "🧠 Analyze Image"}
          </button>
        </div>

        <div className="glass-card">
          <h3 style={{ marginBottom: '16px' }}>📊 Analysis Result</h3>
          
          {!result ? (
            <div style={{ border: '2px dashed #cbd5e1', borderRadius: '12px', padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
              <p style={{ fontSize: '3rem', marginBottom: '16px' }}>👁️</p>
              <p>Results will appear here after analysis</p>
            </div>
          ) : (
            <div className="animate-fade-in" style={{ 
              background: result.prediction === 'No DR' ? '#f0fdf4' : result.prediction.includes('Mild') ? '#fffbeb' : '#fef2f2', 
              border: `2px solid ${result.prediction === 'No DR' ? '#16a34a' : result.prediction.includes('Mild') ? '#d97706' : '#dc2626'}`, 
              borderRadius: '12px', 
              padding: '24px' 
            }}>
              <h3 style={{ color: result.prediction === 'No DR' ? '#16a34a' : result.prediction.includes('Mild') ? '#d97706' : '#dc2626', margin: '0 0 8px' }}>Diagnosis</h3>
              <p style={{ fontSize: '2rem', fontWeight: 700, margin: '0 0 16px', color: result.prediction === 'No DR' ? '#16a34a' : result.prediction.includes('Mild') ? '#d97706' : '#dc2626' }}>{result.prediction}</p>
              
              <hr style={{ opacity: 0.2, margin: '16px 0' }} />
              
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>CONFIDENCE</span>
                  <strong style={{ display: 'block', fontSize: '1.5rem' }}>{result.confidence.toFixed(1)}%</strong>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>SEVERITY</span><br/>
                  <span className="badge" style={{ background: result.prediction === 'No DR' ? 'var(--success)' : result.prediction.includes('Mild') ? 'var(--warning)' : 'var(--danger)', marginTop: '4px' }}>
                    {result.prediction}
                  </span>
                </div>
              </div>

              <button className="btn-secondary" style={{ marginTop: '24px' }} onClick={() => {setResult(null); setFile(null); setPreview(null);}}>
                🔄 Analyze Another
              </button>
            </div>
          )}
        </div>
      </div>
    </SidebarLayout>
  );
}
