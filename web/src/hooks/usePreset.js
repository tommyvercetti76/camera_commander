import { useState } from 'react';
import { postClassicPreset, postSmartPreset } from '../api/client.js';

export function usePreset() {
  const [preset, setPreset]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);

  async function fetchClassic({ brand, camera, lens, genre, condition, mode }) {
    setLoading(true);
    setError(null);
    try {
      const data = await postClassicPreset({
        brand,
        cameraModel: camera.modelName,
        lensName:    lens.lensName,
        genre,
        condition,
        mode: mode || 'apprentice',
      });
      setPreset(data);
      return data;
    } catch (e) {
      setError(e.message);
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function fetchSmart({ interests, mode }) {
    setLoading(true);
    setError(null);
    try {
      const data = await postSmartPreset({ interests, mode: mode || 'apprentice' });
      setPreset(data);
      return data;
    } catch (e) {
      setError(e.message);
      return null;
    } finally {
      setLoading(false);
    }
  }

  function clear() { setPreset(null); setError(null); }

  return { preset, loading, error, fetchClassic, fetchSmart, clear };
}
