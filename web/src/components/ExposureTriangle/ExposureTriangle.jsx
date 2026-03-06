import { motion } from 'framer-motion';
import styles from './ExposureTriangle.module.css';

const VERTICES = [
  { key: 'aperture',    label: 'Aperture',      x: 50,  y: 8,   unit: 'f/', color: 'var(--gold)' },
  { key: 'shutterSpeed', label: 'Shutter',       x: 5,   y: 88,  unit: '',   color: 'var(--teal)' },
  { key: 'iso',         label: 'ISO',            x: 92,  y: 88,  unit: '',   color: 'var(--crimson)' },
];

export default function ExposureTriangle({ iso, aperture, shutterSpeed }) {
  const values = { aperture, shutterSpeed, iso };

  return (
    <div className={styles.wrap}>
      <svg viewBox="0 0 200 140" className={styles.svg} aria-hidden="true">
        <motion.polygon
          points="100,16 10,128 190,128"
          fill="rgba(201,168,76,0.04)"
          stroke="rgba(201,168,76,0.25)"
          strokeWidth="1.5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        />
        {VERTICES.map((v, i) => (
          <g key={v.key}>
            <motion.line
              x1={v.x * 2}
              y1={v.y * 1.4}
              x2={100}
              y2={70}
              stroke={v.color}
              strokeWidth="0.8"
              strokeDasharray="3 3"
              opacity="0.4"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ delay: i * 0.15, duration: 0.6 }}
            />
            <motion.circle
              cx={v.x * 2}
              cy={v.y * 1.4}
              r="5"
              fill={v.color}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', delay: i * 0.15 + 0.3 }}
            />
          </g>
        ))}
      </svg>

      <div className={styles.labels}>
        {VERTICES.map(v => (
          <motion.div
            key={v.key}
            className={styles.labelItem}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <span className={styles.labelName} style={{ color: v.color }}>{v.label}</span>
            <span className={styles.labelValue}>
              {v.unit}{values[v.key]}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
