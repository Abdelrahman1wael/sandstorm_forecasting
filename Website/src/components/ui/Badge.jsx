import React from 'react';

export default function Badge({ children, variant = 'default', style = {} }) {
  const variantStyles = {
    default: { background: 'rgba(255, 255, 255, 0.06)', color: '#cbd5e1' },
    primary: { background: 'rgba(6, 182, 212, 0.15)', color: '#22d3ee' },
    success: { background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' },
    warning: { background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24' },
    danger: { background: 'rgba(239, 68, 68, 0.15)', color: '#f87171' },
    purple: { background: 'rgba(168, 85, 247, 0.15)', color: '#d8b4fe' },
  };

  const selected = variantStyles[variant] || variantStyles.default;

  return (
    <span
      className="stat-badge"
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        fontSize: '0.72rem',
        padding: '0.2rem 0.55rem',
        borderRadius: '6px',
        fontWeight: 600,
        ...selected,
        ...style,
      }}
    >
      {children}
    </span>
  );
}
