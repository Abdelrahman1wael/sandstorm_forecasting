import React from 'react';
import { 
  Wind, 
  Layers, 
  BarChart3, 
  Activity, 
  Cpu, 
  Video, 
  BookOpen, 
  MapPin, 
  Printer 
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

export default function Navbar() {
  const { activeView, setActiveView } = useApp();

  const navItems = [
    { id: 'proposal', label: 'Proposal Chapters', icon: Layers },
    { id: 'simulations', label: 'Live Simulations', icon: BarChart3 },
    { id: 'dashboard', label: 'Operational Dashboard', icon: Activity },
    { id: 'ai-lab', label: 'AI Neural Lab', icon: Cpu },
    { id: 'video', label: 'Presentation Studio', icon: Video },
    { id: 'references', label: '61 Citations (BibTeX)', icon: BookOpen },
    { id: 'roadmap', label: 'SPSS/AMOS/GIS Roadmap', icon: MapPin },
  ];

  return (
    <header className="main-header" style={{ position: 'sticky', top: 0, zIndex: 1000, background: 'rgba(7, 11, 20, 0.88)', backdropFilter: 'blur(12px)', borderBottom: '1px solid var(--border-subtle)' }}>
      <div className="container nav-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.8rem 1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        
        {/* Brand */}
        <div className="nav-brand" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }} onClick={() => setActiveView('proposal')}>
          <div className="brand-logo" style={{ width: 40, height: 40, borderRadius: 10, background: 'linear-gradient(135deg, #f59e0b, #06b6d4)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 16px rgba(245, 158, 11, 0.35)' }}>
            <Wind size={22} color="#070b14" strokeWidth={2.5} />
          </div>
          <div className="brand-text">
            <span className="brand-title" style={{ fontSize: '1.15rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#f8fafc', display: 'block' }}>
              Dust<span style={{ color: '#38bdf8' }}>ML</span>
            </span>
            <span className="brand-subtitle" style={{ fontSize: '0.72rem', color: '#94a3b8', display: 'block' }}>
              USTB 北京科技大学 • Environmental Engineering
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-links" style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', overflowX: 'auto', maxWidth: '100%', padding: '0.2rem' }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id)}
                className={`nav-tab-pill ${isActive ? 'active' : ''}`}
                style={{ whiteSpace: 'nowrap' }}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Actions */}
        <div className="nav-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span className="stat-badge" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.35rem 0.65rem', borderRadius: 6, fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: 5 }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#34d399', display: 'inline-block' }}></span>
            AI-GAMFS 5km
          </span>
          <button 
            className="btn btn-secondary" 
            onClick={() => window.print()}
            style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '0.45rem 0.85rem', fontSize: '0.8rem' }}
          >
            <Printer size={15} />
            <span>Print PDF</span>
          </button>
        </div>

      </div>
    </header>
  );
}
