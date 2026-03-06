# Kamera Quest

> **The answer to: "What camera settings should I use?"**

Kamera Quest is a camera settings intelligence tool built for photographers at every level — from first-time shooters to working professionals. Pick your gear, your scene, and your skill level. Get expert settings instantly.

Built by [Kaayko](https://kaayko.com).

---

## What It Does

You select:
- **Camera body** (Canon or Sony)
- **Lens**
- **Skill level** — Apprentice · Enthusiast · Craftsperson · Professional
- **Genre** — Portrait, Landscape, Astro, Wildlife, Sports, Macro, Indoor / Low Light, Golden Hour, Street, Architecture, Event, Travel
- **Shooting condition** — e.g. "Backlit Golden Hour", "Blue Hour Cityscape", "Hand-held Low Light"

You get:
- Aperture, shutter speed, ISO
- Camera mode, AF mode, AF point, metering, drive mode
- IBIS / OIS-aware shutter adjustments
- Pro tips, common mistakes, rationale
- Shareable settings card

---

## Stack

| Layer | Tech |
|-------|------|
| API | Firebase Cloud Functions v2 · Express · Node 18 |
| Database | Cloud Firestore (`kaaykostore`) |
| Web | React 18 · Vite 5 · CSS Modules · Framer Motion |
| CLI | Python 3 · Rich |
| Infra | Firebase Hosting · GitHub Actions CI/CD |

---

## Project Structure

```
camera_commander/
├── api/                    Firebase Cloud Functions (Express API)
│   ├── src/
│   │   ├── data/           Camera, lens & preset JSON data
│   │   │   ├── cameras/    canon.json, sony.json
│   │   │   ├── lenses/     canon.json, sony.json
│   │   │   └── presets/    12 genre JSON files (247 conditions)
│   │   ├── engine/         EV calculator + preset resolution engine
│   │   ├── middleware/     CORS, rate limiting, Zod validation
│   │   └── routes/         cameras, lenses, presets, smart
│   └── package.json
├── web/                    React web app
│   ├── src/
│   │   ├── api/            API client (fetch + AbortController)
│   │   ├── components/     ExposureTriangle, ResultCard, GearSelector…
│   │   ├── hooks/          useGear, usePreset
│   │   └── pages/          Home, Shoot, Result
│   └── vite.config.js
├── cli/                    Python interactive CLI
│   └── kamera_quest_cli.py
├── scripts/                Data pipeline & validation tools
│   ├── run_acceptance.py   247-criteria automated test suite
│   ├── merge_lenses.py     Lens data migration (v1 → v2 schema)
│   └── validate_presets.py Preset integrity checker
├── dev.sh                  One-command local dev startup
└── firebase.json
```

---

## Local Development

### Prerequisites

- **Node.js 18+** — [nodejs.org](https://nodejs.org)
- **Python 3.9+** — [python.org](https://python.org)
- **Firebase CLI** — `npm install -g firebase-tools && firebase login`
- **Service account** — Place `kaaykostore-sa.json` in the project root (never committed)

### One-command startup

```bash
chmod +x dev.sh
./dev.sh
```

This will:
1. Check prerequisites
2. Install npm dependencies if missing
3. Kill any stale processes on ports 5001 / 5173
4. Start the Firebase Functions emulator (port 5001)
5. Start the Vite dev server (port 5173)

| Service | URL |
|---------|-----|
| Web app | http://localhost:5173 |
| API | http://localhost:5001/kaaykostore/us-central1/api |
| Emulator UI | http://localhost:4000 |

### Manual startup

```bash
# Terminal 1 — API
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/kaaykostore-sa.json"
firebase emulators:start --only functions --project kaaykostore

# Terminal 2 — Web
cd web && npm run dev
```

---

## API Reference

Base URL (production): `https://us-central1-kaaykostore.cloudfunctions.net/api`

### Cameras

```
GET  /cameras/:brand                         → camera list
GET  /cameras/:brand/:modelName              → single camera
GET  /cameras/:brand/:modelName/lenses       → compatible lenses
```

### Presets

```
GET  /presets/meta                           → conditions per genre
POST /presets/classic                        → resolve preset for gear + scene
POST /presets/smart                          → AI-style recommendations
```

**Classic preset request body:**
```json
{
  "brand": "canon",
  "cameraModel": "Canon EOS RP",
  "lensName": "Canon RF 50mm f/1.2L USM",
  "genre": "goldenhour",
  "condition": "GOLDEN_HOUR_PORTRAIT_CLOSEUP",
  "mode": "apprentice"
}
```

Valid `genre` values: `portrait` `landscape` `astro` `wildlife` `sports` `macro` `indoorlowlight` `goldenhour` `street` `architecture` `event` `travel`

Valid `mode` values: `apprentice` `enthusiast` `craftsperson` `professional`

---

## CLI

```bash
cd cli
pip install -r requirements.txt
python kamera_quest_cli.py
python kamera_quest_cli.py --json         # machine-readable output
python kamera_quest_cli.py --api http://localhost:5001/kaaykostore/us-central1/api
```

---

## Data

- **51 Canon cameras** + **51 Canon lenses** (EF, EF-S, RF mounts)
- **20 Sony cameras** + **50 Sony lenses** (E, FE mounts)
- **12 genres** · **247 shooting conditions** with full preset data
- All stored in Cloud Firestore `Kameras/{brand}` documents

To re-upload data after edits:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/kaaykostore-sa.json"
python kamera_firebase_upload.py
```

---

## Tests

```bash
# Automated acceptance suite (247 criteria)
python scripts/run_acceptance.py

# API unit tests
cd api && npm test
```

---

## Deployment

Merging to `main` triggers automatic deployment via GitHub Actions:
- Functions → Firebase Cloud Functions
- Web → Firebase Hosting

Manual deploy:
```bash
cd web && npm run build && cd ..
firebase deploy --project kaaykostore
```

---

## Environment Variables

**`web/.env`** (local dev — leave `VITE_API_BASE` blank to use Vite proxy):
```
VITE_API_BASE=
```

**Production** (`web/.env` is not committed — set via Firebase config or CI):
```
VITE_API_BASE=https://us-central1-kaaykostore.cloudfunctions.net/api
```

The `api/` directory intentionally has **no `.env` file** — the Firebase Functions emulator's parser is incompatible with comment-style env files and the middleware uses hardcoded defaults.

---

*Kamera Quest — Built by Kaayko. For photographers who don't want to miss the shot.*

