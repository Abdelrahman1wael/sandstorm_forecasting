import React from 'react';
import { useApp } from '../../context/AppContext';

export default function Footer() {
  const { setActiveView } = useApp();

  return (
    <footer style={{ background: '#050811', borderTop: '1px solid var(--border-subtle)', padding: '2.5rem 0', marginTop: 'auto' }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.5rem' }}>
        <div>
          <div style={{ fontSize: '1rem', fontWeight: 800, color: '#f8fafc', marginBottom: 4 }}>
            Dust<span style={{ color: '#38bdf8' }}>ML</span> Research Platform
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            北京科技大学 (University of Science and Technology Beijing) • School of Energy and Environmental Engineering
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1.25rem', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
          <span style={{ cursor: 'pointer' }} onClick={() => setActiveView('proposal')}>Proposal Chapters</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActiveView('simulations')}>D3 Simulations</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActiveView('dashboard')}>Dashboard</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActiveView('ai-lab')}>Neural Lab</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActiveView('roadmap')}>SPSS/AMOS/GIS</span>
        </div>

        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Master's Topic Selection (2025.9 Enrollment) • Clean Architecture v1.0
        </div>
      </div>
    </footer>
  );
}
