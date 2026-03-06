#!/usr/bin/env python3
"""
migrate_preset_values.py

One-time migration: normalise all preset JSON files to use canonical
enum values expected by validate_presets.py and presets.test.js.

Mappings applied
─────────────────
mode
  "Aperture Priority"  → "Av"
  "Shutter Priority"   → "Tv"
  "Manual"             → "M"
  "Program"            → "P"

afMode
  "Single AF"          → "single"
  "Continuous AF"      → "continuous"
  "Manual Focus"       → "manual"

afPoint
  "Face/Eye Detection" → "tracking"
  "Face Detection"     → "tracking"
  "Eye Detection"      → "tracking"
  "Subject Tracking"   → "tracking"
  "Subject"            → "tracking"
  "Zone"               → "zone"
  "Center"             → "single"
  "Center Point"       → "single"
  "Wide Area"          → "wide"
  "N/A"                → "wide"

metering
  "Evaluative"         → "evaluative"
  "Spot"               → "spot"
  "Center-Weighted"    → "center-weighted"
  "Manual"             → "evaluative"   # manual exposure still uses a metering mode

driveMode
  "Single Shot"        → "single"
  "Continuous High"    → "continuous_high"
  "Continuous Low"     → "continuous_low"
  "Interval Timer"     → "interval_timer"
  "2s Timer"           → "self_timer_2s"
  "Video/Burst"        → "continuous_high"

difficulty
  "beginner"           → 1
  "intermediate"       → 2
  "advanced"           → 3
"""

import json
import os
import sys

PRESETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'api', 'src', 'data', 'presets'
)

MODE_MAP = {
    'Aperture Priority': 'Av',
    'Shutter Priority':  'Tv',
    'Manual':            'M',
    'Program':           'P',
}

AF_MODE_MAP = {
    'Single AF':    'single',
    'Continuous AF': 'continuous',
    'Manual Focus': 'manual',
}

AF_POINT_MAP = {
    'Face/Eye Detection': 'tracking',
    'Face Detection':     'tracking',
    'Eye Detection':      'tracking',
    'Subject Tracking':   'tracking',
    'Subject':            'tracking',
    'Zone':               'zone',
    'Center':             'single',
    'Center Point':       'single',
    'Wide Area':          'wide',
    'N/A':                'wide',
}

METERING_MAP = {
    'Evaluative':      'evaluative',
    'Spot':            'spot',
    'Center-Weighted': 'center-weighted',
    'Manual':          'evaluative',
}

DRIVE_MAP = {
    'Single Shot':    'single',
    'Continuous High': 'continuous_high',
    'Continuous Low':  'continuous_low',
    'Interval Timer':  'interval_timer',
    '2s Timer':        'self_timer_2s',
    'Video/Burst':     'continuous_high',
}

DIFFICULTY_MAP = {
    'beginner':     1,
    'intermediate': 2,
    'advanced':     3,
}


def migrate_preset(genre, cond_key, p):
    changed = []

    if 'mode' in p and p['mode'] in MODE_MAP:
        old = p['mode']; p['mode'] = MODE_MAP[old]; changed.append(f"mode: {old!r} → {p['mode']!r}")
    if 'afMode' in p and p['afMode'] in AF_MODE_MAP:
        old = p['afMode']; p['afMode'] = AF_MODE_MAP[old]; changed.append(f"afMode: {old!r} → {p['afMode']!r}")
    if 'afPoint' in p and p['afPoint'] in AF_POINT_MAP:
        old = p['afPoint']; p['afPoint'] = AF_POINT_MAP[old]; changed.append(f"afPoint: {old!r} → {p['afPoint']!r}")
    if 'metering' in p and p['metering'] in METERING_MAP:
        old = p['metering']; p['metering'] = METERING_MAP[old]; changed.append(f"metering: {old!r} → {p['metering']!r}")
    if 'driveMode' in p and p['driveMode'] in DRIVE_MAP:
        old = p['driveMode']; p['driveMode'] = DRIVE_MAP[old]; changed.append(f"driveMode: {old!r} → {p['driveMode']!r}")
    if 'difficulty' in p and p['difficulty'] in DIFFICULTY_MAP:
        old = p['difficulty']; p['difficulty'] = DIFFICULTY_MAP[old]; changed.append(f"difficulty: {old!r} → {p['difficulty']}")

    if changed:
        print(f"  [{genre}/{cond_key}] {', '.join(changed)}")

    return p


def main():
    json_files = sorted(f for f in os.listdir(PRESETS_DIR) if f.endswith('.json'))
    total = 0

    for fname in json_files:
        path = os.path.join(PRESETS_DIR, fname)
        with open(path) as fh:
            data = json.load(fh)

        genre = fname.replace('.json', '')
        print(f"\n── {genre} ──")
        if 'conditions' not in data:
            print("  (no conditions key — skipping)")
            continue

        for cond_key, preset in data['conditions'].items():
            migrate_preset(genre, cond_key, preset)
            total += 1

        with open(path, 'w') as fh:
            json.dump(data, fh, indent=2)
            fh.write('\n')

    print(f"\n✓ Migration complete — {total} presets processed across {len(json_files)} files.")


if __name__ == '__main__':
    main()
