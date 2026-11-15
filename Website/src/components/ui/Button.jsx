import React from 'react';

export default function Button({ children, variant = 'primary', onClick, disabled = false, style = {}, className = '' }) {
  const baseClass = variant === 'primary' ? 'btn btn-primary' : 'btn btn-secondary';

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseClass} ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '6px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
        ...style,
      }}
    >
      {children}
    </button>
  );
}
