
export const polarToCartesian = (cx: number, cy: number, r: number, angle: number) => {
  const rad = (angle - 90) * (Math.PI / 180);
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad),
  };
};

export const describeArc = (cx: number, cy: number, r: number, startAngle: number, endAngle: number) => {
  const start = polarToCartesian(cx, cy, r, endAngle);
  const end = polarToCartesian(cx, cy, r, startAngle);
  const largeArc = endAngle - startAngle <= 180 ? 0 : 1;
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} 0 ${end.x} ${end.y}`;
};

export const DIAL_POINTS = [
  { label: 'PROBABLE', angle: 0 },
  { label: 'PLAUSIBLE', angle: 120 },
  { label: 'POSSIBLE', angle: 240 },
];

export const likelihoodColors = {
  probable: '#293E6B ', // Blue
  plausible: '#293E6B', // Purple
  possible: '#293E6B'  // Teal
};

export const polarityColors = {
  'positive': '#78FF8A', // Green
  'negative': '#F23C3C'  // Red
};

export const likelihoodToDegrees = (type: string, val: number) =>
  (val / 100) * 120 +
  ({
    probable: 330,
    plausible: 90,
    possible: 210
  }[type] || 330);
