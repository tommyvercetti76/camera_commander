"""
kamera_quest_cli.py

Professional, aesthetic CLI for camera, lens, and preset selection.
Fully interactive with animated RGB equilateral exposure triangle (Bermuda-style).
Supports “Classic Flow” or three Smart Modes: Noob, Semi-Noob, Narcissist.

Dependencies:
  - requests (`pip install requests`)
"""

import requests
import os
import sys
import time

# ——— CONFIGURATION —————————————————————————————————————————————————————
# In production, replace localhost with your deployed API endpoint
FIREBASE_HOST     = os.getenv('KAMERA_API_HOST', "http://localhost:5001/kaayko-api-dev/us-central1/api/kameras")
PRESET_META_URL   = os.getenv('PRESET_META_URL', "http://localhost:5001/kaayko-api-dev/us-central1/api/presetMeta")
_PRESET_URL       = os.getenv('PRESET_API_URL', "http://localhost:5001/kaayko-api-dev/us-central1/api/getPreset")
SMART_PRESET_ROOT = os.getenv('SMART_PRESET_ROOT', "http://localhost:5001/kaayko-api-dev/us-central1/api/smart_presets")

# ——— HELP TEXT ———————————————————————————————————————————————————————
HELP_TEXT = """
═══════════════════════════════════════════════════════════════════════════════
📚 Kamera Quest CLI HELP 📚

NAVIGATION:
  [0] Back       – Step back one level
  [M] Main Menu  – Jump to main menu
  [Q] Quit       – Exit immediately
  [H] Help       – Show this help screen

MAIN MENU:
  1. Classic Flow    – Traditional brand/model/lens/subject/lighting/preset
  2. Noob Mode       – Smart presets for newcomers
  3. Semi-Noob Mode  –  Intermediate smart presets
  4. Narcissist Mode – Pro-level smart presets

CLASSIC FLOW USAGE:
  1. Brand Selection   – Canon or Sony (dynamically fetched)
  2. Model Selection   – Pick a camera model
  3. Lens Selection    – Pick a compatible lens
  4. Subject Choice    – Portrait, Wildlife, etc.
  5. Lighting Options  – Filtered by subject
  6. Preset Summary    – ISO, Aperture, Shutter Speed
  7. Exposure Triangle – Animated equilateral triangle

SMART MODE USAGE:
  • Enter brand, model, lens, up to N interests
  • Receive tailored presets (24/48/64 per interest)

TIPS & TROUBLESHOOTING:
 - Use number keys to choose.
 - '0' steps back one level.
 - 'M' jumps to main menu.
 - 'H' shows help anytime.
 - If lighting options are empty, return to Subject.
 - Ensure your API host is correct in FIREBASE_HOST.
 - Test endpoints with `curl` if needed.
═══════════════════════════════════════════════════════════════════════════════
"""

# ——— UTILITIES —————————————————————————————————————————————————————
EMOJIS = {
    'Brand': '🏷️',
    'Camera': '📷',
    'Lens': '🔭',
    'Subject': '🎨',
    'Lighting': '🌤️'
}

def color_text(text, color):
    codes = {
        'green':'\033[92m', 'cyan':'\033[96m', 'yellow':'\033[93m',
        'magenta':'\033[95m','red':'\033[91m','white':'\033[97m','reset':'\033[0m'
    }
    return f"{codes[color]}{text}{codes['reset']}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_json(url, method='get', payload=None):
    """Helper to GET or POST and return JSON or {}."""
    try:
        if method=='post':
            r = requests.post(url, json=payload, timeout=5)
        else:
            r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return {}

# ——— FETCH HELPERS —————————————————————————————————————————————————————
def fetch_cameras(brand):
    data = fetch_json(f"{FIREBASE_HOST}/{brand}/cameras")
    return [c.get('modelName') for c in data] if isinstance(data, list) else []

def fetch_lenses(brand, camera):
    data = fetch_json(f"{FIREBASE_HOST}/{brand}/cameras/{camera}/lenses")
    return [l.get('lensName') for l in data] if isinstance(data, list) else []

