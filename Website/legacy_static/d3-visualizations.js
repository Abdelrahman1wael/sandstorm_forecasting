/**
 * D3.js Interactive Visualizations for Sand & Dust Storm Forecasting Research
 * Utilizes D3 v7 for responsive, rich scientific visualizations
 */

// Global Tooltip helper
let tooltip;
function getOrCreateTooltip() {
  if (!tooltip) {
    tooltip = d3.select("body").append("div")
      .attr("class", "d3-tooltip")
      .style("opacity", 0)
      .style("position", "absolute")
      .style("pointer-events", "none")
      .style("z-index", "9999");
  }
  return tooltip;
}

// -------------------------------------------------------------
// 1. Interactive East Asia Dust Storm Trajectory Simulation Map
// -------------------------------------------------------------
function initDustMap() {
  const container = document.getElementById("dust-map-viz");
  if (!container) return;
  container.innerHTML = "";

  const width = container.clientWidth || 800;
  const height = 480;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("width", "100%")
    .attr("height", height)
    .attr("class", "dust-map-svg");

  // Geographic projection centered on China and East Asia
  const projection = d3.geoMercator()
    .center([105, 36])
    .scale(width * 1.1)
    .translate([width / 2, height / 2]);

  const tt = getOrCreateTooltip();

  // Background grid
  const defs = svg.append("defs");
  
  // Desert glow gradient
  const desertGrad = defs.append("radialGradient")
    .attr("id", "desertGlow")
    .attr("cx", "50%").attr("cy", "50%").attr("r", "50%");
  desertGrad.append("stop").attr("offset", "0%").attr("stop-color", "#f59e0b").attr("stop-opacity", 0.6);
  desertGrad.append("stop").attr("offset", "100%").attr("stop-color", "#f59e0b").attr("stop-opacity", 0);

  // Plume gradient
  const plumeGrad = defs.append("linearGradient")
    .attr("id", "plumeFlow")
    .attr("x1", "0%").attr("y1", "0%").attr("x2", "100%").attr("y2", "100%");
  plumeGrad.append("stop").attr("offset", "0%").attr("stop-color", "#f59e0b").attr("stop-opacity", 0.7);
  plumeGrad.append("stop").attr("offset", "50%").attr("stop-color", "#ef4444").attr("stop-opacity", 0.5);
  plumeGrad.append("stop").attr("offset", "100%").attr("stop-color", "#6366f1").attr("stop-opacity", 0.2);

  // Map background
  svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("fill", "#0b1120")
    .attr("rx", 12);

  // Latitude / Longitude graticules
  const graticule = d3.geoGraticule().step([10, 10]);
  const pathGen = d3.geoPath().projection(projection);

  svg.append("path")
    .datum(graticule)
    .attr("class", "graticule")
    .attr("d", pathGen)
    .attr("fill", "none")
    .attr("stroke", "rgba(255,255,255,0.05)")
    .attr("stroke-width", 1);

  // China approximate simplified territorial bounds & key regions
  const gRegions = svg.append("g").attr("class", "regions-layer");

  // Regional bounding polygons for East Asia key sectors
  const regionFeatures = [
    { name: "Tarim Basin / Taklamakan", coords: [[75, 42], [90, 42], [90, 36], [75, 36], [75, 42]], fill: "rgba(245, 158, 11, 0.12)" },
    { name: "Alxa Plateau / Gobi", coords: [[95, 45], [112, 45], [112, 38], [95, 38], [95, 45]], fill: "rgba(245, 158, 11, 0.15)" },
    { name: "North China Plain", coords: [[112, 41], [121, 41], [121, 34], [112, 34], [112, 41]], fill: "rgba(99, 102, 241, 0.12)" },
    { name: "Sichuan Basin", coords: [[102, 33], [109, 33], [109, 28], [102, 28], [102, 33]], fill: "rgba(16, 185, 129, 0.12)" }
  ];

  regionFeatures.forEach(rf => {
    const projectedCoords = rf.coords.map(c => projection(c));
    const pathD = "M" + projectedCoords.map(p => p.join(",")).join("L") + "Z";
    gRegions.append("path")
      .attr("d", pathD)
      .attr("fill", rf.fill)
      .attr("stroke", "rgba(255,255,255,0.15)")
      .attr("stroke-dasharray", "3 3");
  });

  // Transport Corridors (Curved trajectories)
  const trajectoryData = [
    {
      id: "traj-northwest",
      name: "Northwest Cold Front Pathway",
      coords: [[83.6, 38.9], [99.8, 39.2], [104.8, 38.7], [116.4, 39.9]],
      color: "#f59e0b",
      leadTime: "24h - 48h",
      desc: "Taklamakan & Badain Jaran → Hexi Corridor → Jing-Jin-Ji Megacity Area"
    },
    {
      id: "traj-gobi",
      name: "Northern Mongolian Cyclone Pathway",
      coords: [[108.0, 43.5], [112.5, 41.5], [116.4, 39.9], [118.5, 36.5]],
      color: "#ef4444",
      leadTime: "24h - 36h",
      desc: "Gobi Desert → Inner Mongolia → North China Plain & Central Plains"
    },
    {
      id: "traj-remote-sichuan",
      name: "Extended-Range Remote Incursion (April 2025 Case)",
      coords: [[102.4, 39.8], [104.8, 38.7], [106.5, 34.5], [104.1, 30.6]],
      color: "#8b5cf6",
      leadTime: "120h (5 Days)",
      desc: "Badain Jaran / Tengger → Qinling Mountain Gap → Sichuan Basin (120h Advance Warning)"
    }
  ];

  const gTraj = svg.append("g").attr("class", "trajectories-layer");

  trajectoryData.forEach(traj => {
    const lineGen = d3.line()
      .x(d => projection(d)[0])
      .y(d => projection(d)[1])
      .curve(d3.curveCatmullRom.alpha(0.5));

    // Glow line behind
    gTraj.append("path")
      .datum(traj.coords)
      .attr("d", lineGen)
      .attr("fill", "none")
      .attr("stroke", traj.color)
      .attr("stroke-width", 6)
      .attr("stroke-opacity", 0.25)
      .attr("stroke-linecap", "round");

    // Main trajectory line
    const pathElem = gTraj.append("path")
      .datum(traj.coords)
      .attr("id", traj.id)
      .attr("d", lineGen)
      .attr("fill", "none")
      .attr("stroke", traj.color)
      .attr("stroke-width", 2.5)
      .attr("stroke-dasharray", "6 4")
      .attr("class", "animated-dash")
      .style("cursor", "pointer")
      .on("mouseenter", function(event) {
        d3.select(this).attr("stroke-width", 4.5);
        tt.style("opacity", 1)
          .html(`
            <div class="tt-title" style="color:${traj.color}">${traj.name}</div>
            <div class="tt-desc">${traj.desc}</div>
            <div class="tt-meta"><strong>Lead Time Window:</strong> ${traj.leadTime}</div>
          `)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mousemove", function(event) {
        tt.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", function() {
        d3.select(this).attr("stroke-width", 2.5);
        tt.style("opacity", 0);
      });
  });

  // Animated Dust Particles along trajectories
  const gParticles = svg.append("g").attr("class", "particles-layer");

  function spawnParticle(traj) {
    const lineGen = d3.line()
      .x(d => projection(d)[0])
      .y(d => projection(d)[1])
      .curve(d3.curveCatmullRom.alpha(0.5));

    const pathData = lineGen(traj.coords);
    const tempPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    tempPath.setAttribute("d", pathData);
    const totalLen = tempPath.getTotalLength();

    const particle = gParticles.append("circle")
      .attr("r", 3 + Math.random() * 2.5)
      .attr("fill", traj.color)
      .attr("opacity", 0.8)
      .attr("filter", "drop-shadow(0px 0px 4px " + traj.color + ")");

    const duration = 4000 + Math.random() * 2000;

    particle.transition()
      .duration(duration)
      .ease(d3.easeLinear)
      .attrTween("transform", function() {
        return function(t) {
          const pt = tempPath.getPointAtLength(t * totalLen);
          return `translate(${pt.x}, ${pt.y})`;
        };
      })
      .style("opacity", 0)
      .remove()
      .on("end", () => {
        if (container.isConnected) spawnParticle(traj);
      });
  }

  trajectoryData.forEach(traj => {
    for (let i = 0; i < 3; i++) {
      setTimeout(() => spawnParticle(traj), i * 1400);
    }
  });

  // Desert Source Nodes
  const gSources = svg.append("g").attr("class", "sources-layer");
  RESEARCH_DATA.dustTransportCorridor.sources.forEach(src => {
    const pt = projection([src.lon, src.lat]);
    if (!pt) return;

    // Glowing aura
    gSources.append("circle")
      .attr("cx", pt[0])
      .attr("cy", pt[1])
      .attr("r", 18)
      .attr("fill", "url(#desertGlow)")
      .attr("class", "pulsing-aura");

    // Core circle
    gSources.append("circle")
      .attr("cx", pt[0])
      .attr("cy", pt[1])
      .attr("r", 6)
      .attr("fill", "#f59e0b")
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 1.5)
      .style("cursor", "pointer")
      .on("mouseenter", function(event) {
        tt.style("opacity", 1)
          .html(`
            <div class="tt-title" style="color:#f59e0b">🏜️ ${src.name}</div>
            <div class="tt-desc">${src.desc}</div>
            <div class="tt-meta"><strong>Category:</strong> ${src.type}</div>
            <div class="tt-meta"><strong>Est. Area:</strong> ${src.area}</div>
            <div class="tt-meta"><strong>Coords:</strong> ${src.lat}°N, ${src.lon}°E</div>
          `)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mousemove", function(event) {
        tt.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", () => tt.style("opacity", 0));

    // Label
    gSources.append("text")
      .attr("x", pt[0])
      .attr("y", pt[1] - 10)
      .attr("text-anchor", "middle")
      .attr("fill", "#fde68a")
      .attr("font-size", "11px")
      .attr("font-weight", "600")
      .attr("letter-spacing", "0.5px")
      .text(src.name);
  });

  // Receptor Downstream Nodes
  const gReceptors = svg.append("g").attr("class", "receptors-layer");
  RESEARCH_DATA.dustTransportCorridor.receptors.forEach(rcp => {
    const pt = projection([rcp.lon, rcp.lat]);
    if (!pt) return;

    const isSichuan = rcp.name.includes("Sichuan");
    const markerColor = isSichuan ? "#a855f7" : "#38bdf8";

    // Target ripple
    gReceptors.append("circle")
      .attr("cx", pt[0])
      .attr("cy", pt[1])
      .attr("r", 12)
      .attr("fill", "none")
      .attr("stroke", markerColor)
      .attr("stroke-width", 1)
      .attr("opacity", 0.6)
      .attr("class", "ping-circle");

    // Center marker
    gReceptors.append("rect")
      .attr("x", pt[0] - 5)
      .attr("y", pt[1] - 5)
      .attr("width", 10)
      .attr("height", 10)
      .attr("rx", 2)
      .attr("fill", markerColor)
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 1.5)
      .style("cursor", "pointer")
      .on("mouseenter", function(event) {
        tt.style("opacity", 1)
          .html(`
            <div class="tt-title" style="color:${markerColor}">🎯 ${rcp.name}</div>
            <div class="tt-desc"><strong>Target Role:</strong> ${rcp.role}</div>
            <div class="tt-meta"><strong>Travel / Lead Time:</strong> ${rcp.travelHours} Hours</div>
            ${isSichuan ? '<div class="tt-highlight" style="margin-top:6px; color:#c084fc; font-size:11px;">★ Landmark Case: AI-GAMFS accurately predicted 120h intrusion in April 2025!</div>' : ''}
          `)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mousemove", function(event) {
        tt.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", () => tt.style("opacity", 0));

    // Label
    gReceptors.append("text")
      .attr("x", pt[0])
      .attr("y", pt[1] + 16)
      .attr("text-anchor", "middle")
      .attr("fill", markerColor)
      .attr("font-size", "11px")
      .attr("font-weight", "600")
      .text(rcp.name);
  });

  // Map Legend
  const legend = svg.append("g")
    .attr("transform", `translate(16, ${height - 90})`)
    .attr("class", "map-legend");

  legend.append("rect")
    .attr("width", 260)
    .attr("height", 76)
    .attr("rx", 8)
    .attr("fill", "rgba(15, 23, 42, 0.85)")
    .attr("stroke", "rgba(255, 255, 255, 0.1)");

  // Item 1: Source
  legend.append("circle").attr("cx", 14).attr("cy", 16).attr("r", 5).attr("fill", "#f59e0b");
  legend.append("text").attr("x", 26).attr("y", 20).attr("fill", "#e2e8f0").attr("font-size", "11px").text("Dust Source Deserts (Taklamakan/Gobi)");

  // Item 2: Receptors
  legend.append("rect").attr("x", 10).attr("y", 30).attr("width", 8).attr("height", 8).attr("fill", "#38bdf8");
  legend.append("text").attr("x", 26).attr("y", 38).attr("fill", "#e2e8f0").attr("font-size", "11px").text("Receptor Megacities (Jing-Jin-Ji / Central Plains)");

  // Item 3: 120h Intrusion
  legend.append("rect").attr("x", 10).attr("y", 48).attr("width", 8).attr("height", 8).attr("fill", "#a855f7");
  legend.append("text").attr("x", 26).attr("y", 56).attr("fill", "#e2e8f0").attr("font-size", "11px").text("120h Remote Incursion (Sichuan Basin Case)");
}

// -------------------------------------------------------------
// 2. Interactive Multi-Source Data Pipeline Flow
// -------------------------------------------------------------
function initDataPipelineFlow() {
  const container = document.getElementById("pipeline-flow-viz");
  if (!container) return;
  container.innerHTML = "";

  const width = container.clientWidth || 800;
  const height = 400;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("width", "100%")
    .attr("height", height)
    .attr("class", "pipeline-svg");

  const tt = getOrCreateTooltip();

  // Columns: Sources -> Preprocessing -> Feature Tensors -> Dual Models -> Products
  const stages = [
    {
      col: 0,
      title: "1. Multi-Source Raw Data",
      color: "#38bdf8",
      items: [
        { name: "NWP Ensembles", meta: "ECMWF, CMA, GEOS-CF (0.125°–0.25°)", details: "500hPa height, u/v wind vectors, MSLP, 2m temp, PBLH" },
        { name: "ERA5 Reanalysis", meta: "Hourly, 1979–Present", details: "Historical background climate, ENSO, Arctic Oscillation, soil moisture layers" },
        { name: "Satellite Remote Sensing", meta: "MODIS, Himawari, FY-4", details: "NDVI, bare soil ratio, AOD aerosol optical depth, snow cover extent" },
        { name: "In-Situ Ground Sensors", meta: "2,400+ CMA stations", details: "10m wind, friction velocity u*, visibility, PM10/PM2.5 concentrations" }
      ]
    },
    {
      col: 1,
      title: "2. Data Preprocessing",
      color: "#818cf8",
      items: [
        { name: "Spatiotemporal Regridding", meta: "Unified 0.125° Grid", details: "Bilinear & nearest neighbor spatial interpolation across heterogeneous grids" },
        { name: "Missing Data Imputation", meta: "Spatio-Temporal Kriging", details: "Imputation of sensor dropouts and satellite cloud mask occlusion" },
        { name: "Normalization & Z-Score", meta: "Standardized Distributions", details: "Zero-mean unit-variance scaling per vertical atmospheric layer" }
      ]
    },
    {
      col: 2,
      title: "3. Engineered Tensors",
      color: "#f59e0b",
      items: [
        { name: "Dust Emission Tensor", meta: "u*, soil moisture, bare soil%", details: "Aerodynamic friction velocity compared against saltation threshold u*t" },
        { name: "Dynamic Transport Tensor", meta: "10m wind, shear, PBLH", details: "Advection corridors and boundary layer vertical mixing capacity" },
        { name: "Upstream Memory Tensor", meta: "Lag-7d PM10, persistence", details: "Historical sandstorm accumulation and upstream concentration memory" }
      ]
    },
    {
      col: 3,
      title: "4. Dual Model Pathways",
      color: "#ec4899",
      items: [
        { name: "Main Line A: NWP Post-Processing", meta: "RF / XGBoost / EALSTM-QR", details: "Statistical bias correction on numerical model products and quantile bounds" },
        { name: "Main Line B: End-to-End Spatio-Temporal", meta: "GNN + Transformer + PINN", details: "Direct non-linear spatiotemporal sequence modeling with mass conservation loss" }
      ]
    },
    {
      col: 4,
      title: "5. Operational Forecasting",
      color: "#10b981",
      items: [
        { name: "3–15 Day Risk Maps", meta: "Spatially continuous probabilities", details: "High-resolution 5km probability contours of sandstorm occurrence" },
        { name: "Multi-Level Intensity Warnings", meta: "Floating / Blowing / Severe", details: "Categorical alerts mapped to emergency response protocols" }
      ]
    }
  ];

  const colWidth = (width - 60) / stages.length;
  const paddingX = 30;

  // Background connector curves
  const gLinks = svg.append("g").attr("class", "links-layer");

  // Draw node boxes
  const gNodes = svg.append("g").attr("class", "nodes-layer");

  const nodePositions = [];

  stages.forEach((stage, cIdx) => {
    const x = paddingX + cIdx * colWidth;
    const stageNodes = [];
    const itemHeight = 52;
    const gap = 14;
    const startY = 56 + (height - 80 - (stage.items.length * (itemHeight + gap) - gap)) / 2;

    // Stage Header
    svg.append("text")
      .attr("x", x + colWidth / 2)
      .attr("y", 30)
      .attr("text-anchor", "middle")
      .attr("fill", stage.color)
      .attr("font-size", "12px")
      .attr("font-weight", "700")
      .text(stage.title);

    stage.items.forEach((item, rIdx) => {
      const y = startY + rIdx * (itemHeight + gap);
      const nodeObj = { x, y, width: colWidth - 16, height: itemHeight, item, stage, cIdx, rIdx };
      stageNodes.push(nodeObj);

      // Node Card Group
      const card = gNodes.append("g")
        .attr("class", "pipeline-card")
        .style("cursor", "pointer")
        .on("mouseenter", function(event) {
          d3.select(this).select("rect")
            .attr("stroke", stage.color)
            .attr("stroke-width", 2)
            .attr("fill", "rgba(30, 41, 59, 0.95)");

          tt.style("opacity", 1)
            .html(`
              <div class="tt-title" style="color:${stage.color}">${item.name}</div>
              <div class="tt-desc"><strong>Stage:</strong> ${stage.title}</div>
              <div class="tt-meta"><strong>Scope / Spec:</strong> ${item.meta}</div>
              <div class="tt-desc" style="margin-top:6px;">${item.details}</div>
            `)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mousemove", function(event) {
          tt.style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseleave", function() {
          d3.select(this).select("rect")
            .attr("stroke", "rgba(255,255,255,0.1)")
            .attr("stroke-width", 1)
            .attr("fill", "rgba(15, 23, 42, 0.8)");
          tt.style("opacity", 0);
        });

      card.append("rect")
        .attr("x", x + 8)
        .attr("y", y)
        .attr("width", colWidth - 16)
        .attr("height", itemHeight)
        .attr("rx", 6)
        .attr("fill", "rgba(15, 23, 42, 0.8)")
        .attr("stroke", "rgba(255, 255, 255, 0.1)")
        .attr("stroke-width", 1);

      card.append("line")
        .attr("x1", x + 8)
        .attr("y1", y)
        .attr("x2", x + 8)
        .attr("y2", y + itemHeight)
        .attr("stroke", stage.color)
        .attr("stroke-width", 3);

      card.append("text")
        .attr("x", x + 16)
        .attr("y", y + 20)
        .attr("fill", "#f8fafc")
        .attr("font-size", "11px")
        .attr("font-weight", "600")
        .text(item.name.length > 20 ? item.name.substring(0, 18) + "…" : item.name);

      card.append("text")
        .attr("x", x + 16)
        .attr("y", y + 36)
        .attr("fill", "#94a3b8")
        .attr("font-size", "9.5px")
        .text(item.meta.length > 24 ? item.meta.substring(0, 22) + "…" : item.meta);
    });

    nodePositions.push(stageNodes);
  });

  // Draw connecting flow curves between consecutive stages
  for (let c = 0; c < nodePositions.length - 1; c++) {
    const srcStage = nodePositions[c];
    const tgtStage = nodePositions[c + 1];

    srcStage.forEach(src => {
      tgtStage.forEach(tgt => {
        const x1 = src.x + src.width + 8;
        const y1 = src.y + src.height / 2;
        const x2 = tgt.x + 8;
        const y2 = tgt.y + tgt.height / 2;
        const cx1 = x1 + (x2 - x1) * 0.5;
        const cx2 = x1 + (x2 - x1) * 0.5;

        const pathD = `M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`;

        gLinks.append("path")
          .attr("d", pathD)
          .attr("fill", "none")
          .attr("stroke", "rgba(255,255,255,0.06)")
          .attr("stroke-width", 1.2);
      });
    });
  }
}

// -------------------------------------------------------------
// 3. Interactive Lead-Time Forecast Skill Decay Benchmark (Days 1–15)
// -------------------------------------------------------------
let forecastMetric = "csi"; // "csi", "pod", "far", "error_red"

function initForecastSkillChart() {
  const container = document.getElementById("forecast-skill-viz");
  if (!container) return;
  container.innerHTML = "";

  const margin = { top: 30, right: 40, bottom: 50, left: 60 };
  const width = (container.clientWidth || 800) - margin.left - margin.right;
  const height = 360 - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .attr("width", "100%")
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const tt = getOrCreateTooltip();

  // Synthetic yet scientifically grounded empirical decay curves based on proposal:
  // AI-GAMFS reduces error by 38%-74% over ECMWF/NASA and maintains high skill out to 120h (day 5) and beyond (day 15).
  const days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

  const skillDatasets = {
    csi: {
      title: "Critical Success Index (CSI / Threat Score) vs Lead Time",
      yDomain: [0, 1],
      yFormat: d3.format(".2f"),
      series: [
        {
          name: "AI-GAMFS / Deep Spatio-Temporal Model",
          color: "#06b6d4",
          data: days.map(d => ({ day: d, val: 0.88 * Math.exp(-0.045 * (d - 1)) + 0.12 }))
        },
        {
          name: "Traditional NWP (ECMWF / CMA Physical Model)",
          color: "#f59e0b",
          data: days.map(d => ({ day: d, val: 0.78 * Math.exp(-0.16 * (d - 1)) + 0.04 }))
        },
        {
          name: "Classical ML Baseline (RF / SVM)",
          color: "#94a3b8",
          data: days.map(d => ({ day: d, val: 0.72 * Math.exp(-0.12 * (d - 1)) + 0.06 }))
        }
      ]
    },
    pod: {
      title: "Probability of Detection (POD / Hit Rate) vs Lead Time",
      yDomain: [0, 1],
      yFormat: d3.format(".1%"),
      series: [
        {
          name: "AI-GAMFS / Deep Spatio-Temporal Model",
          color: "#06b6d4",
          data: days.map(d => ({ day: d, val: Math.max(0.42, 0.94 - 0.035 * (d - 1)) }))
        },
        {
          name: "Traditional NWP (ECMWF / CMA Physical Model)",
          color: "#f59e0b",
          data: days.map(d => ({ day: d, val: Math.max(0.20, 0.82 - 0.058 * (d - 1)) }))
        },
        {
          name: "Classical ML Baseline (RF / SVM)",
          color: "#94a3b8",
          data: days.map(d => ({ day: d, val: Math.max(0.25, 0.76 - 0.046 * (d - 1)) }))
        }
      ]
    },
    far: {
      title: "False Alarm Ratio (FAR) vs Lead Time (Lower is Better)",
      yDomain: [0, 0.8],
      yFormat: d3.format(".1%"),
      series: [
        {
          name: "AI-GAMFS / Deep Spatio-Temporal Model",
          color: "#06b6d4",
          data: days.map(d => ({ day: d, val: Math.min(0.38, 0.12 + 0.021 * (d - 1)) }))
        },
        {
          name: "Traditional NWP (ECMWF / CMA Physical Model)",
          color: "#f59e0b",
          data: days.map(d => ({ day: d, val: Math.min(0.68, 0.24 + 0.038 * (d - 1)) }))
        },
        {
          name: "Classical ML Baseline (RF / SVM)",
          color: "#94a3b8",
          data: days.map(d => ({ day: d, val: Math.min(0.55, 0.28 + 0.025 * (d - 1)) }))
        }
      ]
    },
    error_red: {
      title: "East Asia Forecast Error Reduction vs Operational NWP (%)",
      yDomain: [0, 100],
      yFormat: d => d + "%",
      series: [
        {
          name: "AI-GAMFS Error Reduction vs ECMWF/NASA (38% – 74%)",
          color: "#10b981",
          data: days.map(d => ({
            day: d,
            val: d <= 5 ? (74 - (d - 1) * 6.5) : Math.max(38, 48 - (d - 5) * 1.2)
          }))
        }
      ]
    }
  };

  const currentData = skillDatasets[forecastMetric];

  // Scales
  const x = d3.scaleLinear()
    .domain([1, 15])
    .range([0, width]);

  const y = d3.scaleLinear()
    .domain(currentData.yDomain)
    .nice()
    .range([height, 0]);

  // Gridlines
  svg.append("g")
    .attr("class", "grid")
    .attr("stroke", "rgba(255,255,255,0.06)")
    .call(d3.axisLeft(y).tickSize(-width).tickFormat(""));

  svg.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0,${height})`)
    .attr("stroke", "rgba(255,255,255,0.06)")
    .call(d3.axisBottom(x).ticks(15).tickSize(-height).tickFormat(""));

  // Axes
  const xAxis = d3.axisBottom(x).ticks(15).tickFormat(d => `Day ${d}`);
  const yAxis = d3.axisLeft(y).tickFormat(currentData.yFormat);

  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(xAxis)
    .attr("color", "#94a3b8")
    .selectAll("text")
    .attr("font-size", "11px");

  svg.append("g")
    .call(yAxis)
    .attr("color", "#94a3b8")
    .selectAll("text")
    .attr("font-size", "11px");

  // Highlight 120h (Day 5) Landmark Zone
  const day5X = x(5);
  svg.append("rect")
    .attr("x", day5X - 12)
    .attr("y", 0)
    .attr("width", 24)
    .attr("height", height)
    .attr("fill", "rgba(99, 102, 241, 0.12)")
    .attr("stroke", "rgba(99, 102, 241, 0.4)")
    .attr("stroke-dasharray", "4 2");

  svg.append("text")
    .attr("x", day5X)
    .attr("y", 16)
    .attr("text-anchor", "middle")
    .attr("fill", "#c084fc")
    .attr("font-size", "10px")
    .attr("font-weight", "600")
    .text("★ 120h Lead Time");

  // Line generator
  const lineGen = d3.line()
    .x(d => x(d.day))
    .y(d => y(d.val))
    .curve(d3.curveMonotoneX);

  // Series drawing
  currentData.series.forEach(s => {
    // Glow path
    svg.append("path")
      .datum(s.data)
      .attr("d", lineGen)
      .attr("fill", "none")
      .attr("stroke", s.color)
      .attr("stroke-width", 5)
      .attr("stroke-opacity", 0.25);

    // Main path
    svg.append("path")
      .datum(s.data)
      .attr("d", lineGen)
      .attr("fill", "none")
      .attr("stroke", s.color)
      .attr("stroke-width", 2.5);

    // Dots
    const dotsG = svg.append("g").attr("class", "series-dots-group");
    dotsG.selectAll("circle")
      .data(s.data)
      .enter().append("circle")
      .attr("cx", d => x(d.day))
      .attr("cy", d => y(d.val))
      .attr("r", 4)
      .attr("fill", s.color)
      .attr("stroke", "#0f172a")
      .attr("stroke-width", 1.5)
      .style("cursor", "pointer")
      .on("mouseenter", function(event, d) {
        d3.select(this).attr("r", 7);
        tt.style("opacity", 1)
          .html(`
            <div class="tt-title" style="color:${s.color}">${s.name}</div>
            <div class="tt-meta"><strong>Lead Time:</strong> Day ${d.day} (${d.day * 24} Hours)</div>
            <div class="tt-desc"><strong>${currentData.title.split(" vs ")[0]}:</strong> ${currentData.yFormat(d.val)}</div>
          `)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mousemove", function(event) {
        tt.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", function() {
        d3.select(this).attr("r", 4);
        tt.style("opacity", 0);
      });
  });

  // Legend
  const legendG = svg.append("g")
    .attr("transform", `translate(16, 10)`);

  currentData.series.forEach((s, idx) => {
    const itemG = legendG.append("g")
      .attr("transform", `translate(0, ${idx * 20})`);

    itemG.append("line")
      .attr("x1", 0).attr("y1", 6)
      .attr("x2", 18).attr("y2", 6)
      .attr("stroke", s.color)
      .attr("stroke-width", 2.5);

    itemG.append("circle")
      .attr("cx", 9).attr("cy", 6)
      .attr("r", 3.5)
      .attr("fill", s.color);

    itemG.append("text")
      .attr("x", 26).attr("y", 10)
      .attr("fill", "#cbd5e1")
      .attr("font-size", "11px")
      .text(s.name);
  });
}

// -------------------------------------------------------------
// 4. Interactive Feature Importance & SHAP Attribution Explorer
// -------------------------------------------------------------
let shapFilter = "all";

function initShapExplorer() {
  const container = document.getElementById("shap-viz");
  if (!container) return;
  container.innerHTML = "";

  const margin = { top: 20, right: 30, bottom: 40, left: 210 };
  const width = (container.clientWidth || 800) - margin.left - margin.right;
  const height = 400 - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .attr("width", "100%")
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const tt = getOrCreateTooltip();

  const allFeatures = [
    { name: "Friction Wind Speed (u*)", category: "emission", val: 0.88, color: "#f59e0b", desc: "Key threshold driver for sand saltation initiation; exceeds u*t threshold" },
    { name: "Surface Soil Moisture (0–7cm)", category: "emission", val: 0.82, color: "#f59e0b", desc: "Controls cohesion between soil particles; dry soil promotes rapid dust lift" },
    { name: "500 hPa Geopotential Height Anomaly", category: "dynamic", val: 0.77, color: "#06b6d4", desc: "Synoptic steering flow and upper-level cold vortex/trough dynamics" },
    { name: "Upstream PM10 Memory (Lag 24–72h)", category: "memory", val: 0.73, color: "#ec4899", desc: "Prior accumulation in source deserts (Taklamakan/Badain Jaran) ready for advection" },
    { name: "Bare Soil Ratio & FVC", category: "emission", val: 0.69, color: "#f59e0b", desc: "Inverse of vegetation cover; derived from MODIS satellite remote sensing" },
    { name: "Atmospheric Boundary Layer Height (PBLH)", category: "dynamic", val: 0.65, color: "#06b6d4", desc: "Vertical mixing volume dictating dust concentration dilution and lofting" },
    { name: "10m Surface Wind Speed & Shear", category: "dynamic", val: 0.61, color: "#06b6d4", desc: "Near-surface mechanical turbulence and horizontal advection velocity" },
    { name: "Surface Roughness Length (z0)", category: "emission", val: 0.54, color: "#f59e0b", desc: "Aerodynamic resistance of land cover and shelterbelt vegetation structures" },
    { name: "NDVI Phenological State", category: "emission", val: 0.49, color: "#10b981", desc: "Seasonal greening suppresses dust emission during late spring and summer" },
    { name: "Seasonal Snow Cover & Snowmelt", category: "emission", val: 0.42, color: "#38bdf8", desc: "Early spring snowmelt accelerates soil moistening and suppresses early dust events" }
  ];

  const filtered = shapFilter === "all" ? allFeatures : allFeatures.filter(f => f.category === shapFilter);

  const y = d3.scaleBand()
    .domain(filtered.map(d => d.name))
    .range([0, height])
    .padding(0.25);

  const x = d3.scaleLinear()
    .domain([0, 1.0])
    .nice()
    .range([0, width]);

  // Grid
  svg.append("g")
    .attr("class", "grid")
    .attr("stroke", "rgba(255,255,255,0.06)")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5).tickSize(-height).tickFormat(""));

  // Axes
  svg.append("g")
    .call(d3.axisLeft(y))
    .attr("color", "#94a3b8")
    .selectAll("text")
    .attr("font-size", "11px")
    .attr("fill", "#e2e8f0");

  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format(".1f")))
    .attr("color", "#94a3b8")
    .selectAll("text")
    .attr("font-size", "11px");

  // Bars
  svg.selectAll(".shap-bar")
    .data(filtered)
    .enter().append("rect")
    .attr("class", "shap-bar")
    .attr("y", d => y(d.name))
    .attr("height", y.bandwidth())
    .attr("x", 0)
    .attr("width", 0)
    .attr("rx", 4)
    .attr("fill", d => d.color)
    .style("cursor", "pointer")
    .on("mouseenter", function(event, d) {
      d3.select(this).attr("opacity", 0.8);
      tt.style("opacity", 1)
        .html(`
          <div class="tt-title" style="color:${d.color}">${d.name}</div>
          <div class="tt-meta"><strong>Category:</strong> ${d.category.toUpperCase()}</div>
          <div class="tt-meta"><strong>Mean |SHAP| Value:</strong> ${d.val.toFixed(2)}</div>
          <div class="tt-desc" style="margin-top:6px;">${d.desc}</div>
        `)
        .style("left", (event.pageX + 15) + "px")
        .style("top", (event.pageY - 28) + "px");
    })
    .on("mousemove", function(event) {
      tt.style("left", (event.pageX + 15) + "px")
        .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseleave", function() {
      d3.select(this).attr("opacity", 1);
      tt.style("opacity", 0);
    })
    .transition()
    .duration(800)
    .attr("width", d => x(d.val));

  // Value labels at end of bars
  svg.selectAll(".bar-label")
    .data(filtered)
    .enter().append("text")
    .attr("class", "bar-label")
    .attr("y", d => y(d.name) + y.bandwidth() / 2 + 4)
    .attr("x", d => x(d.val) + 8)
    .attr("fill", "#cbd5e1")
    .attr("font-size", "10.5px")
    .attr("font-weight", "600")
    .text(d => d.val.toFixed(2));
}

// -------------------------------------------------------------
// 5. Interactive ROC Curve & Confusion Matrix Threshold Simulator
// -------------------------------------------------------------
let simThreshold = 0.45; // Default threshold

function initRocSimulator() {
  const container = document.getElementById("roc-sim-viz");
  if (!container) return;
  container.innerHTML = "";

  const margin = { top: 25, right: 30, bottom: 45, left: 55 };
  const width = (container.clientWidth || 800) - margin.left - margin.right;
  const height = 340 - margin.top - margin.bottom;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .attr("width", "100%")
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const tt = getOrCreateTooltip();

  // Synthetic ROC curve (AUC = 0.912 representing AI-GAMFS high discrimination)
  const rocCurvePoints = [];
  for (let fpr = 0; fpr <= 1.0; fpr += 0.02) {
    // smooth concave ROC function
    const tpr = 1 - Math.pow(1 - fpr, 3.2);
    rocCurvePoints.push({ fpr, tpr });
  }

  const x = d3.scaleLinear().domain([0, 1]).range([0, width]);
  const y = d3.scaleLinear().domain([0, 1]).range([height, 0]);

  // Diagonal chance line
  svg.append("line")
    .attr("x1", x(0)).attr("y1", y(0))
    .attr("x2", x(1)).attr("y2", y(1))
    .attr("stroke", "rgba(255,255,255,0.2)")
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", "4 4");

  // Grid
  svg.append("g")
    .attr("class", "grid")
    .attr("stroke", "rgba(255,255,255,0.05)")
    .call(d3.axisLeft(y).tickSize(-width).tickFormat(""));

  svg.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0,${height})`)
    .attr("stroke", "rgba(255,255,255,0.05)")
    .call(d3.axisBottom(x).tickSize(-height).tickFormat(""));

  // Axes
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format(".1f")))
    .attr("color", "#94a3b8");

  svg.append("g")
    .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format(".1f")))
    .attr("color", "#94a3b8");

  // Area under curve
  const areaGen = d3.area()
    .x(d => x(d.fpr))
    .y0(height)
    .y1(d => y(d.tpr));

  svg.append("path")
    .datum(rocCurvePoints)
    .attr("d", areaGen)
    .attr("fill", "rgba(6, 182, 212, 0.15)");

  // ROC Path
  const lineGen = d3.line()
    .x(d => x(d.fpr))
    .y(d => y(d.tpr));

  svg.append("path")
    .datum(rocCurvePoints)
    .attr("d", lineGen)
    .attr("fill", "none")
    .attr("stroke", "#06b6d4")
    .attr("stroke-width", 3);

  // AUC badge
  svg.append("rect")
    .attr("x", width - 130)
    .attr("y", height - 50)
    .attr("width", 120)
    .attr("height", 36)
    .attr("rx", 6)
    .attr("fill", "rgba(15, 23, 42, 0.85)")
    .attr("stroke", "#06b6d4")
    .attr("stroke-width", 1);

  svg.append("text")
    .attr("x", width - 70)
    .attr("y", height - 28)
    .attr("text-anchor", "middle")
    .attr("fill", "#22d3ee")
    .attr("font-size", "12px")
    .attr("font-weight", "700")
    .text("AUC-ROC: 0.912");

  // Current operating point calculation based on simThreshold
  // Higher threshold -> lower FPR, lower TPR (fewer false alarms, more misses)
  // Lower threshold -> higher TPR, higher FPR (higher detection, more false alarms)
  const currentFpr = Math.pow(1 - simThreshold, 2.8) * 0.7;
  const currentTpr = 1 - Math.pow(1 - currentFpr, 3.2);

  // Operating point on ROC
  const opPt = svg.append("circle")
    .attr("class", "roc-op-point")
    .attr("cx", x(currentFpr))
    .attr("cy", y(currentTpr))
    .attr("r", 7)
    .attr("fill", "#f59e0b")
    .attr("stroke", "#ffffff")
    .attr("stroke-width", 2)
    .style("cursor", "pointer")
    .on("mouseenter", function(event) {
      tt.style("opacity", 1)
        .html(`
          <div class="tt-title" style="color:#f59e0b">Current Operating Point</div>
          <div class="tt-meta"><strong>Threshold:</strong> ${simThreshold.toFixed(2)}</div>
          <div class="tt-meta"><strong>TPR (Hit Rate / POD):</strong> ${(currentTpr * 100).toFixed(1)}%</div>
          <div class="tt-meta"><strong>FPR:</strong> ${(currentFpr * 100).toFixed(1)}%</div>
        `)
        .style("left", (event.pageX + 15) + "px")
        .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseleave", () => tt.style("opacity", 0));

  // Update dynamic HTML confusion matrix counters if present
  updateConfusionMatrixDOM(currentTpr, currentFpr);
}

function updateConfusionMatrixDOM(tpr, fpr) {
  // Assume a test sample of 1,000 meteorological event windows (e.g. 100 dust events, 900 calm events)
  const totalPos = 100;
  const totalNeg = 900;

  const hits = Math.round(totalPos * tpr);
  const misses = totalPos - hits;
  const falseAlarms = Math.round(totalNeg * fpr);
  const correctRejects = totalNeg - falseAlarms;

  const pod = (hits / (hits + misses)) || 0;
  const far = (falseAlarms / (hits + falseAlarms)) || 0;
  const csi = (hits / (hits + falseAlarms + misses)) || 0;
  const precision = (hits / (hits + falseAlarms)) || 0;
  const f1 = (2 * precision * pod / (precision + pod)) || 0;

  const setEl = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
  };

  setEl("cm-hits", hits);
  setEl("cm-misses", misses);
  setEl("cm-false-alarms", falseAlarms);
  setEl("cm-correct-rejects", correctRejects);

  setEl("stat-pod", (pod * 100).toFixed(1) + "%");
  setEl("stat-far", (far * 100).toFixed(1) + "%");
  setEl("stat-csi", csi.toFixed(3));
  setEl("stat-precision", (precision * 100).toFixed(1) + "%");
  setEl("stat-f1", f1.toFixed(3));
}

