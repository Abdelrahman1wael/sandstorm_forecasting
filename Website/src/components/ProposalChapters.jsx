import React, { useState } from 'react';
import { RESEARCH_DATA } from '../data/researchData';
import { BookOpen, FileText, CheckCircle, Clock, Zap, Target } from 'lucide-react';

export default function ProposalChapters() {
  const [activeTab, setActiveTab] = useState('tab-intro');

  const tabs = [
    { id: 'tab-intro', label: '1. Introduction & Background' },
    { id: 'tab-status', label: '2. Research Status & Literature' },
    { id: 'tab-content', label: '3. Research Content' },
    { id: 'tab-methods', label: '4. Research Methods' },
    { id: 'tab-steps', label: '5. Research Steps' },
    { id: 'tab-schedule', label: '6. Time Schedule' },
  ];

  return (
    <section id="research-core" className="container tabs-wrapper" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Thesis Document Chapters</span>
        <h2 className="section-title">Complete Master's Research Proposal Breakdown</h2>
        <p className="section-desc">
          Structured according to the University of Science and Technology Beijing (北京科技大学) Master's Thesis Topic Selection standards, covering background, literature evolution, methodology, steps, and timeline.
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="tab-nav" style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem', marginBottom: '2rem' }}>
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`tab-btn ${activeTab === t.id ? 'active' : ''}`}
            style={{ 
              padding: '0.65rem 1.15rem', 
              borderRadius: 8, 
              border: activeTab === t.id ? '1px solid rgba(6, 182, 212, 0.4)' : '1px solid transparent',
              background: activeTab === t.id ? 'rgba(6, 182, 212, 0.12)' : 'transparent',
              color: activeTab === t.id ? '#38bdf8' : 'var(--text-muted)',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'var(--transition)'
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* TAB 1: Introduction */}
      {activeTab === 'tab-intro' && (
        <div className="tab-pane">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
            
            <div className="detail-card glass-panel" style={{ padding: '1.75rem' }}>
              <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem' }}>
                1.1 Research Background & Problem Formulation
              </h4>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '1rem', lineHeight: 1.65 }}>
                Against the backdrop of global climate change, extreme sandstorms pose severe transnational threats. Research indicates that <strong>over 330 million people across 151 countries</strong> are directly affected. In China, arid and semi-arid regions in the north act as principal sources, where dust plumes transport across continents to central, eastern, and southern China.
              </p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', marginBottom: '1rem', lineHeight: 1.65 }}>
                Between 2010 and 2013 alone, direct economic losses reached <strong>~US$1.0 billion</strong> in northern China. Impacts include catastrophic visibility drops endangering aviation and highway transit, severe PM10/PM2.5 inhalation triggering respiratory and cardiovascular illnesses, and soil desertification.
              </p>
              
              <div className="formula-box" style={{ background: 'rgba(5, 8, 17, 0.85)', borderLeft: '3px solid var(--accent-amber)', padding: '1rem', borderRadius: '0 8px 8px 0', fontSize: '0.85rem', color: '#fde68a', fontFamily: 'var(--font-mono)', margin: '1.25rem 0' }}>
                Traditional NWP Bottleneck: Supercomputers take hours for single high-res run; physical parameterization errors accumulate exponentially; skill drops steeply for extended-range (3–15 days) and seasonal forecasts.
              </div>

              <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.65 }}>
                The emergence of data-driven machine learning, exemplified by China's independently developed <strong>AI-GAMFS large model</strong> (5km resolution, 2x daily update, 38%–74% error reduction vs ECMWF & NASA), proves that AI can capture complex non-linear dynamics and extend lead times to <strong>120 hours (5 days)</strong>.
              </p>
            </div>

            <div className="detail-card glass-panel" style={{ padding: '1.75rem' }}>
              <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem' }}>
                1.2 Theoretical & Practical Significance
              </h4>
              <div style={{ marginBottom: '1.25rem' }}>
                <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '0.4rem', fontSize: '0.95rem' }}>
                  Theoretical Significance:
                </strong>
                <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.6 }}>
                  <li><strong>Cross-Scale Driving Mechanisms:</strong> Quantifying how sub-seasonal to seasonal forcing (ENSO, Arctic Oscillation, blocking highs, snowmelt, vegetation phenology) modulates synoptic cold fronts.</li>
                  <li><strong>New Algorithmic Paradigms:</strong> Advancing spatiotemporal sequence modeling via LSTM, Transformers, and Graph Neural Networks (GNN) combined with Physics-Informed Machine Learning (PINN mass conservation).</li>
                  <li><strong>Unified Benchmark:</strong> Establishing standardized open datasets and 3–15 day forecast labels with rigorous meteorological verification.</li>
                </ul>
              </div>

              <div>
                <strong style={{ color: 'var(--accent-amber)', display: 'block', marginBottom: '0.4rem', fontSize: '0.95rem' }}>
                  Practical Significance:
                </strong>
                <ul style={{ paddingLeft: '1.2rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.6 }}>
                  <li><strong>Proactive Defense:</strong> Transitioning from "passive post-event response" to "proactive outlooks" (watering, dust suppression, healthcare logistics).</li>
                  <li><strong>Sector Meteorological Support:</strong> Optimizing aviation flight plans, protecting photovoltaic solar energy panels from soiling, and reinforcing agricultural greenhouses.</li>
                  <li><strong>Ecological Civilization:</strong> Distinguishing natural desert dust from anthropogenic industrial emissions, guiding the "Three-North" Shelter Forest Program (三北防护林).</li>
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB 2: Literature Review */}
      {activeTab === 'tab-status' && (
        <div className="tab-pane">
          <div className="detail-card glass-panel" style={{ padding: '1.75rem', marginBottom: '1.5rem' }}>
            <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1rem' }}>
              2. Research Status & Academic Literature Evolution
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
              
              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <span className="stat-badge" style={{ background: 'rgba(239,68,68,0.15)', color: '#f87171', marginBottom: 8, display: 'inline-block' }}>Generation 1: Physical NWP</span>
                <h5 style={{ color: '#f8fafc', fontSize: '1rem', margin: '0.4rem 0' }}>WRF-Chem, CUACE/Dust, ECMWF-IFS</h5>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: 1.5 }}>
                  Based strictly on Navier-Stokes fluid mechanics and empirical dust emission schemes (Shao 2004, Owen 1964). Suffers rapid error growth beyond 72 hours due to atmospheric chaos and computational grid limits.
                </p>
              </div>

              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <span className="stat-badge" style={{ background: 'rgba(245,158,11,0.15)', color: '#fbbf24', marginBottom: 8, display: 'inline-block' }}>Generation 2: Classical ML</span>
                <h5 style={{ color: '#f8fafc', fontSize: '1rem', margin: '0.4rem 0' }}>Random Forest, LightGBM, SVM, AutoGluon</h5>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: 1.5 }}>
                  Statistically learns non-linear relationships from tabular ground stations and NWP outputs. Achieves high hit rates (96.7% in Liaoning convection studies) but lacks spatial advection awareness across multi-station corridors.
                </p>
              </div>

              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <span className="stat-badge" style={{ background: 'rgba(56,189,248,0.15)', color: '#38bdf8', marginBottom: 8, display: 'inline-block' }}>Generation 3: Deep Spatiotemporal</span>
                <h5 style={{ color: '#f8fafc', fontSize: '1rem', margin: '0.4rem 0' }}>AI-GAMFS, ST-GNN, PINN Mass PDE</h5>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: 1.5 }}>
                  Combines graph topology of dust transport funnels with physics conservation loss. Extends high-accuracy warning horizon out to 120 hours (5 days) with 38%–74% error reduction vs ECMWF & NASA GEOS-CF.
                </p>
              </div>

            </div>
          </div>
        </div>
      )}

      {/* TAB 3: Research Content */}
      {activeTab === 'tab-content' && (
        <div className="tab-pane">
          <div className="detail-card glass-panel" style={{ padding: '1.75rem' }}>
            <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1.25rem' }}>
              3. Core Research Content (Four Scientific Thrusts)
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
              
              <div style={{ background: 'rgba(15,23,42,0.6)', padding: '1.25rem', borderRadius: 8, borderLeft: '3px solid #38bdf8' }}>
                <h5 style={{ color: '#38bdf8', fontSize: '1rem', marginBottom: '0.5rem' }}>Thrust 1: Multi-Source Heterogeneous Data Harmonization</h5>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.5 }}>
                  Unifying ECMWF/CMA atmospheric variables, ERA5 reanalysis, MODIS/FY-4 satellite aerosol optical depth (AOD), and 28 ground meteorological stations into a standardized 0.125° spatial grid with Kriging imputation.
                </p>
              </div>

              <div style={{ background: 'rgba(15,23,42,0.6)', padding: '1.25rem', borderRadius: 8, borderLeft: '3px solid #f59e0b' }}>
                <h5 style={{ color: '#f59e0b', fontSize: '1rem', marginBottom: '0.5rem' }}>Thrust 2: Main Line A (NWP Statistical Bias Correction)</h5>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.5 }}>
                  Developing tree-ensemble algorithms (LightGBM/HistGradientBoosting) that learn residual error vectors between operational NWP physics simulations and real-world ground sensor readings.
                </p>
              </div>

              <div style={{ background: 'rgba(15,23,42,0.6)', padding: '1.25rem', borderRadius: 8, borderLeft: '3px solid #c084fc' }}>
                <h5 style={{ color: '#c084fc', fontSize: '1rem', marginBottom: '0.5rem' }}>Thrust 3: Main Line B (Physics-Informed Deep Spatiotemporal Modeling)</h5>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.5 }}>
                  Constructing the coupled AI-GAMFS vision/tensor backbone, ST-GNN bidirectional corridor diffusion graph, and PINN loss enforcing Owen aerodynamic friction velocity thresholding.
                </p>
              </div>

              <div style={{ background: 'rgba(15,23,42,0.6)', padding: '1.25rem', borderRadius: 8, borderLeft: '3px solid #10b981' }}>
                <h5 style={{ color: '#10b981', fontSize: '1rem', marginBottom: '0.5rem' }}>Thrust 4: Uncertainty Quantification & Hazard Classification</h5>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.5 }}>
                  Implementing non-parametric quantile regression (P10, P50, P90) via pinball loss and cost-sensitive 5-class hazard classifiers penalizing false negatives during extreme dust storms.
                </p>
              </div>

            </div>
          </div>
        </div>
      )}

      {/* TAB 4: Research Methods & Formulas */}
      {activeTab === 'tab-methods' && (
        <div className="tab-pane">
          <div className="detail-card glass-panel" style={{ padding: '1.75rem' }}>
            <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1.25rem' }}>
              4. Research Methodology & Core Mathematical Formulations
            </h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
              
              <div style={{ background: 'rgba(5, 8, 17, 0.85)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <strong style={{ color: '#f59e0b', fontSize: '0.95rem', display: 'block', marginBottom: '0.5rem' }}>
                  1. Owen's Aerodynamic Saltation Flux (PINN Constraint):
                </strong>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: '#fde68a', background: 'rgba(0,0,0,0.4)', padding: '0.75rem', borderRadius: 6, marginBottom: '0.75rem' }}>
                  F_salt = C * (rho_a / g) * u_*^3 * (1 - u_*t^2 / u_*^2) * I(u_* &gt; u_*t)
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                  Guarantees that sand emissions only initiate once friction velocity u* exceeds threshold u*t (typically 0.35 m/s in Taklamakan/Badain Jaran).
                </p>
              </div>

              <div style={{ background: 'rgba(5, 8, 17, 0.85)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <strong style={{ color: '#38bdf8', fontSize: '0.95rem', display: 'block', marginBottom: '0.5rem' }}>
                  2. Spatiotemporal Mass Conservation PDE:
                </strong>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: '#7dd3fc', background: 'rgba(0,0,0,0.4)', padding: '0.75rem', borderRadius: 6, marginBottom: '0.75rem' }}>
                  L_mass = || div(rho * u) + d_rho / d_t - S_emission + D_settling ||^2
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                  Enforces continuous advection continuity, penalizing the neural network if dust particulate mass appears or disappears unphysically.
                </p>
              </div>

              <div style={{ background: 'rgba(5, 8, 17, 0.85)', padding: '1.25rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <strong style={{ color: '#c084fc', fontSize: '0.95rem', display: 'block', marginBottom: '0.5rem' }}>
                  3. Multi-Quantile Pinball Loss (P10, P50, P90):
                </strong>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: '#e9d5ff', background: 'rgba(0,0,0,0.4)', padding: '0.75rem', borderRadius: 6, marginBottom: '0.75rem' }}>
                  L_pinball(tau) = sum_i max(tau * e_i, (tau - 1) * e_i),  where e_i = y_i - y_hat
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                  Calibrates probabilistic uncertainty bands, providing emergency managers with best-case (P10), median (P50), and worst-case (P90) hazard thresholds.
                </p>
              </div>

            </div>
          </div>
        </div>
      )}

      {/* TAB 5 & 6: Steps & Schedule */}
      {(activeTab === 'tab-steps' || activeTab === 'tab-schedule') && (
        <div className="tab-pane">
          <div className="detail-card glass-panel" style={{ padding: '1.75rem' }}>
            <h4 style={{ fontSize: '1.2rem', color: '#f8fafc', marginBottom: '1.25rem' }}>
              {activeTab === 'tab-steps' ? '5. Implementation Steps & Verification Standards' : '6. 22-Month Master Schedule & Milestones'}
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {[
                { stage: 'Stage 1: Multi-Modal Data Ingestion', desc: 'Harmonize ERA5, CMA ground sensors, FY-4 AOD, and ECMWF into 5km grids.', date: '2025.09 - 2025.11' },
                { stage: 'Stage 2: Main Line A ML Pipeline', desc: 'Train LightGBM tree ensembles on 72h-120h NWP residual bias vectors.', date: '2025.12 - 2026.03' },
                { stage: 'Stage 3: Main Line B Deep Architecture', desc: 'Implement AI-GAMFS backbone, PINN Owen constraint, and ST-GNN corridor diffusion.', date: '2026.04 - 2026.09' },
                { stage: 'Stage 4: Multi-Lead Benchmark & Case Studies', desc: 'Evaluate on historical spring dust outbreaks and verify PICP coverage >= 80%.', date: '2026.10 - 2027.02' },
                { stage: 'Stage 5: Thesis Finalization & Academic Defense', desc: 'Submit 2 SCI Q1 papers, patent software, and complete USTB master\'s oral defense.', date: '2027.03 - 2027.06' },
              ].map((s, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(15,23,42,0.6)', padding: '1rem', borderRadius: 8, border: '1px solid var(--border-subtle)', flexWrap: 'wrap', gap: '0.5rem' }}>
                  <div>
                    <strong style={{ color: '#f8fafc', fontSize: '0.92rem', display: 'block' }}>{s.stage}</strong>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>{s.desc}</span>
                  </div>
                  <span className="stat-badge" style={{ background: 'rgba(6,182,212,0.15)', color: '#22d3ee', fontSize: '0.78rem' }}>
                    {s.date}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </section>
  );
}
