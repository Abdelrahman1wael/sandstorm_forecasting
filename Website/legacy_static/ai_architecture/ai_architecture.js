/**
 * ==============================================================================
 * DUST-ML AI ARCHITECTURE & NEURAL LABORATORY: CONTROLLER LOGIC
 * University of Science and Technology Beijing (北京科技大学)
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  const data = window.AI_ARCH_MOCK_DATA;
  if (!data) {
    console.error('AI_ARCH_MOCK_DATA not loaded!');
    return;
  }

  // --- STATE ---
  let selectedLayerId = 'layer-aigamfs-swin';
  let selectedStationId = 'station-chengdu'; // Default to landmark 120h case
  let selectedLeadTimeIndex = 2; // Default to 120h (Day 5)
  let selectedModelType = 'aigamfs';
  let selectedTensorId = 'tensor-nwp';
  let activeTab = 'benchmark';

  // --- 1. INITIALIZE ARCHITECTURE TOPOLOGY LAYERS ---
  function initArchitectureLayers() {
    const container = document.getElementById('layers-grid');
    if (!container) return;

    container.innerHTML = '';
    data.ARCHITECTURE_LAYERS.forEach(layer => {
      const isSelected = layer.id === selectedLayerId;
      const card = document.createElement('div');
      card.className = `layer-interactive-card ${isSelected ? 'selected' : ''}`;
      card.dataset.id = layer.id;

      card.innerHTML = `
        <div class="layer-card-tag">${layer.branch}</div>
        <div class="layer-card-name">${layer.name}</div>
        <div class="layer-card-meta">
          <span>Params: <strong>${(layer.parameters / 1e6).toFixed(1)}M</strong></span>
          <span>Compute: <strong>${layer.hardwareFlops}</strong></span>
        </div>
      `;

      card.addEventListener('click', () => {
        selectedLayerId = layer.id;
        document.querySelectorAll('.layer-interactive-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        renderLayerInspector(layer);
      });

      container.appendChild(card);
    });

    // Render initial selected layer
    const initialLayer = data.getLayerById(selectedLayerId);
    renderLayerInspector(initialLayer);
  }

  function renderLayerInspector(layer) {
    const inspector = document.getElementById('layer-inspector');
    if (!inspector) return;

    inspector.innerHTML = `
      <div class="inspector-header">
        <div>
          <h4>${layer.name}</h4>
          <span class="inspector-branch-badge">${layer.branch} • ${layer.type}</span>
        </div>
        <div style="text-align: right;">
          <div style="font-size:0.75rem; color:var(--text-muted);">PARAMETER FOOTPRINT</div>
          <div style="font-size:1.4rem; font-weight:800; color:var(--cyan-bright); font-family:var(--font-mono);">
            ${(layer.parameters / 1e6).toFixed(2)}M
          </div>
        </div>
      </div>

      <div class="inspector-grid">
        <div class="inspector-prop">
          <div class="inspector-prop-label">Input Tensor Shape</div>
          <div class="inspector-prop-val">${layer.inputShape}</div>
        </div>
        <div class="inspector-prop">
          <div class="inspector-prop-label">Output Tensor Shape</div>
          <div class="inspector-prop-val">${layer.outputShape}</div>
        </div>
        <div class="inspector-prop">
          <div class="inspector-prop-label">Activation Function</div>
          <div class="inspector-prop-val">${layer.activation}</div>
        </div>
        <div class="inspector-prop">
          <div class="inspector-prop-label">Compute Throughput</div>
          <div class="inspector-prop-val">${layer.hardwareFlops}</div>
        </div>
      </div>

      <div class="inspector-prop-label" style="margin-bottom:0.4rem;">ANALYTIC TENSOR FORMULATION</div>
      <div class="math-formula-box">
        <code>${layer.formula}</code>
      </div>

      <div style="font-size:0.88rem; color:var(--text-sub); line-height:1.65; margin-top:0.75rem;">
        <strong>Scientific Role:</strong> ${layer.description}
      </div>
    `;
  }

  // --- 2. INITIALIZE INFERENCE SANDBOX ---
  function initInferenceSandbox() {
    const stationSelect = document.getElementById('select-station');
    const leadSlider = document.getElementById('slider-lead');
    const leadValLabel = document.getElementById('lead-val-label');
    const runBtn = document.getElementById('btn-run-model');

    if (stationSelect) {
      stationSelect.innerHTML = '';
      data.FORECAST_STATIONS.forEach(station => {
        const opt = document.createElement('option');
        opt.value = station.id;
        opt.textContent = `${station.name} — [${station.region}]`;
        if (station.id === selectedStationId) opt.selected = true;
        stationSelect.appendChild(opt);
      });

      stationSelect.addEventListener('change', (e) => {
        selectedStationId = e.target.value;
        executeInference();
      });
    }

    if (leadSlider && leadValLabel) {
      const leads = ["24h (Day 1)", "72h (Day 3)", "120h (Day 5)", "168h (Day 7)", "240h (Day 10)", "360h (Day 15)"];
      leadSlider.addEventListener('input', (e) => {
        selectedLeadTimeIndex = parseInt(e.target.value, 10);
        leadValLabel.textContent = leads[selectedLeadTimeIndex];
        executeInference();
      });
    }

    if (runBtn) {
      runBtn.addEventListener('click', () => {
        runBtn.classList.add('running');
        runBtn.innerHTML = '⚡ Neural Forward Pass...';
        setTimeout(() => {
          runBtn.classList.remove('running');
          runBtn.innerHTML = '⚡ Run AI Inference Pipeline';
          executeInference();
        }, 320);
      });
    }

    executeInference();
  }

  function executeInference() {
    const station = data.getStationById(selectedStationId);
    const forecast = station.leadTimeForecasts[selectedLeadTimeIndex];

    // Station Summary Header
    const titleEl = document.getElementById('out-station-title');
    const coordEl = document.getElementById('out-station-coords');
    if (titleEl) titleEl.textContent = `${station.name} (${station.type})`;
    if (coordEl) coordEl.textContent = `Lat: ${station.coordinates.lat}°N, Lon: ${station.coordinates.lon}°E | Elev: ${station.coordinates.elevationM}m | Lead: ${forecast.lead}`;

    // Metric Displays
    const pm10El = document.getElementById('out-pm10-val');
    const catBadge = document.getElementById('out-category-badge');
    const threatEl = document.getElementById('out-threat-val');
    const residualEl = document.getElementById('out-residual-val');

    if (pm10El) pm10El.textContent = `${forecast.pm10_p50}`;
    
    // Category colors
    let badgeColor = '#10b981';
    let badgeBg = 'rgba(16, 185, 129, 0.15)';
    if (forecast.category.includes('Severe')) {
      badgeColor = '#ef4444';
      badgeBg = 'rgba(239, 68, 68, 0.2)';
    } else if (forecast.category.includes('Sandstorm')) {
      badgeColor = '#f97316';
      badgeBg = 'rgba(249, 115, 22, 0.2)';
    } else if (forecast.category.includes('Blowing')) {
      badgeColor = '#eab308';
      badgeBg = 'rgba(234, 179, 8, 0.2)';
    } else if (forecast.category.includes('Floating')) {
      badgeColor = '#c084fc';
      badgeBg = 'rgba(192, 132, 252, 0.2)';
    }

    if (catBadge) {
      catBadge.textContent = forecast.category;
      catBadge.style.color = badgeColor;
      catBadge.style.backgroundColor = badgeBg;
      catBadge.style.borderColor = badgeColor;
    }

    if (threatEl) threatEl.textContent = `${(forecast.threatScore * 100).toFixed(1)}%`;
    if (residualEl) residualEl.textContent = `${forecast.pinnResidual}`;

    // Quantile Bars
    renderQuantileBars(forecast);

    // SHAP Waterfall
    renderShapWaterfall(station);
  }

  function renderQuantileBars(forecast) {
    const p10Bar = document.getElementById('bar-p10');
    const p50Bar = document.getElementById('bar-p50');
    const p90Bar = document.getElementById('bar-p90');

    const p10Val = document.getElementById('val-p10');
    const p50Val = document.getElementById('val-p50');
    const p90Val = document.getElementById('val-p90');

    const maxScale = Math.max(forecast.p90 * 1.15, 1000);

    if (p10Bar) p10Bar.style.width = `${Math.min(100, (forecast.p10 / maxScale) * 100)}%`;
    if (p50Bar) p50Bar.style.width = `${Math.min(100, (forecast.pm10_p50 / maxScale) * 100)}%`;
    if (p90Bar) p90Bar.style.width = `${Math.min(100, (forecast.p90 / maxScale) * 100)}%`;

    if (p10Val) p10Val.textContent = `${forecast.p10} μg/m³`;
    if (p50Val) p50Val.textContent = `${forecast.pm10_p50} μg/m³`;
    if (p90Val) p90Val.textContent = `${forecast.p90} μg/m³`;
  }

  function renderShapWaterfall(station) {
    const list = document.getElementById('shap-list-container');
    if (!list) return;

    list.innerHTML = '';
    station.shapContributions.forEach(item => {
      const row = document.createElement('div');
      row.className = 'shap-item';

      row.innerHTML = `
        <div class="shap-name" title="${item.feature}">${item.feature}</div>
        <div class="shap-bar-track">
          <div class="shap-bar-fill ${item.direction}" style="width: ${item.pct}%;"></div>
        </div>
        <div class="shap-val" style="color: ${item.direction === 'positive' ? '#f87171' : '#34d399'};">
          ${item.value}
        </div>
      `;
      list.appendChild(row);
    });
  }

  // --- 3. PINN PHYSICS ENGINE SIMULATOR ---
  function initPinnSimulator() {
    const uStarInput = document.getElementById('sim-ustar');
    const uStarTInput = document.getElementById('sim-ustart');
    const smInput = document.getElementById('sim-sm');

    const uStarVal = document.getElementById('sim-ustar-val');
    const uStarTVal = document.getElementById('sim-ustart-val');
    const smVal = document.getElementById('sim-sm-val');

    function updatePhysics() {
      const uStar = parseFloat(uStarInput.value);
      const uStarT = parseFloat(uStarTInput.value);
      const sm = parseFloat(smInput.value);

      if (uStarVal) uStarVal.textContent = `${uStar.toFixed(2)} m/s`;
      if (uStarTVal) uStarTVal.textContent = `${uStarT.toFixed(2)} m/s`;
      if (smVal) smVal.textContent = `${(sm * 100).toFixed(1)}%`;

      const result = data.calculatePhysicsResidual(uStar, uStarT, sm);

      const banner = document.getElementById('pinn-status-banner');
      if (banner) {
        banner.textContent = result.status;
        banner.className = `physics-status-banner ${result.saltationActive ? 'active' : 'quiescent'}`;
      }

      const shearEl = document.getElementById('pinn-shear-val');
      const fluxEl = document.getElementById('pinn-flux-val');
      const lossEl = document.getElementById('pinn-loss-val');
      const errEl = document.getElementById('pinn-err-val');

      if (shearEl) shearEl.textContent = result.shearRatio;
      if (fluxEl) fluxEl.textContent = `${result.saltationFluxMg} mg/m²s`;
      if (lossEl) lossEl.textContent = result.pinnLoss;
      if (errEl) errEl.textContent = result.massBalanceError;
    }

    if (uStarInput && uStarTInput && smInput) {
      uStarInput.addEventListener('input', updatePhysics);
      uStarTInput.addEventListener('input', updatePhysics);
      smInput.addEventListener('input', updatePhysics);
      updatePhysics();
    }
  }

  // --- 4. ST-GNN CORRIDOR NETWORK GRAPH (SVG RENDERER) ---
  function initStgnnNetworkGraph() {
    const svg = document.getElementById('stgnn-network-svg');
    if (!svg) return;

    const graph = data.CORRIDOR_GRAPH_DATA;
    const width = 960;
    const height = 480;

    let svgHtml = `
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
        </marker>
        <linearGradient id="edge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ef4444" stop-opacity="0.8" />
          <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.7" />
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.8" />
        </linearGradient>
      </defs>
    `;

    // Render links
    graph.links.forEach(link => {
      const sourceNode = graph.nodes.find(n => n.id === link.source);
      const targetNode = graph.nodes.find(n => n.id === link.target);
      if (!sourceNode || !targetNode) return;

      const strokeWidth = (link.weight * 3).toFixed(1);
      const isBenchmark = link.target === 'sichuan_basin';

      svgHtml += `
        <line x1="${sourceNode.x}" y1="${sourceNode.y}" x2="${targetNode.x}" y2="${targetNode.y}"
          stroke="${isBenchmark ? '#c084fc' : 'rgba(56, 189, 248, 0.45)'}"
          stroke-width="${isBenchmark ? 3.5 : strokeWidth}"
          stroke-dasharray="${isBenchmark ? '6,4' : 'none'}"
          marker-end="url(#arrow)"
        />
        <text x="${(sourceNode.x + targetNode.x) / 2}" y="${(sourceNode.y + targetNode.y) / 2 - 6}"
          fill="#94a3b8" font-size="10" font-family="JetBrains Mono" text-anchor="middle">
          ${link.transitHours}h (${link.distanceKm}km)
        </text>
      `;
    });

    // Render nodes
    graph.nodes.forEach(node => {
      let nodeColor = '#06b6d4';
      if (node.category === 'source') nodeColor = '#ef4444';
      else if (node.category === 'bottleneck') nodeColor = '#f59e0b';
      else if (node.category === 'corridor') nodeColor = '#8b5cf6';
      else if (node.id === 'sichuan_basin') nodeColor = '#c084fc';

      svgHtml += `
        <g class="graph-node-group" style="cursor: pointer;" data-id="${node.id}">
          <circle cx="${node.x}" cy="${node.y}" r="${node.id === 'sichuan_basin' ? 14 : 11}"
            fill="${nodeColor}" fill-opacity="0.25" stroke="${nodeColor}" stroke-width="2" />
          <circle cx="${node.x}" cy="${node.y}" r="4" fill="${nodeColor}" />
          <text x="${node.x}" y="${node.y + 22}" fill="#f8fafc" font-size="11" font-weight="600"
            font-family="Outfit" text-anchor="middle">
            ${node.label.split(' ')[0]}
          </text>
          <text x="${node.x}" y="${node.y + 34}" fill="#94a3b8" font-size="9"
            font-family="Inter" text-anchor="middle">
            ${node.role}
          </text>
        </g>
      `;
    });

    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.innerHTML = svgHtml;
  }

  // --- 5. BENCHMARK & CONVERGENCE TABS ---
  function initBenchmarkTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const contentBox = document.getElementById('tab-content-container');

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeTab = btn.dataset.tab;
        renderTabContent(activeTab, contentBox);
      });
    });

    renderTabContent('benchmark', contentBox);
  }

  function renderTabContent(tab, container) {
    if (!container) return;

    if (tab === 'benchmark') {
      let rowsHtml = '';
      data.MODEL_BENCHMARKS.forEach(bm => {
        const aigamfs = bm.models['AI-GAMFS (Coupled Deep)'];
        const lineA = bm.models['Main Line A (LightGBM/XGB)'];
        const ecmwf = bm.models['ECMWF IFS (Operational NWP)'];
        const cma = bm.models['CMA-GFS (CMA Physical NWP)'];

        const errorGain = (((ecmwf.rmse - aigamfs.rmse) / ecmwf.rmse) * 100).toFixed(1);

        rowsHtml += `
          <tr>
            <td><strong>${bm.leadTime}</strong></td>
            <td><strong>${aigamfs.rmse}</strong> μg/m³</td>
            <td>${lineA.rmse} μg/m³</td>
            <td style="color:#f87171;">${ecmwf.rmse} μg/m³</td>
            <td style="color:#f87171;">${cma.rmse} μg/m³</td>
            <td><span class="tag-highlight">-${errorGain}% Error</span></td>
            <td><strong style="color:var(--emerald-bright);">${(aigamfs.threatScore * 100).toFixed(1)}%</strong></td>
          </tr>
        `;
      });

      container.innerHTML = `
        <div class="benchmark-table-wrapper">
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>Forecast Lead Horizon</th>
                <th>AI-GAMFS (Proposed)</th>
                <th>Main Line A (Trees)</th>
                <th>ECMWF IFS (NWP)</th>
                <th>CMA-GFS (NWP)</th>
                <th>AI Accuracy Gain</th>
                <th>AI Threat Score (TS)</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
            </tbody>
          </table>
        </div>
      `;
    } else if (tab === 'telemetry') {
      const logs = data.TRAINING_TELEMETRY;
      // Draw SVG convergence chart
      const w = 900;
      const h = 260;
      const padding = 40;

      // Extract points
      const pointsTotal = logs.map((l, i) => `${padding + (i / 99) * (w - 2 * padding)},${h - padding - (l.totalLoss / 0.22) * (h - 2 * padding)}`).join(' ');
      const pointsMse = logs.map((l, i) => `${padding + (i / 99) * (w - 2 * padding)},${h - padding - (l.dataMse / 0.22) * (h - 2 * padding)}`).join(' ');
      const pointsPinn = logs.map((l, i) => `${padding + (i / 99) * (w - 2 * padding)},${h - padding - (l.pinnSaltationLoss / 0.08) * (h - 2 * padding)}`).join(' ');

      container.innerHTML = `
        <div style="margin-bottom:1rem; font-size:0.85rem; color:var(--text-sub);">
          Physics-Informed Loss Convergence across 100 Epochs (4x NVIDIA A100 SXM4 Cluster):
        </div>
        <svg viewBox="0 0 ${w} ${h}" style="width:100%; height:260px; background:#040711; border-radius:8px; border:1px solid var(--border-subtle);">
          <polyline fill="none" stroke="#38bdf8" stroke-width="2.5" points="${pointsTotal}" />
          <polyline fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4,3" points="${pointsMse}" />
          <polyline fill="none" stroke="#10b981" stroke-width="1.8" points="${pointsPinn}" />
          
          <line x1="${padding}" y1="${h - padding}" x2="${w - padding}" y2="${h - padding}" stroke="rgba(255,255,255,0.15)" stroke-width="1" />
          <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${h - padding}" stroke="rgba(255,255,255,0.15)" stroke-width="1" />
          
          <text x="${padding}" y="${padding - 10}" fill="#94a3b8" font-size="10" font-family="JetBrains Mono">Loss Magnitude</text>
          <text x="${w - padding - 80}" y="${h - padding + 25}" fill="#94a3b8" font-size="10" font-family="JetBrains Mono">Epoch 100</text>
        </svg>
        <div style="display:flex; gap:1.5rem; margin-top:0.75rem; font-size:0.75rem; color:var(--text-muted);">
          <span><span style="color:#38bdf8; font-weight:700;">—</span> Total Joint Loss</span>
          <span><span style="color:#f59e0b; font-weight:700;">---</span> Data-Driven MSE Loss</span>
          <span><span style="color:#10b981; font-weight:700;">—</span> PINN Saltation Physics Loss</span>
        </div>
      `;
    } else if (tab === 'confusion') {
      const cm = data.COST_MATRIX;
      let tableRows = '';
      cm.classes.forEach((trueClass, rIdx) => {
        let cells = '';
        cm.classes.forEach((predClass, cIdx) => {
          const val = cm.matrixSample[rIdx][cIdx];
          const isDiag = rIdx === cIdx;
          cells += `<td style="background:${isDiag ? 'rgba(16,185,129,0.15)' : 'transparent'}; font-weight:${isDiag ? '700' : '400'}; color:${isDiag ? 'var(--emerald-bright)' : 'var(--text-sub)'}">${val}</td>`;
        });
        tableRows += `<tr><td><strong>${trueClass}</strong></td>${cells}</tr>`;
      });

      container.innerHTML = `
        <div style="margin-bottom:1rem; font-size:0.85rem; color:var(--text-sub);">
          Asymmetric Cost Matrix & 5-Tier Hazard Classification (Severe Miss Penalty = 100x):
        </div>
        <div class="benchmark-table-wrapper">
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>True \\ Predicted</th>
                <th>Clean</th>
                <th>Floating Dust</th>
                <th>Blowing Sand</th>
                <th>Sandstorm</th>
                <th>Severe Sandstorm</th>
              </tr>
            </thead>
            <tbody>
              ${tableRows}
            </tbody>
          </table>
        </div>
      `;
    }
  }

  // --- 6. RAW MOCK TENSOR & JSON INSPECTOR ---
  function initJsonInspector() {
    const pills = document.querySelectorAll('.tensor-pill');
    const codeView = document.getElementById('json-display-code');
    const copyBtn = document.getElementById('btn-copy-json');

    function updateCodeView() {
      let payload = {};
      if (selectedTensorId === 'system-spec') {
        payload = data.SYSTEM_SPEC;
      } else if (selectedTensorId === 'full-mock') {
        payload = data;
      } else {
        payload = data.INPUT_TENSORS.find(t => t.id === selectedTensorId) || data.INPUT_TENSORS[0];
      }

      if (codeView) {
        codeView.textContent = JSON.stringify(payload, null, 2);
      }
    }

    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        selectedTensorId = pill.dataset.id;
        updateCodeView();
      });
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        if (codeView) {
          navigator.clipboard.writeText(codeView.textContent).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '✅ Copied!';
            setTimeout(() => { copyBtn.innerHTML = originalText; }, 1800);
          });
        }
      });
    }

    updateCodeView();
  }

  // --- RUN ALL INITIALIZATIONS ---
  initArchitectureLayers();
  initInferenceSandbox();
  initPinnSimulator();
  initStgnnNetworkGraph();
  initBenchmarkTabs();
  initJsonInspector();

  console.log('DustML AI Architecture & Mock Data Subsystem successfully initialized.');
});
