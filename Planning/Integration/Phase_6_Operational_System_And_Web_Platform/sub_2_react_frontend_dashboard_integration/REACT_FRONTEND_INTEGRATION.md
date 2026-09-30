# 💻 Phase 6 • Subfolder 2: React Frontend Dashboard Integration
### *Vite + React 19 Clean Architecture, Interactive Visualizations & Live Forecaster*
**Phase Horizon:** April 2027 – May 2027  
**Parent Phase:** Phase 6 (Operational System, Web Platform & Pre-Defense)

---

## 🎯 1. Operational Goal & Clean Frontend Architecture

Phase 6.2 completes the interactive web platform in `Website/`, designed for operational meteorologists, municipal decision-makers, and thesis defense presentations:

```
Website/src/
├── api/          # dustmlApi.js (FastAPI fetch client with defensive fallback)
├── components/   # Atomic UI (Button, Card, Badge) & Layout (Navbar, Footer)
├── context/      # AppContext.jsx (Active view switcher, dark-mode theme)
├── hooks/        # useForecaster.js (Reactive slider bindings to physics formulas)
├── pages/        # 7 High-Impact Pages:
│   ├── ProposalPage.jsx     (Chapters 1-6 proposal viewer)
│   ├── SimulationsPage.jsx  (6 interactive SVG simulation benchmarks)
│   ├── DashboardPage.jsx    (Live station forecaster with quantile envelopes)
│   ├── NeuralLabPage.jsx    (Interactive PINN saltation & loss curve emulator)
│   ├── VideoStudioPage.jsx  (10-scene academic video presentation player)
│   ├── ReferencesPage.jsx   (61-paper bibliographic catalog with BibTeX copy)
│   └── RoadmapPage.jsx      (12-week schedule & SPSS/AMOS/GIS matrix)
└── services/     # physicsService.js (Owen saltation and mass continuity checks)
```

---

## 🎨 2. Visual Standards & Zero-Tailwind Policy

Per project specifications, the frontend uses **Vanilla CSS** with tailored dark-mode HSL design tokens in `index.css`:
* Primary Accent: Cyan (`#06b6d4` / `#22d3ee`)
* Hazard Levels: CMA Red (`#ef4444`), Orange (`#f97316`), Yellow (`#eab308`), Blue (`#3b82f6`)
* Glassmorphism: `backdrop-filter: blur(12px)` with subtle border glow.

---

## 📋 3. Phase 6.2 Deliverables
* Fully functional React app building in $< 500\text{ ms}$ via `vite build` with zero runtime lint errors.
