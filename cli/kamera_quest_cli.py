"""
kamera_quest_cli.py

Professional, aesthetic CLI for camera, lens, and preset selection.
Fully interactive with animated RGB exposure triangle.
Supports Classic Flow or three Smart Modes: Apprentice, Enthusiast, Craftsperson.

Dependencies:
  pip install requests python-dotenv
"""

import requests
import os
import sys
import time
import json
import argparse
from urllib.parse import quote

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ——— CONFIGURATION ———————————————————————————————————————————————————————
API_BASE = os.getenv(
    'KAMERA_API_BASE',
    'https://us-central1-kaaykostore.cloudfunctions.net/api'
).rstrip('/')

# ——— HELP TEXT ——————————————————————————————————————————————————————————
HELP_TEXT = """
═══════════════════════════════════════════════════════════════════════════════
  Kamera Quest CLI  |  HELP
═══════════════════════════════════════════════════════════════════════════════

NAVIGATION:
  [0] Back       – Step back one level
  [M] Main Menu  – Jump to main menu
  [Q] Quit       – Exit immediately
  [H] Help       – Show this help screen

MAIN MENU:
  1. Classic Flow    – Interactive brand / model / lens / genre / condition
  2. Apprentice Mode – Smart presets for newcomers (fundamentals only)
  3. Enthusiast Mode – Intermediate smart presets (more technical detail)
  4. Craftsperson    – Pro-level smart presets (full technical breakdown)

CLASSIC FLOW:
  1. Brand            – canon or sony
  2. Camera Model     – pulled live from the Kamera API
  3. Lens             – compatible lenses for the selected body
  4. Genre            – portrait, landscape, astro, wildlife, sports …
  5. Condition        – sub-condition within the genre
  6. Exposure Summary – ISO, aperture, shutter speed + pro tip

SMART MODE:
  • Enter interests as a comma-separated list (e.g. portrait, street)
  • Receive tailored preset recommendations for each interest

CLI FLAGS:
  --json       Output raw JSON (disables interactive UI)
  --api BASE   Override API base URL

ENV VARS:
  KAMERA_API_BASE  Override the default API endpoint

TROUBLESHOOTING:
  - Verify connectivity: curl $KAMERA_API_BASE/health
  - Check KAMERA_API_BASE is set correctly for your environment
  - Use --json to script against the CLI output
═══════════════════════════════════════════════════════════════════════════════
"""

GENRES = [
    'portrait', 'landscape', 'astro', 'wildlife',
    'sports', 'macro', 'indoorlowlight', 'goldenhour',
    'street', 'architecture', 'event', 'travel',
]

GENRE_LABELS = {
    'portrait': 'Portrait',
    'landscape': 'Landscape',
    'astro': 'Astro',
    'wildlife': 'Wildlife',
    'sports': 'Sports',
    'macro': 'Macro',
    'indoorlowlight': 'Indoor / Low Light',
    'goldenhour': 'Golden Hour',
    'street': 'Street',
    'architecture': 'Architecture',
    'event': 'Event',
    'travel': 'Travel',
}

SMART_MODES = {
    'Apprentice Mode':   'apprentice',
    'Enthusiast Mode':   'enthusiast',
    'Craftsperson Mode': 'craftsperson',
}

EMOJIS = {
    'Brand': '🏷️',
    'Camera': '📷',
    'Lens': '🔭',
    'Genre': '🎨',
    'Condition': '🌤️',
}

# ——— COLOURS ——————————————————————————————————————————————————————————————
def c(text, color):
    codes = {
        'green':   '\033[92m',
        'cyan':    '\033[96m',
        'yellow':  '\033[93m',
        'magenta': '\033[95m',
        'red':     '\033[91m',
        'white':   '\033[97m',
        'gold':    '\033[33m',
        'reset':   '\033[0m',
    }
    return f"{codes.get(color, '')}{text}{codes['reset']}"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ——— HTTP HELPERS ——————————————————————————————————————————————————————————
def _get(path):
    """GET {API_BASE}{path} → parsed JSON or raises RuntimeError."""
    url = f"{API_BASE}{path}"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to API at {API_BASE}. Check KAMERA_API_BASE.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"API error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        raise RuntimeError(str(e))


def _post(path, payload):
    """POST {API_BASE}{path} with JSON payload → parsed JSON or raises RuntimeError."""
    url = f"{API_BASE}{path}"
    try:
        r = requests.post(url, json=payload, timeout=8)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to API at {API_BASE}. Check KAMERA_API_BASE.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"API error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        raise RuntimeError(str(e))


