const { z } = require('zod');

// Valid brands — extend this list when new brands are added to data/
const VALID_BRANDS = ['canon', 'sony'];

// Valid genre keys — must match keys in api/src/data/presets/index.js
const VALID_GENRES = [
  'portrait', 'landscape', 'astro', 'wildlife', 'sports',
  'macro', 'indoorlowlight', 'goldenhour', 'street',
  'architecture', 'event', 'travel'
];

// Valid modes — these are the four user archetypes
const VALID_MODES = ['apprentice', 'enthusiast', 'craftsperson', 'professional'];

const ClassicPresetSchema = z.object({
  brand:       z.string().toLowerCase().refine(v => VALID_BRANDS.includes(v), {
                 message: `brand must be one of: ${VALID_BRANDS.join(', ')}`
               }),
  cameraModel: z.string().min(2).max(120),
  lensName:    z.string().min(2).max(120),
  genre:       z.string().toLowerCase().refine(v => VALID_GENRES.includes(v), {
                 message: `genre must be one of: ${VALID_GENRES.join(', ')}`
               }),
  condition:   z.string().min(2).max(80).transform(s => s.toUpperCase()),
  mode:        z.enum(VALID_MODES).optional().default('apprentice'),
});

// Gear fields are optional for smart mode — if provided the engine applies
// gear-aware adjustments (IBIS, flash sync, aperture clamping); if omitted
// generic recommendations are returned instead.
const SmartPresetSchema = z.object({
  brand:       z.string().toLowerCase().refine(v => VALID_BRANDS.includes(v), {
                 message: `brand must be one of: ${VALID_BRANDS.join(', ')}`
               }).optional(),
  cameraModel: z.string().min(2).max(120).optional(),
  lensName:    z.string().min(2).max(120).optional(),
  mode:        z.enum(VALID_MODES),
  interests:   z.array(z.string().min(2).max(40)).min(1).max(16),
});

function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      const firstError = result.error.errors[0];
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: firstError.message,
          field: firstError.path.join('.'),
        }
      });
    }
    req.body = result.data;
    next();
  };
}

module.exports = { validate, ClassicPresetSchema, SmartPresetSchema, VALID_GENRES };
