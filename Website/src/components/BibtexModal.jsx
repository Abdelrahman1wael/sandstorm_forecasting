import React, { useState } from 'react';
import { X, Copy, Check, Code } from 'lucide-react';

export default function BibtexModal({ reference, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!reference) return null;

  const citeKey = reference.authors 
    ? `${reference.authors.split(',')[0].trim().replace(/\s+/g, '')}${reference.year || '2025'}`
    : `DustML${reference.year || '2025'}`;

  const bibtex = `@article{${citeKey},
  title = {${reference.title || 'Sand and Dust Storm Forecasting Research'}},
  author = {${reference.authors || 'DustML Research Team'}},
  journal = {${reference.journal || 'Environmental Science & Atmospheric Technology'}},
  year = {${reference.year || '2025'}}${reference.volume ? `,\n  volume = {${reference.volume}}` : ''}${reference.pages ? `,\n  pages = {${reference.pages}}` : ''}${reference.doi ? `,\n  doi = {${reference.doi}}` : ''}
}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(bibtex);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: 640 }}>
        
        <button className="modal-close-btn" onClick={onClose}>
          <X size={18} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: '1rem' }}>
          <Code size={20} color="var(--accent-cyan)" />
          <h3 style={{ fontSize: '1.2rem', color: '#f8fafc', fontWeight: 800 }}>
            BibTeX Citation Generator
          </h3>
        </div>

        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
          Standard LaTeX / BibTeX entry formatted for top-tier academic environmental and meteorology journals:
        </p>

        <div style={{ position: 'relative', marginBottom: '1.25rem' }}>
          <pre style={{ 
            background: 'rgba(5, 8, 17, 0.95)', 
            border: '1px solid var(--border-subtle)', 
            padding: '1.25rem', 
            borderRadius: 8, 
            fontFamily: 'var(--font-mono)', 
            fontSize: '0.82rem', 
            color: '#38bdf8', 
            overflowX: 'auto',
            lineHeight: 1.5
          }}>
            {bibtex}
          </pre>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button className="btn btn-secondary" onClick={onClose} style={{ padding: '0.5rem 1rem', fontSize: '0.82rem' }}>
            Close
          </button>
          <button 
            className="btn btn-primary" 
            onClick={handleCopy}
            style={{ padding: '0.5rem 1.25rem', fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: 6 }}
          >
            {copied ? <Check size={16} color="#34d399" /> : <Copy size={16} />}
            <span>{copied ? 'Copied to Clipboard!' : 'Copy BibTeX'}</span>
          </button>
        </div>

      </div>
    </div>
  );
}
