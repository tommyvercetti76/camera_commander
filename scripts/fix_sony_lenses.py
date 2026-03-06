#!/usr/bin/env python3
"""fix_sony_lenses.py — Deduplicate sony_lenses.json and add 17 real missing Sony lenses."""
import json

ROOT = "/Users/Rohan/Desktop/camera_project"
path = f"{ROOT}/sony_lenses.json"

# Standard compatible cameras for full-frame (FE) lenses
FF_CAMS = [
    "Sony Alpha a7 III", "Sony Alpha a7R IV", "Sony Alpha a7S III",
    "Sony Alpha a7C", "Sony Alpha a7 IV", "Sony Alpha a1",
    "Sony Alpha a9 II", "Sony Alpha a7R V"
]
# APS-C compatible cameras (also mount FF bodies)
APS_CAMS = FF_CAMS + ["Sony Alpha a6700", "Sony Alpha a6600", "Sony Alpha a6400", "Sony Alpha a6100"]

# 17 real Sony lenses to add
NEW_LENSES = [
    {
        "lensName": "Sony FE 24-105mm f/4 G OSS",
        "focalLength": "24-105mm",
        "aperture": "f/4",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["G-Series", "Weather Sealed", "OSS"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 85mm f/1.8",
        "focalLength": "85mm",
        "aperture": "f/1.8",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": False,
        "specialFeatures": ["Lightweight"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 35mm f/1.8",
        "focalLength": "35mm",
        "aperture": "f/1.8",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": False,
        "specialFeatures": ["Compact", "Lightweight"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 50mm f/1.8",
        "focalLength": "50mm",
        "aperture": "f/1.8",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": False,
        "specialFeatures": ["Lightweight", "Budget-Friendly"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 16-35mm f/4 ZA OSS Vario-Tessar T*",
        "focalLength": "16-35mm",
        "aperture": "f/4",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["Zeiss T* Coating", "OSS", "Weather Sealed"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 300mm f/2.8 GM OSS",
        "focalLength": "300mm",
        "aperture": "f/2.8",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": True,
        "specialFeatures": ["G Master", "Weather Sealed", "OSS"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 100mm f/2.8 STF GM OSS",
        "focalLength": "100mm",
        "aperture": "f/2.8",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": True,
        "specialFeatures": ["G Master", "STF Bokeh", "Weather Sealed", "OSS"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE PZ 28-135mm f/4 G OSS",
        "focalLength": "28-135mm",
        "aperture": "f/4",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["G-Series", "Power Zoom", "Weather Sealed", "OSS"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony E 10-18mm f/4 OSS",
        "focalLength": "10-18mm",
        "aperture": "f/4",
        "mountType": "E",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["APS-C", "Ultra-Wide", "OSS"],
        "compatibleCameras": APS_CAMS
    },
    {
        "lensName": "Sony E 16-70mm f/4 ZA OSS",
        "focalLength": "16-70mm",
        "aperture": "f/4",
        "mountType": "E",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["APS-C", "Zeiss T* Coating", "OSS"],
        "compatibleCameras": APS_CAMS
    },
    {
        "lensName": "Sony E 30mm f/3.5 Macro",
        "focalLength": "30mm",
        "aperture": "f/3.5",
        "mountType": "E",
        "lensType": "Prime",
        "imageStabilization": False,
        "specialFeatures": ["APS-C", "Macro 1:1"],
        "compatibleCameras": APS_CAMS
    },
    {
        "lensName": "Sony E 50mm f/1.8 OSS",
        "focalLength": "50mm",
        "aperture": "f/1.8",
        "mountType": "E",
        "lensType": "Prime",
        "imageStabilization": True,
        "specialFeatures": ["APS-C", "OSS"],
        "compatibleCameras": APS_CAMS
    },
    {
        "lensName": "Sony FE 24-70mm f/2.8 GM",
        "focalLength": "24-70mm",
        "aperture": "f/2.8",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": False,
        "specialFeatures": ["G Master", "Weather Sealed"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 500mm f/4 GM OSS",
        "focalLength": "500mm",
        "aperture": "f/4",
        "mountType": "FE",
        "lensType": "Prime",
        "imageStabilization": True,
        "specialFeatures": ["G Master", "Weather Sealed", "OSS"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony FE 70-400mm f/4-5.6 G SSM II",
        "focalLength": "70-400mm",
        "aperture": "f/4-5.6",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": False,
        "specialFeatures": ["G-Series", "Telephoto"],
        "compatibleCameras": FF_CAMS
    },
    {
        "lensName": "Sony E PZ 18-105mm f/4 G OSS",
        "focalLength": "18-105mm",
        "aperture": "f/4",
        "mountType": "E",
        "lensType": "Zoom",
        "imageStabilization": True,
        "specialFeatures": ["APS-C", "G-Series", "Power Zoom", "OSS"],
        "compatibleCameras": APS_CAMS
    },
    {
        "lensName": "Sony FE 20-70mm f/4 G",
        "focalLength": "20-70mm",
        "aperture": "f/4",
        "mountType": "FE",
        "lensType": "Zoom",
        "imageStabilization": False,
        "specialFeatures": ["G-Series", "Ultra-Wide Standard Zoom"],
        "compatibleCameras": FF_CAMS
    },
]

# Load current source, deduplicate, then append new lenses
src = json.load(open(path))
seen = set()
unique = []
for l in src:
    if l['lensName'] not in seen:
        seen.add(l['lensName'])
        unique.append(l)

print(f"Deduplication: {len(src)} → {len(unique)} unique")

for nl in NEW_LENSES:
    if nl['lensName'] not in seen:
        unique.append(nl)
        seen.add(nl['lensName'])
    else:
        print(f"  SKIP (already present): {nl['lensName']}")

print(f"After adding new lenses: {len(unique)} total")

with open(path, 'w') as f:
    json.dump(unique, f, indent=2)
print(f"Wrote {path}")