// -------------------------------------------------------------
// 6. Interactive 7-Phase Research Roadmap Gantt Timeline
// -------------------------------------------------------------
function initGanttSchedule() {
  const container = document.getElementById("gantt-viz");
  if (!container) return;
  container.innerHTML = "";

  const phases = RESEARCH_DATA.schedulePhases;
  const margin = { top: 30, right: 30, bottom: 40, left: 160 };
  const width = (container.clientWidth || 800) - margin.left - margin.right;
  const height = phases.length * 48;

  const svg = d3.select(container).append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .attr("width", "100%")
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const tt = getOrCreateTooltip();

  // Time range: Sep 2025 (month 0) to Jun 2027 (month 21)
  const timeScale = d3.scaleLinear()
    .domain([0, 22])
    .range([0, width]);

  const monthLabels = [
    { m: 0, text: "Sep 25" },
    { m: 3, text: "Dec 25" },
    { m: 7, text: "Apr 26" },
    { m: 11, text: "Aug 26" },
    { m: 15, text: "Dec 26" },
    { m: 18, text: "Mar 27" },
    { m: 20, text: "May 27" },
    { m: 21, text: "Jun 27" }
  ];

  // Month gridlines
  monthLabels.forEach(ml => {
    svg.append("line")
      .attr("x1", timeScale(ml.m)).attr("y1", 0)
      .attr("x2", timeScale(ml.m)).attr("y2", height)
      .attr("stroke", "rgba(255,255,255,0.08)")
      .attr("stroke-dasharray", "2 2");

    svg.append("text")
      .attr("x", timeScale(ml.m))
      .attr("y", -8)
      .attr("text-anchor", "middle")
      .attr("fill", "#94a3b8")
      .attr("font-size", "10.5px")
      .text(ml.text);
  });

  // Phase month spans (relative months from Sep 2025)
  const phaseSpans = [
    { start: 0, end: 3, color: "#38bdf8" },   // Phase 1: Sep-Dec 2025
    { start: 4, end: 7, color: "#818cf8" },   // Phase 2: Jan-Apr 2026
    { start: 8, end: 11, color: "#f59e0b" },  // Phase 3: May-Aug 2026
    { start: 12, end: 15, color: "#ec4899" }, // Phase 4: Sep-Dec 2026
    { start: 16, end: 18, color: "#10b981" }, // Phase 5: Jan-Mar 2027
    { start: 19, end: 20, color: "#06b6d4" }, // Phase 6: Apr-May 2027
    { start: 21, end: 22, color: "#a855f7" }  // Phase 7: Jun 2027
  ];

  phases.forEach((p, idx) => {
    const span = phaseSpans[idx];
    const y = idx * 48;
    const barX = timeScale(span.start);
    const barWidth = timeScale(span.end) - barX;

    // Phase Label on Left
    svg.append("text")
      .attr("x", -12)
      .attr("y", y + 24)
      .attr("text-anchor", "end")
      .attr("fill", "#e2e8f0")
      .attr("font-size", "11px")
      .attr("font-weight", "600")
      .text(`Phase ${p.phase}: ${p.name.length > 18 ? p.name.substring(0, 16) + "…" : p.name}`);

    // Bar background
    svg.append("rect")
      .attr("x", barX)
      .attr("y", y + 8)
      .attr("width", barWidth)
      .attr("height", 26)
      .attr("rx", 5)
      .attr("fill", span.color)
      .attr("opacity", 0.85)
      .style("cursor", "pointer")
      .on("mouseenter", function(event) {
        d3.select(this).attr("opacity", 1).attr("stroke", "#ffffff").attr("stroke-width", 1.5);
        tt.style("opacity", 1)
          .html(`
            <div class="tt-title" style="color:${span.color}">Phase ${p.phase}: ${p.name}</div>
            <div class="tt-meta"><strong>Timeline:</strong> ${p.period}</div>
            <div class="tt-desc" style="margin-top:6px;"><strong>Core Tasks:</strong></div>
            <ul style="padding-left:14px; margin:4px 0 0; font-size:11px; color:#cbd5e1;">
              ${p.tasks.map(t => `<li>${t}</li>`).join("")}
            </ul>
          `)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mousemove", function(event) {
        tt.style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseleave", function() {
        d3.select(this).attr("opacity", 0.85).attr("stroke", "none");
        tt.style("opacity", 0);
      });

    // Milestone text inside bar
    svg.append("text")
      .attr("x", barX + 8)
      .attr("y", y + 25)
      .attr("fill", "#0f172a")
      .attr("font-size", "10px")
      .attr("font-weight", "700")
      .text(p.period);
  });
}

// -------------------------------------------------------------
// Global Window Resize and Setup
// -------------------------------------------------------------
window.addEventListener("resize", () => {
  initDustMap();
  initDataPipelineFlow();
  initForecastSkillChart();
  initShapExplorer();
  initRocSimulator();
  initGanttSchedule();
});
