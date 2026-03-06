import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Camera, ChevronDown } from 'lucide-react';
import { useGear } from '../hooks/useGear.js';
import styles from './Home.module.css';

const BRANDS = ['canon', 'sony'];

export default function Home() {
  const navigate = useNavigate();
  const { brand, setBrand, cameras, camera, setCamera, lenses, lens, setLens, loading, error } = useGear();
  const [mode, setMode] = useState('apprentice');

  const MODES = [
    { value: 'apprentice',   label: 'Apprentice',   desc: 'Learning the basics' },
    { value: 'enthusiast',   label: 'Enthusiast',   desc: 'Getting serious' },
    { value: 'craftsperson', label: 'Craftsperson', desc: 'Mastering technique' },
    { value: 'professional', label: 'Professional', desc: 'Client-level work' },
  ];

  function handleStart() {
    if (!brand || !camera || !lens) return;
    navigate('/shoot', { state: { brand, camera, lens, mode } });
  }

  return (
    <div className={styles.page}>
      <motion.header
        className={styles.hero}
        initial={{ opacity: 0, y: -24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className={styles.logoMark}>
          <Camera size={32} color="var(--gold)" />
        </div>
        <h1 className={`${styles.title} serif`}>Kamera Quest</h1>
        <p className={styles.tagline}>Perfect settings for every shot, instantly.</p>
      </motion.header>

      <motion.main
        className={styles.form}
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        {/* Brand */}
        <div className={styles.field}>
          <label className={styles.label}>Camera Brand</label>
          <div className={styles.selectWrap}>
            <select
              className={styles.select}
              value={brand}
              onChange={e => setBrand(e.target.value)}
            >
              <option value="">Select brand…</option>
              {BRANDS.map(b => (
                <option key={b} value={b}>{b.charAt(0).toUpperCase() + b.slice(1)}</option>
              ))}
            </select>
            <ChevronDown size={16} className={styles.chevron} />
          </div>
        </div>

        {/* Camera Model */}
        <div className={styles.field}>
          <label className={styles.label}>Camera Body</label>
          <div className={styles.selectWrap}>
            <select
              className={styles.select}
              value={camera?.modelName || ''}
              onChange={e => setCamera(cameras.find(c => c.modelName === e.target.value) || null)}
              disabled={!brand || loading}
            >
              <option value="">
                {loading ? 'Loading…' : brand ? 'Select camera…' : 'Choose brand first'}
              </option>
              {cameras.map(c => (
                <option key={c.modelName} value={c.modelName}>{c.modelName}</option>
              ))}
            </select>
            <ChevronDown size={16} className={styles.chevron} />
          </div>
        </div>

        {/* Lens */}
        <div className={styles.field}>
          <label className={styles.label}>Lens</label>
          <div className={styles.selectWrap}>
            <select
              className={styles.select}
              value={lens?.lensName || ''}
              onChange={e => setLens(lenses.find(l => l.lensName === e.target.value) || null)}
              disabled={!camera || loading}
            >
              <option value="">
                {loading ? 'Loading…' : camera ? 'Select lens…' : 'Choose camera first'}
              </option>
              {lenses.map(l => (
                <option key={l.lensName} value={l.lensName}>{l.lensName}</option>
              ))}
            </select>
            <ChevronDown size={16} className={styles.chevron} />
          </div>
        </div>

        {/* Mode */}
        <div className={styles.field}>
          <label className={styles.label}>Skill Level</label>
          <div className={styles.modeGrid}>
            {MODES.map(m => (
              <button
                key={m.value}
                className={`${styles.modeBtn} ${mode === m.value ? styles.modeBtnActive : ''}`}
                onClick={() => setMode(m.value)}
                type="button"
              >
                <span className={styles.modeName}>{m.label}</span>
                <span className={styles.modeDesc}>{m.desc}</span>
              </button>
            ))}
          </div>
        </div>

        {error && <p className={styles.error}>{error}</p>}

        <button
          className={styles.cta}
          onClick={handleStart}
          disabled={!brand || !camera || !lens}
          type="button"
        >
          Choose Your Scene →
        </button>
      </motion.main>
    </div>
  );
}