# ——— FETCH FUNCTIONS ————————————————————————————————————————————————————
def fetch_cameras(brand):
    """Returns list of camera objects [{modelName, ibisStops, ...}]."""
    data = _get(f"/cameras/{brand}")
    return data.get('cameras', [])


def fetch_lenses(brand, model_name):
    """Returns list of lens objects [{lensName, hasOIS, oisStops, ...}]."""
    data = _get(f"/cameras/{brand}/{quote(model_name, safe='')}/lenses")
    return data.get('lenses', [])


def fetch_preset_meta():
    """Returns preset meta: {genres: {portrait: {displayName, conditions: [{key, displayName}]}}}."""
    return _get('/presets/meta')


def fetch_classic_preset(brand, camera, lens, genre, condition, mode):
    """POST /presets/classic → full preset object."""
    payload = {
        'brand':       brand,
        'cameraModel': camera['modelName'],
        'lensName':    lens['lensName'],
        'genre':       genre,
        'condition':   condition,
        'mode':        mode,
    }
    return _post('/presets/classic', payload)


def fetch_smart_presets(interests, mode):
    """POST /presets/smart → smart preset results."""
    payload = {'interests': interests, 'mode': mode}
    return _post('/presets/smart', payload)


# ——— EXPOSURE TRIANGLE ———————————————————————————————————————————————
def exposure_triangle(preset, selections):
    aperture = preset.get('aperture', '—')
    shutter  = preset.get('shutterSpeed', '—')
    iso      = preset.get('ISO', '—')

    tri = [
        "        /\\        ",
        "       /  \\       ",
        "      /    \\      ",
        "     /  Exp \\     ",
        "    /        \\    ",
        "   /          \\   ",
        "  /____________\\  ",
    ]
    frame_colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

    for frame_c in frame_colors:
        clear()
        print(c("  Kamera Quest  |  Exposure Summary", 'magenta'))
        print(c('═' * 60, 'magenta'))
        for k, v in selections.items():
            print(c(f"  {EMOJIS.get(k, '')} {k}: {v}", 'cyan'))
        print()
        # Apex
        print(frame_c + f"  Aperture: f/{aperture}".center(60) + '\033[0m')
        for idx, line in enumerate(tri):
            if idx == len(tri) - 1:
                left  = c(f"Shutter: {shutter}", 'cyan')
                right = c(f"ISO: {iso}", 'yellow')
                print(f"  {left}  {frame_c}{line}\033[0m  {right}")
            else:
                print(frame_c + line.center(64) + '\033[0m')
        print(c('═' * 60, 'magenta'))
        time.sleep(0.22)

    # After animation, display metadata
    print()
    if preset.get('mode'):
        print(c(f"  Mode:       {preset['mode']}", 'white'))
    if preset.get('afMode'):
        print(c(f"  AF Mode:    {preset['afMode']}", 'white'))
    if preset.get('metering'):
        print(c(f"  Metering:   {preset['metering']}", 'white'))
    if preset.get('driveMode'):
        print(c(f"  Drive:      {preset['driveMode']}", 'white'))
    if preset.get('requiresTripod'):
        print(c("  ⚠  Tripod required", 'yellow'))
    if preset.get('ibisBonus'):
        print(c("  ✦  IBIS beneficial", 'green'))
    if preset.get('rationale'):
        print()
        print(c("  WHY THESE SETTINGS", 'gold'))
        print(f"  {preset['rationale']}")
    if preset.get('proTip'):
        print()
        print(c("  PRO TIP", 'gold'))
        print(f"  {preset['proTip']}")
    if preset.get('commonMistake'):
        print()
        print(c("  COMMON MISTAKE", 'red'))
        print(f"  {preset['commonMistake']}")

    print()
    input(c("  Press Enter to return to main menu.", 'yellow'))


