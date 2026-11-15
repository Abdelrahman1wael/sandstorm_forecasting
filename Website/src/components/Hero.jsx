import React from 'react';
import { RESEARCH_DATA } from '../data/researchData';
import { Sparkles, Video, Cpu, ArrowRight, ShieldAlert, TrendingUp, Compass, Clock } from 'lucide-react';

export default function Hero({ setActiveView }) {
  const { metadata, numericalHighlights } = RESEARCH_DATA;

  return (
    <section className="hero-section" style={{ padding: '3.5rem 0 2rem' }}>
      <div className="container">
        
        {/* Header Metadata Badge */}
        <div className="hero-header-badge" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.6rem', background: 'rgba(30, 41, 59, 0.6)', border: '1px solid var(--border-subtle)', padding: '0.35rem 0.9rem', borderRadius: 999, fontSize: '0.8rem', color: '#cbd5e1', marginBottom: '1.25rem' }}>
          <span>🏛️ {metadata.reportType}</span>
          <span>•</span>
          <span>Enrollment: {metadata.enrollmentDate}</span>
          <span>•</span>
          <span style={{ color: '#38bdf8', fontWeight: 600, cursor: 'pointer' }} onClick={() => setActiveView('video')}>
            ▶ 1080p Presentation Video Ready
          </span>
        </div>

        {/* Hero Title */}
        <h1 className="hero-title" style={{ fontSize: 'clamp(1.8rem, 3.8vw, 3rem)', fontWeight: 900, lineHeight: 1.18, letterSpacing: '-0.03em', marginBottom: '1.25rem', color: '#f8fafc' }}>
          Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting
        </h1>

        <p className="hero-subtitle" style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', maxWidth: '920px', lineHeight: 1.65, marginBottom: '2rem' }}>
          Overcoming the predictability bottleneck of traditional physical Numerical Weather Prediction (NWP) across <strong>3–15 day extended-range</strong> and sub-seasonal horizons. Integrating multi-source heterogeneous observations, physics-informed neural constraints (PINN), graph spatial networks (GNN), and aerosol-meteorology coupled large models.
        </p>

        {/* Feature Callout Banners */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem', marginBottom: '2.5rem' }}>
          
          {/* Video Studio Card */}
          <div 
            onClick={() => setActiveView('video')}
            style={{ 
              background: 'rgba(15, 23, 42, 0.85)', 
              border: '1px solid #1e3a8a', 
              borderLeft: '4px solid #38bdf8', 
              borderRadius: 10, 
              padding: '1rem 1.25rem', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              cursor: 'pointer',
              transition: 'var(--transition)'
            }}
            className="feature-hover-card"
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, background: 'rgba(56, 189, 248, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Video size={24} color="#38bdf8" />
              </div>
              <div>
                <div style={{ color: '#f8fafc', fontWeight: 700, fontSize: '0.95rem' }}>Official Academic Presentation Video</div>
                <div style={{ color: '#94a3b8', fontSize: '0.8rem' }}>10 Scenes • ~8.5 Min • English Neural Narration & Captions</div>
              </div>
            </div>
            <button className="btn btn-primary" style={{ padding: '0.4rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: 4 }}>
              <span>Watch</span>
              <ArrowRight size={13} />
            </button>
          </div>

          {/* AI Neural Lab Card */}
          <div 
            onClick={() => setActiveView('ai-lab')}
            style={{ 
              background: 'rgba(15, 23, 42, 0.85)', 
              border: '1px solid #581c87', 
              borderLeft: '4px solid #c084fc', 
              borderRadius: 10, 
              padding: '1rem 1.25rem', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              cursor: 'pointer',
              transition: 'var(--transition)'
            }}
            className="feature-hover-card"
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, background: 'rgba(192, 132, 252, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Cpu size={24} color="#c084fc" />
              </div>
              <div>
                <div style={{ color: '#f8fafc', fontWeight: 700, fontSize: '0.95rem' }}>Interactive AI Neural Architecture Lab</div>
                <div style={{ color: '#94a3b8', fontSize: '0.8rem' }}>PINN Aerodynamic Saltation & ST-GNN Corridor Simulator</div>
              </div>
            </div>
            <button className="btn btn-secondary" style={{ padding: '0.4rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: 4, background: '#1e1b4b', border: '1px solid #4338ca', color: '#c7d2fe' }}>
              <span>Launch</span>
              <ArrowRight size={13} />
            </button>
          </div>

        </div>

        {/* Hero Tag Pills */}
        <div className="hero-tags" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '2.5rem' }}>
          <div className="tag-pill"><strong>University:</strong> {metadata.institution}</div>
          <div className="tag-pill"><strong>Major:</strong> {metadata.major}</div>
          <div className="tag-pill"><strong>Target Horizon:</strong> {metadata.targetForecastHorizon}</div>
          <div className="tag-pill"><strong>Key Models:</strong> AI-GAMFS, PINN, ST-GNN, Quantile Heads</div>
          <div className="tag-pill"><strong>Dual Lines:</strong> Line A (NWP Bias Correction) + Line B (Deep Learning)</div>
        </div>

        {/* Empirical Numerical Highlights Grid */}
        <div className="numerical-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          {numericalHighlights.map((stat, idx) => (
            <div key={idx} className="stat-card glass-panel" style={{ padding: '1.25rem', borderLeft: idx % 2 === 0 ? '3px solid var(--accent-amber)' : '3px solid var(--accent-cyan)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>{stat.label}</span>
                <span className="stat-badge" style={{ fontSize: '0.68rem', padding: '0.15rem 0.45rem', borderRadius: 4, background: 'rgba(255,255,255,0.06)', color: '#38bdf8' }}>
                  {stat.badge}
                </span>
              </div>
              <div className="stat-value" style={{ fontSize: '1.85rem', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.02em', margin: '0.2rem 0' }}>
                {stat.value}
              </div>
              <div className="stat-subtext" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                {stat.subtext}
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
