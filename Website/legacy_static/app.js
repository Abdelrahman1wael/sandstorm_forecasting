/**
 * Main Application Logic for Sand & Dust Storm Forecasting Research Portal
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Populate numerical stats cards
  populateStatsCards();

  // 2. Populate references table and category filters
  populateReferences();

  // 3. Initialize D3 Visualizations
  setTimeout(() => {
    initDustMap();
    initDataPipelineFlow();
    initForecastSkillChart();
    initShapExplorer();
    initRocSimulator();
    initGanttSchedule();
  }, 100);

  // 4. Setup Interactive Listeners
  setupEventListeners();
});

// -------------------------------------------------------------
// Populate Quick Numerical Highlights
// -------------------------------------------------------------
function populateStatsCards() {
  const container = document.getElementById("stats-cards-grid");
  if (!container) return;

  const colorClasses = ["amber", "cyan", "indigo", "emerald", "amber", "cyan", "indigo", "emerald"];

  container.innerHTML = RESEARCH_DATA.numericalHighlights.map((item, idx) => `
    <div class="stat-card glass-panel ${colorClasses[idx % colorClasses.length]}">
      <div class="stat-badge">${item.badge}</div>
      <div class="stat-value">${item.value}</div>
      <div class="stat-label">${item.label}</div>
      <div class="stat-subtext">${item.subtext}</div>
    </div>
  `).join("");
}

// -------------------------------------------------------------
// Populate References and Filter System
// -------------------------------------------------------------
let currentRefSearch = "";
let currentRefCategory = "All";

function populateReferences() {
  const tableBody = document.getElementById("ref-table-body");
  const catContainer = document.getElementById("ref-category-filters");
  if (!tableBody || !catContainer) return;

  // Extract unique categories
  const categories = ["All", ...new Set(RESEARCH_DATA.references.map(r => r.category))];

  // Render Category Filter Pills
  catContainer.innerHTML = categories.map(cat => `
    <button class="cat-pill ${cat === currentRefCategory ? 'active' : ''}" data-cat="${cat}">
      ${cat}
    </button>
  `).join("");

  // Attach pill click events
  catContainer.querySelectorAll(".cat-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      catContainer.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentRefCategory = pill.dataset.cat;
      filterReferences();
    });
  });

  filterReferences();
}

function filterReferences() {
  const tableBody = document.getElementById("ref-table-body");
  const counter = document.getElementById("ref-count-label");
  if (!tableBody) return;

  const query = currentRefSearch.toLowerCase().trim();

  const filtered = RESEARCH_DATA.references.filter(r => {
    const matchCat = currentRefCategory === "All" || r.category === currentRefCategory;
    const matchSearch = !query || 
      r.title.toLowerCase().includes(query) ||
      r.authors.toLowerCase().includes(query) ||
      r.journal.toLowerCase().includes(query) ||
      (r.notes && r.notes.toLowerCase().includes(query)) ||
      String(r.year).includes(query) ||
      String(r.id) === query;

    return matchCat && matchSearch;
  });

  if (counter) {
    counter.innerText = `Showing ${filtered.length} of ${RESEARCH_DATA.references.length} Citations`;
  }

  if (filtered.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="4" style="text-align:center; padding: 2rem; color: #94a3b8;">
          No matching citations found for "<strong>${currentRefSearch}</strong>" in category "${currentRefCategory}".
        </td>
      </tr>
    `;
    return;
  }

  tableBody.innerHTML = filtered.map(r => `
    <tr class="ref-row" data-id="${r.id}" style="cursor:pointer;">
      <td class="ref-num">[${r.id}]</td>
      <td>
        <div class="ref-title">${r.title}</div>
        <div class="ref-authors">${r.authors}</div>
      </td>
      <td>
        <div class="ref-journal">${r.journal} (${r.year})</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Vol: ${r.volume || 'N/A'}, pp. ${r.pages || 'N/A'}</div>
      </td>
      <td>
        <span class="cat-pill" style="font-size:0.7rem; pointer-events:none;">${r.category}</span>
        <button class="btn btn-secondary btn-sm" onclick="openRefModal(${r.id}); event.stopPropagation();" style="margin-top:6px; padding:2px 8px; font-size:0.75rem;">
          Details & BibTeX
        </button>
      </td>
    </tr>
  `).join("");

  // Attach row click listeners
  tableBody.querySelectorAll(".ref-row").forEach(row => {
    row.addEventListener("click", () => {
      openRefModal(Number(row.dataset.id));
    });
  });
}

// -------------------------------------------------------------
// Reference Details & BibTeX Modal
// -------------------------------------------------------------
window.openRefModal = function(refId) {
  const ref = RESEARCH_DATA.references.find(r => r.id === refId);
  if (!ref) return;

  const modal = document.getElementById("ref-modal");
  const modalContent = document.getElementById("modal-ref-content");
  if (!modal || !modalContent) return;

  const bibtex = `@article{ref_${ref.id}_${ref.year},
  author    = {${ref.authors.replace(/\bet al\b\.?/i, "and others")}},
  title     = {${ref.title}},
  journal   = {${ref.journal}},
  year      = {${ref.year}},
  volume    = {${ref.volume || ""}},
  pages     = {${ref.pages || ""}},
  doi       = {${ref.doi || ""}}
}`;

  modalContent.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
      <span class="stat-badge" style="background:rgba(6,182,212,0.15); color:#22d3ee;">Citation Reference [${ref.id}]</span>
      <span class="cat-pill" style="font-size:0.75rem;">${ref.category}</span>
    </div>
    
    <h3 style="font-size:1.25rem; color:#ffffff; margin-bottom:0.75rem;">${ref.title}</h3>
    <p style="color:#94a3b8; font-size:0.88rem; margin-bottom:0.5rem;"><strong>Authors:</strong> ${ref.authors}</p>
    <p style="color:#94a3b8; font-size:0.88rem; margin-bottom:0.5rem;"><strong>Publication:</strong> ${ref.journal} (${ref.year})</p>
    <p style="color:#94a3b8; font-size:0.88rem; margin-bottom:1rem;"><strong>Volume / Pages:</strong> ${ref.volume || 'N/A'}, pp. ${ref.pages || 'N/A'}</p>
    
    ${ref.doi ? `
      <div style="margin-bottom:1.25rem;">
        <strong>DOI Link:</strong> 
        <a href="https://doi.org/${ref.doi}" target="_blank" rel="noopener noreferrer" style="word-break:break-all;">
          https://doi.org/${ref.doi} ↗
        </a>
      </div>
    ` : ''}

    <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:0.85rem; margin-bottom:1.25rem;">
      <strong style="color:#cbd5e1; font-size:0.85rem;">Significance in Proposal:</strong>
      <p style="color:#94a3b8; font-size:0.82rem; margin-top:0.35rem; line-height:1.5;">${ref.notes || 'Core citation supporting methodology and literature survey.'}</p>
    </div>

    <div style="position:relative;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span style="font-size:0.8rem; font-weight:600; color:#cbd5e1;">BibTeX Citation:</span>
        <button class="btn btn-secondary btn-sm" id="btn-copy-bibtex" style="padding:2px 8px; font-size:0.75rem;">
          📋 Copy BibTeX
        </button>
      </div>
      <pre style="background:#090d16; border:1px solid rgba(255,255,255,0.1); border-radius:6px; padding:0.75rem; font-family:var(--font-mono); font-size:0.75rem; color:#67e8f9; overflow-x:auto;">${bibtex}</pre>
    </div>
  `;

  modal.classList.add("active");

  const copyBtn = document.getElementById("btn-copy-bibtex");
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(bibtex).then(() => {
        copyBtn.innerText = "✓ Copied!";
        setTimeout(() => { copyBtn.innerText = "📋 Copy BibTeX"; }, 2000);
      });
    });
  }
};

window.closeRefModal = function() {
  const modal = document.getElementById("ref-modal");
  if (modal) modal.classList.remove("active");
};

// -------------------------------------------------------------
// Event Listeners Setup
// -------------------------------------------------------------
function setupEventListeners() {
  // Modal overlay click close
  const modal = document.getElementById("ref-modal");
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeRefModal();
    });
  }

  // Reference live search input
  const searchInput = document.getElementById("ref-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentRefSearch = e.target.value;
      filterReferences();
    });
  }

  // Forecast skill chart metric buttons
  document.querySelectorAll(".skill-metric-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".skill-metric-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      forecastMetric = btn.dataset.metric;
      initForecastSkillChart();
    });
  });

  // SHAP feature filter buttons
  document.querySelectorAll(".shap-cat-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".shap-cat-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      shapFilter = btn.dataset.cat;
      initShapExplorer();
    });
  });

  // ROC Threshold slider
  const threshSlider = document.getElementById("threshold-slider");
  const threshValLabel = document.getElementById("threshold-val-label");
  if (threshSlider && threshValLabel) {
    threshSlider.addEventListener("input", (e) => {
      simThreshold = parseFloat(e.target.value);
      threshValLabel.innerText = simThreshold.toFixed(2);
      initRocSimulator();
    });
  }

  // General Tabs Switching
  document.querySelectorAll(".tab-nav").forEach(nav => {
    nav.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.dataset.tab;
        const parent = nav.closest(".tabs-wrapper") || document;

        nav.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        parent.querySelectorAll(".tab-pane").forEach(pane => {
          if (pane.id === targetId) {
            pane.classList.add("active");
          } else {
            pane.classList.remove("active");
          }
        });
      });
    });
  });
}
