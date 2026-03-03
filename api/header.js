export default function handler(req, res) {
  res.setHeader('Content-Type', 'image/svg+xml');
  res.setHeader('Cache-Control', 'public, max-age=3600');
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  const svg = `<svg width="900" height="200" viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#020818"/>
      <stop offset="40%" style="stop-color:#041530"/>
      <stop offset="100%" style="stop-color:#020818"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="sg" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="b1"/>
      <feGaussianBlur stdDeviation="2" result="b2"/>
      <feMerge><feMergeNode in="b1"/><feMergeNode in="b1"/><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="hex" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M20 0 L40 10 L40 30 L20 40 L0 30 L0 10 Z" fill="none" stroke="#0a2a4a" stroke-width="0.5" opacity="0.4"/>
    </pattern>
  </defs>

  <rect width="900" height="200" fill="url(#bg)"/>
  <rect width="900" height="200" fill="url(#hex)" opacity="0.5"/>
  <line x1="0" y1="1" x2="900" y2="1" stroke="#00d4ff" stroke-width="1.5" opacity="0.8" filter="url(#glow)"/>
  <line x1="0" y1="199" x2="900" y2="199" stroke="#00d4ff" stroke-width="1.5" opacity="0.8" filter="url(#glow)"/>

  ${['N','I','L','E','S','H'].map((l, i) => {
    const x = 180 + i * 52;
    const delay = 0.1 + i * 0.2;
    return `
  <ellipse cx="${x}" cy="148" rx="4" ry="4" fill="none" stroke="#00d4ff" stroke-width="1.2" opacity="0">
    <animate attributeName="rx" values="4;32;4" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
    <animate attributeName="ry" values="2;6;2" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
    <animate attributeName="opacity" values="0.8;0;0.8" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
  </ellipse>
  <text x="${x}" y="-60" font-family="Courier New, monospace" font-size="70" font-weight="900"
        fill="#00d4ff" filter="url(#sg)" text-anchor="middle">${l}
    <animate attributeName="y" values="-60;142;130;135" dur="1.1s" fill="freeze" begin="${delay}s"
             calcMode="spline" keySplines="0.25 0.1 0.25 1;0.5 0 0.75 0.5;0.5 0.5 0.75 1"/>
    <animate attributeName="opacity" values="0;1" dur="0.25s" fill="freeze" begin="${delay}s"/>
  </text>`;
  }).join('')}

  ${['S','A','H','O','O'].map((l, i) => {
    const x = 520 + i * 52;
    const delay = 1.4 + i * 0.2;
    return `
  <ellipse cx="${x}" cy="148" rx="4" ry="4" fill="none" stroke="#38bdf8" stroke-width="1.2" opacity="0">
    <animate attributeName="rx" values="4;32;4" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
    <animate attributeName="ry" values="2;6;2" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
    <animate attributeName="opacity" values="0.8;0;0.8" dur="2.8s" repeatCount="indefinite" begin="${delay}s"/>
  </ellipse>
  <text x="${x}" y="-60" font-family="Courier New, monospace" font-size="70" font-weight="900"
        fill="#38bdf8" filter="url(#sg)" text-anchor="middle">${l}
    <animate attributeName="y" values="-60;142;130;135" dur="1.1s" fill="freeze" begin="${delay}s"
             calcMode="spline" keySplines="0.25 0.1 0.25 1;0.5 0 0.75 0.5;0.5 0.5 0.75 1"/>
    <animate attributeName="opacity" values="0;1" dur="0.25s" fill="freeze" begin="${delay}s"/>
  </text>`;
  }).join('')}

  <text x="450" y="178" font-family="Courier New, monospace" font-size="13" font-weight="400"
        fill="#7dd3fc" text-anchor="middle" letter-spacing="5" opacity="0">
    &#9889;  FULL-STACK  &#183;  ML ENGINEER  &#183;  APP BUILDER  &#9889;
    <animate attributeName="opacity" values="0;1" dur="1s" fill="freeze" begin="2.8s"/>
  </text>
</svg>`;

  res.status(200).send(svg);
}
