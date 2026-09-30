import React from 'react';

export default function Card({ children, style = {}, className = '', borderLeftColor = null }) {
  return (
    <div
      className={`glass-panel ${className}`}
      style={{
        padding: '1.25rem',
        borderLeft: borderLeftColor ? `3px solid ${borderLeftColor}` : undefined,
        ...style,
      }}
    >
      {children}
    </div>
  );
}
