/**
 * Text and Number Formatters
 */

export function formatPM10(val) {
  if (val === undefined || val === null || isNaN(val)) return '0 μg/m³';
  return `${Math.round(val)} μg/m³`;
}

export function formatVelocity(val) {
  if (val === undefined || val === null || isNaN(val)) return '0.00 m/s';
  return `${Number(val).toFixed(2)} m/s`;
}

export function formatPercentage(val) {
  if (val === undefined || val === null || isNaN(val)) return '0.0%';
  return `${Number(val).toFixed(1)}%`;
}

export function formatLeadDay(hours) {
  const day = Math.round(hours / 24);
  return `Day ${day} (+${hours}h)`;
}