def fetch_available_conditions():
    return fetch_json(PRESET_META_URL)

def fetch_classic_preset(subject, lighting):
    payload = {
        'scenario': subject.lower().replace(' ', '_'),
        'condition': lighting.lower().replace(' ', '_')
    }
    return fetch_json(_PRESET_URL, method='post', payload=payload)

def fetch_smart_presets(mode, brand, cameraModel, lensName, interests):
    url = f"{SMART_PRESET_ROOT}/{mode.lower().replace(' ', '_')}"
    payload = {
        'brand': brand,
        'cameraModel': cameraModel,
        'lensName': lensName,
        'interests': interests
    }
    return fetch_json(url, method='post', payload=payload)

# ——— EXPOSURE TRIANGLE —————————————————————————————————————————————————————
def exposure_triangle(aperture, shutter, iso, selections):
    tri = [
        "       /\\       ",
        "      /  \\      ",
        "     /    \\     ",
        "    /      \\    ",
        "   /        \\   ",
        "  /__________\\  "
    ]
    top_lbl   = f"Aperture: {aperture}"
    left_lbl  = f"Shutter: {shutter}"
    right_lbl = f"ISO: {iso}"
    frames    = ['\033[91m','\033[92m','\033[93m','\033[94m','\033[95m','\033[96m']

    for c in frames:
        clear_screen()
        # Selections summary
        print(color_text("📋 Your Selections:", 'cyan'))
        for k,v in selections.items():
            print(color_text(f" {EMOJIS.get(k,'')} {k}: {v}", 'white'))
        print(c + '═'*60 + '\033[0m')
        # Apex
        print(c + top_lbl.center(60) + '\033[0m')
        # Draw triangle
        for idx, line in enumerate(tri):
            if idx==2:
                eye_line = line[:8] + '👁️' + line[9:]
                print(c + eye_line.center(60) + '\033[0m')
            elif idx==5:
                print(c + left_lbl.ljust(20) + line + right_lbl.rjust(20) + '\033[0m')
            else:
                print(c + line.center(60) + '\033[0m')
        print(c + '═'*60 + '\033[0m')
        time.sleep(0.25)
    input(color_text("\n🛑 Press Enter to return to main menu.", 'yellow'))

# ——— GENERIC MENU —————————————————————————————————————————————————————
def menu(options, title, prev=None):
    """Display a menu, return selected option, 'main' or None."""
    while True:
        clear_screen()
        print(color_text("✨ Kamera Quest CLI ✨", 'magenta'))
        if prev:
            for k,v in prev.items():
                print(color_text(f"{EMOJIS.get(k,'')} {k}: {v}", 'cyan'))
        print(color_text(f"\n{title}", 'cyan'))
        print(color_text('═'*60, 'magenta'))
        for i, opt in enumerate(options, 1):
            print(color_text(f"[{i}] {opt}", 'white'))
        print(color_text("[0] Back | [M] Main Menu | [Q] Quit | [H] Help", 'yellow'))
        choice = input(color_text(" Enter choice: ","magenta")).lower()
        if choice=='q':
            sys.exit(color_text("\nGoodbye!\n",'magenta'))
        if choice=='m':
            return 'main'
        if choice=='h':
            clear_screen()
            print(color_text(HELP_TEXT,'cyan'))
            input(color_text("\nPress Enter to continue.", 'yellow'))
            continue
        if choice=='0':
            return None
        if choice.isdigit() and 1<=int(choice)<=len(options):
            return options[int(choice)-1]
        print(color_text("⚠️ Invalid choice, try again.", 'red'))
        time.sleep(1)

