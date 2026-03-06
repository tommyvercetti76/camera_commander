#!/usr/bin/env python3
"""Fix invalid afPoint and driveMode values in all preset JSON files."""
import json
import os
import glob

PRESETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'api', 'src', 'data', 'presets'
)

# Mapping of invalid -> valid replacements
# face -> tracking (subject-aware AF point tracking is closest semantic match)
# centre -> wide (wide area AF is the intent for product/food/macro centre shots)
# silent_single -> single (no "silent" driveMode enum; map to single)

fixed = 0
for filepath in sorted(glob.glob(os.path.join(PRESETS_DIR, '*.json'))):
    name = os.path.basename(filepath)
    data = json.load(open(filepath))
    changed = False

    conditions = data.get('conditions', {})
    for cond_key, cond in conditions.items():
        if cond.get('afPoint') == 'face':
            cond['afPoint'] = 'tracking'
            changed = True
            print(name + ' / ' + cond_key + ': afPoint face -> tracking')
        if cond.get('afPoint') == 'centre':
            cond['afPoint'] = 'wide'
            changed = True
            print(name + ' / ' + cond_key + ': afPoint centre -> wide')
        if cond.get('driveMode') == 'silent_single':
            cond['driveMode'] = 'single'
            changed = True
            print(name + ' / ' + cond_key + ': driveMode silent_single -> single')

    if changed:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
        fixed += 1

print('Fixed ' + str(fixed) + ' files.')
