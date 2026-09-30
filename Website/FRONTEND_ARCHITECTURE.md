# 🏗️ DustML React Frontend: Clean Code Architecture

This document describes the clean, enterprise-grade architecture implemented in the `Website/` React application, strictly adhering to the modern frontend clean code paradigm:

```
Website/ (Frontend Root)
├── node_modules/
├── public/
├── legacy_static/               # Archived original HTML/JS static files
├── index.html                   # HTML5 Entry with Inter & Outfit Fonts
├── package.json                 # Dependency Manifest (React 19, Vite, Lucide-React)
├── vite.config.js               # Fast Vite Bundler Configuration
│
└── src/
    ├── 🌐 api/                  # Backend Connection
    │   └── dustmlApi.js         # REST endpoints connection (FastAPI) with client fallback
    │
    ├── 📁 assets/               # Static Files
    │   └── (Logos, icons, media references)
    │
    ├── 🧩 components/           # Reusable Components
    │   ├── layout/              # Structural Layout Blocks
    │   │   ├── Navbar.jsx       # Header navigation with view tabs & status badge
    │   │   └── Footer.jsx       # Academic footer with links & institutional info
    │   │
    │   ├── ui/                  # Reusable Atomic UI Elements
    │   │   ├── Badge.jsx        # Colored status badges
    │   │   ├── Button.jsx       # Primary & secondary button variants
    │   │   ├── Card.jsx         # Glassmorphic panel wrapper
    │   │   └── Modal.jsx        # Popup backdrop & container
    │   │
    │   ├── Hero.jsx             # Hero presentation banner & numerical statistics
    │   ├── ProposalChapters.jsx # Interactive Chapters 1 to 6
    │   ├── SimulationsSuite.jsx # 6 Interactive D3 & SVG Simulation Engines
    │   ├── OperationalDashboard.jsx # Real-time forecast & PINN physics simulator
    │   ├── AiNeuralLab.jsx      # PINN friction & AI-GAMFS neural visualizer
    │   ├── VideoStudio.jsx      # Synchronized 10-scene academic presentation viewer
    │   ├── ReferencesDatabase.jsx # Searchable 61-paper bibliographic catalog
    │   ├── MethodologyRoadmap.jsx # 12-Week SPSS/AMOS/GIS & Decision Matrix
    │   └── BibtexModal.jsx      # Instant BibTeX citation copy modal
    │
    ├── 🧊 context/              # Global State Management
    │   └── AppContext.jsx       # Active view, selected station, BibTeX selection state
    │
    ├── 🪙 data/                 # Static Content & Literature
    │   ├── researchData.js      # Complete 61 references, metrics, formulas, chapters
    │   └── videoMetadata.json   # 10 presentation scenes, voiceovers, timestamps
    │
    ├── 🪝 hooks/                # Custom Logic & State Hooks
    │   └── useForecaster.js     # Reactive forecast calculations & hazard triggers
    │
    ├── 📰 pages/                # Application Pages
    │   ├── ProposalPage.jsx     # Master's topic selection chapters & executive overview
    │   ├── SimulationsPage.jsx  # Interactive meteorological & algorithmic engines
    │   ├── DashboardPage.jsx    # Real-time operational forecasting center
    │   ├── NeuralLabPage.jsx    # PINN and AI-GAMFS neural visualizer
    │   ├── VideoStudioPage.jsx  # Synchronized video presentation studio
    │   ├── ReferencesPage.jsx   # Searchable literature & BibTeX database
    │   └── RoadmapPage.jsx      # Tri-pillar SPSS/AMOS/GIS & crisis decision matrix
    │
    ├── ⚙️ services/             # Frontend Business & Physics Logic
    │   ├── physicsService.js    # Owen saltation flux, PINN mass residual, quantiles
    │   └── bibtexService.js     # Citation key parser & LaTeX formatting
    │
    ├── 🛠️ utils/                # Utility Functions
    │   ├── constants.js         # Station coordinates, threshold limits, colors
    │   └── formatters.js        # Velocity, PM10, percentage, and date string formatters
    │
    ├── App.jsx                  # Root Application Orchestrator
    ├── main.jsx                 # React 19 Entrypoint
    └── index.css                # Dark Glassmorphism Design System & HSL Tokens
```

---

## 🚀 Running the Clean React Application

To start the local development server:

```bash
cd Website
npm run dev
```

To build the optimized production bundle:

```bash
cd Website
npm run build
```

---

## 🌟 Key Architecture Benefits

1. **Separation of Concerns:** Business logic (physics formulas, saltation thresholds) is in `services/`, not tangled inside UI components.
2. **Global State Cleanliness:** Navigation and modals are managed centrally in `context/AppContext.jsx`.
3. **Reusable Atomic UI:** Shared cards, badges, and buttons in `components/ui/` eliminate code duplication.
4. **Backend Ready:** `api/dustmlApi.js` connects smoothly to the FastAPI server on port 8000, while operating with full synthetic simulations if the backend is offline.
5. **Ultra-Fast Performance:** Pure React reactive SVG graphics eliminate DOM reconciliation lag.
