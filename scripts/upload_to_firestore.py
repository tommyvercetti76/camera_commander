#!/usr/bin/env python3
"""
upload_to_firestore.py

Syncs camera and lens JSON data from api/src/data/ to Firestore.
Run this after updating any camera or lens JSON files.

Usage:
    python scripts/upload_to_firestore.py

Requirements:
    pip install firebase-admin

Authentication:
    Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your
    service account JSON path. Do NOT put the SA file in this repo.

    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-sa.json

    OR: run this from a machine where Firebase CLI is authenticated.
"""

import json
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore

# ── PATHS (relative to this script) ──────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.dirname(SCRIPT_DIR)
DATA_DIR    = os.path.join(REPO_ROOT, 'api', 'src', 'data')
CAMERAS_DIR = os.path.join(DATA_DIR, 'cameras')
LENSES_DIR  = os.path.join(DATA_DIR, 'lenses')

BRANDS = ['canon', 'sony']
COLLECTION_NAME = 'Kameras'


def init_firebase():
    """Initialize Firebase. Uses GOOGLE_APPLICATION_CREDENTIALS env var."""
    if not firebase_admin._apps:
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if cred_path:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    return firestore.client()


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def upload_brand(db, brand):
    cameras_path = os.path.join(CAMERAS_DIR, f'{brand}.json')
    lenses_path  = os.path.join(LENSES_DIR,  f'{brand}.json')

    if not os.path.exists(cameras_path):
        print(f'[WARN] Missing camera file: {cameras_path}', file=sys.stderr)
        return
    if not os.path.exists(lenses_path):
        print(f'[WARN] Missing lens file: {lenses_path}', file=sys.stderr)
        return

    cameras_data = load_json(cameras_path)
    lenses_data  = load_json(lenses_path)

    doc_ref = db.collection(COLLECTION_NAME).document(brand.lower())
    doc_ref.set({
        'brand':   brand.lower(),
        'cameras': cameras_data.get('cameras', []),
        'lenses':  lenses_data.get('lenses', []),
    })
    print(f'[OK] Uploaded {brand}: '
          f'{len(cameras_data.get("cameras", []))} cameras, '
          f'{len(lenses_data.get("lenses", []))} lenses')


def main():
    print('Kamera Quest — Firestore Upload')
    print('=' * 40)

    db = init_firebase()

    errors = 0
    for brand in BRANDS:
        try:
            upload_brand(db, brand)
        except Exception as exc:
            print(f'[ERROR] {brand}: {exc}', file=sys.stderr)
            errors += 1

    print('=' * 40)
    if errors:
        print(f'Completed with {errors} error(s).', file=sys.stderr)
        sys.exit(1)
    else:
        print('All brands uploaded successfully.')


if __name__ == '__main__':
    main()
