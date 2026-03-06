#!/usr/bin/env python3
"""
migrate_v3_data.py

Applies all v3 data corrections documented in camera_v3.md.
Run from the repo root: python3 scripts/migrate_v3_data.py

Fixes applied:
  1. Canon camera maxFlashSync corrections (R5/R3/R5II → 1/250, R1 → 1/300)
  2. Sony camera corrections (ibisStops, maxFlashSync, weatherSealed)
  3. RF-S lenses: remove full-frame RF bodies from compatibleCameras
  4. EF lenses: add all RF full-frame bodies via adapter
  5. EF-S lenses: add RF-S crop bodies via adapter
  6. MACRO_EXTREME_CLOSEUP: aperture 22 → 11 (avoid diffraction)
  7. DANCE_FLOOR: shutterSpeed 1/250 → 1/320 + improved commonMistake
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMERAS_DIR = os.path.join(ROOT, 'api', 'src', 'data', 'cameras')
LENSES_DIR  = os.path.join(ROOT, 'api', 'src', 'data', 'lenses')
PRESETS_DIR = os.path.join(ROOT, 'api', 'src', 'data', 'presets')


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
    print(f"  ✓ saved {os.path.relpath(path, ROOT)}")


# ── 1. Canon camera corrections ──────────────────────────────────────────────
print("\n── Canon camera corrections ──")
canon_cameras = load(os.path.join(CAMERAS_DIR, 'canon.json'))

CANON_FLASH_CORRECTIONS = {
    'Canon EOS R5':          '1/250',
    'Canon EOS R5 Mark II':  '1/250',
    'Canon EOS R3':          '1/250',
    'Canon EOS R1':          '1/300',
}

CANON_DR_CORRECTIONS = {
    'Canon EOS R5':          14.5,
    'Canon EOS R5 Mark II':  15.0,
    'Canon EOS R6':          13.8,
    'Canon EOS R6 Mark II':  14.0,
    'Canon EOS R3':          13.8,
    'Canon EOS 5D Mark IV':  13.6,
    'Canon EOS 6D Mark II':  12.5,
}

for cam in canon_cameras['cameras']:
    name = cam['modelName']
    if name in CANON_FLASH_CORRECTIONS:
        old = cam.get('maxFlashSync')
        new = CANON_FLASH_CORRECTIONS[name]
        if old != new:
            cam['maxFlashSync'] = new
            print(f"  {name}: maxFlashSync {old} → {new}")
    if name in CANON_DR_CORRECTIONS:
        old = cam.get('dynamicRange')
        new = CANON_DR_CORRECTIONS[name]
        if old != new:
            cam['dynamicRange'] = new
            print(f"  {name}: dynamicRange {old} → {new}")

save(os.path.join(CAMERAS_DIR, 'canon.json'), canon_cameras)


# ── 2. Sony camera corrections ────────────────────────────────────────────────
print("\n── Sony camera corrections ──")
sony_cameras = load(os.path.join(CAMERAS_DIR, 'sony.json'))

SONY_CORRECTIONS = {
    # name: {field: new_value}
    'Sony Alpha a6500':    {'maxFlashSync': '1/250'},
    'Sony Alpha a6600':    {'maxFlashSync': '1/250'},
    'Sony Alpha a6700':    {'maxFlashSync': '1/250'},
    'Sony Alpha a7C':      {'maxFlashSync': '1/250'},
    'Sony Alpha a7C II':   {'maxFlashSync': '1/250', 'weatherSealed': False},
    'Sony Alpha a7CR':     {'maxFlashSync': '1/250', 'weatherSealed': False},
    'Sony Alpha a9 III':   {'ibisStops': 8},
    'Sony Alpha a1':       {'ibisStops': 5.5},
    'Sony Alpha a7 IV':    {'ibisStops': 5.5, 'dynamicRange': 15.0},
    'Sony Alpha a7R III':  {'ibisStops': 5.5},
    'Sony Alpha a9 II':    {'ibisStops': 5.5},
    'Sony Alpha a7S III':  {'ibisStops': 5.5},
}

for cam in sony_cameras['cameras']:
    name = cam['modelName']
    if name in SONY_CORRECTIONS:
        for field, new_val in SONY_CORRECTIONS[name].items():
            old = cam.get(field)
            if old != new_val:
                cam[field] = new_val
                print(f"  {name}: {field} {old!r} → {new_val!r}")

save(os.path.join(CAMERAS_DIR, 'sony.json'), sony_cameras)


# ── 3 & 4. Canon lens compatibility fixes ────────────────────────────────────
print("\n── Canon lens compatibility fixes ──")
canon_lenses = load(os.path.join(LENSES_DIR, 'canon.json'))

# Full-frame RF bodies (EF adapter works on all of these)
RF_FF_BODIES = [
    'Canon EOS R', 'Canon EOS RP', 'Canon EOS Ra',
    'Canon EOS R5', 'Canon EOS R6', 'Canon EOS R3', 'Canon EOS R5 C',
    'Canon EOS R6 Mark II', 'Canon EOS R8', 'Canon EOS R1', 'Canon EOS R5 Mark II',
]

# RF-S crop bodies (EF-S via adapter works on these)
RF_S_BODIES = [
    'Canon EOS R7', 'Canon EOS R10', 'Canon EOS R50', 'Canon EOS R100',
]

for lens in canon_lenses['lenses']:
    name    = lens['lensName']
    mount   = lens['mountType']
    current = lens['compatibleCameras']

    if mount == 'RF-S':
        # Remove full-frame RF bodies — RF-S is APS-C only
        cleaned = [b for b in current if b not in RF_FF_BODIES]
        # Ensure all RF-S crop bodies are present
        for body in RF_S_BODIES:
            if body not in cleaned:
                cleaned.append(body)
        if cleaned != current:
            removed = [b for b in current if b not in cleaned]
            added   = [b for b in cleaned if b not in current]
            print(f"  [{mount}] {name[:55]}")
            if removed: print(f"    removed: {removed}")
            if added:   print(f"    added:   {added}")
            lens['compatibleCameras'] = cleaned

    elif mount == 'EF':
        # EF lenses work on all RF bodies via Canon Mount Adapter EF-EOS R
        added = []
        for body in RF_FF_BODIES:
            if body not in current:
                current.append(body)
                added.append(body)
        if added:
            print(f"  [EF] {name[:55]}")
            print(f"    added RF bodies: {added}")

    elif mount == 'EF-S':
        # EF-S lenses work on RF-S bodies via adapter (crop-to-crop)
        added = []
        for body in RF_S_BODIES:
            if body not in current:
                current.append(body)
                added.append(body)
        if added:
            print(f"  [EF-S] {name[:55]}")
            print(f"    added RF-S bodies: {added}")

save(os.path.join(LENSES_DIR, 'canon.json'), canon_lenses)


# ── 5. Preset: MACRO_EXTREME_CLOSEUP aperture fix ────────────────────────────
print("\n── Preset fix: MACRO_EXTREME_CLOSEUP ──")
macro = load(os.path.join(PRESETS_DIR, 'macro.json'))
cond = macro['conditions']['MACRO_EXTREME_CLOSEUP']
if cond['aperture'] != 11:
    print(f"  aperture: {cond['aperture']} → 11")
    cond['aperture'] = 11
    cond['proTip'] = (
        'Use focus stacking at f/11 across 15–30 exposures for maximum sharpness '
        'and depth. f/22 appears to offer more DOF but diffraction softening '
        'negates all fine detail on sensors above 20MP. Stack in Helicon Focus '
        'or Zerene Stacker.'
    )
    cond['commonMistake'] = (
        'Choosing f/22 for more depth of field at extreme magnification. '
        'Diffraction kicks in hard above f/11 on modern sensors — the resulting '
        'image is softer than f/11 despite the smaller aperture.'
    )
save(os.path.join(PRESETS_DIR, 'macro.json'), macro)


# ── 6. Preset: DANCE_FLOOR shutter fix ───────────────────────────────────────
print("\n── Preset fix: DANCE_FLOOR ──")
indoorlowlight = load(os.path.join(PRESETS_DIR, 'indoorlowlight.json'))
df = indoorlowlight['conditions']['DANCE_FLOOR']
if df['shutterSpeed'] != '1/320':
    print(f"  shutterSpeed: {df['shutterSpeed']} → 1/320")
    df['shutterSpeed'] = '1/320'
    df['commonMistake'] = (
        'Using 1/250s — fast arm movements and spinning dancers will show motion '
        'blur at that speed. Push to 1/400 and raise ISO if you still see blur.'
    )
save(os.path.join(PRESETS_DIR, 'indoorlowlight.json'), indoorlowlight)


print("\n✓ v3 data migration complete.")
