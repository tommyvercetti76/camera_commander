#!/usr/bin/env python3
"""Fix remaining Sony camera values that the first migration pass missed."""
import json

path = 'api/src/data/cameras/sony.json'
s = json.load(open(path))

REMAINING = {
    'Sony Alpha a6300':  {'maxFlashSync': '1/250'},
    'Sony Alpha a6400':  {'maxFlashSync': '1/250'},
    'Sony ZV-E10':       {'maxFlashSync': '1/250'},
    'Sony Alpha a1':     {'maxFlashSync': '1/250'},
    'Sony Alpha a7R IV': {'ibisStops': 5.5},
}

for cam in s['cameras']:
    n = cam['modelName']
    if n in REMAINING:
        for field, val in REMAINING[n].items():
            old = cam.get(field)
            if old != val:
                cam[field] = val
                print(n + ': ' + field + ' ' + str(old) + ' to ' + str(val))

with open(path, 'w') as f:
    json.dump(s, f, indent=2)
    f.write('\n')

print('done')
