# Kamera Quest CLI

Interactive terminal tool for instant camera settings — built on the Kamera Quest API.

## Installation

```bash
cd cli
pip install -r requirements.txt
```

## Usage

```bash
# Interactive mode
python kamera_quest_cli.py

# Output raw JSON (scriptable)
python kamera_quest_cli.py --json

# Override API endpoint
python kamera_quest_cli.py --api http://localhost:5001/kaayko-api-dev/us-central1/api
```

## Configuration

| Variable          | Default                                                              | Description              |
|-------------------|----------------------------------------------------------------------|--------------------------|
| `KAMERA_API_BASE` | `https://us-central1-kaayko-api-dev.cloudfunctions.net/api`         | API base URL             |

Create a `.env` file in the `cli/` directory:

```
KAMERA_API_BASE=http://localhost:5001/kaayko-api-dev/us-central1/api
```

## Flows

### Classic Flow
Step through Brand → Camera → Lens → Genre → Condition to get a tailored preset with
an animated exposure triangle and full metadata (AF mode, metering, drive mode, pro tip,
common mistakes).

### Smart Modes
- **Apprentice** – Simplified output for newcomers
- **Enthusiast** – Intermediate detail level
- **Craftsperson** – Full professional breakdown

## Navigation

| Key | Action             |
|-----|--------------------|
| `0` | Back one step      |
| `M` | Jump to main menu  |
| `Q` | Quit               |
| `H` | Show in-app help   |
