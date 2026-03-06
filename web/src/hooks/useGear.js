import { useState, useEffect } from 'react';
import { getCameras, getCameraLenses } from '../api/client.js';

export function useGear() {
  const [brand, setBrand]         = useState('');
  const [cameras, setCameras]     = useState([]);
  const [camera, setCamera]       = useState(null);
  const [lenses, setLenses]       = useState([]);
  const [lens, setLens]           = useState(null);
  const [loadingCams, setLoadingCams] = useState(false);
  const [loadingLens, setLoadingLens] = useState(false);
  const [error, setError]         = useState(null);

  useEffect(() => {
    if (!brand) { setCameras([]); setCamera(null); setLenses([]); setLens(null); return; }
    setLoadingCams(true);
    setError(null);
    getCameras(brand)
      .then(d => { setCameras(d.cameras || []); setCamera(null); setLens(null); setLenses([]); })
      .catch(e => setError(e.message))
      .finally(() => setLoadingCams(false));
  }, [brand]);

  useEffect(() => {
    if (!brand || !camera) { setLenses([]); setLens(null); return; }
    const controller = new AbortController();
    setLoadingLens(true);
    getCameraLenses(brand, camera.modelName, controller.signal)
      .then(d => { setLenses(d.lenses || []); setLens(null); })
      .catch(e => { if (e.name !== 'AbortError' && e.message !== 'Request timed out. Check your connection.') setError(e.message); })
      .finally(() => { if (!controller.signal.aborted) setLoadingLens(false); });
    return () => controller.abort();
  }, [brand, camera]);

  return {
    brand, setBrand,
    cameras, camera, setCamera,
    lenses, lens, setLens,
    loading: loadingCams || loadingLens,
    error,
  };
}
