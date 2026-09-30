/**
 * DustML Backend API Client (FastAPI Connection with Mock Fallback)
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

export const dustmlApi = {
  /**
   * Health Check
   */
  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(1500) });
      if (!res.ok) throw new Error('API offline');
      return await res.json();
    } catch {
      return { status: 'mock_fallback', message: 'Local client simulation active' };
    }
  },

  /**
   * Query Station Forecast
   */
  async getStationPrediction(stationCode, params) {
    try {
      const res = await fetch(`${API_BASE_URL}/predict_station`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ station_code: stationCode, ...params }),
        signal: AbortSignal.timeout(2000)
      });
      if (!res.ok) throw new Error('API error');
      return await res.json();
    } catch {
      // Graceful fallback to client calculation
      return null;
    }
  }
};
