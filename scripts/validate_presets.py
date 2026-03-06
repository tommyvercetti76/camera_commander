#!/usr/bin/env python3
"""
validate_presets.py

Validates all preset JSON files against the v2 schema.
Exits with code 1 if any validation fails (CI will catch this).

Usage:
    python scripts/validate_presets.py
"""

import json
import os
import sys

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT    = os.path.dirname(SCRIPT_DIR)
PRESETS_DIR  = os.path.join(REPO_ROOT, 'api', 'src', 'data', 'presets')

REQUIRED_GENRES = [
    'portrait', 'landscape', 'astro', 'wildlife', 'sports',
    'macro', 'indoorlowlight', 'goldenhour', 'street',
    'architecture', 'event', 'travel'
]

REQUIRED_FIELDS = [
    'displayName', 'ISO', 'aperture', 'shutterSpeed', 'mode',
    'afMode', 'afPoint', 'metering', 'driveMode',
    'requiresTripod', 'requiresTracking', 'requiresNDFilter',
    'ibisBonus', 'difficulty', 'rationale', 'proTip',
    'commonMistake', 'tags'
]

VALID_MODES     = {'Av', 'Tv', 'M', 'P'}
VALID_AF_MODES  = {'single', 'continuous', 'manual'}
VALID_AF_POINTS = {'single', 'zone', 'wide', 'tracking'}
VALID_METERING  = {'evaluative', 'spot', 'center-weighted'}
VALID_DRIVE     = {'single', 'continuous_low', 'continuous_high', 'interval_timer', 'self_timer_2s'}

errors = []
warnings = []


def err(genre, cond, msg):
    errors.append(f'[ERROR] {genre}/{cond}: {msg}')


def warn(genre, cond, msg):
    warnings.append(f'[WARN] {genre}/{cond}: {msg}')


def validate_preset(genre, cond_key, p):
    for field in REQUIRED_FIELDS:
        if field not in p:
            err(genre, cond_key, f'missing field: {field}')

    if 'mode' in p and p['mode'] not in VALID_MODES:
        err(genre, cond_key, f'invalid mode: {p["mode"]}')
    if 'afMode' in p and p['afMode'] not in VALID_AF_MODES:
        err(genre, cond_key, f'invalid afMode: {p["afMode"]}')
    if 'afPoint' in p and p['afPoint'] not in VALID_AF_POINTS:
        err(genre, cond_key, f'invalid afPoint: {p["afPoint"]}')
    if 'metering' in p and p['metering'] not in VALID_METERING:
        err(genre, cond_key, f'invalid metering: {p["metering"]}')
    if 'driveMode' in p and p['driveMode'] not in VALID_DRIVE:
        err(genre, cond_key, f'invalid driveMode: {p["driveMode"]}')
    if 'ISO' in p and not isinstance(p['ISO'], (int, float)):
        err(genre, cond_key, f'ISO must be a number, got {type(p["ISO"]).__name__}')
    if 'aperture' in p and not isinstance(p['aperture'], (int, float)):
        err(genre, cond_key, f'aperture must be a number, got {type(p["aperture"]).__name__}')
    if 'shutterSpeed' in p and not isinstance(p['shutterSpeed'], str):
        err(genre, cond_key, f'shutterSpeed must be a string')
    if 'difficulty' in p and p['difficulty'] not in (1, 2, 3):
        err(genre, cond_key, f'difficulty must be 1, 2, or 3')
    if 'tags' in p and not isinstance(p['tags'], list):
        err(genre, cond_key, f'tags must be a list')

    # Deep-sky tracking check
    if genre == 'astro' and cond_key == 'DEEP_SKY_OBJECTS':
        if not p.get('requiresTracking'):
            err(genre, cond_key, 'DEEP_SKY_OBJECTS must have requiresTracking=true')
        rationale = p.get('rationale', '')
        if 'tracking' not in rationale.lower():
            warn(genre, cond_key, 'rationale should mention tracking mount')


def main():
    print('Kamera Quest — Preset Validation')
    print('=' * 40)

    missing_genres = []
    for genre in REQUIRED_GENRES:
        path = os.path.join(PRESETS_DIR, f'{genre}.json')
        if not os.path.exists(path):
            missing_genres.append(genre)
            errors.append(f'[ERROR] Missing preset file: {genre}.json')
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            errors.append(f'[ERROR] {genre}.json: JSON parse error: {exc}')
            continue

        if 'conditions' not in data:
            errors.append(f'[ERROR] {genre}.json: missing "conditions" key')
            continue

        for cond_key, preset in data['conditions'].items():
            validate_preset(genre, cond_key, preset)

        print(f'  {genre}: {len(data["conditions"])} conditions checked')

    print('=' * 40)

    for w in warnings:
        print(w)
    for e in errors:
        print(e, file=sys.stderr)

    if errors:
        print(f'\nValidation FAILED: {len(errors)} error(s), {len(warnings)} warning(s).', file=sys.stderr)
        sys.exit(1)
    else:
        print(f'\nValidation PASSED. {len(warnings)} warning(s).')


if __name__ == '__main__':
    main()