# ——— CLASSIC FLOW —————————————————————————————————————————————————————
def classic_flow():
    selections = {}
    state = 'brand'

    while True:
        if state=='brand':
            choice = menu(['canon','sony'], "🏷️ Choose Camera Brand")
            if choice in (None,'main'): return
            selections.clear(); selections['Brand']=choice; state='camera'

        elif state=='camera':
            cams = fetch_cameras(selections['Brand'])
            choice = menu(cams, "📷 Choose Camera Model", {'Brand': selections['Brand']})
            if choice=='main': return
            if choice is None: state='brand'; continue
            selections['Camera']=choice; state='lens'

        elif state=='lens':
            lenses = fetch_lenses(selections['Brand'], selections['Camera'])
            choice = menu(lenses, "🔭 Choose Lens", {'Brand':selections['Brand'],'Camera':selections['Camera']})
            if choice=='main': return
            if choice is None: state='camera'; continue
            selections['Lens']=choice; state='subject'

        elif state=='subject':
            subjects=['Portrait','Wildlife','Sports','Landscape','Astro','Indoor Lowlight','Golden Hour Sunset','Macro']
            choice = menu(subjects, "🎨 Choose Subject", selections)
            if choice=='main': return
            if choice is None: state='lens'; continue
            selections['Subject']=choice; state='lighting'

        elif state=='lighting':
            meta = fetch_available_conditions()
            key = selections['Subject'].lower().replace(' ','_')
            cond = meta.get(key, [])
            if not cond:
                clear_screen(); print(color_text("⚠️ No lighting presets available.",'red'))
                input(color_text("\nPress Enter to retry.",'yellow'))
                state='subject'; continue

            opts=[c.replace('_',' ').title() for c in cond]
            choice = menu(opts, "🌤️ Choose Lighting Condition", selections)
            if choice=='main': return
            if choice is None: state='subject'; continue
            selections['Lighting']=choice

            # fetch and display
            resp = fetch_classic_preset(selections['Subject'], selections['Lighting'])
            preset = resp.get('preset')
            if not preset:
                clear_screen(); print(color_text("⚠️ Preset not found.",'red'))
                input(color_text("\nPress Enter to retry.",'yellow'))
                state='lighting'; continue

            # show triangle
            exposure_triangle(preset['aperture'], preset['shutterSpeed'], preset['ISO'], selections)
            return

# ——— SMART MODE FLOW —————————————————————————————————————————————————————
def smart_mode_flow(mode):
    clear_screen()
    print(color_text(f"🚀 Entering {mode} 🚀", 'magenta'))
    brand      = input(color_text("Camera Brand: ", 'cyan')).lower()
    cameraModel= input(color_text("Camera Model: ", 'cyan'))
    lensName   = input(color_text("Lens Name: ", 'cyan'))
    raw = input(color_text("Interests (comma-separated, up to 16): ", 'cyan'))
    interests  = [i.strip().lower() for i in raw.split(',') if i.strip()]

    resp = fetch_smart_presets(mode, brand, cameraModel, lensName, interests)
    if 'error' in resp:
        print(color_text(f"⚠️ {resp['error']}", 'red'))
    else:
        for interest, presets in resp.items():
            print(color_text(f"\n🎯 {interest.title()} Presets:", 'yellow'))
            for p in presets:
                print(color_text(f" ISO {p['ISO']} | ƒ/{p['aperture']} | {p['shutterSpeed']}", 'green'))
    input(color_text("\n🛑 Press Enter to return to main menu.", 'yellow'))

# ——— MAIN LOOP —————————————————————————————————————————————————————
def main():
    while True:
        top = menu(
            ['Classic Flow','Noob Mode','Semi-Noob Mode','Narcissist Mode'],
            "🏁 Main Menu: Choose Flow or Mode"
        )
        if top=='Classic Flow':
            classic_flow()
        elif top=='Noob Mode':
            smart_mode_flow('noob')
        elif top=='Semi-Noob Mode':
            smart_mode_flow('semi_noob')
        elif top=='Narcissist Mode':
            smart_mode_flow('narcissist')
        # if top is None or 'main', simply loop back

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(color_text("\nThanks for using Kamera Quest CLI! Goodbye!\n",'magenta'))