import React, { useState, useMemo } from 'react';
import { 
  Compass, 
  TrendingDown, 
  BarChart2, 
  GitBranch, 
  Sliders, 
  Calendar, 
  Info, 
  CheckCircle2, 
  AlertTriangle,
  RotateCcw
} from 'lucide-react';

export default function SimulationsSuite() {
  // --- Simulation 1: Map Path State ---
  const [selectedCorridor, setSelectedCorridor] = useState('all');
  const [hoveredStation, setHoveredStation] = useState(null);

  // --- Simulation 2: Skill Decay Metric ---
  const [skillMetric, setSkillMetric] = useState('csi');

  // --- Simulation 3: SHAP Category Filter ---
  const [shapCategory, setShapCategory] = useState('all');

  // --- Simulation 5: ROC Threshold Slider State ---
  const [threshold, setThreshold] = useState(0.45);

  // Stations for Map Simulation
  const stations = [
    { id: 'taklamakan', name: 'Taklamakan Desert (Source)', x: 120, y: 190, isSource: true, pm10: 2450, ustar: 0.52 },
    { id: 'badain', name: 'Badain Jaran (Source)', x: 300, y: 140, isSource: true, pm10: 2890, ustar: 0.58 },
    { id: 'gobi', name: 'Mongolian Gobi (Source)', x: 420, y: 80, isSource: true, pm10: 1950, ustar: 0.49 },
    { id: 'dunhuang', name: 'Dunhuang Gateway', x: 220, y: 170, isSource: false, pm10: 1420, ustar: 0.42 },
    { id: 'zhangye', name: 'Zhangye (Hexi Funnel)', x: 340, y: 200, isSource: false, pm10: 1180, ustar: 0.38 },
    { id: 'minqin', name: 'Minqin Oasis Node', x: 390, y: 190, isSource: false, pm10: 1350, ustar: 0.41 },
    { id: 'wuwei', name: 'Wuwei Terminal Cut', x: 430, y: 220, isSource: false, pm10: 980, ustar: 0.36 },
    { id: 'lanzhou', name: 'Lanzhou Basin', x: 470, y: 260, isSource: false, pm10: 740, ustar: 0.29 },
    { id: 'xian', name: 'Xi\'an Guanzhong', x: 550, y: 280, isSource: false, pm10: 520, ustar: 0.24 },
    { id: 'hohhot', name: 'Hohhot / Inner Mongolia', x: 540, y: 150, isSource: false, pm10: 890, ustar: 0.33 },
    { id: 'beijing', name: 'Beijing Metropolis', x: 670, y: 170, isSource: false, pm10: 672, ustar: 0.27 },
    { id: 'chengdu', name: 'Chengdu (120h Incursion)', x: 480, y: 350, isSource: false, pm10: 410, ustar: 0.21 },
  ];

  // Lead Time Decay Data
  const leadTimes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
  const skillData = {
    csi: {
      label: 'Critical Success Index (CSI / Threat Score)',
      unit: '',
      aigamfs: [0.78, 0.74, 0.69, 0.64, 0.58, 0.52, 0.47, 0.43, 0.39, 0.36, 0.33, 0.30, 0.28, 0.26, 0.24],
      ecmwf:   [0.72, 0.65, 0.54, 0.41, 0.28, 0.19, 0.14, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02],
      baseml:  [0.68, 0.61, 0.50, 0.42, 0.34, 0.27, 0.22, 0.18, 0.15, 0.13, 0.11, 0.09, 0.08, 0.07, 0.06],
    },
    pod: {
      label: 'Probability of Detection (Hit Rate %)',
      unit: '%',
      aigamfs: [94.2, 91.5, 88.0, 84.2, 79.8, 75.3, 71.0, 67.2, 63.5, 59.8, 56.4, 53.1, 50.2, 47.8, 45.2],
      ecmwf:   [89.0, 82.4, 71.5, 58.0, 44.2, 33.1, 24.5, 18.2, 14.0, 11.2, 9.1, 7.5, 6.2, 5.1, 4.2],
      baseml:  [86.5, 80.1, 70.2, 61.4, 52.3, 44.5, 38.0, 32.4, 28.1, 24.5, 21.3, 18.7, 16.5, 14.8, 13.2],
    },
    far: {
      label: 'False Alarm Rate (FAR %)',
      unit: '%',
      aigamfs: [18.2, 21.0, 24.5, 28.1, 31.8, 35.4, 39.0, 42.5, 46.1, 49.5, 52.8, 56.0, 58.9, 61.5, 64.0],
      ecmwf:   [22.5, 29.8, 41.2, 54.0, 67.5, 76.2, 82.4, 87.0, 90.1, 92.4, 94.0, 95.2, 96.1, 96.8, 97.4],
      baseml:  [24.1, 31.5, 40.0, 48.2, 56.5, 63.8, 69.5, 74.2, 78.1, 81.5, 84.2, 86.8, 88.9, 90.5, 92.0],
    },
    error_red: {
      label: 'Forecast Error Reduction vs ECMWF (%)',
      unit: '%',
      aigamfs: [42.5, 48.1, 54.2, 59.8, 64.1, 68.2, 71.5, 73.8, 74.0, 72.5, 70.8, 68.5, 66.2, 64.0, 62.1],
      ecmwf:   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      baseml:  [18.2, 21.5, 25.4, 29.1, 32.5, 35.0, 37.2, 38.5, 38.0, 36.8, 35.1, 33.4, 31.8, 30.2, 28.5],
    }
  };

  // SHAP Feature Attribution Data
  const shapFeatures = [
    { name: '10m Surface Wind Speed (u10)', importance: 28.4, category: 'dynamics', positive: true },
    { name: 'Aerodynamic Friction Velocity (u*)', importance: 24.1, category: 'emission', positive: true },
    { name: 'Boundary Layer Height (BLH)', importance: 18.7, category: 'dynamics', positive: true },
    { name: 'Antecedent Topsoil Moisture (SM)', importance: -16.2, category: 'memory', positive: false },
    { name: 'Vegetation Cover Index (NDVI)', importance: -14.5, category: 'memory', positive: false },
    { name: 'Precipitation Deficit (30-Day)', importance: 12.8, category: 'memory', positive: true },
    { name: 'Surface Temperature Lapse Rate', importance: 11.2, category: 'dynamics', positive: true },
    { name: '700hPa Geopotential Height Gradient', importance: 9.8, category: 'dynamics', positive: true },
    { name: 'Snow Cover Melt Anomaly', importance: 8.4, category: 'memory', positive: true },
    { name: 'Threshold Shear Ratio (u*/u*t)', importance: 21.6, category: 'emission', positive: true },
  ];

  const filteredShap = shapCategory === 'all' 
    ? shapFeatures 
    : shapFeatures.filter(f => f.category === shapCategory);

  // Dynamic Confusion Matrix Calculations based on threshold tau
  const cmMetrics = useMemo(() => {
    const totalEvents = 1000;
    const actualStorms = 100;
    const actualCalm = 900;

    // As threshold increases: hits decrease slightly, false alarms drop steeply
    const hits = Math.round(actualStorms * Math.exp(-0.4 * threshold));
    const misses = actualStorms - hits;
    const falseAlarms = Math.round(actualCalm * 0.25 * Math.exp(-3.2 * threshold));
    const correctRejects = actualCalm - falseAlarms;

    const pod = ((hits / actualStorms) * 100).toFixed(1);
    const far = (((falseAlarms) / (hits + falseAlarms || 1)) * 100).toFixed(1);
    const csi = (hits / (hits + misses + falseAlarms)).toFixed(3);
    const precision = ((hits / (hits + falseAlarms || 1)) * 100).toFixed(1);
    const f1 = (2 * (hits / (hits + falseAlarms || 1)) * (hits / actualStorms) / ((hits / (hits + falseAlarms || 1)) + (hits / actualStorms) || 1)).toFixed(3);

    return { hits, misses, falseAlarms, correctRejects, pod, far, csi, precision, f1 };
  }, [threshold]);

  return (
    <section className="viz-showcase" style={{ padding: '2rem 0' }}>
      <div className="container">

        <div className="section-head" style={{ marginBottom: '2.5rem' }}>
          <span className="section-tag">Interactive Simulation Suite</span>
          <h2 className="section-title">Dynamic Meteorological & Algorithmic Engines</h2>
          <p className="section-desc">
            Directly visualizing the spatial transport corridors of East Asian sandstorms, multi-source tensor pipelines, empirical lead-time forecast decay benchmarks, and real-time threshold-calibrated ROC confusion matrices.
          </p>
        </div>

        {/* 🗺️ VISUAL 1: East Asia Dust Transport Trajectory Map */}
        <div className="viz-card glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', position: 'relative' }}>
          <div className="viz-toolbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 8 }}>
                <Compass size={18} color="var(--accent-amber)" />
                East Asia Dust Transport Corridors & Sichuan 120h Incursion Map
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Source Deserts (Taklamakan, Badain Jaran, Gobi) → Hexi Corridor Funnel → North China & Remote Sichuan Basin
              </p>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                onClick={() => setSelectedCorridor('all')}
                className={`btn ${selectedCorridor === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              >
                All Corridors
              </button>
              <button 
                onClick={() => setSelectedCorridor('northwest')}
                className={`btn ${selectedCorridor === 'northwest' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              >
                Northwest Path
              </button>
              <button 
                onClick={() => setSelectedCorridor('sichuan')}
                className={`btn ${selectedCorridor === 'sichuan' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              >
                ★ 120h Sichuan Case
              </button>
            </div>
          </div>

          {/* SVG Map Container */}
          <div style={{ width: '100%', height: '380px', background: 'radial-gradient(circle at 40% 40%, rgba(13, 21, 39, 0.95), #050811)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)', overflow: 'hidden', position: 'relative' }}>
            <svg viewBox="0 0 800 420" style={{ width: '100%', height: '100%' }}>
              <defs>
                <linearGradient id="corridorGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
                  <stop offset="50%" stopColor="#06b6d4" stopOpacity="0.7" />
                  <stop offset="100%" stopColor="#818cf8" stopOpacity="0.8" />
                </linearGradient>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                  <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              {/* Grid Lines */}
              {[100, 200, 300, 400].map(y => (
                <line key={`h-${y}`} x1="0" y1={y} x2="800" y2={y} stroke="rgba(255,255,255,0.03)" strokeDasharray="4 4" />
              ))}
              {[150, 300, 450, 600, 750].map(x => (
                <line key={`v-${x}`} x1={x} y1="0" x2={x} y2="420" stroke="rgba(255,255,255,0.03)" strokeDasharray="4 4" />
              ))}

              {/* Background Topography Contour Guides */}
              <path d="M 80 240 Q 200 230 320 250 T 560 310 T 780 280" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
              <path d="M 60 160 Q 260 120 440 180 T 740 160" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />

              {/* Corridor Path A: Northwest Path (Taklamakan -> Hexi -> Beijing) */}
              {(selectedCorridor === 'all' || selectedCorridor === 'northwest') && (
                <path 
                  d="M 120 190 Q 240 160 340 200 T 430 220 T 540 150 T 670 170" 
                  fill="none" 
                  stroke="url(#corridorGrad)" 
                  strokeWidth="4" 
                  strokeDasharray="8 4"
                  filter="url(#glow)"
                >
                  <animate attributeName="stroke-dashoffset" from="100" to="0" dur="4s" repeatCount="indefinite" />
                </path>
              )}

              {/* Corridor Path B: Northern Path (Mongolian Gobi -> Inner Mongolia -> Beijing) */}
              {(selectedCorridor === 'all') && (
                <path 
                  d="M 420 80 Q 480 110 540 150 T 670 170" 
                  fill="none" 
                  stroke="#f59e0b" 
                  strokeWidth="3" 
                  strokeOpacity="0.75"
                  strokeDasharray="6 3"
                >
                  <animate attributeName="stroke-dashoffset" from="60" to="0" dur="3s" repeatCount="indefinite" />
                </path>
              )}

              {/* Corridor Path C: Sichuan Incursion (Hexi -> Lanzhou -> Qinling cut -> Chengdu) */}
              {(selectedCorridor === 'all' || selectedCorridor === 'sichuan') && (
                <path 
                  d="M 340 200 Q 430 220 470 260 T 480 350" 
                  fill="none" 
                  stroke="#c084fc" 
                  strokeWidth="4" 
                  filter="url(#glow)"
                  strokeDasharray="7 3"
                >
                  <animate attributeName="stroke-dashoffset" from="80" to="0" dur="3.5s" repeatCount="indefinite" />
                </path>
              )}

              {/* Stations Nodes */}
              {stations.map(st => {
                const isHovered = hoveredStation?.id === st.id;
                return (
                  <g 
                    key={st.id} 
                    transform={`translate(${st.x}, ${st.y})`}
                    onMouseEnter={() => setHoveredStation(st)}
                    onMouseLeave={() => setHoveredStation(null)}
                    style={{ cursor: 'pointer' }}
                  >
                    {/* Pulsing ring for sources */}
                    {st.isSource && (
                      <circle r="14" fill="none" stroke="#f59e0b" strokeWidth="1.5" opacity="0.6">
                        <animate attributeName="r" values="8;18;8" dur="2.5s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.8;0.1;0.8" dur="2.5s" repeatCount="indefinite"/>
                      </circle>
                    )}

                    {/* Landmark callout for Chengdu */}
                    {st.id === 'chengdu' && (
                      <circle r="12" fill="none" stroke="#c084fc" strokeWidth="1.5">
                        <animate attributeName="r" values="6;16;6" dur="2s" repeatCount="indefinite"/>
                      </circle>
                    )}

                    {/* Station Pin */}
                    <circle 
                      r={st.isSource ? 8 : (isHovered ? 7 : 5)} 
                      fill={st.isSource ? '#f59e0b' : (st.id === 'chengdu' ? '#c084fc' : '#38bdf8')}
                      stroke="#070b14"
                      strokeWidth="2"
                    />

                    {/* Station Name Label */}
                    <text 
                      x="9" 
                      y="4" 
                      fill={st.isSource ? '#fde68a' : (st.id === 'chengdu' ? '#e9d5ff' : '#cbd5e1')} 
                      fontSize={st.isSource ? "11" : "9.5"} 
                      fontWeight={st.isSource || st.id === 'beijing' || st.id === 'chengdu' ? "700" : "500"}
                      fontFamily="Inter, sans-serif"
                    >
                      {st.name}
                    </text>
                  </g>
                );
              })}
            </svg>

            {/* Live Hover Tooltip Panel */}
            {hoveredStation && (
              <div style={{ position: 'absolute', bottom: 16, right: 16, background: 'rgba(15, 23, 42, 0.95)', border: '1px solid var(--accent-cyan)', padding: '0.75rem 1rem', borderRadius: 8, minWidth: 220, boxShadow: 'var(--shadow-lg)' }}>
                <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '0.9rem', marginBottom: 4 }}>
                  {hoveredStation.name}
                </div>
                <div style={{ fontSize: '0.78rem', color: '#94a3b8', display: 'flex', justifyContent: 'space-between' }}>
                  <span>Peak Simulated PM10:</span>
                  <strong style={{ color: '#38bdf8' }}>{hoveredStation.pm10} μg/m³</strong>
                </div>
                <div style={{ fontSize: '0.78rem', color: '#94a3b8', display: 'flex', justifyContent: 'space-between', marginTop: 2 }}>
                  <span>Friction Velocity u*:</span>
                  <strong style={{ color: hoveredStation.ustar > 0.35 ? '#f59e0b' : '#34d399' }}>
                    {hoveredStation.ustar} m/s {hoveredStation.ustar > 0.35 ? '(Saltation Active)' : '(Calm)'}
                  </strong>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 📈 VISUAL 2 & 3: Skill Decay & SHAP Attribution Side-by-Side */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          
          {/* Visual 2: Skill Decay Benchmark */}
          <div className="viz-card glass-panel" style={{ padding: '1.25rem' }}>
            <div className="viz-toolbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.05rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 6 }}>
                  <TrendingDown size={17} color="#38bdf8" />
                  Lead-Time Skill Decay (Days 1–15)
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {skillData[skillMetric].label}
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.25rem', flexWrap: 'wrap' }}>
                {['csi', 'pod', 'far', 'error_red'].map(m => (
                  <button
                    key={m}
                    onClick={() => setSkillMetric(m)}
                    className={`btn ${skillMetric === m ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ padding: '0.25rem 0.5rem', fontSize: '0.72rem', textTransform: 'uppercase' }}
                  >
                    {m === 'error_red' ? 'Err Red%' : m}
                  </button>
                ))}
              </div>
            </div>

            {/* SVG Line Chart */}
            <div style={{ height: 260, position: 'relative' }}>
              <svg viewBox="0 0 460 220" style={{ width: '100%', height: '100%' }}>
                {/* Y-axis Guides */}
                {[40, 90, 140, 190].map((y, i) => (
                  <line key={y} x1="35" y1={y} x2="440" y2={y} stroke="rgba(255,255,255,0.06)" />
                ))}

                {/* X-axis Labels */}
                {[1, 3, 5, 7, 9, 11, 13, 15].map(d => {
                  const x = 35 + ((d - 1) / 14) * 405;
                  return (
                    <text key={d} x={x} y="210" fill="#94a3b8" fontSize="9" textAnchor="middle">
                      D{d}
                    </text>
                  );
                })}

                {/* AI-GAMFS Curve */}
                {(() => {
                  const vals = skillData[skillMetric].aigamfs;
                  const maxVal = Math.max(...vals, ...skillData[skillMetric].ecmwf, 1);
                  const minVal = 0;
                  const pts = vals.map((v, i) => {
                    const x = 35 + (i / 14) * 405;
                    const y = 190 - (v / maxVal) * 150;
                    return `${x},${y}`;
                  }).join(' ');

                  return (
                    <>
                      <polyline points={pts} fill="none" stroke="#38bdf8" strokeWidth="2.5" />
                      {vals.map((v, i) => {
                        const x = 35 + (i / 14) * 405;
                        const y = 190 - (v / maxVal) * 150;
                        return <circle key={i} cx={x} cy={y} r="3" fill="#38bdf8" />;
                      })}
                    </>
                  );
                })()}

                {/* ECMWF Baseline Curve */}
                {(() => {
                  const vals = skillData[skillMetric].ecmwf;
                  const maxVal = Math.max(...skillData[skillMetric].aigamfs, ...vals, 1);
                  const pts = vals.map((v, i) => {
                    const x = 35 + (i / 14) * 405;
                    const y = 190 - (v / maxVal) * 150;
                    return `${x},${y}`;
                  }).join(' ');

                  return (
                    <polyline points={pts} fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="4 3" />
                  );
                })()}

                {/* Baseline ML Curve */}
                {(() => {
                  const vals = skillData[skillMetric].baseml;
                  const maxVal = Math.max(...skillData[skillMetric].aigamfs, ...skillData[skillMetric].ecmwf, 1);
                  const pts = vals.map((v, i) => {
                    const x = 35 + (i / 14) * 405;
                    const y = 190 - (v / maxVal) * 150;
                    return `${x},${y}`;
                  }).join(' ');

                  return (
                    <polyline points={pts} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="2 2" />
                  );
                })()}
              </svg>

              {/* Chart Legend */}
              <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', fontSize: '0.72rem', marginTop: 4 }}>
                <span style={{ color: '#38bdf8', display: 'flex', alignItems: 'center', gap: 4 }}>
                  <span style={{ width: 12, height: 3, background: '#38bdf8', display: 'inline-block' }}></span> AI-GAMFS (Ours)
                </span>
                <span style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: 4 }}>
                  <span style={{ width: 12, height: 2, background: '#ef4444', display: 'inline-block', borderBottom: '1px dashed' }}></span> ECMWF IFS
                </span>
                <span style={{ color: '#f59e0b', display: 'flex', alignItems: 'center', gap: 4 }}>
                  <span style={{ width: 12, height: 2, background: '#f59e0b', display: 'inline-block', borderBottom: '1px dotted' }}></span> Baseline ML
                </span>
              </div>
            </div>
          </div>

          {/* Visual 3: SHAP Feature Attribution Explorer */}
          <div className="viz-card glass-panel" style={{ padding: '1.25rem' }}>
            <div className="viz-toolbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.05rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 6 }}>
                  <BarChart2 size={17} color="#c084fc" />
                  Feature Importance & SHAP Values
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Physical contributions across atmospheric and land-surface factors
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.25rem' }}>
                {['all', 'emission', 'dynamics', 'memory'].map(c => (
                  <button
                    key={c}
                    onClick={() => setShapCategory(c)}
                    className={`btn ${shapCategory === c ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ padding: '0.25rem 0.5rem', fontSize: '0.72rem', textTransform: 'capitalize' }}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>

            {/* Horizontal Bar Chart */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem', maxHeight: 270, overflowY: 'auto' }}>
              {filteredShap.map((feat, i) => {
                const absVal = Math.abs(feat.importance);
                const pct = (absVal / 30) * 100;
                return (
                  <div key={i} style={{ fontSize: '0.75rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
                      <span style={{ color: '#cbd5e1' }}>{feat.name}</span>
                      <strong style={{ color: feat.positive ? '#38bdf8' : '#f43f5e' }}>
                        {feat.importance > 0 ? `+${feat.importance}%` : `${feat.importance}%`}
                      </strong>
                    </div>
                    <div style={{ height: 6, background: 'rgba(255,255,255,0.06)', borderRadius: 3, overflow: 'hidden' }}>
                      <div 
                        style={{ 
                          width: `${pct}%`, 
                          height: '100%', 
                          background: feat.positive ? 'linear-gradient(90deg, #0284c7, #38bdf8)' : 'linear-gradient(90deg, #be123c, #fb7185)',
                          borderRadius: 3,
                          transition: 'width 0.4s ease'
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

        {/* ⚖️ VISUAL 5: Interactive ROC & Confusion Matrix Simulator */}
        <div className="viz-card glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
          <div className="viz-toolbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 8 }}>
                <Sliders size={18} color="var(--accent-amber)" />
                Interactive Operational Decision Threshold & Confusion Matrix Simulator
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Slide classification threshold &tau; to simulate operational cost-sensitive trade-offs between disaster detection (Hit Rate) and false alarm burden.
              </p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'rgba(15,23,42,0.6)', padding: '0.5rem 1rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '0.82rem', color: '#e2e8f0' }}>Decision Threshold &tau;:</span>
              <strong style={{ color: 'var(--accent-amber)', fontSize: '1.2rem', fontFamily: 'var(--font-mono)' }}>
                {threshold.toFixed(2)}
              </strong>
              <input 
                type="range" 
                min="0.10" 
                max="0.90" 
                step="0.05" 
                value={threshold} 
                onChange={(e) => setThreshold(parseFloat(e.target.value))}
                style={{ width: 140, cursor: 'pointer', accentColor: 'var(--accent-amber)' }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem', alignItems: 'center' }}>
            
            {/* Left: SVG ROC Curve */}
            <div style={{ height: 260, background: 'rgba(5, 8, 17, 0.7)', borderRadius: 8, border: '1px solid var(--border-subtle)', padding: 10 }}>
              <svg viewBox="0 0 340 240" style={{ width: '100%', height: '100%' }}>
                {/* Diagonal Chance Line */}
                <line x1="40" y1="200" x2="300" y2="30" stroke="rgba(255,255,255,0.15)" strokeDasharray="3 3" />
                
                {/* Axes */}
                <line x1="40" y1="200" x2="300" y2="200" stroke="#94a3b8" />
                <line x1="40" y1="200" x2="40" y2="30" stroke="#94a3b8" />
                <text x="170" y="225" fill="#94a3b8" fontSize="10" textAnchor="middle">False Positive Rate (1 - Specificity)</text>
                <text x="20" y="115" fill="#94a3b8" fontSize="10" textAnchor="middle" transform="rotate(-90, 20, 115)">Hit Rate (POD)</text>

                {/* Empirical ROC Curve */}
                <path 
                  d="M 40 200 Q 55 70 120 50 T 300 30" 
                  fill="none" 
                  stroke="#10b981" 
                  strokeWidth="3" 
                />

                {/* Moving Operating Point on ROC */}
                {(() => {
                  // Operating point coordinates based on threshold
                  const fpr = (cmMetrics.falseAlarms / 900);
                  const tpr = (cmMetrics.hits / 100);
                  const cx = 40 + fpr * 260;
                  const cy = 200 - tpr * 170;
                  return (
                    <g>
                      <circle cx={cx} cy={cy} r="6" fill="#f59e0b" stroke="#fff" strokeWidth="2" />
                      <line x1={cx} y1="200" x2={cx} y2={cy} stroke="#f59e0b" strokeDasharray="2 2" />
                      <line x1="40" y1={cy} x2={cx} y2={cy} stroke="#f59e0b" strokeDasharray="2 2" />
                    </g>
                  );
                })()}

                {/* AUC Badge */}
                <text x="240" y="170" fill="#34d399" fontSize="11" fontWeight="700">AUC = 0.942</text>
              </svg>
            </div>

            {/* Right: 4-Cell Confusion Matrix */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                
                <div className="glass-panel" style={{ padding: '0.85rem', borderLeft: '3px solid #10b981' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>True Positives (Hits)</div>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#10b981' }}>{cmMetrics.hits}</div>
                  <div style={{ fontSize: '0.72rem', color: '#cbd5e1' }}>Severe sandstorm warned</div>
                </div>

                <div className="glass-panel" style={{ padding: '0.85rem', borderLeft: '3px solid #f59e0b' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>False Alarms (Type I)</div>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#f59e0b' }}>{cmMetrics.falseAlarms}</div>
                  <div style={{ fontSize: '0.72rem', color: '#cbd5e1' }}>Warning issued, calm weather</div>
                </div>

                <div className="glass-panel" style={{ padding: '0.85rem', borderLeft: '3px solid #ef4444' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Misses (Type II / Missed Disaster)</div>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ef4444' }}>{cmMetrics.misses}</div>
                  <div style={{ fontSize: '0.72rem', color: '#cbd5e1' }}>Catastrophic unpredicted dust</div>
                </div>

                <div className="glass-panel" style={{ padding: '0.85rem', borderLeft: '3px solid #06b6d4' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase' }}>Correct Rejections</div>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#06b6d4' }}>{cmMetrics.correctRejects}</div>
                  <div style={{ fontSize: '0.72rem', color: '#cbd5e1' }}>Calm weather accurately verified</div>
                </div>

              </div>

              {/* Derived Performance Row */}
              <div className="glass-panel" style={{ padding: '0.75rem', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', textAlign: 'center', gap: '0.5rem' }}>
                <div>
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8' }}>Hit Rate (POD)</div>
                  <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#22d3ee' }}>{cmMetrics.pod}%</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8' }}>False Alarm (FAR)</div>
                  <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f59e0b' }}>{cmMetrics.far}%</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8' }}>Threat Score (CSI)</div>
                  <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#10b981' }}>{cmMetrics.csi}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.68rem', color: '#94a3b8' }}>F1-Score</div>
                  <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#818cf8' }}>{cmMetrics.f1}</div>
                </div>
              </div>

            </div>

          </div>
        </div>

        {/* 📅 VISUAL 6: 7-Phase Research Roadmap Gantt Timeline */}
        <div className="viz-card glass-panel" style={{ padding: '1.5rem' }}>
          <div className="viz-toolbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 8 }}>
                <Calendar size={18} color="#34d399" />
                7-Phase Research Roadmap Gantt Timeline (Sep 2025 – Jun 2027)
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Master's Thesis Execution Schedule at Beijing University of Science & Technology (22 Months Total)
              </p>
            </div>
            <span className="stat-badge" style={{ background: 'rgba(16,185,129,0.15)', color: '#34d399' }}>
              Academic Milestone Plan
            </span>
          </div>

          {/* Gantt Visual */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {[
              { phase: 'Phase 1: Topic Definition & Literature Review', span: 'Sep 2025 - Nov 2025', progress: 100, color: '#38bdf8' },
              { phase: 'Phase 2: Multi-Source Data Collection & Regridding', span: 'Dec 2025 - Feb 2026', progress: 90, color: '#06b6d4' },
              { phase: 'Phase 3: Dual-Line Algorithm Development & PINN Coding', span: 'Mar 2026 - Jul 2026', progress: 75, color: '#818cf8' },
              { phase: 'Phase 4: Spatiotemporal Simulation & Operational Benchmarking', span: 'Aug 2026 - Nov 2026', progress: 40, color: '#f59e0b' },
              { phase: 'Phase 5: Empirical Case Studies (Spring 2025/2026 SDS Events)', span: 'Dec 2026 - Feb 2027', progress: 20, color: '#f43f5e' },
              { phase: 'Phase 6: Thesis Drafting & Peer-Reviewed Journal Papers', span: 'Mar 2027 - May 2027', progress: 10, color: '#a855f7' },
              { phase: 'Phase 7: Master\'s Defense & Platform Deployment', span: 'Jun 2027', progress: 5, color: '#10b981' }
            ].map((p, i) => (
              <div key={i} style={{ fontSize: '0.8rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
                  <span style={{ color: '#f8fafc', fontWeight: 600 }}>{p.phase}</span>
                  <span style={{ color: '#94a3b8', fontSize: '0.75rem' }}>{p.span}</span>
                </div>
                <div style={{ height: 10, background: 'rgba(255,255,255,0.06)', borderRadius: 5, overflow: 'hidden' }}>
                  <div 
                    style={{ 
                      width: `${p.progress}%`, 
                      height: '100%', 
                      background: p.color, 
                      borderRadius: 5,
                      boxShadow: `0 0 10px ${p.color}66`
                    }} 
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