# ——— GENERIC MENU ————————————————————————————————————————————————————
def menu(options, title, prev=None):
    """
    Display a numbered menu. Returns the selected option string, None (back), or 'main'.
    options: list of strings (display labels)
    """
    while True:
        clear()
        print(c("  ✦ Kamera Quest CLI ✦", 'magenta'))
        if prev:
            for k, v in prev.items():
                print(c(f"  {EMOJIS.get(k, '')} {k}: {v}", 'cyan'))
        print(c(f"\n  {title}", 'cyan'))
        print(c('  ' + '─' * 56, 'magenta'))
        for i, opt in enumerate(options, 1):
            print(c(f"  [{i:>2}] {opt}", 'white'))
        print(c("  [ 0] Back  |  [M] Main Menu  |  [Q] Quit  |  [H] Help", 'yellow'))
        choice = input(c("  → ", 'magenta')).strip().lower()

        if choice == 'q':
            sys.exit(c("\n  Goodbye!\n", 'magenta'))
        if choice == 'm':
            return 'main'
        if choice == 'h':
            clear()
            print(c(HELP_TEXT, 'cyan'))
            input(c("  Press Enter to continue.", 'yellow'))
            continue
        if choice == '0':
            return None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        print(c("  ⚠  Invalid choice.", 'red'))
        time.sleep(0.8)


# ——— CLASSIC FLOW ————————————————————————————————————————————————————
def classic_flow(json_mode=False):
    selections = {}
    state = 'brand'

    # In JSON mode we read args up front.  Interactive mode loops through states.
    brand_obj  = None  # full camera object
    camera_obj = None  # full camera object
    lens_obj   = None  # full lens object
    genre_key  = None
    cond_key   = None

    while True:
        # ── Brand ──────────────────────────────────────────────────
        if state == 'brand':
            choice = menu(['canon', 'sony'], "Choose Camera Brand")
            if choice in (None, 'main'):
                return
            selections = {}
            brand = choice
            selections['Brand'] = brand
            state = 'camera'

        # ── Camera ─────────────────────────────────────────────────
        elif state == 'camera':
            try:
                cameras = fetch_cameras(selections['Brand'])
            except RuntimeError as e:
                print(c(f"\n  ⚠  {e}", 'red'))
                input(c("  Press Enter to try again.", 'yellow'))
                continue

            if not cameras:
                print(c("  ⚠  No cameras returned by API.", 'red'))
                input(c("  Press Enter to go back.", 'yellow'))
                state = 'brand'; continue

            cam_names = [cam['modelName'] for cam in cameras]
            choice = menu(cam_names, "Choose Camera Model", {'Brand': selections['Brand']})
            if choice == 'main': return
            if choice is None: state = 'brand'; continue
            camera_obj = next((cam for cam in cameras if cam['modelName'] == choice), None)
            selections['Camera'] = choice
            state = 'lens'

        # ── Lens ───────────────────────────────────────────────────
        elif state == 'lens':
            try:
                lenses = fetch_lenses(selections['Brand'], selections['Camera'])
            except RuntimeError as e:
                print(c(f"\n  ⚠  {e}", 'red'))
                input(c("  Press Enter to try again.", 'yellow'))
                continue

            if not lenses:
                print(c("  ⚠  No lenses returned for this camera.", 'red'))
                input(c("  Press Enter to go back.", 'yellow'))
                state = 'camera'; continue

            lens_names = [l['lensName'] for l in lenses]
            prev = {'Brand': selections['Brand'], 'Camera': selections['Camera']}
            choice = menu(lens_names, "Choose Lens", prev)
            if choice == 'main': return
            if choice is None: state = 'camera'; continue
            lens_obj = next((l for l in lenses if l['lensName'] == choice), None)
            selections['Lens'] = choice
            state = 'genre'

        # ── Genre ──────────────────────────────────────────────────
        elif state == 'genre':
            genre_labels = [GENRE_LABELS[g] for g in GENRES]
            prev = {k: selections[k] for k in ('Brand', 'Camera', 'Lens')}
            choice = menu(genre_labels, "Choose Genre", prev)
            if choice == 'main': return
            if choice is None: state = 'lens'; continue
            # Map label back to key
            genre_key = GENRES[genre_labels.index(choice)]
            selections['Genre'] = choice
            state = 'condition'

        # ── Condition ──────────────────────────────────────────────
        elif state == 'condition':
            try:
                meta = fetch_preset_meta()
            except RuntimeError as e:
                print(c(f"\n  ⚠  {e}", 'red'))
                input(c("  Press Enter to try again.", 'yellow'))
                continue

            # /presets/meta returns {portrait: [{key, displayName}], ...}
            conditions = meta.get(genre_key, [])  # [{key, displayName}]

            if not conditions:
                print(c("  ⚠  No conditions found for this genre.", 'red'))
                input(c("  Press Enter to go back.", 'yellow'))
                state = 'genre'; continue

            cond_display = [cond.get('displayName', cond['key']) for cond in conditions]
            prev = {k: selections[k] for k in ('Brand', 'Camera', 'Lens', 'Genre')}
            choice = menu(cond_display, "Choose Shooting Condition", prev)
            if choice == 'main': return
            if choice is None: state = 'genre'; continue

            cond_idx = cond_display.index(choice)
            cond_key = conditions[cond_idx]['key']
            selections['Condition'] = choice
            state = 'result'

        # ── Fetch & Display ────────────────────────────────────────
        elif state == 'result':
            try:
                preset = fetch_classic_preset(
                    selections['Brand'],
                    camera_obj,
                    lens_obj,
                    genre_key,
                    cond_key,
                    mode='apprentice',
                )
            except RuntimeError as e:
                print(c(f"\n  ⚠  {e}", 'red'))
                input(c("  Press Enter to go back.", 'yellow'))
                state = 'condition'; continue

            if json_mode:
                print(json.dumps(preset, indent=2))
                return

            exposure_triangle(preset, selections)
            return


