const allPresets = require('../src/data/presets/index');

const REQUIRED_FIELDS = [
  'displayName', 'ISO', 'aperture', 'shutterSpeed', 'mode',
  'afMode', 'afPoint', 'metering', 'driveMode',
  'requiresTripod', 'requiresTracking', 'requiresNDFilter',
  'ibisBonus', 'difficulty', 'rationale', 'proTip',
  'commonMistake', 'tags'
];

const VALID_MODES     = new Set(['Av', 'Tv', 'M', 'P']);
const VALID_AF_MODES  = new Set(['single', 'continuous', 'manual']);
const VALID_AF_POINTS = new Set(['single', 'zone', 'wide', 'tracking']);
const VALID_METERING  = new Set(['evaluative', 'spot', 'center-weighted']);
const VALID_DRIVE     = new Set(['single', 'continuous_low', 'continuous_high']);

describe('Preset data integrity', () => {
  test('all 12 genres are present', () => {
    const expected = [
      'portrait', 'landscape', 'astro', 'wildlife', 'sports',
      'macro', 'indoorlowlight', 'goldenhour', 'street',
      'architecture', 'event', 'travel'
    ];
    for (const genre of expected) {
      expect(allPresets).toHaveProperty(genre);
    }
  });

  for (const [genre, genreData] of Object.entries(allPresets)) {
    describe(`genre: ${genre}`, () => {
      test('has conditions object', () => {
        expect(genreData).toHaveProperty('conditions');
        expect(typeof genreData.conditions).toBe('object');
      });

      test('has at least one condition', () => {
        expect(Object.keys(genreData.conditions).length).toBeGreaterThan(0);
      });

      for (const [condKey, preset] of Object.entries(genreData.conditions || {})) {
        describe(`condition: ${condKey}`, () => {
          test('has all required fields', () => {
            for (const field of REQUIRED_FIELDS) {
              expect(preset).toHaveProperty(field);
            }
          });

          test('mode is valid', () => {
            expect(VALID_MODES.has(preset.mode)).toBe(true);
          });

          test('afMode is valid', () => {
            expect(VALID_AF_MODES.has(preset.afMode)).toBe(true);
          });

          test('afPoint is valid', () => {
            expect(VALID_AF_POINTS.has(preset.afPoint)).toBe(true);
          });

          test('metering is valid', () => {
            expect(VALID_METERING.has(preset.metering)).toBe(true);
          });

          test('driveMode is valid', () => {
            expect(VALID_DRIVE.has(preset.driveMode)).toBe(true);
          });

          test('ISO is a number', () => {
            expect(typeof preset.ISO).toBe('number');
          });

          test('aperture is a number', () => {
            expect(typeof preset.aperture).toBe('number');
          });

          test('shutterSpeed is a string', () => {
            expect(typeof preset.shutterSpeed).toBe('string');
          });

          test('difficulty is 1, 2, or 3', () => {
            expect([1, 2, 3]).toContain(preset.difficulty);
          });

          test('tags is an array', () => {
            expect(Array.isArray(preset.tags)).toBe(true);
          });
        });
      }

      if (genre === 'astro') {
        test('DEEP_SKY_OBJECTS has requiresTracking=true', () => {
          const dso = genreData.conditions['DEEP_SKY_OBJECTS'];
          if (dso) {
            expect(dso.requiresTracking).toBe(true);
          }
        });
      }
    });
  }
});
