import React, { useState } from 'react';
import { Cpu, Play, CheckCircle2, Sliders, Activity, Sparkles, Layers } from 'lucide-react';

export default function AiNeuralLab() {
  const [isRunningPass, setIsRunningPass] = useState(false);
  const [passOutput, setPassOutput] = useState(null);
  const [frictionSlider, setFrictionSlider] = useState(0.46);

  const ustar_t = 0.35;
  const isSaltationActive = frictionSlider > ustar_t;
  const saltationFlux = isSaltationActive 
    ? (0.25 * (1.225 / 9.81) * Math.pow(frictionSlider, 3) * (1 - Math.pow(ustar_t / frictionSlider, 2)) * 1000).toFixed(2)
    : 0;

  const handleRunForwardPass = () => {
    setIsRunningPass(true);
    setTimeout(() => {
      setIsRunningPass(false);
      setPassOutput({
        timeMs: 42.8,
        backboneEmbeddingDim: 64,
        stGnnNodeLatents: 14,
        p50Forecast: 382.4,
        p10Forecast: 215.1,
        p90Forecast: 642.0,
        hazardClass: 'Class 3 (Severe Sandstorm Threat)',
        pinnResidual: '0.0034 (Within Bounds)'
      });
    }, 600);
  };

  return (
    <section className="container" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Deep Learning Laboratory</span>
        <h2 className="section-title">Coupled AI-GAMFS & Physics-Informed Neural Network (PINN) Lab</h2>
        <p className="section-desc">
          Interactive neural playground demonstrating multi-modal tensor ingestion (NWP 6-channel + Satellite 3-channel), 14-node Spatio-Temporal Graph Neural Network (ST-GNN) advection, and differentiable PINN mass conservation constraints.
        </p>
      </div>

      {/* Grid: Forward Pass Controller & PINN Friction Lab */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        
        {/* Forward Pass Card */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h4 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '0.8rem', display: 'flex', alignItems: 'center', gap: 8 }}>
              <Cpu size={18} color="#c084fc" />
              Real-Time Neural Forward Pass Emulator
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
              Simulates a live multi-modal tensor forward pass through the Coupled AI-GAMFS backbone (6x16x16 NWP + 3x32x32 FY-4 Sat) and the 14-station ST-GNN.
            </p>

            <button 
              onClick={handleRunForwardPass} 
              disabled={isRunningPass}
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.75rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, background: 'linear-gradient(135deg, #7c3aed, #4f46e5)' }}
            >
              {isRunningPass ? (
                <>
                  <Activity size={18} className="animate-spin" />
                  <span>Computing Multi-Modal Tensor Pass...</span>
                </>
              ) : (
                <>
                  <Play size={18} />
                  <span>Execute Neural Forward Pass</span>
                </>
              )}
            </button>
          </div>

          {/* Forward Pass Telemetry Result */}
          {passOutput && (
            <div style={{ background: 'rgba(5, 8, 17, 0.85)', border: '1px solid #7c3aed', borderRadius: 8, padding: '1rem', marginTop: '1.25rem', animation: 'fadeIn 0.3s ease' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <strong style={{ color: '#c084fc', fontSize: '0.85rem' }}>✅ Forward Pass Complete</strong>
                <span className="stat-badge" style={{ background: 'rgba(192, 132, 252, 0.2)', color: '#e9d5ff', fontSize: '0.72rem' }}>
                  {passOutput.timeMs} ms latency
                </span>
              </div>
              <div style={{ fontSize: '0.78rem', color: '#cbd5e1', display: 'flex', flexDirection: 'column', gap: 4 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Backbone Latent Dimension:</span>
                  <strong>{passOutput.backboneEmbeddingDim}-D Tensor</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Median Forecast P50:</span>
                  <strong style={{ color: '#38bdf8' }}>{passOutput.p50Forecast} μg/m³</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Uncertainty Range [P10, P90]:</span>
                  <strong style={{ color: '#f59e0b' }}>[{passOutput.p10Forecast}, {passOutput.p90Forecast}] μg/m³</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>PINN Mass Residual:</span>
                  <strong style={{ color: '#34d399' }}>{passOutput.pinnResidual}</strong>
                </div>
              </div>
            </div>
          )}

        </div>

        {/* PINN Friction Velocity Slider Lab */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h4 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '0.8rem', display: 'flex', alignItems: 'center', gap: 8 }}>
            <Sliders size={18} color="var(--accent-amber)" />
            Owen Aerodynamic Saltation Trigger Simulator
          </h4>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
            Adjust friction velocity u* past the critical aerodynamic threshold u*t (0.35 m/s) to observe non-linear dust emission activation in the physics loss term.
          </p>

          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: 6 }}>
              <span style={{ color: '#cbd5e1' }}>Friction Velocity (u*):</span>
              <strong style={{ color: isSaltationActive ? '#f59e0b' : '#34d399', fontSize: '1.1rem', fontFamily: 'var(--font-mono)' }}>
                {frictionSlider.toFixed(2)} m/s
              </strong>
            </div>
            <input 
              type="range" min="0.10" max="0.90" step="0.01" value={frictionSlider}
              onChange={e => setFrictionSlider(parseFloat(e.target.value))}
              style={{ width: '100%', accentColor: isSaltationActive ? '#f59e0b' : '#34d399' }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: '#94a3b8', marginTop: 4 }}>
              <span>0.10 m/s (Calm)</span>
              <span style={{ color: '#f59e0b' }}>Threshold u*t = 0.35 m/s</span>
              <span>0.90 m/s (Gale)</span>
            </div>
          </div>

          <div style={{ background: isSaltationActive ? 'rgba(245, 158, 11, 0.12)' : 'rgba(16, 185, 129, 0.12)', border: isSaltationActive ? '1px solid #f59e0b' : '1px solid #10b981', borderRadius: 8, padding: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <span style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Aerodynamic Regime:</span>
              <strong style={{ color: isSaltationActive ? '#f59e0b' : '#34d399', fontSize: '0.92rem' }}>
                {isSaltationActive ? 'ACTIVE PARTICULATE SALTATION' : 'AERODYNAMIC EQUILIBRIUM'}
              </strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Computed Owen Dust Flux:</span>
              <strong style={{ color: isSaltationActive ? '#f59e0b' : '#94a3b8', fontSize: '1.1rem', fontFamily: 'var(--font-mono)' }}>
                {saltationFlux} mg/m·s
              </strong>
            </div>
          </div>
        </div>

      </div>

      {/* 100-Epoch Loss Convergence Architecture */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h4 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: 8 }}>
          <Layers size={18} color="#38bdf8" />
          Multi-Loss Optimization Convergence (100 Epochs)
        </h4>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
          Simultaneous convergence of Quantile Pinball Loss (P10/P50/P90), Cost-Sensitive Cross-Entropy, and Physics-Informed Mass Continuity PDE residual.
        </p>

        <div style={{ height: 240 }}>
          <svg viewBox="0 0 700 200" style={{ width: '100%', height: '100%' }}>
            {/* Grid */}
            {[40, 90, 140, 190].map(y => (
              <line key={y} x1="50" y1={y} x2="680" y2={y} stroke="rgba(255,255,255,0.05)" />
            ))}
            
            {/* Loss Curves */}
            {/* Total Loss */}
            <path 
              d="M 50 40 Q 120 120 250 150 T 500 175 T 680 182" 
              fill="none" 
              stroke="#38bdf8" 
              strokeWidth="3" 
            />
            {/* PINN Mass Loss */}
            <path 
              d="M 50 60 Q 150 140 300 168 T 550 184 T 680 189" 
              fill="none" 
              stroke="#10b981" 
              strokeWidth="2" 
              strokeDasharray="4 3" 
            />
            {/* Hazard Cross-Entropy */}
            <path 
              d="M 50 50 Q 180 110 320 155 T 600 178 T 680 184" 
              fill="none" 
              stroke="#f59e0b" 
              strokeWidth="2" 
              strokeDasharray="2 2" 
            />

            {/* Labels */}
            <text x="680" y="175" fill="#38bdf8" fontSize="10" textAnchor="end">Total Multi-Task Loss</text>
            <text x="680" y="195" fill="#10b981" fontSize="10" textAnchor="end">PINN Mass PDE Residual</text>
          </svg>
        </div>
      </div>

    </section>
  );
}
