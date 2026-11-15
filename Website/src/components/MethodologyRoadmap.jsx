import React from 'react';
import { MapPin, BarChart3, GitMerge, ShieldAlert, ArrowRight, CheckCircle2, Clock } from 'lucide-react';

export default function MethodologyRoadmap() {
  const steps = [
    {
      num: '01',
      title: 'GIS Spatial Feature Extraction',
      tools: 'ArcGIS Pro / QGIS',
      desc: 'Extract remote sensing AOD, elevation (DEM), vegetation index (NDVI), and proximity buffer zones to desert corridors.',
      badge: 'Spatial Feature Eng',
      color: '#38bdf8'
    },
    {
      num: '02',
      title: 'IBM SPSS Data Hygiene & Screening',
      tools: 'IBM SPSS Statistics v26+',
      desc: 'Screen 10,000+ socio-ecological and health surveys. Multivariate outliers (Mahalanobis D²), normality tests, Cronbach\'s alpha, and EFA.',
      badge: 'Data Screening & EFA',
      color: '#f59e0b'
    },
    {
      num: '03',
      title: 'IBM SPSS AMOS Latent Modeling',
      tools: 'IBM SPSS AMOS (SEM)',
      desc: 'Confirmatory Factor Analysis (CFA), convergent validity (AVE > 0.5), discriminant validity, and 5,000-bootstrap mediation path testing.',
      badge: 'Causal Path & SEM',
      color: '#c084fc'
    },
    {
      num: '04',
      title: 'GIS Spatialization & Econometrics',
      tools: 'ArcGIS / GeoDa / GWR',
      desc: 'Map AMOS latent factor scores and regression residuals back to spatial coordinates. Run Moran\'s I, Getis-Ord Gi* hot spots, and GWR.',
      badge: 'Hot Spot & GWR Maps',
      color: '#10b981'
    }
  ];

  const weeks = [
    { range: 'Weeks 1–4', label: 'SPSS Foundations & Psychometrics', desc: 'Data hygiene, missing values (MCAR), normality screening, ANOVA, EFA, and Hayes PROCESS macro.' },
    { range: 'Weeks 5–8', label: 'AMOS Structural Equation Modeling', desc: 'CFA model identification, CR & AVE validity, 5,000 bias-corrected bootstrapping, multi-group invariance.' },
    { range: 'Weeks 9–11', label: 'GIS Spatial Science & Cartography', desc: 'Coordinate reference systems (WGS84 vs UTM), Kriging interpolation, Global/Local Moran\'s I, and GWR.' },
    { range: 'Week 12', label: 'Unified Research Paper Synthesis', desc: 'Complete paper compilation: spatial exposure -> SPSS cleaning -> AMOS latent equations -> GIS spatial maps.' },
  ];

  return (
    <section className="container" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Empirical Research Tri-Pillar</span>
        <h2 className="section-title">SPSS, AMOS & GIS Integration Roadmap</h2>
        <p className="section-desc">
          Methodological framework connecting physical satellite/ground spatial data (GIS) with socio-ecological questionnaire screening (SPSS) and latent structural equation modeling (AMOS).
        </p>
      </div>

      {/* 4-Step Synergistic Pipeline */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem', marginBottom: '2.5rem' }}>
        {steps.map((st, i) => (
          <div key={i} className="glass-panel" style={{ padding: '1.5rem', borderTop: `3px solid ${st.color}`, position: 'relative' }}>
            <span style={{ fontSize: '1.75rem', fontWeight: 900, color: 'rgba(255,255,255,0.1)', position: 'absolute', top: 12, right: 16 }}>
              {st.num}
            </span>
            <span className="stat-badge" style={{ background: `${st.color}15`, color: st.color, fontSize: '0.72rem', marginBottom: 8, display: 'inline-block' }}>
              {st.badge}
            </span>
            <h4 style={{ fontSize: '1.05rem', color: '#f8fafc', margin: '0.4rem 0' }}>
              {st.title}
            </h4>
            <div style={{ fontSize: '0.78rem', color: 'var(--accent-amber)', marginBottom: '0.5rem', fontWeight: 600 }}>
              {st.tools}
            </div>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              {st.desc}
            </p>
          </div>
        ))}
      </div>

      {/* 12-Week Master Schedule */}
      <div className="glass-panel" style={{ padding: '1.75rem', marginBottom: '2.5rem' }}>
        <h4 style={{ fontSize: '1.15rem', color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: 8 }}>
          <Clock size={18} color="#38bdf8" />
          12-Week Master Implementation Schedule
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          {weeks.map((w, idx) => (
            <div key={idx} style={{ background: 'rgba(15,23,42,0.6)', padding: '1.1rem', borderRadius: 8, borderLeft: '3px solid #38bdf8' }}>
              <span style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>{w.range}</span>
              <h5 style={{ color: '#f8fafc', fontSize: '0.92rem', margin: '0.3rem 0 0.5rem' }}>{w.label}</h5>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.78rem', lineHeight: 1.45 }}>{w.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Disaster Decision Matrix Preview */}
      <div className="glass-panel" style={{ padding: '1.75rem' }}>
        <h4 style={{ fontSize: '1.15rem', color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: 8 }}>
          <ShieldAlert size={18} color="var(--accent-amber)" />
          Operational Disaster Decision-Making Matrix (From Hexi Crisis Story)
        </h4>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
          Actionable protocols for municipal and emergency authorities mapped to AI lead-time confidence horizons:
        </p>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: '#94a3b8' }}>
                <th style={{ padding: '0.65rem' }}>Lead Horizon</th>
                <th style={{ padding: '0.65rem' }}>AI Signal & Physical Trigger</th>
                <th style={{ padding: '0.65rem' }}>Operational Action Mandate</th>
                <th style={{ padding: '0.65rem' }}>Responsible Entity</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '0.65rem', fontWeight: 700, color: '#38bdf8' }}>T - 15 to 10 Days</td>
                <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>AI-GAMFS S2S anomaly &gt; 0.65, desert topsoil moisture deficit</td>
                <td style={{ padding: '0.65rem', color: '#cbd5e1' }}>Check state grain silo seals, allocate emergency water reserves</td>
                <td style={{ padding: '0.65rem', color: '#94a3b8' }}>Emergency & Water Resources</td>
              </tr>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '0.65rem', fontWeight: 700, color: '#f59e0b' }}>T - 7 Days</td>
                <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>PINN friction velocity u* &gt; 0.35 m/s, ST-GNN corridor alert</td>
                <td style={{ padding: '0.65rem', color: '#cbd5e1' }}>Reinforce greenhouse films, pre-alert rail speed restrictions</td>
                <td style={{ padding: '0.65rem', color: '#94a3b8' }}>Agriculture Bureau, China Railway</td>
              </tr>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '0.65rem', fontWeight: 700, color: '#ef4444' }}>T - 5 Days (120h)</td>
                <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>NWP divergence, Line A bias correction active, P90 &gt; 500 μg/m³</td>
                <td style={{ padding: '0.65rem', color: '#cbd5e1' }}>Issue commercial flight diversion advisory, pre-wet arterial roads</td>
                <td style={{ padding: '0.65rem', color: '#94a3b8' }}>Civil Aviation (CAAC), Urban Mgmt</td>
              </tr>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                <td style={{ padding: '0.65rem', fontWeight: 700, color: '#c084fc' }}>T - 72 Hours</td>
                <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>Prediction interval width contracts (&lt; 300), Category 4 alert</td>
                <td style={{ padding: '0.65rem', color: '#cbd5e1' }}>Mandatory school outdoor cancellation, halt open-air construction</td>
                <td style={{ padding: '0.65rem', color: '#94a3b8' }}>Education, Ecology & Environment</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>

    </section>
  );
}
