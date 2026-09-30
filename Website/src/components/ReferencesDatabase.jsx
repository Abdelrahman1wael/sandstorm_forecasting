import React, { useState, useMemo } from 'react';
import { RESEARCH_DATA } from '../data/researchData';
import { Search, BookOpen, ExternalLink, Code, Filter } from 'lucide-react';

export default function ReferencesDatabase({ onOpenBibtex }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const refs = RESEARCH_DATA.references || [];

  const categories = [
    { id: 'all', label: 'All References (61)' },
    { id: 'nwp', label: 'Physical NWP & Atmospheric Dust' },
    { id: 'ml', label: 'Classical ML & Statistical Methods' },
    { id: 'deep', label: 'Deep Spatiotemporal & AI Foundation' },
    { id: 's2s', label: 'Sub-Seasonal & Teleconnections' },
  ];

  const filteredRefs = useMemo(() => {
    return refs.filter(r => {
      const matchText = (r.title + ' ' + r.authors + ' ' + r.journal + ' ' + r.year)
        .toLowerCase()
        .includes(searchQuery.toLowerCase());

      const matchCat = selectedCategory === 'all' || 
        (selectedCategory === 'nwp' && (r.category?.includes('NWP') || r.category?.includes('Physical'))) ||
        (selectedCategory === 'ml' && (r.category?.includes('Machine') || r.category?.includes('Statistical'))) ||
        (selectedCategory === 'deep' && (r.category?.includes('Deep') || r.category?.includes('AI'))) ||
        (selectedCategory === 's2s' && (r.category?.includes('Seasonal') || r.category?.includes('Climate')));

      return matchText && matchCat;
    });
  }, [refs, searchQuery, selectedCategory]);

  return (
    <section className="container" style={{ padding: '2rem 0 3.5rem' }}>
      
      <div className="section-head" style={{ marginBottom: '2rem' }}>
        <span className="section-tag">Academic Literature Catalog</span>
        <h2 className="section-title">61-Reference Peer-Reviewed Bibliographic Database</h2>
        <p className="section-desc">
          Search, filter, and inspect all 61 academic literature sources supporting the USTB master's thesis proposal, complete with DOIs and instant BibTeX generation.
        </p>
      </div>

      {/* Search & Category Filter Toolbar */}
      <div className="glass-panel" style={{ padding: '1.25rem', marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        
        {/* Search Bar */}
        <div style={{ position: 'relative', width: '100%' }}>
          <Search size={18} color="#94a3b8" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)' }} />
          <input 
            type="text" 
            placeholder="Search by author, article title, journal, or publication year..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '0.75rem 1rem 0.75rem 2.75rem', 
              borderRadius: 8, 
              background: 'rgba(5, 8, 17, 0.8)', 
              border: '1px solid var(--border-subtle)', 
              color: '#f8fafc',
              fontSize: '0.9rem',
              outline: 'none'
            }}
          />
        </div>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {categories.map(c => (
            <button
              key={c.id}
              onClick={() => setSelectedCategory(c.id)}
              className={`btn ${selectedCategory === c.id ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.4rem 0.85rem', fontSize: '0.78rem' }}
            >
              {c.label}
            </button>
          ))}
        </div>

      </div>

      {/* Results Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', fontSize: '0.85rem', color: '#94a3b8' }}>
        <span>Showing <strong>{filteredRefs.length}</strong> matching academic citations</span>
      </div>

      {/* Reference Cards List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredRefs.map((r, idx) => (
          <div key={idx} className="glass-panel" style={{ padding: '1.25rem', borderLeft: '3px solid var(--accent-cyan)' }}>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', marginBottom: '0.4rem' }}>
              <h4 style={{ fontSize: '0.98rem', color: '#f8fafc', fontWeight: 700, lineHeight: 1.4 }}>
                [{r.id || idx + 1}] {r.title}
              </h4>
              <button 
                onClick={() => onOpenBibtex(r)}
                className="btn btn-secondary" 
                style={{ padding: '0.3rem 0.65rem', fontSize: '0.72rem', display: 'flex', alignItems: 'center', gap: 4, flexShrink: 0 }}
              >
                <Code size={13} /> BibTeX
              </button>
            </div>

            <div style={{ fontSize: '0.82rem', color: 'var(--accent-amber)', marginBottom: '0.35rem' }}>
              {r.authors} ({r.year})
            </div>

            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              <em>{r.journal}</em>
              {r.volume ? `, Vol. ${r.volume}` : ''}
              {r.pages ? `, pp. ${r.pages}` : ''}
            </div>

            {r.doi && (
              <a 
                href={r.doi.startsWith('http') ? r.doi : `https://doi.org/${r.doi}`} 
                target="_blank" 
                rel="noreferrer"
                style={{ fontSize: '0.75rem', color: '#38bdf8', display: 'inline-flex', alignItems: 'center', gap: 4, textDecoration: 'none' }}
              >
                <span>DOI: {r.doi}</span>
                <ExternalLink size={12} />
              </a>
            )}

          </div>
        ))}
      </div>

    </section>
  );
}
