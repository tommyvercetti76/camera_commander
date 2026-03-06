#!/usr/bin/env python3
"""merge_lenses.py — Convert v1 source lens data to v2 schema and merge with existing v2 files."""
import json, re, os

ROOT = "/Users/Rohan/Desktop/camera_project"

def parse_focal(focal_str):
    """'16-35mm' → (16, 35);  '50mm' → (50, 50)"""
    nums = [int(x) for x in re.findall(r'\d+', str(focal_str))]
    if len(nums) >= 2: return nums[0], nums[1]
    if len(nums) == 1: return nums[0], nums[0]
    return 0, 0

def parse_aperture(ap_str):
    """'f/2.8' → (2.8, 2.8); 'f/3.5-5.6' → (3.5, 5.6); 'f/4-5.6' → (4.0, 5.6)"""
    nums = [float(x) for x in re.findall(r'[\d.]+', str(ap_str))]
    if len(nums) >= 2: return nums[0], nums[1]
    if len(nums) == 1: return nums[0], nums[0]
    return 0.0, 0.0

# OIS stop estimates by lens family name patterns (heuristic)
OIS_STOP_HINTS = {
    'IS II USM': 4, 'IS USM': 4, 'IS STM': 4, 'IS II': 4,
    'IS L': 5, 'GM II': 0, 'GM ': 0,
    'OSS': 4, 'OIS': 4,
    'STM': 0,
}

def estimate_ois_stops(lens_name, has_ois):
    if not has_ois: return 0
    name = lens_name.upper()
    if 'IS L' in name or 'L IS' in name: return 5
    if 'IS II' in name: return 4
    if ' IS ' in name or name.endswith(' IS'): return 4
    if 'OSS' in name: return 4
    if 'OIS' in name: return 4
    return 3  # default when IS is present

def guess_filter_thread(focal_min, focal_max, aperture_max):
    """Very rough heuristic for common filter thread sizes."""
    max_ap = aperture_max  # smaller number = wider aperture = bigger front element
    if max_ap <= 1.4:
        if focal_min >= 85: return 77
        return 82
    if max_ap <= 1.8:
        if focal_min >= 50: return 67
        return 58
    if max_ap <= 2.8:
        if focal_min <= 24: return 82
        if focal_min >= 70: return 77
        return 72
    if max_ap <= 4.0:
        if focal_min <= 15: return 82
        if focal_max >= 200: return 77
        return 77
    return 67

def v1_to_v2(lens_v1):
    name = lens_v1['lensName']
    mount = lens_v1.get('mountType', '')
    focal = lens_v1.get('focalLength', '')
    ap_str = lens_v1.get('aperture', 'f/0')
    has_ois = lens_v1.get('imageStabilization', False)
    compatible = lens_v1.get('compatibleCameras', [])

    min_fl, max_fl = parse_focal(focal)
    max_ap, max_ap_tele = parse_aperture(ap_str)
    ois_stops = estimate_ois_stops(name, has_ois)
    filter_thread = guess_filter_thread(min_fl, max_fl, max_ap)

    return {
        "lensName": name,
        "mountType": mount,
        "minFocalLength": min_fl,
        "maxFocalLength": max_fl,
        "maxAperture": max_ap,
        "maxApertureAtTele": max_ap_tele,
        "hasOIS": has_ois,
        "oisStops": ois_stops,
        "filterThread": filter_thread,
        "compatibleCameras": compatible
    }

brands = [
    ("canon", f"{ROOT}/canon_lenses.json", f"{ROOT}/api/src/data/lenses/canon.json"),
    ("sony",  f"{ROOT}/sony_lenses.json",  f"{ROOT}/api/src/data/lenses/sony.json"),
]

for brand, src_path, out_path in brands:
    src_lenses = json.load(open(src_path))
    existing = json.load(open(out_path))
    v2_lenses = existing['lenses']
    v2_names = {l['lensName'] for l in v2_lenses}

    added = 0
    for l in src_lenses:
        if l['lensName'] not in v2_names:
            v2_lenses.append(v1_to_v2(l))
            added += 1

    with open(out_path, 'w') as f:
        json.dump({"lenses": v2_lenses}, f, indent=2)
    print(f"{brand}: added {added} lenses → total {len(v2_lenses)}")

print("Done.")
