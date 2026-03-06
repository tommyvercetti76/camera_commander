const API_BASE = import.meta.env.VITE_API_BASE || '/api';
const TIMEOUT_MS = 10000;

async function request(path, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const url = `${API_BASE}${path}`;
  const { signal: callerSignal, headers: callerHeaders, ...rest } = options;
  try {
    const res = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...callerHeaders },
      signal: callerSignal ?? controller.signal,
      ...rest,
    });
    let data;
    try { data = await res.json(); }
    catch { throw new Error(`API error: ${res.status}`); }
    if (!res.ok) {
      const msg = data?.error?.message || data?.message || `HTTP ${res.status}`;
      throw new Error(msg);
    }
    return data;
  } catch (e) {
    if (e.name === 'AbortError') throw new Error('Request timed out. Check your connection.');
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

export function getCameras(brand) {
  return request(`/cameras/${brand}`);
}

export function getCameraLenses(brand, modelName, signal) {
  return request(`/cameras/${brand}/${encodeURIComponent(modelName)}/lenses`, signal ? { signal } : {});
}

export function getPresetMeta() {
  return request('/presets/meta');
}

export function postClassicPreset(payload) {
  return request('/presets/classic', { method: 'POST', body: JSON.stringify(payload) });
}

export function postSmartPreset(payload) {
  return request('/presets/smart', { method: 'POST', body: JSON.stringify(payload) });
}
