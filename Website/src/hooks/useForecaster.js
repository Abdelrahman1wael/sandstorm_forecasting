import { useState, useMemo } from 'react';
import { CORRIDOR_STATIONS, HAZARD_LEVELS } from '../utils/constants';
import { physicsService } from '../services/physicsService';

export function useForecaster(defaultCode = 'DH') {
  const [stationCode, setStationCode] = useState(defaultCode);
  const [windU10, setWindU10] = useState(14.5);
  const [ustar, setUstar] = useState(0.48);
  const [soilMoisture, setSoilMoisture] = useState(0.04);
  const [aod, setAod] = useState(0.65);

  const currentStation = useMemo(() => {
    return CORRIDOR_STATIONS.find(s => s.code === stationCode) || CORRIDOR_STATIONS[0];
  }, [stationCode]);

  const physics = useMemo(() => {
    return physicsService.calculateSaltation(ustar, currentStation.ustar_t, windU10);
  }, [ustar, currentStation, windU10]);

  const forecasts = useMemo(() => {
    const baseVal = physics.isSaltation
      ? currentStation.basePm10 * 1.45 + physics.fluxMg * 0.35
      : currentStation.basePm10 * 0.75;
    return physicsService.generateQuantiles(baseVal);
  }, [currentStation, physics]);

  const hazardLevel = useMemo(() => {
    const d1 = forecasts[0];
    return HAZARD_LEVELS.find(h => d1.p50 >= h.min) || HAZARD_LEVELS[HAZARD_LEVELS.length - 1];
  }, [forecasts]);

  return {
    stationCode,
    setStationCode,
    windU10,
    setWindU10,
    ustar,
    setUstar,
    soilMoisture,
    setSoilMoisture,
    aod,
    setAod,
    currentStation,
    physics,
    forecasts,
    hazardLevel
  };
}
