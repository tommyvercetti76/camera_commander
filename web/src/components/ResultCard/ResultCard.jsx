import { motion } from 'framer-motion';
import { Lightbulb, AlertTriangle, Tag } from 'lucide-react';
import styles from './ResultCard.module.css';

function Setting({ label, value }) {
  return (
    <div className={styles.setting}>
      <span className={styles.settingLabel}>{label}</span>
      <span className={`${styles.settingValue} mono`}>{value}</span>
    </div>
  );
}

function Badge({ children }) {
  return <span className={styles.badge}>{children}</span>;
}

export default function ResultCard({ preset }) {
  if (!preset) return null;

  return (
    <motion.div
      className={styles.card}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
    >
      {/* IBIS-adjusted shutter + flash warnings */}
      {(preset.shutterSpeedWithIBIS || (preset.warnings && preset.warnings.length > 0)) && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Gear Adjustments</h2>
          {preset.shutterSpeedWithIBIS && (
            <div className={styles.ibisBadge}>
              <span className={styles.settingLabel}>Stabilised shutter</span>
              <span className={`${styles.settingValue} mono`}>{preset.shutterSpeedWithIBIS}</span>
              {preset.ibisStopsApplied && (
                <span className={styles.ibisNote}>({preset.ibisStopsApplied} stop{preset.ibisStopsApplied !== 1 ? 's' : ''} IBIS/OIS)</span>
              )}
            </div>
          )}
          {Array.isArray(preset.warnings) && preset.warnings.map((w, i) => (
            <div key={i} className={`${styles.section} ${styles.warnSection}`} style={{ marginTop: 6 }}>
              <AlertTriangle size={14} color="var(--crimson)" />
              <p className={styles.body} style={{ margin: 0 }}>{w}</p>
            </div>
          ))}
        </section>
      )}

      {/* Camera Settings Grid */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Camera Settings</h2>
        <div className={styles.settingsGrid}>
          <Setting label="Mode"         value={preset.mode || '—'} />
          <Setting label="AF Mode"      value={preset.afMode || '—'} />
          <Setting label="AF Point"     value={preset.afPoint || '—'} />
          <Setting label="Metering"     value={preset.metering || '—'} />
          <Setting label="Drive Mode"   value={preset.driveMode || '—'} />
          <Setting label="Difficulty"   value={preset.difficulty || '—'} />
        </div>
      </section>

      {/* Flags */}
      {(preset.requiresTripod || preset.requiresTracking || preset.requiresNDFilter || preset.ibisBonus) && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Requirements & Bonuses</h2>
          <div className={styles.flagGrid}>
            {preset.requiresTripod   && <Badge>Tripod required</Badge>}
            {preset.requiresTracking && <Badge>Subject tracking</Badge>}
            {preset.requiresNDFilter && <Badge>ND filter needed</Badge>}
            {preset.ibisBonus        && <span className={`${styles.badge} ${styles.badgeGreen}`}>IBIS beneficial</span>}
          </div>
        </section>
      )}

      {/* Rationale */}
      {preset.rationale && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Why These Settings</h2>
          <p className={styles.body}>{preset.rationale}</p>
        </section>
      )}

      {/* Pro Tip */}
      {preset.proTip && (
        <section className={`${styles.section} ${styles.tipSection}`}>
          <Lightbulb size={16} color="var(--gold)" />
          <div>
            <h2 className={`${styles.sectionTitle} text-gold`}>Pro Tip</h2>
            <p className={styles.body}>{preset.proTip}</p>
          </div>
        </section>
      )}

      {/* Common Mistake */}
      {preset.commonMistake && (
        <section className={`${styles.section} ${styles.warnSection}`}>
          <AlertTriangle size={16} color="var(--crimson)" />
          <div>
            <h2 className={`${styles.sectionTitle} text-crimson`}>Common Mistake</h2>
            <p className={styles.body}>{preset.commonMistake}</p>
          </div>
        </section>
      )}

      {/* Tags */}
      {Array.isArray(preset.tags) && preset.tags.length > 0 && (
        <section className={styles.section}>
          <div className={styles.tagsRow}>
            <Tag size={13} color="var(--text-dim)" />
            {preset.tags.map(tag => (
              <span key={tag} className={styles.tag}>{tag}</span>
            ))}
          </div>
        </section>
      )}
    </motion.div>
  );
}
