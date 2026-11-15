/**
 * Core Application Constants & Domain Configurations
 */

export const CORRIDOR_STATIONS = [
  { code: 'DH', name: 'Dunhuang (Gateway)', ustar_t: 0.35, isSource: true, basePm10: 1200, x: 220, y: 170 },
  { code: 'ZY', name: 'Zhangye (Hexi Funnel)', ustar_t: 0.36, isSource: false, basePm10: 950, x: 340, y: 200 },
  { code: 'MQ', name: 'Minqin (Oasis Edge)', ustar_t: 0.35, isSource: true, basePm10: 1400, x: 390, y: 190 },
  { code: 'WW', name: 'Wuwei (Terminal)', ustar_t: 0.37, isSource: false, basePm10: 820, x: 430, y: 220 },
  { code: 'LZ', name: 'Lanzhou (Basin)', ustar_t: 0.38, isSource: false, basePm10: 680, x: 470, y: 260 },
  { code: 'HH', name: 'Hohhot (Northern Path)', ustar_t: 0.36, isSource: false, basePm10: 750, x: 540, y: 150 },
  { code: 'BJ', name: 'Beijing (Metropolis)', ustar_t: 0.40, isSource: false, basePm10: 580, x: 670, y: 170 },
  { code: 'CD', name: 'Chengdu (120h Incursion)', ustar_t: 0.42, isSource: false, basePm10: 380, x: 480, y: 350 },
];

export const HAZARD_LEVELS = [
  { min: 1000, name: 'Level 5: Severe Sandstorm (特强沙尘暴)', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.2)' },
  { min: 500,  name: 'Level 4: Sandstorm (沙尘暴)', color: '#f97316', bg: 'rgba(249, 115, 22, 0.2)' },
  { min: 250,  name: 'Level 3: Blowing Sand (扬沙)', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.2)' },
  { min: 100,  name: 'Level 2: Suspended Dust (浮尘)', color: '#06b6d4', bg: 'rgba(6, 182, 212, 0.2)' },
  { min: 0,    name: 'Level 1: Normal Clean Air (正常)', color: '#10b981', bg: 'rgba(16, 185, 129, 0.2)' }
];

export const LEAD_TIMES_HOURS = [24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360];
