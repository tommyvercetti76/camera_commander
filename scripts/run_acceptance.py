#!/usr/bin/env python3
"""Kamera Quest acceptance test runner — executable AUTO tests."""
import json, re, os, glob, sys

ROOT = "api/src/data"
results = []

def p(ac, label, passed, detail=""):
    mark = "PASS" if passed else "FAIL"
    print(f"  [{mark}]  {ac}  {label}" + (f"\n         > {detail}" if detail else ""))
    results.append((ac, passed, detail))
    return passed

def parse_shutter(s):
    s = str(s)
    if '/' in s:
        n, d = s.split('/')
        return float(n) / float(d)
    return float(s)

# ── Load data ─────────────────────────────────────────────────────────────
canon_cams_data = json.load(open(f'{ROOT}/cameras/canon.json'))['cameras']
sony_cams_data  = json.load(open(f'{ROOT}/cameras/sony.json'))['cameras']
canon_lenses    = json.load(open(f'{ROOT}/lenses/canon.json'))['lenses']
sony_lenses     = json.load(open(f'{ROOT}/lenses/sony.json'))['lenses']
canon_cams = {c['modelName'] for c in canon_cams_data}
sony_cams  = {c['modelName'] for c in sony_cams_data}

# ── EV calculator (mirrors api/src/engine/evCalc.js) ─────────────────────
import math
def compute_ev(aperture, shutter_str, iso):
    t = parse_shutter(shutter_str)
    return math.log2((aperture**2) / t) - math.log2(iso / 100)

def apply_ibis_bonus(shutter_str, stops):
    stops = min(stops, 3)  # AC-140 cap
    t = parse_shutter(shutter_str)
    new_t = t * (2 ** stops)
    new_t = min(new_t, 1.0)  # AC-141 cap: never >1s handheld
    # Round to nearest standard shutter
    standards = [1/8000,1/6400,1/5000,1/4000,1/3200,1/2500,1/2000,1/1600,
                 1/1250,1/1000,1/800,1/640,1/500,1/400,1/320,1/250,1/200,
                 1/160,1/125,1/100,1/80,1/60,1/50,1/40,1/30,1/25,1/20,
                 1/15,1/13,1/10,1/8,1/6,1/5,0.25,0.3,0.4,0.5,0.6,0.8,1.0]
    closest = min(standards, key=lambda x: abs(x - new_t))
    if closest < 0.1:
        return f"1/{round(1/closest)}"
    return str(round(closest, 2))

print("\n" + "="*60)
print("  KAMERA QUEST — ACCEPTANCE TESTS (AUTO)")
print("="*60 + "\n")

print("  SUITE 19 — EXPOSURE MATHEMATICS")
print("  " + "-"*56)

# AC-137 Sunny 16 — f/16, 1/125s, ISO 100 → EV ≈ log2(256 * 125) = 14.97
ev = compute_ev(16, "1/125", 100)
p("AC-137", f"Sunny 16 EV≈15 (got {ev:.3f})", 14.8 <= ev <= 15.2)

# AC-138 parseShutterToSeconds
cases = [("1/400",0.0025),("1/8000",0.000125),("30",30.0),("0.5",0.5),("1",1.0)]
all_ok = all(abs(parse_shutter(s)-e) < 0.0001 for s,e in cases)
p("AC-138", "parseShutterToSeconds all cases", all_ok,
  "" if all_ok else str([(s, parse_shutter(s), e) for s,e in cases if abs(parse_shutter(s)-e) >= 0.0001]))

# AC-139 applyIBISBonus 3-stop
r139 = apply_ibis_bonus("1/400", 3)
p("AC-139", f"IBIS 3-stop on 1/400 → 1/50 or 1/60 (got {r139})", r139 in ("1/50","1/60"))

# AC-140 8-stop IBIS capped at 3
r140 = apply_ibis_bonus("1/400", 8)
p("AC-140", f"8-stop IBIS capped at 3 (got {r140})", r140 in ("1/50","1/60"))

# AC-141 IBIS result never >1s
r141 = apply_ibis_bonus("1/30", 3)
p("AC-141", f"IBIS result never >1s (1/30+3stops → {r141})", parse_shutter(r141) <= 1.0+0.01)

# AC-143 EV portrait sunny > night
ev_sunny = compute_ev(2.8, "1/400", 100)
ev_night = compute_ev(1.8, "1/60",  1600)
p("AC-143", f"EV sunny ({ev_sunny:.1f}) > night ({ev_night:.1f})", ev_sunny > ev_night)

# AC-144 ISO monotonically increases with darkness (portrait genre)
portrait = json.load(open(f'{ROOT}/presets/portrait.json'))['conditions']
isos = {k: v['ISO'] for k, v in portrait.items()}
# Verify a reasonable ordering exists
sunny_iso = next((v for k,v in isos.items() if 'SUNNY' in k or 'OUTDOOR' in k), None)
indoor_iso = next((v for k,v in isos.items() if 'INDOOR' in k or 'DIM' in k), None)
night_iso = next((v for k,v in isos.items() if 'NIGHT' in k or 'LOW_LIGHT' in k or 'AMBIENT' in k), None)
if sunny_iso and indoor_iso and night_iso:
    p("AC-144", f"ISO progression: sunny={sunny_iso} indoor={indoor_iso} night={night_iso}",
      sunny_iso < night_iso, f"Expected {sunny_iso} < {night_iso}")
