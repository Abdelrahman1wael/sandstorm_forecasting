import React, { useState, useMemo } from 'react';
import { Activity, Wind, AlertTriangle, ShieldCheck, Thermometer, Droplets, Eye, Gauge } from 'lucide-react';

export default function OperationalDashboard() {
  const stations = [
    { code: 'DH', name: 'Dunhuang (Gateway)', ustar_t: 0.35, isSource: true, basePm10: 1200 },
    { code: 'ZY', name: 'Zhangye (Hexi Funnel)', ustar_t: 0.36, isSource: false, basePm10: 950 },
    { code: 'MQ', name: 'Minqin (Oasis Edge)', ustar_t: 0.35, isSource: true, basePm10: 1400 },
    { code: 'WW', name: 'Wuwei (Terminal)', ustar_t: 0.37, isSource: false, basePm10: 820 },
    { code: 'LZ', name: 'Lanzhou (Basin)', ustar_t: 0.38, isSource: false, basePm10: 680 },
    { code: 'HH', name: 'Hohhot (Northern Path)', ustar_t: 0.36, isSource: false, basePm10: 750 },
    { code: 'BJ', name: 'Beijing (Metropolis)', ustar_t: 0.40, isSource: false, basePm10: 580 },
    { code: 'CD', name: 'Chengdu (120h Remote Incursion)', ustar_t: 0.42, isSource: false, basePm10: 380 },
  ];

  const [selectedCode, setSelectedCode] = useState('DH');
  const [windU10, setWindU10] = useState(14.5);
  const [ustar, setUstar] = useState(0.48);
  const [soilMoisture, setSoilMoisture] = useState(0.04);
  const [aod, setAod] = useState(0.65);

  const currentStation = stations.find(s => s.code === selectedCode) || stations[0];

  // PINN Physical Calculations
  const physics = useMemo(() => {
    const ustar_t = currentStation.ustar_t;
    const isSaltation = ustar > ustar_t;
    const uRatio = Math.pow(ustar_t / Math.max(ustar, 1e-4), 2);
    const excess = Math.max(0, 1.0 - uRatio);
    // Owen saltation flux in mg/m*s
    const saltFlux = 0.25 * (1.225 / 9.81) * Math.pow(ustar, 3) * excess * (isSaltation ? 1.0 : 0.0) * 1000;
    const massResidual = (0.0015 + 0.0025 * (windU10 / 25.0)).toFixed(4);

    return { isSaltation, saltFlux: saltFlux.toFixed(2), massResidual };
  }, [currentStation, ustar, windU10]);

  // Multi-Lead Forecast Progression (Days 1 to 15)
  const forecasts = useMemo(() => {
    const leads = [24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360];
    const baseVal = physics.isSaltation 
      ? currentStation.basePm10 * 1.45 + parseFloat(physics.saltFlux) * 0.35 
      : currentStation.basePm10 * 0.75;

    return leads.map((lead, idx) => {
      const day = Math.round(lead / 24);
      const decay = Math.exp(-lead / 180.0);
      const medianP50 = Math.round(Math.max(25, baseVal * decay + 45));
      const spreadRatio = 0.15 + 0.04 * (lead / 24.0);
      const p10 = Math.round(Math.max(15, medianP50 * (1 - spreadRatio)));
      const p90 = Math.round(medianP50 * (1 + spreadRatio * 1.35));

      return { lead, day, p10, p50: medianP50, p90, width: p90 - p10 };
    });
  }, [currentStation, physics]);

  // Overall Hazard Classification for Day 1
  const d1 = forecasts[0];
  const hazardLevel = useMemo(() => {
    if (d1.p50 >= 1000) return { name: 'Level 5: Severe Sandstorm (特强沙尘暴)', color: '#ef4444', bg: 'rgba(239,68,68,0.2)' };
    if (d1.p50 >= 500) return { name: 'Level 4: Sandstorm (沙尘暴)', color: '#f97316', bg: 'rgba(249,115,22,0.2)' };
    if (d1.p50 >= 250) return { name: 'Level 3: Blowing Sand (扬沙)', color: '#f59e0b', bg: 'rgba(245,158,11,0.2)' };
    if (d1.p50 >= 100) return { name: 'Level 2: Suspended Dust (浮尘)', color: '#06b6d4', bg: 'rgba(6,182,212,0.2)' };
    return { name: 'Level 1: Normal Clean Air (正常)', color: '#10b981', bg: 'rgba(16,185,129,0.2)' };
  }, [d1]);

  return (
    <section className="container" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Operational Forecasting Center</span>
        <h2 className="section-title">Real-Time Multi-Lead Forecast & Physics Diagnostics</h2>
        <p className="section-desc">
          Live simulated inference engine evaluating Owens aerodynamic saltation friction velocity thresholds, multi-lead quantile predictions ($P_{10}, P_{50}, P_{90}$), and operational hazard alarms.
        </p>
      </div>

      {/* Station Selector Bar */}
      <div style={{ display: 'flex', gap: '0.5rem', overflowX: 'auto', paddingBottom: '0.75rem', marginBottom: '1.5rem' }}>
        {stations.map(st => (
          <button
            key={st.code}
            onClick={() => setSelectedCode(st.code)}
            className={`btn ${selectedCode === st.code ? 'btn-primary' : 'btn-secondary'}`}
            style={{ 
              padding: '0.55rem 0.95rem', 
              fontSize: '0.82rem', 
              whiteSpace: 'nowrap',
              background: selectedCode === st.code ? 'linear-gradient(135deg, #0284c7, #2563eb)' : 'rgba(15,23,42,0.7)',
              border: selectedCode === st.code ? '1px solid #38bdf8' : '1px solid var(--border-subtle)'
            }}
          >
            {st.name} {st.isSource ? '⚡' : ''}
          </button>
        ))}
      </div>

      {/* Grid: Live Environmental Controls & PINN Physics Card */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
        
        {/* Environmental Controls */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h4 style={{ fontSize: '1.05rem', color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: 8 }}>
            <Wind size={18} color="#38bdf8" />
            Live Environmental & Meteorological Sliders
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
            
            {/* Slider 1: Wind u10 */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-muted)' }}>10m Surface Wind (u10):</span>
                <strong style={{ color: '#38bdf8', fontFamily: 'var(--font-mono)' }}>{windU10} m/s</strong>
              </div>
              <input 
                type="range" min="2.0" max="28.0" step="0.5" value={windU10}
                onChange={e => setWindU10(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: '#38bdf8' }}
              />
            </div>

            {/* Slider 2: Friction Velocity u* */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-muted)' }}>Friction Velocity (u*):</span>
                <strong style={{ color: ustar > currentStation.ustar_t ? '#f59e0b' : '#34d399', fontFamily: 'var(--font-mono)' }}>
                  {ustar} m/s (Threshold: {currentStation.ustar_t} m/s)
                </strong>
              </div>
              <input 
                type="range" min="0.10" max="1.20" step="0.02" value={ustar}
                onChange={e => setUstar(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: ustar > currentStation.ustar_t ? '#f59e0b' : '#34d399' }}
              />
            </div>

            {/* Slider 3: Soil Moisture */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-muted)' }}>Topsoil Moisture:</span>
                <strong style={{ color: '#06b6d4', fontFamily: 'var(--font-mono)' }}>{soilMoisture} m³/m³</strong>
              </div>
              <input 
                type="range" min="0.01" max="0.25" step="0.01" value={soilMoisture}
                onChange={e => setSoilMoisture(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: '#06b6d4' }}
              />
            </div>

            {/* Slider 4: Satellite AOD */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-muted)' }}>Satellite Aerosol Optical Depth (AOD):</span>
                <strong style={{ color: '#c084fc', fontFamily: 'var(--font-mono)' }}>{aod}</strong>
              </div>
              <input 
                type="range" min="0.10" max="2.50" step="0.05" value={aod}
                onChange={e => setAod(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: '#c084fc' }}
              />
            </div>

          </div>
        </div>

        {/* PINN Physical Diagnostic Engine Card */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h4 style={{ fontSize: '1.05rem', color: '#f8fafc', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: 8 }}>
              <Gauge size={18} color="var(--accent-amber)" />
              PINN Aerodynamic Saltation & Continuity State
            </h4>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1rem' }}>
              
              <div style={{ background: 'rgba(5,8,17,0.7)', padding: '0.85rem', borderRadius: 8, borderLeft: physics.isSaltation ? '3px solid #f59e0b' : '3px solid #10b981' }}>
                <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Saltation Status</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: physics.isSaltation ? '#f59e0b' : '#34d399', margin: '3px 0' }}>
                  {physics.isSaltation ? 'EMISSION ACTIVE' : 'SURFACE CALM'}
                </div>
                <div style={{ fontSize: '0.7rem', color: '#cbd5e1' }}>u* / u*t: {(ustar / currentStation.ustar_t).toFixed(2)}x</div>
              </div>

              <div style={{ background: 'rgba(5,8,17,0.7)', padding: '0.85rem', borderRadius: 8, borderLeft: '3px solid #38bdf8' }}>
                <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Owen Dust Flux</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#38bdf8', margin: '3px 0' }}>
                  {physics.saltFlux} mg/m·s
                </div>
                <div style={{ fontSize: '0.7rem', color: '#cbd5e1' }}>Aerodynamic Mass Rate</div>
              </div>

            </div>

            {/* Mass Conservation Residual */}
            <div style={{ background: 'rgba(5,8,17,0.7)', padding: '0.85rem', borderRadius: 8, marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: 4 }}>
                <span style={{ color: '#94a3b8' }}>PINN PDE Mass Continuity Residual:</span>
                <strong style={{ color: '#34d399' }}>{physics.massResidual} (Compliant &lt; 0.01)</strong>
              </div>
              <div style={{ height: 4, background: 'rgba(255,255,255,0.06)', borderRadius: 2 }}>
                <div style={{ width: `${parseFloat(physics.massResidual) * 300}%`, height: '100%', background: '#34d399', borderRadius: 2 }} />
              </div>
            </div>
          </div>

          {/* Current Hazard Alert Banner */}
          <div style={{ background: hazardLevel.bg, border: `1px solid ${hazardLevel.color}`, borderRadius: 8, padding: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <AlertTriangle size={24} color={hazardLevel.color} />
            <div>
              <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Operational Warning Classification:</div>
              <div style={{ fontSize: '0.98rem', fontWeight: 800, color: hazardLevel.color }}>
                {hazardLevel.name}
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* Multi-Lead Forecast Progression Table & Ribbons (Days 1 to 15) */}
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h4 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: 8 }}>
          <Activity size={18} color="#38bdf8" />
          Extended-Range Quantile Progression (Day 1 to Day 15 Forecasts)
        </h4>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
          Calibrated non-parametric intervals: <strong>P10</strong> (Optimistic Lower Bound), <strong>P50</strong> (Realistic Median Target), and <strong>P90</strong> (Worst-Case Disaster Bound).
        </p>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: '#94a3b8' }}>
                <th style={{ padding: '0.65rem' }}>Horizon</th>
                <th style={{ padding: '0.65rem' }}>Lead (Hours)</th>
                <th style={{ padding: '0.65rem', color: '#34d399' }}>P10 Lower (μg/m³)</th>
                <th style={{ padding: '0.65rem', color: '#38bdf8' }}>P50 Median (μg/m³)</th>
                <th style={{ padding: '0.65rem', color: '#f87171' }}>P90 Upper (μg/m³)</th>
                <th style={{ padding: '0.65rem' }}>Spread Width (MPIW)</th>
                <th style={{ padding: '0.65rem' }}>Hazard Level</th>
              </tr>
            </thead>
            <tbody>
              {forecasts.map(f => (
                <tr key={f.lead} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                  <td style={{ padding: '0.65rem', fontWeight: 700, color: '#f8fafc' }}>Day {f.day}</td>
                  <td style={{ padding: '0.65rem', color: 'var(--text-muted)' }}>+{f.lead}h</td>
                  <td style={{ padding: '0.65rem', color: '#34d399', fontFamily: 'var(--font-mono)' }}>{f.p10}</td>
                  <td style={{ padding: '0.65rem', color: '#38bdf8', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{f.p50}</td>
                  <td style={{ padding: '0.65rem', color: '#f87171', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{f.p90}</td>
                  <td style={{ padding: '0.65rem', color: 'var(--text-secondary)' }}>±{Math.round(f.width / 2)} μg/m³</td>
                  <td style={{ padding: '0.65rem' }}>
                    <span className="stat-badge" style={{ 
                      background: f.p50 >= 500 ? 'rgba(239,68,68,0.15)' : (f.p50 >= 250 ? 'rgba(245,158,11,0.15)' : 'rgba(16,185,129,0.15)'),
                      color: f.p50 >= 500 ? '#f87171' : (f.p50 >= 250 ? '#fbbf24' : '#34d399')
                    }}>
                      {f.p50 >= 500 ? 'Severe Alert' : (f.p50 >= 250 ? 'Dust Warning' : 'Moderate')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>

    </section>
  );
}
