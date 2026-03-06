import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ChevronDown } from 'lucide-react';
import { getPresetMeta } from '../api/client.js';
import { usePreset } from '../hooks/usePreset.js';
import styles from './Shoot.module.css';

const GENRE_LABELS = {
  portrait: 'Portrait', landscape: 'Landscape', astro: 'Astro',
  wildlife: 'Wildlife', sports: 'Sports', macro: 'Macro',
  indoorlowlight: 'Indoor / Low Light', goldenhour: 'Golden Hour',
  street: 'Street', architecture: 'Architecture',
  event: 'Event', travel: 'Travel',
};

export default function Shoot() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state;

  const [genre, setGenre] = useState('');
  const [meta, setMeta] = useState(null);
  const [condition, setCondition] = useState('');
  const { loading, error, fetchClassic } = usePreset();

  useEffect(() => {
    if (!state) { navigate('/'); return; }
    getPresetMeta().then(setMeta).catch(console.error);
  }, [state, navigate]);

  const conditions = (meta && genre) ? (meta[genre] || []) : [];

  async function handleGetSettings() {
    if (!genre || !condition) return;
    const result = await fetchClassic({
      brand: state.brand,
      camera: state.camera,
      lens: state.lens,
      genre,
      condition,
      mode: state.mode,
    });
    if (result) {
      navigate('/result', { state: { preset: result.preset ?? result, gear: state, genre, condition } });
    }
  }

  if (!state) return null;

  return (
    <div className={styles.page}>
      <motion.div
        className={styles.inner}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <button className={styles.back} onClick={() => navigate('/')} type="button">
          <ArrowLeft size={18} /> Back
        </button>

        <header className={styles.header}>
          <h1 className={`${styles.title} serif`}>What are you shooting?</h1>
          <p className={styles.sub}>
            <span className="text-gold">{state.camera?.modelName}</span>
            {' + '}
            <span className="text-teal">{state.lens?.lensName}</span>
          </p>
        </header>

        {/* Genre Grid */}
        <section>
          <p className={styles.sectionLabel}>Genre</p>
          <div className={styles.genreGrid}>
            {Object.entries(GENRE_LABELS).map(([key, label]) => (
              <button
                key={key}
                className={`${styles.genreBtn} ${genre === key ? styles.genreBtnActive : ''}`}
                onClick={() => { setGenre(key); setCondition(''); }}
                type="button"
              >
                {label}
              </button>
            ))}
          </div>
        </section>

        {/* Condition */}
        {genre && (
          <motion.section
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
          >
            <p className={styles.sectionLabel}>Shooting Condition</p>
            <div className={styles.selectWrap}>
              <select
                className={styles.select}
                value={condition}
                onChange={e => setCondition(e.target.value)}
              >
                <option value="">Choose a condition…</option>
                {conditions.map(c => (
                  <option key={c.key} value={c.key}>{c.displayName || c.key}</option>
                ))}
              </select>
              <ChevronDown size={16} className={styles.chevron} />
            </div>
          </motion.section>
        )}

        {error && <p className={styles.error}>{error}</p>}

        <button
          className={styles.cta}
          onClick={handleGetSettings}
          disabled={!genre || !condition || loading}
          type="button"
        >
          {loading ? 'Calculating…' : 'Get My Settings →'}
        </button>
      </motion.div>
    </div>
  );
}
