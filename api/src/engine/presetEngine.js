/**
 * presetEngine.js — Core preset resolution logic
 *
 * Given a camera, lens, genre, and condition key, returns a fully resolved
 * preset object with settings adjusted for the specific gear (IBIS, OIS, etc.)
 *
 * The engine reads from data/ files loaded by AGENT-B.
 */

const allPresets = require('../data/presets/index');
const { applyIBISBonus, parseShutterToSeconds, parseMaxShutter } = require('./evCalc');

function resolvePreset(camera, lens, genre, condition) {
  const genreData = allPresets[genre.toLowerCase()];
  if (!genreData) {
    return { error: { code: 'GENRE_NOT_FOUND', message: `Genre not found: ${genre}` } };
  }

  const conditionKey = condition.toUpperCase();
  const base = genreData.conditions[conditionKey];
  if (!base) {
    return { error: { code: 'PRESET_NOT_FOUND', message: `Condition not found: ${condition}` } };
  }

  // Deep clone the preset so we don't mutate cached data
  const preset = Object.assign({}, base);
  preset.genre = genre;
  preset.condition = conditionKey;

  // ── Gear-aware adjustments ──────────────────────────────────────────────────

  // IBIS/OIS bonus — apply if preset benefits from stabilisation
  if (preset.ibisBonus) {
    const cameraIBIS = camera.IBIS ? (camera.ibisStops || 0) : 0;
    const lensOIS    = lens.hasOIS  ? (lens.oisStops || 0)  : 0;
    // Only the better of the two applies (they don't stack for shutter calcs)
    const bestStops  = Math.max(cameraIBIS, lensOIS);
    if (bestStops > 0) {
      const newShutter = applyIBISBonus(preset.shutterSpeed, bestStops);
      // Don't go slower than 1/focal_length handheld rule would allow
      preset.shutterSpeedWithIBIS = newShutter;
      preset.ibisStopsApplied     = bestStops;
    }
  }

  // Flash sync check — warn if preset exceeds camera's max flash sync
  if (camera.maxFlashSync) {
    const syncSeconds  = parseShutterToSeconds(camera.maxFlashSync);
    const presetSeconds = parseShutterToSeconds(preset.shutterSpeed);
    if (presetSeconds < syncSeconds && preset.mode !== 'M') {
      preset.warnings = preset.warnings || [];
      preset.warnings.push(`Shutter ${preset.shutterSpeed} exceeds flash sync ${camera.maxFlashSync}. Use M mode or HSS flash.`);
    }
  }

  // Attach gear info to the response
  preset.camera = {
    modelName:    camera.modelName,
    IBIS:         camera.IBIS,
    ibisStops:    camera.ibisStops || 0,
    weatherSealed: camera.weatherSealed || false,
  };
  preset.lens = {
    lensName: lens.lensName,
    hasOIS:   lens.hasOIS,
    oisStops: lens.oisStops || 0,
  };

  return { preset };
}

// Validate lens is compatible with camera
function validateCompatibility(camera, lens) {
  if (!Array.isArray(lens.compatibleCameras)) return true;
  return lens.compatibleCameras.some(
    c => c.toLowerCase() === camera.modelName.toLowerCase()
  );
}

module.exports = { resolvePreset, validateCompatibility };
