import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Share2, RotateCcw } from 'lucide-react';
import ResultCard from '../components/ResultCard/ResultCard.jsx';
import ExposureTriangle from '../components/ExposureTriangle/ExposureTriangle.jsx';
import { generateShareCard } from '../utils/shareCard.js';
import styles from './Result.module.css';

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state;

  if (!state?.preset) {
    navigate('/');
    return null;
  }

  const { preset, gear, genre, condition } = state;

  async function handleShare() {
    try {
      const blob = await generateShareCard(preset);
      if (blob && navigator.share) {
        const file = new File([blob], 'kamera-quest.png', { type: 'image/png' });
        await navigator.share({ title: 'Kamera Quest Settings', files: [file] });
      } else if (blob) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'kamera-quest.png';
        a.click();
        URL.revokeObjectURL(url);
      }
    } catch (e) {
      console.error('Share failed', e);
    }
  }

  return (
    <div className={styles.page}>
      <motion.div
        className={styles.inner}
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className={styles.topBar}>
          <button className={styles.back} onClick={() => navigate('/shoot', { state: gear })} type="button">
            <ArrowLeft size={18} /> Back
          </button>
          <div className={styles.topActions}>
            <button className={styles.iconBtn} onClick={handleShare} type="button" aria-label="Share settings">
              <Share2 size={18} />
            </button>
            <button className={styles.iconBtn} onClick={() => navigate('/')} type="button" aria-label="Start over">
              <RotateCcw size={18} />
            </button>
          </div>
        </div>

        <header className={styles.header}>
          <p className={styles.crumb}>
            <span className="text-gold">{genre}</span>
            {' / '}
            <span className="text-teal">{preset.displayName || condition}</span>
          </p>
          <h1 className={`${styles.title} serif`}>Your Settings</h1>
          <p className={styles.gear}>
            {gear?.camera?.modelName} + {gear?.lens?.lensName}
          </p>
        </header>

        <ExposureTriangle
          iso={preset.ISO}
          aperture={preset.aperture}
          shutterSpeed={preset.shutterSpeed}
        />

        <ResultCard preset={preset} />
      </motion.div>
    </div>
  );
}
