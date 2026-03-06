/**
 * Generates a PNG share card for a preset result using the Canvas API.
 * @param {object} preset - The preset result object from the API.
 * @returns {Promise<Blob|null>}
 */
export async function generateShareCard(preset) {
  const W = 1200, H = 630;
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  // Background
  ctx.fillStyle = '#0A0A0F';
  ctx.fillRect(0, 0, W, H);

  // Gold accent bar top
  ctx.fillStyle = '#C9A84C';
  ctx.fillRect(0, 0, W, 6);

  // Title
  ctx.fillStyle = '#C9A84C';
  ctx.font = "bold 52px 'Playfair Display', Georgia, serif";
  ctx.fillText('Kamera Quest', 72, 110);

  // Subtitle (displayName)
  const displayName = preset.displayName || '';
  ctx.fillStyle = '#E8E8F0';
  ctx.font = "400 32px 'DM Sans', system-ui, sans-serif";
  ctx.fillText(displayName, 72, 160);

  // Big exposure values
  const bigItems = [
    { label: 'ISO',      value: String(preset.ISO || '—') },
    { label: 'Aperture', value: `f/${preset.aperture || '—'}` },
    { label: 'Shutter',  value: String(preset.shutterSpeed || '—') },
  ];
  const colors = ['#FF4B4B', '#C9A84C', '#4ECDC4'];
  const colW = (W - 144) / 3;

  bigItems.forEach((item, i) => {
    const x = 72 + i * colW;
    ctx.fillStyle = colors[i];
    ctx.font = "bold 20px 'DM Sans', system-ui, sans-serif";
    ctx.fillText(item.label.toUpperCase(), x, 260);
    ctx.fillStyle = '#E8E8F0';
    ctx.font = "bold 64px 'DM Mono', 'Fira Mono', monospace";
    ctx.fillText(item.value, x, 350);
  });

  // Divider
  ctx.strokeStyle = '#2A2A38';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(72, 400);
  ctx.lineTo(W - 72, 400);
  ctx.stroke();

  // Mode and difficulty
  ctx.fillStyle = '#888899';
  ctx.font = "400 22px 'DM Sans', system-ui, sans-serif";
  ctx.fillText(`Mode: ${preset.mode || '—'}  |  Difficulty: ${preset.difficulty || '—'}`, 72, 460);

  // Pro tip (truncated)
  if (preset.proTip) {
    const tip = preset.proTip.length > 100 ? preset.proTip.slice(0, 97) + '…' : preset.proTip;
    ctx.fillStyle = '#C9A84C';
    ctx.font = "600 18px 'DM Sans', system-ui, sans-serif";
    ctx.fillText('PRO TIP', 72, 520);
    ctx.fillStyle = '#E8E8F0';
    ctx.font = "400 18px 'DM Sans', system-ui, sans-serif";
    ctx.fillText(tip, 72, 548);
  }

  // Footer
  ctx.fillStyle = '#888899';
  ctx.font = "400 16px 'DM Sans', system-ui, sans-serif";
  ctx.fillText('kamera.quest', W - 180, H - 32);

  return new Promise(resolve => canvas.toBlob(blob => resolve(blob), 'image/png'));
}