else:
    p("AC-144", f"ISO progression check (sunny={sunny_iso} indoor={indoor_iso} night={night_iso})",
      sunny_iso is not None and night_iso is not None and sunny_iso < night_iso)

print("\n  SUITE 20 — DATA INTEGRITY")
print("  " + "-"*56)

# AC-146 Canon cross-ref
orphans_c = sorted({n for l in canon_lenses for n in l.get('compatibleCameras',[]) if n not in canon_cams and 'sony' not in n.lower()})
p("AC-146", "Canon modelName cross-ref (no orphans)", orphans_c == [], str(orphans_c[:5]) if orphans_c else "")

# AC-147 Sony cross-ref
orphans_s = sorted({n for l in sony_lenses for n in l.get('compatibleCameras',[]) if n not in sony_cams and 'canon' not in n.lower()})
p("AC-147", "Sony modelName cross-ref (no orphans)", orphans_s == [], str(orphans_s[:5]) if orphans_s else "")

# AC-148 No duplicate displayNames
dup_issues = []
for f in sorted(glob.glob(f'{ROOT}/presets/*.json')):
    data = json.load(open(f))
    names = [v.get('displayName','') for v in data.get('conditions',{}).values()]
    seen = set(); dups = []
    for n in names:
        if n in seen: dups.append(n)
        seen.add(n)
    if dups: dup_issues.append(f"{os.path.basename(f)}:{dups}")
p("AC-148", "No duplicate displayNames per genre", dup_issues == [], str(dup_issues))

# AC-149 No cross-brand contamination
cross = []
for l in canon_lenses:
    for n in l.get('compatibleCameras',[]):
        if 'sony' in n.lower() or 'alpha' in n.lower() or ' zv' in n.lower():
            cross.append(f"Canon:{l['lensName']}->{n}")
for l in sony_lenses:
    for n in l.get('compatibleCameras',[]):
        if 'canon' in n.lower() or ' eos ' in n.lower():
            cross.append(f"Sony:{l['lensName']}->{n}")
p("AC-149", "No cross-brand contamination", cross == [], str(cross))

# AC-150 SCREAMING_SNAKE_CASE
bad_keys = []
pat = re.compile(r'^[A-Z][A-Z0-9_]*$')
for f in glob.glob(f'{ROOT}/presets/*.json'):
    data = json.load(open(f))
    bad_keys += [f"{os.path.basename(f)}:{k}" for k in data.get('conditions',{}) if not pat.match(k)]
p("AC-150", "All condition keys SCREAMING_SNAKE_CASE", bad_keys == [], str(bad_keys))

# AC-151 shutterSpeed parseable
bad_ss = []
for f in glob.glob(f'{ROOT}/presets/*.json'):
    data = json.load(open(f))
    for k,v in data.get('conditions',{}).items():
        ss = v.get('shutterSpeed')
        try:
            if parse_shutter(ss) <= 0: bad_ss.append(f"{os.path.basename(f)}/{k}:{ss}")
        except: bad_ss.append(f"{os.path.basename(f)}/{k}: bad '{ss}'")
p("AC-151", "All shutterSpeed parseable", bad_ss == [], str(bad_ss[:3]))

# AC-153 Canon lens count
p("AC-153", f"Canon lens count >= 51 (got {len(canon_lenses)})", len(canon_lenses) >= 51)

# AC-154 Sony lens count
p("AC-154", f"Sony lens count >= 50 (got {len(sony_lenses)})", len(sony_lenses) >= 50)

# AC-155 All required fields present
REQ = ['ISO','aperture','shutterSpeed','mode','afMode','metering','driveMode','requiresTripod','rationale','proTip','commonMistake']
miss = []
for f in glob.glob(f'{ROOT}/presets/*.json'):
    data = json.load(open(f))
    for k,v in data.get('conditions',{}).items():
        m = [x for x in REQ if x not in v]
        if m: miss.append(f"{os.path.basename(f)}/{k}:{m}")
p("AC-155", "All preset conditions have required fields", miss == [], str(miss[:2]))

print("\n  SUITE 01 — IMPLEMENTATION CHECKS")
print("  " + "-"*56)

# AC-097 AbortController in client.js
client_src = ""
try:
    client_src = open("web/src/api/client.js").read()
except: pass
p("AC-097", "AbortController in web/src/api/client.js", "AbortController" in client_src or "timeout" in client_src,
  "Not found — need to add fetch timeout")

# AC-105 AbortController in useGear.js (race condition guard)
gear_src = ""
try:
    gear_src = open("web/src/hooks/useGear.js").read()
except: pass
p("AC-105", "AbortController in useGear.js (race condition)", "AbortController" in gear_src,
  "Not found — rapid brand switching may cause race condition")

# AC-127 CLI --json and --brand flags
cli_src = ""
try:
    cli_src = open("cli/kamera_quest_cli.py").read()
except: pass
p("AC-127", "CLI --json flag implemented", "--json" in cli_src)

# ── Summary ───────────────────────────────────────────────────────────────
total = len(results)
passed = sum(1 for _,ok,_ in results if ok)
failed = total - passed
print(f"\n{'='*60}")
print(f"  RESULT: {passed}/{total} PASSED  |  {failed} FAILED")
failures = [(ac,d) for ac,ok,d in results if not ok]
if failures:
    print(f"\n  FAILURES (requires fixes):")
    for ac,d in failures:
        print(f"    [{ac}] {d[:100]}")
print("="*60)
sys.exit(0 if failed == 0 else 1)
