#!/usr/bin/env python3
"""
add_v3_genres_and_conditions.py

Adds:
  - New conditions to existing genres (astro, landscape, wildlife, sports, macro, portrait)
  - 9 new genre JSON files (food, realestate, automotive, product, concert,
    underwater, drone, newborn, fashion)
  - Updates api/src/data/presets/index.js
  - Updates api/src/middleware/validate.js VALID_GENRES list
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESETS_DIR = os.path.join(ROOT, 'api', 'src', 'data', 'presets')


def load_preset(name):
    return json.load(open(os.path.join(PRESETS_DIR, name + '.json')))


def save_preset(name, data):
    path = os.path.join(PRESETS_DIR, name + '.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
    print('  saved ' + path.replace(ROOT + '/', ''))


# ─────────────────────────────────────────────────────────────────────────────
# NEW CONDITIONS FOR EXISTING GENRES
# ─────────────────────────────────────────────────────────────────────────────

# ASTRO -----------------------------------------------------------------------
astro = load_preset('astro')

astro['conditions']['MILKY_WAY_APS_C_CROP'] = {
    "displayName": "Milky Way APS-C Crop",
    "ISO": 3200,
    "aperture": 2.8,
    "shutterSpeed": "12",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "self_timer_2s",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "APS-C crop factor (1.5-1.6x) shortens the safe shutter at any given focal length. On a 24mm lens: 500 / (24 x 1.6) = 13s maximum before star trailing — 12s for safety.",
    "proTip": "Use the NPF rule for precision: (35 x aperture + 30 x pixel_pitch) / focal_length_equivalent. On a 24MP APS-C sensor this gives ~10-12s at 24mm f/2.8.",
    "commonMistake": "Applying the 20-second rule from full-frame guides to an APS-C camera. This produces star trails on crop sensors. Always apply the crop factor to your maximum shutter calculation.",
    "tags": ["milky way", "aps-c", "crop sensor", "star trails"]
}

astro['conditions']['LUNAR_ECLIPSE_BLOOD_MOON'] = {
    "displayName": "Lunar Eclipse / Blood Moon",
    "ISO": 1600,
    "aperture": 2.8,
    "shutterSpeed": "2",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "centre",
    "metering": "spot",
    "driveMode": "self_timer_2s",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "During totality the Moon dims by ~10,000x compared to a full moon. The existing ECLIPSE_PHOTOGRAPHY preset is correct for solar eclipses and partial phases, but completely wrong for the blood moon totality phase.",
    "proTip": "Expose for the red colour, not the bright limb edge. Use live histogram and adjust continuously as the Moon dims. During partial phases bracket every 30 seconds.",
    "commonMistake": "Using the same settings throughout the entire eclipse. Brightness changes 10,000x from full moon to totality — you must continuously adjust ISO and shutter as the eclipse progresses.",
    "tags": ["eclipse", "blood moon", "lunar", "totality"]
}

astro['conditions']['DEEP_SKY_UNTRACKED'] = {
    "displayName": "Deep Sky Untracked",
    "ISO": 12800,
    "aperture": 2.8,
    "shutterSpeed": "15",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "interval_timer",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "For those without a tracking mount. Maximum ISO compensates for the limited 15s exposure. Stack 20-50 frames in post to reduce noise. Only bright nebulae near the galactic core are realistic targets without tracking.",
    "proTip": "Stack using Sequator (free, Windows) or Siril (free, Mac/PC). 20 stacked untracked frames beats a single 5-minute tracked frame for noise reduction.",
    "commonMistake": "Attempting 120s without tracking produces star trails, not nebulae. Invest in a star tracker (iOptron SkyGuider Pro, Sky-Watcher Star Adventurer) before attempting deep sky objects.",
    "tags": ["deep sky", "nebula", "untracked", "stacking", "high ISO"]
}

save_preset('astro', astro)

# LANDSCAPE -------------------------------------------------------------------
landscape = load_preset('landscape')

landscape['conditions']['STORM_LIGHTNING'] = {
    "displayName": "Storm and Lightning",
    "ISO": 100,
    "aperture": 8,
    "shutterSpeed": "30",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "interval_timer",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "Bulb or 30s exposure in the dark means any lightning bolt that fires during the exposure registers automatically. ISO 100 because lightning is extremely bright — the bolt itself provides the light.",
    "proTip": "Point into the storm cell, not directly at individual lightning. Use a cable release or intervalometer. In light-polluted skies, narrow to f/16 to avoid overexposing the background.",
    "commonMistake": "Using autofocus in the dark — the camera hunts and misses the shot entirely. Set manual focus to infinity before the storm arrives, then lock it.",
    "tags": ["lightning", "storm", "long exposure", "bulb", "weather"]
}

landscape['conditions']['TIME_LAPSE_SETUP'] = {
    "displayName": "Time Lapse Setup",
    "ISO": 400,
    "aperture": 5.6,
    "shutterSpeed": "1/50",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "interval_timer",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": True,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "The 180-degree shutter rule: shutter speed = double the frame interval. For 25fps playback with 1-second intervals, 1/50s is correct. ND filter required in daylight to achieve 1/50s. Manual mode is mandatory — any aperture variation causes flicker.",
    "proTip": "Deflicker in post using LRTimelapse or DaVinci Resolve. Shoot RAW for maximum dynamic range. Use ND8-ND64 to achieve 1/50s in bright daylight.",
    "commonMistake": "Using aperture priority — any aperture micro-shift between frames causes visible flicker in the final video. Manual mode only, every time.",
    "tags": ["timelapse", "ND filter", "video", "interval", "motion"]
}

landscape['conditions']['SNOWY_SCENE'] = {
    "displayName": "Snowy Scene",
    "ISO": 100,
    "aperture": 11,
    "shutterSpeed": "1/250",
    "mode": "Av",
    "afMode": "single",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "single",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 1,
    "rationale": "Snow reflects ~90% of light and fools evaluative metering into underexposing — the camera renders snow as grey. Set +1 to +1.5EV exposure compensation to restore white snow.",
    "proTip": "Use spot or centre-weighted metering on a mid-tone in the scene (a coat, bare tree bark) instead of the snow itself. Or set evaluative metering with +1.3EV compensation.",
    "commonMistake": "Trusting evaluative metering on snow — the image will look grey and underexposed. Always apply positive exposure compensation in snowy scenes.",
    "tags": ["snow", "winter", "exposure compensation", "metering"]
}

save_preset('landscape', landscape)

# WILDLIFE --------------------------------------------------------------------
wildlife = load_preset('wildlife')

wildlife['conditions']['NOCTURNAL_WILDLIFE'] = {
    "displayName": "Nocturnal Wildlife",
    "ISO": 12800,
    "aperture": 2.8,
    "shutterSpeed": "1/125",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_low",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": True,
    "difficulty": 3,
    "rationale": "Owls, foxes, badgers, and other nocturnal animals require maximum ISO and fastest aperture. 1/125s freezes most nocturnal movement without needing flash, which would disturb animals.",
    "proTip": "Use a red-light torch at low intensity — most nocturnal animals cannot clearly detect red wavelengths and are less likely to be startled. An IR spotlight with an appropriate sensor opens further possibilities.",
    "commonMistake": "Using white light — this immediately stops natural behaviour and causes animals to flee. Red light at low intensity is the professional standard for nocturnal wildlife observation.",
    "tags": ["nocturnal", "night", "high ISO", "wildlife", "low light"]
}

wildlife['conditions']['CAPTIVE_ZOO_ENCLOSURE'] = {
    "displayName": "Captive Zoo Enclosure",
    "ISO": 1600,
    "aperture": 2.8,
    "shutterSpeed": "1/500",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": True,
    "difficulty": 2,
    "rationale": "Wide aperture optically blurs enclosure bars and mesh fences. Fast shutter freezes unpredictable animal movement.",
    "proTip": "Hold the lens directly against the mesh or glass to eliminate it optically. At f/2.8, mesh just 5cm from the front element disappears completely into bokeh.",
    "commonMistake": "Shooting through glass at an angle — reflections destroy the shot. Position perpendicular to the glass and press a rubber lens hood against it to eliminate reflections.",
    "tags": ["zoo", "enclosure", "bars", "bokeh", "captive animals"]
}

wildlife['conditions']['SAFARI_MOVING_VEHICLE'] = {
    "displayName": "Safari from Moving Vehicle",
    "ISO": 400,
    "aperture": 5.6,
    "shutterSpeed": "1/1000",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": True,
    "difficulty": 2,
    "rationale": "Vehicle vibration and subject motion combine at safari speeds. 1/1000s eliminates both sources of blur and allows sharp shots from a moving vehicle.",
    "proTip": "Use a beanbag over the window sill as a lens support — far more stable than handholding from a vehicle. Switch to electronic shutter to eliminate mirror slap vibration.",
    "commonMistake": "Leaving IBIS/OIS active on a moving vehicle — stabilisation systems can misinterpret vehicle rocking as motion to compensate and actively introduce blur. Check your specific OIS mode.",
    "tags": ["safari", "vehicle", "motion", "wildlife", "africa"]
}

wildlife['conditions']['HIDE_LONG_WAIT'] = {
    "displayName": "Bird Hide / Wildlife Blind",
    "ISO": 400,
    "aperture": 6.3,
    "shutterSpeed": "1/1000",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "Bird hides and wildlife blinds require pre-configured gear before the animal arrives. Pre-focused, pre-metered — no fumbling when the decisive moment happens.",
    "proTip": "Set your camera to anticipated conditions before dawn. Let eyes adjust to darkness before opening the hide window. Pre-focus on the expected perch or feeding station.",
    "commonMistake": "Leaving auto-ISO maximum range too high — in bright morning light auto-ISO may jump to ISO 6400 unnecessarily. Set auto-ISO max to 3200 for daylight hide work.",
    "tags": ["hide", "blind", "birds", "patience", "dawn"]
}

save_preset('wildlife', wildlife)

# SPORTS ----------------------------------------------------------------------
sports = load_preset('sports')

sports['conditions']['SWIMMING_POOL_AQUATICS'] = {
    "displayName": "Swimming Pool Aquatics",
    "ISO": 1600,
    "aperture": 2.8,
    "shutterSpeed": "1/1000",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "Indoor pool lighting is typically tungsten or fluorescent at EV 8-10. 1/1000s freezes water splashes and swimmer arms. f/2.8 is mandatory to maintain adequate exposure.",
    "proTip": "Shoot just after the turn — swimmers are fastest and create the most dynamic water spray. The peak dramatic moment is breaching the surface at the wall.",
    "commonMistake": "Underestimating competitive swimmer speed — 1/500s still shows motion blur at Olympic or competitive level. Use 1/1000s minimum for crisp freeze frames.",
    "tags": ["swimming", "aquatics", "pool", "splash", "indoor sports"]
}

sports['conditions']['CYCLING_ROAD_PANNING'] = {
    "displayName": "Cycling Road Panning",
    "ISO": 200,
    "aperture": 8,
    "shutterSpeed": "1/125",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "Panning with cyclists at 40-60km/h requires 1/60-1/125s to blur the background while keeping the rider sharp. f/8 provides depth margin if the pan timing isn't perfect.",
    "proTip": "Position yourself at exactly 90 degrees to the road for maximum panning blur effect. Follow the rider for at least 2 full seconds before pressing the shutter.",
    "commonMistake": "Panning from the shoulders — this creates unwanted vertical movement that blurs the rider vertically. Pan exclusively from the waist, keeping the camera perfectly level throughout.",
    "tags": ["cycling", "panning", "motion blur", "road", "action"]
}

sports['conditions']['BOXING_MMA_INDOOR'] = {
    "displayName": "Boxing and MMA Indoor",
    "ISO": 6400,
    "aperture": 2.8,
    "shutterSpeed": "1/1000",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "Combat sports arenas are typically EV 6-8. Punches reach 30-50km/h at impact and require 1/1000s minimum to freeze cleanly. f/2.8 is mandatory for adequate exposure.",
    "proTip": "Focus on the gloves rather than the face for decisive impact moments. Anticipate the punch and begin the burst half a second before the glove connects.",
    "commonMistake": "Shooting at 1/500s — arm speed in combat sports makes gloves completely blurred at that speed. 1/1000s is the absolute minimum for clean punch freeze frames.",
    "tags": ["boxing", "MMA", "combat", "martial arts", "indoor", "action"]
}

sports['conditions']['EQUESTRIAN_JUMP'] = {
    "displayName": "Equestrian Show Jumping",
    "ISO": 400,
    "aperture": 6.3,
    "shutterSpeed": "1/2000",
    "mode": "Tv",
    "afMode": "continuous",
    "afPoint": "wide",
    "metering": "evaluative",
    "driveMode": "continuous_high",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "Horse and rider at the apex of a jump — the body is momentarily suspended. 1/2000s freezes hooves cleanly mid-air with no motion blur on the legs.",
    "proTip": "Position at the far side of the fence, not the approach side — this gives you the profile shot with horse and rider in full suspended form. Start the burst three strides before the jump.",
    "commonMistake": "Firing the shutter too late — the peak moment is when all four hooves are off the ground at the apex. Start the burst before the horse leaves the ground and let the buffer capture the peak.",
    "tags": ["equestrian", "horse", "jump", "show jumping", "outdoor sports"]
}

save_preset('sports', sports)

# MACRO -----------------------------------------------------------------------
macro = load_preset('macro')

macro['conditions']['MACRO_FOCUS_STACK_SETUP'] = {
    "displayName": "Macro Focus Stack Setup",
    "ISO": 100,
    "aperture": 11,
    "shutterSpeed": "1/160",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "centre",
    "metering": "evaluative",
    "driveMode": "interval_timer",
    "requiresTripod": True,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "Focus stacking requires absolute consistency between frames. f/11 provides enough depth of field per frame for clean transitions in post while avoiding diffraction. Manual mode prevents any exposure variation that would destroy the composite.",
    "proTip": "Use a focusing rail for repeatable 0.1mm increments. 15-30 frames at f/11 typically covers a small insect from eyes to wingtips. Stack in Helicon Focus or Zerene Stacker for best results.",
    "commonMistake": "Shooting at f/22 for perceived maximum depth — the DOF advantage of f/22 over f/11 is marginal at macro distances, but diffraction softening is severe and obvious on sensors above 20MP. Always stack at f/11.",
    "tags": ["focus stack", "macro", "stacking", "rail", "detail"]
}

macro['conditions']['SNOWFLAKE_MACRO'] = {
    "displayName": "Snowflake Macro",
    "ISO": 100,
    "aperture": 16,
    "shutterSpeed": "1/200",
    "mode": "M",
    "afMode": "manual",
    "afPoint": "centre",
    "metering": "evaluative",
    "driveMode": "single",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 3,
    "rationale": "Snowflakes melt in 30-90 seconds requiring fast, precise work. Handheld with macro flash. f/16 provides adequate depth at high magnification. Ring flash or twin flash sync at 1/200s.",
    "proTip": "Pre-chill camera and lens before going outside — a warm lens fogs instantly in cold air from condensation. Catch flakes on black velvet or a cold glass slide. Work in shade — direct sunlight melts crystals in seconds.",
    "commonMistake": "Bringing warm equipment outside without acclimatisation — lens condensation instantly ruins images. Keep equipment cold throughout the session, store it in a cool bag between shoots.",
    "tags": ["snowflake", "crystal", "winter", "macro flash", "nature"]
}

save_preset('macro', macro)

# PORTRAIT --------------------------------------------------------------------
portrait = load_preset('portrait')

portrait['conditions']['NEWBORN_STUDIO'] = {
    "displayName": "Newborn Studio",
    "ISO": 400,
    "aperture": 5.6,
    "shutterSpeed": "1/160",
    "mode": "M",
    "afMode": "single",
    "afPoint": "face",
    "metering": "evaluative",
    "driveMode": "silent_single",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "f/5.6 provides enough depth of field for a full newborn body photographed from above. 1/160s ensures no motion blur from startle reflexes. ISO 400 minimises noise without grain visible in soft skin.",
    "proTip": "Use a large octobox or north-facing window at 45 degrees to eliminate harsh shadows. Silent electronic shutter prevents startle reactions. Set white balance warm (3200-4000K) for correct skin tone.",
    "commonMistake": "Using flash at full power. Newborns are photosensitive. Use bounce flash at -2EV or continuous LED lighting at 3200K. Silent shutter is critical — mirror slap causes startle reflex.",
    "tags": ["newborn", "baby", "studio", "natural light", "silent shutter"]
}

portrait['conditions']['EDITORIAL_HIGH_FASHION'] = {
    "displayName": "Editorial High Fashion",
    "ISO": 100,
    "aperture": 8,
    "shutterSpeed": "1/160",
    "mode": "M",
    "afMode": "single",
    "afPoint": "face",
    "metering": "evaluative",
    "driveMode": "continuous_low",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 2,
    "rationale": "f/8 provides full sharpness from face to fingertips — editorial demands technical perfection throughout. ISO 100 for maximum dynamic range and tonal gradation. 1/160 syncs with studio strobe.",
    "proTip": "Use a 1.2-1.4m Profoto octabox at camera-left as key, silver reflector camera-right as fill. Check histogram on every frame. Magazine editors expect technically perfect exposures with no clipping.",
    "commonMistake": "Shooting wide open (f/1.4-f/2.8) for fashion — atmospheric, but editorial clients demand sharpness throughout the frame. f/8 is the industry standard for technical fashion photography.",
    "tags": ["fashion", "editorial", "studio", "strobe", "commercial"]
}

portrait['conditions']['MATERNITY_OUTDOOR'] = {
    "displayName": "Maternity Outdoor",
    "ISO": 100,
    "aperture": 2.8,
    "shutterSpeed": "1/400",
    "mode": "Av",
    "afMode": "single",
    "afPoint": "face",
    "metering": "evaluative",
    "driveMode": "single",
    "requiresTripod": False,
    "requiresTracking": False,
    "requiresNDFilter": False,
    "ibisBonus": False,
    "difficulty": 1,
    "rationale": "f/2.8 provides shallow depth of field that separates the subject from background. 1/400s ensures no motion blur in flowing garments. Golden hour side lighting reveals form at its most flattering.",
    "proTip": "Shoot 45 minutes before sunset for soft directional light that reveals the silhouette. Position subject so the sun backlights the profile. The bump reads best from the side in warm light.",
    "commonMistake": "Shooting at noon with flat overhead light — this removes all form definition. Golden hour or open shade only. Avoid backlit locations where harsh sun hits the camera lens directly.",
    "tags": ["maternity", "pregnancy", "outdoor", "golden hour", "silhouette"]
}

save_preset('portrait', portrait)


# ─────────────────────────────────────────────────────────────────────────────
# NEW GENRE FILES
# ─────────────────────────────────────────────────────────────────────────────

def write_genre(name, display_name, conditions):
    data = {
        "genre": name,
        "displayName": display_name,
        "conditions": conditions
    }
    save_preset(name, data)


# FOOD ------------------------------------------------------------------------
write_genre('food', 'Food Photography', {
    "FOOD_HERO_NATURAL_LIGHT": {
        "displayName": "Food Hero Shot Natural Light",
        "ISO": 100, "aperture": 5.6, "shutterSpeed": "1/125",
        "mode": "Av", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Overhead window light, hero shot. f/5.6 keeps the entire dish sharp from front to back. Colour accuracy is critical — ISO 100 ensures maximum tonal fidelity.",
        "proTip": "Position the dish at 45 degrees to a north-facing or diffused window. Use a white reflector opposite the window to fill shadows. Shoot tethered to check colour on a calibrated display.",
        "commonMistake": "Shooting at f/2.8 for bokeh — individual food elements fall out of focus and the dish loses its story. f/5.6 keeps all elements readable.",
        "tags": ["food", "hero shot", "natural light", "window", "table"]
    },
    "FOOD_DARK_MOODY": {
        "displayName": "Dark Moody Food",
        "ISO": 400, "aperture": 2.8, "shutterSpeed": "1/100",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "Low-key atmospheric lighting from a single directional candle or rim light source. f/2.8 creates shallow DOF that isolates the hero element in deep shadow.",
        "proTip": "Use a single bare speedlight or LED panel at hard 90-degree side angle for maximum shadow drama. Black cards opposite the light increase the shadow depth further.",
        "commonMistake": "Over-lighting the shadow side — dark moody food photography depends on deep, unlit shadows. Resist the urge to fill the shadows with reflectors.",
        "tags": ["food", "moody", "dark", "low key", "atmospheric"]
    },
    "FOOD_OVERHEAD_FLAT_LAY": {
        "displayName": "Overhead Flat Lay",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/125",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Flat lay requires the lens to be perfectly perpendicular overhead. f/8 keeps all elements in the composition sharp across the entire frame from edge to edge.",
        "proTip": "Use a tripod arm extended directly overhead with a bubble level. Shoot tethered so you can adjust composition without repositioning. Even, diffused window light or a large softbox overhead.",
        "commonMistake": "Shooting at a slight angle rather than perfectly overhead — even a 5-degree tilt creates perspective distortion that makes round plates look oval.",
        "tags": ["food", "flat lay", "overhead", "lifestyle", "composition"]
    },
    "FOOD_STEAM_ACTION": {
        "displayName": "Food Steam and Action",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/500",
        "mode": "Tv", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Capture rising steam: fast shutter freezes individual steam tendrils rather than recording a blur. Backlight rims the steam to make it visible against dark backgrounds.",
        "proTip": "Place a bare speedlight or continuous LED directly behind and slightly above the dish as a rim light. The steam only reads against a dark background — use black or deep-toned backdrop.",
        "commonMistake": "Shooting in flat frontal light — steam is invisible without strong backlight. The setup requires deliberate directional rim lighting to capture steam effectively.",
        "tags": ["food", "steam", "backlight", "hot food", "action"]
    },
    "FOOD_RESTAURANT_AMBIENT": {
        "displayName": "Restaurant Ambient No Flash",
        "ISO": 1600, "aperture": 2.8, "shutterSpeed": "1/100",
        "mode": "Av", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "No-flash restaurant photography using ambient light only. Restaurant lighting is typically tungsten at EV 5-7. White balance must be manually set to the restaurant's colour temperature.",
        "proTip": "Set custom white balance from a white napkin or use Kelvin mode — auto white balance often goes wrong in mixed restaurant lighting. Find a table near a window for supplemental natural light.",
        "commonMistake": "Using the built-in flash — this blows out the dish, creates harsh shadows, and is disruptive to other diners. Ambient-only is both more flattering and more considerate.",
        "tags": ["restaurant", "ambient", "no flash", "food", "low light"]
    },
    "FOOD_PRODUCT_STUDIO": {
        "displayName": "Food Product Studio",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Commercial catalogue product: maximum sharpness throughout, strobe-controlled lighting, fully repeatable results. f/11 maximises depth. Strobe synced at 1/160s.",
        "proTip": "Use a colour checker card on the first frame for accurate post-processing. Shoot tethered with live view to verify focus before committing. Document your lighting setup for future matching.",
        "commonMistake": "Inconsistent white balance between frames — impossible to match in post. Set a fixed Kelvin value and do not let AWB shift between shots.",
        "tags": ["food", "product", "studio", "strobe", "commercial", "catalogue"]
    }
})

# REAL ESTATE -----------------------------------------------------------------
write_genre('realestate', 'Real Estate Photography', {
    "REALESTATE_INTERIOR_BRIGHT": {
        "displayName": "Interior Bright",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/30",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Expose for windows to preserve view and prevent blown highlights; let interior tone come naturally. Bracket -2EV / 0 / +2EV for HDR blending in post. Wide angle ultra-wide preferred.",
        "proTip": "Turn on all interior lights before shooting — mixing warm tungsten with cool daylight creates challenging colour balance. Shoot multiple exposures for HDR blending. Straighten verticals using lens shift or in post.",
        "commonMistake": "Exposing for the interior and blowing the windows to white — property buyers want to see the view. Always preserve window detail even if the interior is dark.",
        "tags": ["real estate", "interior", "HDR", "wide angle", "property"]
    },
    "REALESTATE_HDR_BASE_FRAME": {
        "displayName": "HDR Bracket Base Frame",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/4",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "HDR middle frame: bracket +2EV and -2EV around this base exposure. Five-frame bracket covers the full dynamic range of a typical interior. Tripod is mandatory for frame alignment.",
        "proTip": "Use the camera's built-in AEB (Auto Exposure Bracketing) to fire all frames without touching the camera. Process in Lightroom HDR merge or Photomatix for natural results.",
        "commonMistake": "Handheld HDR shooting — even IBIS cannot fully align 5 frames for clean merging. Tripod is non-negotiable for real estate HDR.",
        "tags": ["real estate", "HDR", "bracket", "interior", "tripod"]
    },
    "REALESTATE_EXTERIOR_DAY": {
        "displayName": "Exterior Daytime",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/250",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Exterior in daylight: f/11 delivers maximum depth of field across the full building facade and landscaping. Sharp and bright — the clean standard for property listings.",
        "proTip": "Shoot at 45-degree angle to the main facade to show both the front and side elevation. Mid-morning or mid-afternoon sun creates more dimensional shadows than noon shooting.",
        "commonMistake": "Shooting directly into the sun — blown sky and dark facade. Position the sun behind or to the side, then use fill flash or a reflector for the shadow side.",
        "tags": ["real estate", "exterior", "daylight", "facade", "property"]
    },
    "REALESTATE_TWILIGHT_EXTERIOR": {
        "displayName": "Twilight Exterior",
        "ISO": 100, "aperture": 8, "shutterSpeed": "8",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Twilight: the 20-30 minute window after sunset where interior lights balance against the deep blue sky. This is the signature premium real estate shot that commands higher fees.",
        "proTip": "Pre-focus before it gets dark and lock it. The window is only 20 minutes — work quickly. Turn on every interior light in the property beforehand. Bracket exposures.",
        "commonMistake": "Arriving too late — after full dark, the sky goes black and the magic is gone. Arrive 30 minutes before sunset and be set up and ready the moment the balance point arrives.",
        "tags": ["real estate", "twilight", "blue hour", "exterior", "premium"]
    },
    "REALESTATE_BATHROOM_DETAIL": {
        "displayName": "Bathroom Detail",
        "ISO": 400, "aperture": 11, "shutterSpeed": "1/60",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Tight bathroom spaces: bounce flash from ceiling, ultra-wide angle, and geometrically perfect composition. ISO 400 provides flexibility in confined low-light spaces.",
        "proTip": "Mount a speedlight on camera and angle the head at the ceiling — bounce flash creates even, shadow-free light that suits tiled surfaces. Remove all personal items from counters before shooting.",
        "commonMistake": "Forgetting to remove personal hygiene items, towels, and accessories — buyers want to see the bathroom, not the current owner's toiletries.",
        "tags": ["real estate", "bathroom", "detail", "interior", "tight space"]
    },
    "REALESTATE_POOL_GOLDEN_HOUR": {
        "displayName": "Pool and Outdoor Golden Hour",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/60",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Pool and outdoor living areas: golden warmth + polarising filter to cut water surface reflections and saturate the pool colour. The signature premium outdoor property shot.",
        "proTip": "A circular polariser used at 90 degrees from the sun eliminates water surface reflections and turns the pool a deep, saturated blue. Golden hour light warms the surrounding paving.",
        "commonMistake": "Shooting the pool at noon — harsh shadows across paving, blown sky, and flat pool colour. Golden hour is non-negotiable for aspirational outdoor property photography.",
        "tags": ["real estate", "pool", "outdoor", "golden hour", "polariser"]
    }
})

# AUTOMOTIVE ------------------------------------------------------------------
write_genre('automotive', 'Automotive Photography', {
    "AUTO_STUDIO_THREE_QUARTER": {
        "displayName": "Studio Three-Quarter",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Studio three-quarter angle is the automotive industry standard: maximum sharpness throughout, even strobe lighting. Polarising filter essential to manage paint reflections.",
        "proTip": "Use a polariser to control paint reflections from overhead softboxes. Rotate it to the position that creates the most flattering highlight travel across the hood and door panels.",
        "commonMistake": "Leaving visible softbox reflections in the paint without shaping them — professional automotive shots require a smooth, controlled highlight band across the panels.",
        "tags": ["automotive", "studio", "three-quarter", "commercial", "strobe"]
    },
    "AUTO_OUTDOOR_OVERCAST": {
        "displayName": "Outdoor Overcast",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/200",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Overcast sky is perfect natural light for cars: no harsh specular highlights or hard shadows, even illumination of all paint surfaces, and rich colour saturation.",
        "proTip": "Seek out a clean backdrop — wet tarmac, a simple wall, or empty car park. Reflections of the sky in dark paint add depth. Shoot low to the ground to remove horizon clutter.",
        "commonMistake": "Dismissing overcast days and waiting for sun — professional car photographers prefer overcast because it eliminates the hardest reflections to manage.",
        "tags": ["automotive", "outdoor", "overcast", "natural light", "car"]
    },
    "AUTO_TRACKING_SHOT": {
        "displayName": "Tracking / Rolling Shot",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/30",
        "mode": "M", "afMode": "continuous", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Camera car or panning at low shutter: 1/30s blurs rotating wheels and road surface creating the motion impression while keeping the body sharp with subject-tracking AF.",
        "proTip": "Use a fluid head on a camera car for smooth tracking. The car being photographed should travel at 40-60km/h for convincing wheel blur at 1/30s. Multiple passes needed.",
        "commonMistake": "Using too fast a shutter speed — 1/200s freezes wheels completely, which paradoxically makes the car look stationary. Wheel blur is essential for the motion aesthetic.",
        "tags": ["automotive", "tracking", "rolling shot", "motion", "panning"]
    },
    "AUTO_INTERIOR_DETAIL": {
        "displayName": "Interior Detail",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/80",
        "mode": "Av", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "Dashboard, steering wheel, gear selector: mixed LED display and ambient headliner light. f/5.6 provides DOF for the dashboard span. ISO 400 handles the lower light levels.",
        "proTip": "Use a wide-to-standard prime (24-50mm) rather than an ultra-wide — interior details distort badly at 12-16mm. Light the headliner with a small off-camera LED for even coverage.",
        "commonMistake": "Shooting interiors in direct sunlight — harsh stripes of light across seats and dashboard. Always shoot with all doors closed using a supplemental LED for clean, even light.",
        "tags": ["automotive", "interior", "dashboard", "detail", "car"]
    },
    "AUTO_GOLDEN_HOUR_GLAMOUR": {
        "displayName": "Golden Hour Glamour",
        "ISO": 100, "aperture": 5.6, "shutterSpeed": "1/250",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Warm directional side light, intentional lens flare, and rich shadow depth. A 15-minute window at golden hour creates automotive images that cannot be replicated at any other time.",
        "proTip": "Position the car so the sun rakes across the hood at 30-45 degrees. Intentional sun flares add cinematic quality — remove the lens hood for this effect.",
        "commonMistake": "Arriving on location without scouting the sun angle in advance — the golden hour window is only 15-20 minutes and you cannot afford to spend it finding the right angle.",
        "tags": ["automotive", "golden hour", "outdoor", "glamour", "light"]
    },
    "AUTO_NIGHT_LIGHT_TRAILS": {
        "displayName": "Night with Light Trails",
        "ISO": 100, "aperture": 11, "shutterSpeed": "15",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Static car composition: 15s exposure captures light trails from passing traffic creating dynamic energy around a stationary vehicle. f/11 keeps the car sharp throughout.",
        "proTip": "Light the car itself with a separate speedlight during the exposure — a single pop of off-camera flash illuminates the car while the long exposure captures trailing ambient light.",
        "commonMistake": "Expecting consistent light trails from the first attempt — this technique requires multiple exposures as traffic pattern varies. Plan on 15-30 attempts to get clean trails.",
        "tags": ["automotive", "night", "light trails", "long exposure", "car"]
    }
})

# PRODUCT ---------------------------------------------------------------------
write_genre('product', 'Product Photography', {
    "PRODUCT_WHITE_BACKGROUND": {
        "displayName": "White Background Studio",
        "ISO": 100, "aperture": 16, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Amazon and e-commerce standard: f/16 maximum depth of field across entire product, strobe balanced for pure white background. Over-expose background by 2 stops on separate circuit.",
        "proTip": "Use two background lights at equal power to blow the background pure white without spill onto the product. Main product light from above at 45-degree angle. Check all four corners of background for grey.",
        "commonMistake": "Relying on retouching to make the background white — it is far faster and more consistent to nail pure white in-camera with correct lighting ratios.",
        "tags": ["product", "white background", "e-commerce", "studio", "strobe"]
    },
    "PRODUCT_LIFESTYLE_NATURAL": {
        "displayName": "Lifestyle Natural Light",
        "ISO": 200, "aperture": 5.6, "shutterSpeed": "1/200",
        "mode": "Av", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Product in a lifestyle context: natural light, shallow DOF creates warmth and context. Shows the product being used or placed in a real environment rather than isolated.",
        "proTip": "Build a mini lifestyle set that tells a story — the product surrounded by relevant supporting objects at natural proportions. Use window light from the side for depth and warmth.",
        "commonMistake": "Choosing a background that distracts from the product — the product should always be the primary subject. Backgrounds should support, not compete.",
        "tags": ["product", "lifestyle", "natural light", "context", "brand"]
    },
    "PRODUCT_REFLECTIVE_SURFACE": {
        "displayName": "Reflective Surface Product",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Jewellery and glass: light tent or sweep diffuser eliminates specular reflections from strobe. The product surface reflects everything — you and the camera must be hidden.",
        "proTip": "Use a light tent or shoot through a hole in a V-flat. Polarising filter over lens and strobe in tandem can eliminate reflections. Work on acrylic mirror surface for controlled reflections.",
        "commonMistake": "Seeing the camera or photographer reflected in the product surface — always check the product for unwanted reflections before shooting. Use a black V-flat with a hole for the lens.",
        "tags": ["product", "jewellery", "glass", "reflective", "light tent"]
    },
    "PRODUCT_DARK_DRAMATIC": {
        "displayName": "Dark Dramatic Product",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Dark background with single controlled strobe creates high-contrast drama that positions product as premium. Common for spirits, fragrances, and luxury goods.",
        "proTip": "A single strip softbox to one side at 70-90 degrees creates a sharp light-to-shadow transition that defines the product shape dramatically. Black cards absorb spill light.",
        "commonMistake": "Using a soft, flat lighting setup on a dark background — without contrast and shadow depth the product appears flat. Hard directional light is essential for this look.",
        "tags": ["product", "dark background", "dramatic", "premium", "luxury"]
    },
    "PRODUCT_BEVERAGE_BACKLIT": {
        "displayName": "Beverage Backlit",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Drinks photography from behind creates the backlit glass effect — light passes through the liquid illuminating colour and translucency. Signature technique for spirits and wine.",
        "proTip": "Place the strobe or LED directly behind the glass at the same height. A hair light from above creates rim separation. Use a black background for maximum colour saturation in the glass.",
        "commonMistake": "Placing the light in front of the drink — this shows only the surface, not the glowing translucent quality that makes beverage photography compelling.",
        "tags": ["product", "beverage", "backlit", "drinks", "spirits"]
    },
    "PRODUCT_SCALE_COMPARISON": {
        "displayName": "Scale Comparison Shot",
        "ISO": 100, "aperture": 16, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": True, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Size reference shot: maximum DOF to keep both product and scale reference in sharp focus. Consistent lighting and clean background for series shooting.",
        "proTip": "Use a ruler, coin, or common object for scale. Keep camera perfectly level for consistency across a product range. Document all camera and light settings for matched reshoots.",
        "commonMistake": "Changing camera position or height between similar products in a range — inconsistent perspective makes comparison charts look unprofessional.",
        "tags": ["product", "scale", "size reference", "e-commerce", "catalogue"]
    }
})

# CONCERT ---------------------------------------------------------------------
write_genre('concert', 'Concert and Live Music Photography', {
    "CONCERT_LARGE_ARENA": {
        "displayName": "Large Arena Concert",
        "ISO": 12800, "aperture": 2.8, "shutterSpeed": "1/500",
        "mode": "M", "afMode": "continuous", "afPoint": "face",
        "metering": "spot", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Arena concerts: highest available ISO and fastest shutter to freeze moving performers under harsh, directional stage lighting. f/2.8 required for any meaningful exposure.",
        "proTip": "Anticipate the lighting changes — most shows have predictable light cues. A bright spotlight hit on the performer is peak moment. Meter constantly and adjust between songs.",
        "commonMistake": "Waiting passively for the shot — concert photography demands aggressive positioning in the pit, anticipating the peak moment, and constant ISO adjustments as lighting changes.",
        "tags": ["concert", "arena", "live music", "stage", "performer"]
    },
    "CONCERT_INTIMATE_VENUE": {
        "displayName": "Intimate Small Venue",
        "ISO": 6400, "aperture": 1.8, "shutterSpeed": "1/250",
        "mode": "M", "afMode": "continuous", "afPoint": "face",
        "metering": "spot", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Small venues and clubs have lower ceilings that bounce ambient stage light more evenly. f/1.8 prime preferred for maximum light gathering capability. ISO 6400 manageable on modern sensors.",
        "proTip": "Position at the front end of the bar or at a table side-angle for a less formal, more intimate perspective. f/1.8 primes (35mm or 50mm) outperform f/2.8 zooms for this shooting environment.",
        "commonMistake": "Shooting from the back of the venue to avoid intrusion — the resulting images are small, distant, and lack the energy of the performance. Get closer, be respectful, and shoot during songs not between.",
        "tags": ["concert", "small venue", "intimate", "club", "live music"]
    },
    "CONCERT_DRAMATIC_BACKLIT": {
        "displayName": "Dramatic Backlit Stage",
        "ISO": 3200, "aperture": 2.8, "shutterSpeed": "1/250",
        "mode": "M", "afMode": "continuous", "afPoint": "face",
        "metering": "spot", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Backlit performer against intense stage wash: expose for the face using spot metering, not for the lights. This creates the silhouette-edge look with retained facial detail.",
        "proTip": "Use spot metering on the face and lock exposure. The background lights will blow out slightly — that is intentional and part of the aesthetic. Shoot RAW for highlight recovery options.",
        "commonMistake": "Spot metering on the bright background lights rather than the performer's face — this underexposes the face to a silhouette. Face metering only for this technique.",
        "tags": ["concert", "backlit", "stage lighting", "dramatic", "performer"]
    },
    "CONCERT_FESTIVAL_DAYTIME": {
        "displayName": "Festival Daytime Stage",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/1000",
        "mode": "Av", "afMode": "continuous", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Outdoor festival daylight: near-standard daylight conditions on an open-air stage. Fast shutter needed for performer movement. f/5.6 covers depth across moving subjects.",
        "proTip": "Use the longer end of a zoom (70-200mm f/2.8) to isolate the performer from the crowd and tighten the frame. Golden hour afternoon shows produce the best light.",
        "commonMistake": "Using concert night settings outdoors — ISO 12800 and f/2.8 will grossly overexpose in bright festival daylight. Adapt to the available light rather than using a preset blindly.",
        "tags": ["concert", "festival", "outdoor", "daylight", "live music"]
    },
    "CONCERT_PYROTECHNICS": {
        "displayName": "Pyrotechnics and Fire",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/1000",
        "mode": "M", "afMode": "continuous", "afPoint": "wide",
        "metering": "spot", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Pyrotechnic bursts are extremely bright — expose for the fire burst itself, not for the performer. 1/1000s freezes the burst. ISO 100 prevents the bloom from overexposing.",
        "proTip": "Watch the show in rehearsal or the first night to learn where and when pyrotechnics fire. Position to keep the performer in frame with the burst. The anticipation shot beats the reaction shot.",
        "commonMistake": "Using concert night-mode settings (ISO 12800) when pyrotechnics fire — the burst grossly overexposes at high ISO. Switch to ISO 100 when fire effects are programmed.",
        "tags": ["concert", "pyrotechnics", "fire", "burst", "stage effects"]
    },
    "CONCERT_ACOUSTIC_INTIMATE": {
        "displayName": "Acoustic Intimate Performance",
        "ISO": 3200, "aperture": 1.8, "shutterSpeed": "1/125",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "spot", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "Folk and acoustic sets in dimly lit venues with relatively low, controlled ambient light and slower performer movement. 1/125s sufficient. Quieter driveMode is more respectful.",
        "proTip": "For solo acoustic performers, single drive mode and thoughtful shot selection during natural breaks is more respectful and often yields better images than burst shooting.",
        "commonMistake": "Using burst mode during quiet acoustic songs — the sound of the shutter burst is audible, disruptive to the performance and audience, and unnecessary for slow-moving subjects.",
        "tags": ["concert", "acoustic", "folk", "intimate", "performance"]
    }
})

# UNDERWATER ------------------------------------------------------------------
write_genre('underwater', 'Underwater Photography', {
    "UNDERWATER_SHALLOW_REEF": {
        "displayName": "Shallow Reef 0-10m",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/250",
        "mode": "Av", "afMode": "continuous", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "0-10m depth: ambient natural light remains significant. Correct for the blue/cyan cast in post (warm up 500-1500K). f/5.6 provides DOF across reef subjects.",
        "proTip": "Position yourself so the sun is behind and above you for best natural lighting on subjects. Red and orange tones disappear below 5m — add a red filter or use strobe for accurate colour.",
        "commonMistake": "Not correcting the colour cast in post — underwater images shot in ambient light will have a heavy blue-green cast that removes all warm tones from the subject.",
        "tags": ["underwater", "reef", "shallow", "scuba", "ocean"]
    },
    "UNDERWATER_DEEP_MACRO": {
        "displayName": "Deep Macro with Strobe",
        "ISO": 1600, "aperture": 2.8, "shutterSpeed": "1/200",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Deep macro beyond 20m: strobe is mandatory for colour. Fast shutter 1/200s reduces backscatter from particles in the water column. f/2.8 at macro distances provides adequate DOF.",
        "proTip": "Position strobes wide at 45-degree angles rather than pointing direct — this side-lighting minimises backscatter from particles between lens and subject. Move slowly to avoid disturbing sediment.",
        "commonMistake": "Pointing strobes directly at the subject — forward-facing strobe illuminates every particle in the water column, creating a blizzard of backscatter. Side-angle lighting is essential.",
        "tags": ["underwater", "macro", "strobe", "deep", "backscatter"]
    },
    "UNDERWATER_WIDE_PELAGIC": {
        "displayName": "Wide Angle Pelagic",
        "ISO": 800, "aperture": 5.6, "shutterSpeed": "1/500",
        "mode": "Tv", "afMode": "continuous", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Blue water open ocean with large subjects (sharks, mantas, whale sharks): fast shutter for unpredictable subject movement. Wide angle captures the animal in its environment.",
        "proTip": "Get close and shoot wide — a 10-17mm fisheye or 8-15mm at 1-2m from a large subject creates far more dramatic results than a telephoto from range. Approach slowly and steadily.",
        "commonMistake": "Trying to use too long a focal length underwater — water reduces contrast and sharpness with distance. Getting physically close with a wide lens always beats shooting from range.",
        "tags": ["underwater", "wide angle", "pelagic", "shark", "ocean"]
    },
    "UNDERWATER_SILHOUETTE": {
        "displayName": "Silhouette Against Surface",
        "ISO": 200, "aperture": 8, "shutterSpeed": "1/500",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Classic underwater technique: expose for the bright surface directly above, which silhouettes any subject below. Fast shutter and f/8 prevent the surface from overexposing.",
        "proTip": "Shoot upward from just below the subject with the sun behind and above creating a bright sunburst through the surface. The subject's identity is revealed by shape alone.",
        "commonMistake": "Exposing for the subject itself — this overexposes the bright surface to pure white. Always expose for the surface and let the subject silhouette naturally.",
        "tags": ["underwater", "silhouette", "surface", "backlit", "ocean"]
    },
    "UNDERWATER_REEF_UPWARD": {
        "displayName": "Reef Looking Upward",
        "ISO": 400, "aperture": 8, "shutterSpeed": "1/500",
        "mode": "Av", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Looking up through coral reef structure toward the surface: fast shutter to freeze water surface motion patterns. f/8 keeps both the reef in foreground and the surface in focus.",
        "proTip": "Use a fisheye lens or ultra-wide to maximise the sense of looking up through a coral forest. Time the shot when surface ripple patterns are most graphic and dynamic.",
        "commonMistake": "Using too slow a shutter on the upward shot — the water surface constantly moves and blurs at 1/125s. Use 1/500s minimum for sharp surface texture.",
        "tags": ["underwater", "upward", "reef", "surface", "coral"]
    },
    "UNDERWATER_CAVERN": {
        "displayName": "Underwater Cavern",
        "ISO": 3200, "aperture": 2.8, "shutterSpeed": "1/125",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Underwater cave and cavern environments: torch and strobe light only, slow movement to avoid disturbing sediment, maximum available sensitivity.",
        "proTip": "Cavern photography requires two light sources minimum for safety. Position your torch to create a light beam through the cavern as a compositional element. Move slowly — disturbed sediment ruins visibility for 30 minutes.",
        "commonMistake": "Fin-kicking near the cavern floor — sediment disturbed by fins creates a brown-out that ruins visibility for every diver in the group. All movement must be controlled and deliberate.",
        "tags": ["underwater", "cavern", "cave", "torch", "technical diving"]
    }
})

# DRONE -----------------------------------------------------------------------
write_genre('drone', 'Drone and Aerial Photography', {
    "DRONE_BRIGHT_DAY_STILLS": {
        "displayName": "Bright Day Stills",
        "ISO": 100, "aperture": 5.6, "shutterSpeed": "1/1000",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Standard daytime drone stills: fast shutter counters drone vibration and any residual gimbal micro-movement. ISO 100 for maximum sensor quality at altitude.",
        "proTip": "Check gimbal calibration before each flight. Dial in exposure before ascending — sky at 100m EV is typically 14-15. Use AEB bracketing for high-contrast coastal or urban scenes.",
        "commonMistake": "Using slow shutter speeds at altitude — even a stabilised drone at 1/100s produces visible motion blur in stills. Use 1/1000s minimum for sharp drone stills.",
        "tags": ["drone", "aerial", "daylight", "stills", "UAV"]
    },
    "DRONE_GOLDEN_HOUR": {
        "displayName": "Golden Hour Aerial",
        "ISO": 200, "aperture": 5.6, "shutterSpeed": "1/500",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Golden hour light quality from altitude is different from ground level — longer shadows create topographic texture across landscape, city, or coastal terrain.",
        "proTip": "Launch 20 minutes before golden hour begins — ascending to altitude takes time and the window is short. Pre-plan compositions using Google Earth and sun position apps.",
        "commonMistake": "Launching at the start of golden hour — by the time the drone reaches altitude and you find composition, the best light has passed. Launch early and be ready.",
        "tags": ["drone", "aerial", "golden hour", "landscape", "UAV"]
    },
    "DRONE_BLUE_HOUR": {
        "displayName": "Blue Hour Low Light",
        "ISO": 400, "aperture": 2.8, "shutterSpeed": "1/100",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "City lights emerging against deep blue sky during blue hour. The 20-minute window after golden hour. 1/100s is the lowest practical shutter for moving drone without unacceptable blur.",
        "proTip": "Most DJI gimbals have 1/100s as a practical minimum for sharp stills. Use noise reduction on RAW files in post — blue hour ISO 400 is very manageable on modern drone sensors.",
        "commonMistake": "Flying past the blue hour window into full dark — city light photography at night loses the sky detail and requires longer exposures that exceed drone stability limits.",
        "tags": ["drone", "aerial", "blue hour", "city lights", "UAV"]
    },
    "DRONE_COASTAL_WATER": {
        "displayName": "Coastal and Water",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/1000",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Bright coastal scenes and water reflections: maximum shutter to freeze wave motion and prevent reflection blurring. f/8 for complete sharpness across the entire frame.",
        "proTip": "Polarising filter adapter (available for some drones) significantly improves water colour saturation and cuts surface glare. Position to keep sun at 90 degrees to the water for maximum effect.",
        "commonMistake": "Shooting directly into the sun over water — the specular reflection overexposes massively. Keep the sun behind or to the side when shooting reflective water surfaces.",
        "tags": ["drone", "aerial", "coastal", "water", "ocean"]
    },
    "DRONE_URBAN_GRID": {
        "displayName": "Urban Grid Top-Down",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/500",
        "mode": "M", "afMode": "single", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "90-degree straight-down nadir shot: urban grid patterns, road intersections, building roof patterns. Maximum sharpness and zero motion blur from a stable hover.",
        "proTip": "Set the gimbal to exactly 90 degrees (nadir) and hold a stable hover for 3-5 seconds before shooting. Shoot in calm wind conditions only — any wind movement at nadir creates disorienting blur.",
        "commonMistake": "Attempting nadir shots in gusty wind — the rotor wash pattern changes with gusts and the hovering stability required for clean nadir shots is not achievable.",
        "tags": ["drone", "aerial", "nadir", "urban", "top-down", "geometry"]
    },
    "DRONE_SUBJECT_TRACKING": {
        "displayName": "Subject Tracking Mode",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/1000",
        "mode": "Tv", "afMode": "continuous", "afPoint": "wide",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Subject and drone both moving: combined motion requires extra shutter speed. Subject tracking mode on modern drones uses AI recognition to maintain framing automatically.",
        "proTip": "Test ActiveTrack or equivalent subject tracking in a low-risk area before using it on important subjects. The drone follows a AI-identified subject — verify it has locked correctly before committing to a flight path.",
        "commonMistake": "Trusting subject tracking without verification — AI tracking can lose the subject and switch to a different object. Always monitor the tracking lock indicator and be ready to take manual control.",
        "tags": ["drone", "aerial", "tracking", "subject", "follow me", "action"]
    }
})

# NEWBORN / FAMILY ------------------------------------------------------------
write_genre('newborn', 'Newborn and Family Photography', {
    "FAMILY_OUTDOOR_GROUP": {
        "displayName": "Family Outdoor Group",
        "ISO": 100, "aperture": 5.6, "shutterSpeed": "1/250",
        "mode": "Av", "afMode": "continuous", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Family of 4-8 people: f/5.6 provides depth across all faces regardless of depth arrangement. 1/250s stops children moving. Continuous shooting captures genuine interactions.",
        "proTip": "Give the family a task rather than asking them to pose — run toward camera, whisper something to each other, walk and hold hands. Genuine interaction always beats forced posing.",
        "commonMistake": "Trying to get everyone to look at the camera simultaneously — this produces stiff, formal images. Capture the family interacting with each other for warmth and authenticity.",
        "tags": ["family", "outdoor", "group", "portrait", "natural"]
    },
    "NEWBORN_POSED_STUDIO": {
        "displayName": "Newborn Posed Studio",
        "ISO": 400, "aperture": 5.6, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "silent_single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Fully controlled studio, consistent artificial light, complete control over all variables. Never use flash on newborns — continuous LED or fluorescent only. Silent electronic shutter prevents startle reflex.",
        "proTip": "Warm the studio to 26-28C so the baby stays settled during posing. White noise played from a speaker helps maintain settled sleep. Work slowly with an assistant — safety during posing is paramount.",
        "commonMistake": "Rushing posing setups — a settled newborn can be moved but takes 10-20 minutes to resettle after being disturbed. Patience and slowness produce far better results than working quickly.",
        "tags": ["newborn", "posed", "studio", "baby", "LED", "silent shutter"]
    },
    "TODDLER_CANDID": {
        "displayName": "Toddler Candid",
        "ISO": 1600, "aperture": 2.8, "shutterSpeed": "1/500",
        "mode": "Av", "afMode": "continuous", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "Toddlers move fast and unpredictably. High shutter, maximum aperture, and high ISO accept the trade-off of noise for consistently sharp expressions at peak movement.",
        "proTip": "Get down to the child's eye level. Let the child lead the play and photograph from behind a phone or toy — direct camera attention often stops natural behaviour cold.",
        "commonMistake": "Trying to direct toddlers — they do not respond to positioning instructions. Follow the child with the camera. Anticipate, do not react.",
        "tags": ["toddler", "candid", "children", "action", "family"]
    },
    "FAMILY_INDOOR_WINDOW": {
        "displayName": "Family Indoor Window Light",
        "ISO": 800, "aperture": 2.8, "shutterSpeed": "1/160",
        "mode": "Av", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 1,
        "rationale": "Soft directional window light, no flash, warmth and naturalness. The single window creates dimensional lighting that flatters faces while maintaining the warmth of the home environment.",
        "proTip": "Position family within 2m of a large window. A white wall or reflector opposite the window fills the shadow side softly. Check white balance — window light shifts throughout the day.",
        "commonMistake": "Using fill flash which destroys the natural window light quality and introduces mixed colour temperature. Embrace the natural light direction, use a reflector if fill is needed.",
        "tags": ["family", "indoor", "window light", "natural", "home"]
    },
    "SIBLING_INTERACTION": {
        "displayName": "Sibling Interaction",
        "ISO": 800, "aperture": 4, "shutterSpeed": "1/320",
        "mode": "Av", "afMode": "continuous", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Multiple children: f/4 minimum for depth across two faces side by side. 1/320s freezes active play. Faces at different depths require more DOF than single-subject photography.",
        "proTip": "Give siblings a shared activity — building something, looking at a book, running together. The interaction between siblings creates visual relationships that posed shots cannot replicate.",
        "commonMistake": "Shooting at f/2.0 when two children are side by side — the near child is sharp and the far child falls out of focus. f/4 minimum when faces are in the same plane.",
        "tags": ["siblings", "family", "children", "candid", "interaction"]
    },
    "MATERNITY_BACKLIT": {
        "displayName": "Maternity Backlit Silhouette",
        "ISO": 100, "aperture": 2.8, "shutterSpeed": "1/400",
        "mode": "M", "afMode": "single", "afPoint": "centre",
        "metering": "spot", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Backlit silhouette at golden hour — the bump and form are revealed by side lighting against a bright background. Spot meter the bright background to ensure correct silhouette exposure.",
        "proTip": "Position the subject so the setting sun is directly behind and to the slightly to the side, creating a rim light. The profile shot reveals the bump form most clearly.",
        "commonMistake": "Shooting from the front with backlight — this creates an exposed face against a blown background. The profile or three-quarter view is required for the backlit silhouette technique.",
        "tags": ["maternity", "pregnancy", "silhouette", "backlit", "golden hour"]
    }
})

# FASHION / BEAUTY ------------------------------------------------------------
write_genre('fashion', 'Fashion and Beauty Photography', {
    "BEAUTY_CLOSEUP_STUDIO": {
        "displayName": "Beauty Close-Up Studio",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Maximum sharpness is required for skin texture and makeup detail in beauty close-ups. f/11 ensures pores, lashes, and lip texture are all rendered with clinical precision.",
        "proTip": "Use a 100mm macro or 85mm portrait lens at 1m distance for a flattering perspective at this DOF. Clamshell lighting (two softboxes at 45 degrees above and below) eliminates shadows on the face.",
        "commonMistake": "Shooting beauty close-ups at f/2.8 — one eye is sharp and the other falls out of focus. For close facial work, f/8-f/11 is required to keep the full face in the plane of focus.",
        "tags": ["beauty", "closeup", "studio", "makeup", "skin texture"]
    },
    "FASHION_FULL_LENGTH": {
        "displayName": "Fashion Full Length",
        "ISO": 100, "aperture": 8, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Head to toe full-length fashion: f/8 keeps both face and shoes sharp. Even softbox key lighting provides technical perfection from crown to sole. 1/160s syncs with strobe.",
        "proTip": "Shoot at model's hip height, not eye level — this elongates the legs in the frame. Use an even, large softbox to eliminate specular highlights on fabric that read as technical highlights in print.",
        "commonMistake": "Shooting from above eye level — this foreshortens legs and is unflattering for fashion. Camera should be at mid-body or below for full-length fashion photography.",
        "tags": ["fashion", "full length", "studio", "strobe", "commercial"]
    },
    "FASHION_HIGH_KEY": {
        "displayName": "High Key Fashion",
        "ISO": 100, "aperture": 11, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 2,
        "rationale": "Pure white background, airy editorial look. Over-expose the background by 2 stops on a separate circuit. Maximum DOF from f/11 ensures no detail is lost in a high-key technical shot.",
        "proTip": "Use two background lights at equal power aimed directly at the white sweep, balanced to remain 2 stops above the key light. Clean separation matters: meter the background and subject independently.",
        "commonMistake": "Letting background spill onto the subject creating a halo wash — position the subject 2 metres from the background and use flags to control background light spill onto the model.",
        "tags": ["fashion", "high key", "white background", "airy", "editorial"]
    },
    "FASHION_DARK_EDITORIAL": {
        "displayName": "Dark Editorial",
        "ISO": 400, "aperture": 4, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_low",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 3,
        "rationale": "Dark dramatic editorial: single hard light source creating deep, defined shadows. f/4 provides subject-background separation on a dark sweep while keeping the face sharp.",
        "proTip": "A single fresnel spotlight or bare strobe from 90 degrees at the same height as the face creates the hard directional shadows that define dark editorial. Deep shadows are the point, not a mistake.",
        "commonMistake": "Adding fill light to soften the shadows — dark editorial requires courage to let shadows be deep and black. Any fill light immediately softens the intended aesthetic.",
        "tags": ["fashion", "editorial", "dark", "dramatic", "hard light"]
    },
    "BEAUTY_RING_LIGHT": {
        "displayName": "Beauty Ring Light",
        "ISO": 100, "aperture": 5.6, "shutterSpeed": "1/160",
        "mode": "M", "afMode": "single", "afPoint": "face",
        "metering": "evaluative", "driveMode": "single",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": False,
        "difficulty": 1,
        "rationale": "Ring light: circular catch-lights in both eyes, even facial illumination, the signature look of commercial beauty and social media fashion photography.",
        "proTip": "Position the ring light exactly at camera height with the lens through the centre. The circular catch-light in both eyes is the identifiable signature of this technique — check it carefully before shooting.",
        "commonMistake": "Using the ring light at an angle — this eliminates the circular catch-light that defines ring light photography and creates uneven, unflattering illumination across the face.",
        "tags": ["beauty", "ring light", "catch light", "fashion", "social media"]
    },
    "FASHION_OUTDOOR_URBAN": {
        "displayName": "Street Fashion Urban",
        "ISO": 400, "aperture": 4, "shutterSpeed": "1/500",
        "mode": "Av", "afMode": "continuous", "afPoint": "face",
        "metering": "evaluative", "driveMode": "continuous_high",
        "requiresTripod": False, "requiresTracking": False,
        "requiresNDFilter": False, "ibisBonus": True,
        "difficulty": 2,
        "rationale": "Street fashion in the urban environment: ambient city light, natural setting, movement. 1/500s freezes garment movement and walking. f/4 provides subject separation from urban background.",
        "proTip": "Scout locations for interesting background texture, colour, and depth. Shoot between pedestrian crowds. Overcast days work as well as golden hour for consistent results across a series.",
        "commonMistake": "Shooting at high noon with harsh shadows across the face — find open shade or wait for a cloudy break. Harsh facial shadows are impossible to remove cleanly in post.",
        "tags": ["fashion", "outdoor", "urban", "street", "lifestyle"]
    }
})


# ─────────────────────────────────────────────────────────────────────────────
# UPDATE index.js
# ─────────────────────────────────────────────────────────────────────────────
index_path = os.path.join(PRESETS_DIR, 'index.js')
new_index = """module.exports = {
  portrait:       require('./portrait.json'),
  landscape:      require('./landscape.json'),
  astro:          require('./astro.json'),
  wildlife:       require('./wildlife.json'),
  sports:         require('./sports.json'),
  macro:          require('./macro.json'),
  indoorlowlight: require('./indoorlowlight.json'),
  goldenhour:     require('./goldenhour.json'),
  street:         require('./street.json'),
  architecture:   require('./architecture.json'),
  event:          require('./event.json'),
  travel:         require('./travel.json'),
  food:           require('./food.json'),
  realestate:     require('./realestate.json'),
  automotive:     require('./automotive.json'),
  product:        require('./product.json'),
  concert:        require('./concert.json'),
  underwater:     require('./underwater.json'),
  drone:          require('./drone.json'),
  newborn:        require('./newborn.json'),
  fashion:        require('./fashion.json'),
};
"""
with open(index_path, 'w') as f:
    f.write(new_index)
print('  updated api/src/data/presets/index.js')


# ─────────────────────────────────────────────────────────────────────────────
# UPDATE validate.js VALID_GENRES
# ─────────────────────────────────────────────────────────────────────────────
validate_path = os.path.join(ROOT, 'api', 'src', 'middleware', 'validate.js')
with open(validate_path) as f:
    content = f.read()

old_genres = """const VALID_GENRES = [
  'portrait', 'landscape', 'astro', 'wildlife', 'sports',
  'macro', 'indoorlowlight', 'goldenhour', 'street',
  'architecture', 'event', 'travel'
];"""

new_genres = """const VALID_GENRES = [
  'portrait', 'landscape', 'astro', 'wildlife', 'sports',
  'macro', 'indoorlowlight', 'goldenhour', 'street',
  'architecture', 'event', 'travel',
  'food', 'realestate', 'automotive', 'product',
  'concert', 'underwater', 'drone', 'newborn', 'fashion',
];"""

if old_genres in content:
    content = content.replace(old_genres, new_genres)
    with open(validate_path, 'w') as f:
        f.write(content)
    print('  updated api/src/middleware/validate.js VALID_GENRES')
else:
    print('  WARNING: could not find VALID_GENRES pattern in validate.js — check manually')


print('\n v3 genres and conditions complete.')