# ——— SMART MODE FLOW ——————————————————————————————————————————————————
def smart_mode_flow(mode_value, json_mode=False):
    clear()
    label = {v: k for k, v in SMART_MODES.items()}.get(mode_value, mode_value.title())
    print(c(f"\n  ✦ {label} ✦", 'magenta'))
    print(c('  ' + '─' * 56, 'magenta'))

    raw = input(c("  Interests (comma-separated, e.g. portrait, street): ", 'cyan'))
    interests = [i.strip().lower() for i in raw.split(',') if i.strip()]

    if not interests:
        print(c("  ⚠  No interests entered.", 'red'))
        input(c("  Press Enter to return.", 'yellow'))
        return

    print(c("\n  Fetching smart presets…", 'yellow'))
    try:
        resp = fetch_smart_presets(interests, mode_value)
    except RuntimeError as e:
        print(c(f"\n  ⚠  {e}", 'red'))
        input(c("  Press Enter to return.", 'yellow'))
        return

    if json_mode:
        print(json.dumps(resp, indent=2))
        return

    # API response: {mode, presetsByInterest: [{interest, genre, presets: [...]}]}
    print(c('\n  ' + '═' * 56, 'magenta'))
    for block in resp.get('presetsByInterest', []):
        interest = block.get('interest', '?')
        print(c(f"\n  ● {interest.upper()} PRESETS", 'gold'))
        presets = block.get('presets', [])
        if not presets:
            print(c("    (no presets returned)", 'red'))
            continue
        for p in presets:
            name = p.get('displayName') or p.get('condition', '—')
            iso  = p.get('ISO', '—')
            ap   = p.get('aperture', '—')
            ss   = p.get('shutterSpeed', '—')
            diff = p.get('difficulty', '')
            tip  = p.get('proTip', '')
            print(c(f"    {name}", 'cyan'))
            print(c(f"      ISO {iso}  |  f/{ap}  |  {ss}", 'white'))
            if diff:
                print(c(f"      Difficulty: {diff}", 'yellow'))
            if tip:
                print(c(f"      Tip: {tip}", 'green'))

    print(c('\n  ' + '═' * 56, 'magenta'))
    input(c("  Press Enter to return to main menu.", 'yellow'))


# ——— MAIN LOOP ————————————————————————————————————————————————————————
def main():
    parser = argparse.ArgumentParser(
        prog='kamera_quest_cli',
        description='Kamera Quest – Professional camera settings assistant',
    )
    parser.add_argument(
        '--json', action='store_true',
        help='Output raw JSON (non-interactive)',
    )
    parser.add_argument(
        '--api', metavar='BASE_URL',
        help='Override API base URL',
    )
    args = parser.parse_args()

    if args.api:
        global API_BASE
        API_BASE = args.api.rstrip('/')

    json_mode = args.json

    MAIN_OPTIONS = ['Classic Flow'] + list(SMART_MODES.keys())

    while True:
        top = menu(MAIN_OPTIONS, "Main Menu  |  Choose Flow or Mode")

        if top == 'Classic Flow':
            classic_flow(json_mode=json_mode)

        elif top in SMART_MODES:
            smart_mode_flow(SMART_MODES[top], json_mode=json_mode)

        elif top is None or top == 'main':
            continue  # loop back


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n\n  Thanks for using Kamera Quest CLI! Goodbye!\n", 'magenta'))
