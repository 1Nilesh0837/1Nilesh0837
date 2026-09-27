#!/usr/bin/env python3
"""Generate Cyber Synthwave Highway Animated Footer SVG.

Builds:
    assets/footer-synthwave.svg (830x185)
Featuring an animated neon sports car cruising down an infinite perspective
retro-grid into a glowing synthwave sun and cyberpunk city horizon.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_SVG = ROOT / "assets/footer-synthwave.svg"


def build_synthwave_svg():
    w, h = 830, 185
    horizon_y = 95
    vanish_x = 415

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n')
    svg.append('<defs>\n')
    
    # Sky Gradient
    svg.append('  <linearGradient id="sky-grad" x1="0%" y1="0%" x2="0%" y2="100%">\n')
    svg.append('    <stop offset="0%" stop-color="#04060E"/>\n')
    svg.append('    <stop offset="50%" stop-color="#0B0E20"/>\n')
    svg.append('    <stop offset="85%" stop-color="#22092C"/>\n')
    svg.append('    <stop offset="100%" stop-color="#3D0C38"/>\n')
    svg.append('  </linearGradient>\n')

    # Synthwave Sun Gradient
    svg.append('  <linearGradient id="sun-grad" x1="0%" y1="0%" x2="0%" y2="100%">\n')
    svg.append('    <stop offset="0%" stop-color="#FFF066"/>\n')
    svg.append('    <stop offset="40%" stop-color="#FF007F"/>\n')
    svg.append('    <stop offset="100%" stop-color="#7928CA"/>\n')
    svg.append('  </linearGradient>\n')

    # Road Gradient
    svg.append(f'  <linearGradient id="road-grad" x1="0%" y1="0%" x2="0%" y2="100%">\n')
    svg.append('    <stop offset="0%" stop-color="#14061F"/>\n')
    svg.append('    <stop offset="40%" stop-color="#090E1F"/>\n')
    svg.append('    <stop offset="100%" stop-color="#050811"/>\n')
    svg.append('  </linearGradient>\n')

    # Horizon Glow Gradient
    svg.append('  <radialGradient id="horizon-glow" cx="50%" cy="50%" r="50%">\n')
    svg.append('    <stop offset="0%" stop-color="#FF007F" stop-opacity="0.4"/>\n')
    svg.append('    <stop offset="60%" stop-color="#7928CA" stop-opacity="0.15"/>\n')
    svg.append('    <stop offset="100%" stop-color="#000000" stop-opacity="0"/>\n')
    svg.append('  </radialGradient>\n')

    # Car Underglow
    svg.append('  <radialGradient id="car-glow" cx="50%" cy="50%" r="50%">\n')
    svg.append('    <stop offset="0%" stop-color="#00FF9F" stop-opacity="0.7"/>\n')
    svg.append('    <stop offset="40%" stop-color="#38BDF8" stop-opacity="0.3"/>\n')
    svg.append('    <stop offset="100%" stop-color="#000000" stop-opacity="0"/>\n')
    svg.append('  </radialGradient>\n')

    # Exhaust Flame
    svg.append('  <linearGradient id="flame-grad" x1="0%" y1="0%" x2="0%" y2="100%">\n')
    svg.append('    <stop offset="0%" stop-color="#00FF9F"/>\n')
    svg.append('    <stop offset="50%" stop-color="#38BDF8"/>\n')
    svg.append('    <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>\n')
    svg.append('  </linearGradient>\n')

    # Neon glow filter
    svg.append('  <filter id="neon" x="-20%" y="-20%" width="140%" height="140%">\n')
    svg.append('    <feGaussianBlur stdDeviation="3" result="blur"/>\n')
    svg.append('    <feComposite in="SourceGraphic" in2="blur" operator="over"/>\n')
    svg.append('  </filter>\n')

    # Animations
    svg.append('  <style>\n')
    svg.append('    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }\n')
    svg.append('    @keyframes highway-move {\n')
    svg.append('      0% { transform: translateY(0); }\n')
    svg.append('      100% { transform: translateY(85px); }\n')
    svg.append('    }\n')
    svg.append('    @keyframes car-bounce {\n')
    svg.append('      0%, 100% { transform: translateY(0); }\n')
    svg.append('      50% { transform: translateY(-1.5px); }\n')
    svg.append('    }\n')
    svg.append('    @keyframes thruster-flicker {\n')
    svg.append('      0%, 100% { opacity: 0.9; transform: scaleY(1); }\n')
    svg.append('      50% { opacity: 0.5; transform: scaleY(0.75); }\n')
    svg.append('    }\n')
    svg.append('    @keyframes star-twinkle {\n')
    svg.append('      0%, 100% { opacity: 0.8; }\n')
    svg.append('      50% { opacity: 0.2; }\n')
    svg.append('    }\n')
    svg.append('    .car-group { animation: car-bounce 0.8s infinite ease-in-out; transform-origin: 415px 145px; }\n')
    svg.append('    .flame-left { animation: thruster-flicker 0.25s infinite ease-in-out; transform-origin: 395px 156px; }\n')
    svg.append('    .flame-right { animation: thruster-flicker 0.25s infinite ease-in-out 0.12s; transform-origin: 435px 156px; }\n')
    svg.append('    .star-a { animation: star-twinkle 2s infinite ease-in-out; }\n')
    svg.append('    .star-b { animation: star-twinkle 3s infinite ease-in-out 1s; }\n')
    svg.append('    .txt-hud { font-size: 8.5px; font-weight: 800; letter-spacing: 0.8px; }\n')
    svg.append('  </style>\n')

    # Clip path for highway region (below horizon)
    svg.append('  <clipPath id="road-clip">\n')
    svg.append(f'    <rect x="0" y="{horizon_y}" width="{w}" height="{h - horizon_y}"/>\n')
    svg.append('  </clipPath>\n')
    
    # Pattern for highway speed bars
    svg.append('</defs>\n')

    # Main Card Base
    svg.append(f'<rect width="{w}" height="{h}" rx="12" fill="#0A101F" stroke="#1E3A5F" stroke-width="1.2"/>\n')

    # Sky Canvas
    svg.append(f'<rect x="2" y="2" width="{w-4}" height="{horizon_y-2}" fill="url(#sky-grad)"/>\n')

    # Twinkling Stars
    star_coords = [
        (35, 20), (80, 45), (140, 25), (210, 50), (280, 22), (340, 48),
        (480, 42), (540, 18), (620, 50), (690, 24), (745, 46), (800, 20),
        (110, 65), (250, 70), (580, 68), (710, 65)
    ]
    for idx, (sx, sy) in enumerate(star_coords):
        cls = "star-a" if idx % 2 == 0 else "star-b"
        r = 1.2 if idx % 3 == 0 else 0.8
        svg.append(f'<circle class="{cls}" cx="{sx}" cy="{sy}" r="{r}" fill="#FFFFFF"/>\n')

    # Synthwave Sun at Horizon Center
    sun_r = 38
    sun_cy = horizon_y - 2
    svg.append(f'<g transform="translate({vanish_x},{sun_cy})">\n')
    # Sun circle
    svg.append(f'  <circle cx="0" cy="0" r="{sun_r}" fill="url(#sun-grad)"/>\n')
    # Horizontal blind lines cut through sun
    for s_idx in range(6):
        slit_y = 6 + s_idx * 5.5
        slit_h = 1.4 + s_idx * 0.4
        svg.append(f'  <rect x="-{sun_r}" y="{slit_y}" width="{sun_r*2}" height="{slit_h}" fill="#0B0E20"/>\n')
    svg.append('</g>\n')

    # Cyberpunk City Skyline Silhouettes
    buildings = [
        # (x, w, h)
        (25, 22, 28), (50, 16, 42), (68, 25, 30), (95, 18, 52), (115, 30, 24),
        (150, 20, 36), (172, 26, 48), (200, 18, 32), (220, 28, 44), (250, 22, 26),
        (275, 18, 38), (295, 24, 20),
        # Right side
        (515, 24, 22), (542, 18, 40), (563, 26, 32), (592, 18, 50), (612, 30, 26),
        (645, 20, 38), (668, 26, 46), (696, 18, 30), (716, 28, 42), (746, 22, 24),
        (770, 18, 36), (790, 25, 28)
    ]
    for bx, bw, bh in buildings:
        by = horizon_y - bh
        svg.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#060914"/>\n')
        # Glowing antenna on taller towers
        if bh >= 42:
            svg.append(f'<line x1="{bx+bw//2}" y1="{by-8}" x2="{bx+bw//2}" y2="{by}" stroke="#FF007F" stroke-width="0.8"/>\n')
            svg.append(f'<circle cx="{bx+bw//2}" cy="{by-8}" r="1" fill="#00FF9F"/>\n')
        # Window dots
        if bh > 30:
            for wy in range(by + 8, horizon_y - 4, 8):
                svg.append(f'<rect x="{bx+3}" y="{wy}" width="2" height="2" fill="#38BDF8" opacity="0.6"/>\n')
                if bw > 20:
                    svg.append(f'<rect x="{bx+bw-5}" y="{wy}" width="2" height="2" fill="#FF007F" opacity="0.6"/>\n')

    # Horizon Glow Burst
    svg.append(f'<ellipse cx="{vanish_x}" cy="{horizon_y}" rx="240" ry="18" fill="url(#horizon-glow)"/>\n')
    svg.append(f'<line x1="2" y1="{horizon_y}" x2="{w-2}" y2="{horizon_y}" stroke="#FF007F" stroke-width="1.2" opacity="0.8"/>\n')

    # ── RETRO PERSPECTIVE HIGHWAY (y = horizon_y .. h) ──
    # Road Base
    svg.append(f'<rect x="2" y="{horizon_y}" width="{w-4}" height="{h-horizon_y-2}" fill="url(#road-grad)"/>\n')

    # Perspective Longitudinal Rays (Radiating from Vanishing Point)
    radiating_targets = [
        # (bottom_x, opacity, color)
        (-60, 0.3, "#A855F7"),
        (20, 0.4, "#A855F7"),
        (100, 0.5, "#FF007F"),
        (190, 0.6, "#FF007F"),
        (280, 0.7, "#38BDF8"),
        (350, 0.9, "#00FF9F"),
        (415, 0.7, "#00FF9F"), # Center lane
        (480, 0.9, "#00FF9F"),
        (550, 0.7, "#38BDF8"),
        (640, 0.6, "#FF007F"),
        (730, 0.5, "#FF007F"),
        (810, 0.4, "#A855F7"),
        (890, 0.3, "#A855F7"),
    ]
    for rx, op, col in radiating_targets:
        svg.append(f'<line x1="{vanish_x}" y1="{horizon_y}" x2="{rx}" y2="{h-2}" stroke="{col}" stroke-width="1" opacity="{op}"/>\n')

    # Infinite Moving Crossbars (Animated via SVG SMIL keyframe translation)
    # Using 8 perspective lines that travel downward
    svg.append(f'<g clip-path="url(#road-clip)">\n')
    
    # 2 sets of moving horizontal lines for seamless infinite loop
    for loop_id in [1, 2]:
        delay = "0s" if loop_id == 1 else "-1s"
        svg.append(f'<g opacity="0.8">\n')
        # Animate vertical expansion
        for bar_idx in range(9):
            # Non-linear perspective spacing
            ratio = (bar_idx / 8.0)
            initial_y = horizon_y + int((ratio ** 2.2) * (h - horizon_y))
            sw = 0.6 + ratio * 2.2
            svg.append(
                f'  <line x1="2" y1="{initial_y}" x2="{w-2}" y2="{initial_y}" stroke="#38BDF8" stroke-width="{sw:.1f}" opacity="{0.2 + ratio * 0.7:.2f}">\n'
                f'    <animate attributeName="y1" values="{horizon_y};{h+15}" dur="2s" begin="{delay}" repeatCount="indefinite"/>\n'
                f'    <animate attributeName="y2" values="{horizon_y};{h+15}" dur="2s" begin="{delay}" repeatCount="indefinite"/>\n'
                f'    <animate attributeName="stroke-width" values="0.5;3" dur="2s" begin="{delay}" repeatCount="indefinite"/>\n'
                f'    <animate attributeName="opacity" values="0.1;0.9;0" keyTimes="0;0.85;1" dur="2s" begin="{delay}" repeatCount="indefinite"/>\n'
                f'  </line>\n'
            )
        svg.append('</g>\n')
    svg.append('</g>\n')

    # ── CYBER SPORTS CAR (Centered at x=415, y=140) ──
    cx = vanish_x
    cy = 138

    # Neon road underglow
    svg.append(f'<ellipse cx="{cx}" cy="{cy+24}" rx="55" ry="12" fill="url(#car-glow)"/>\n')

    # Car Group (with subtle engine bounce animation)
    svg.append(f'<g class="car-group">\n')

    # Dual Plasma Thrusters Exhaust Flames
    flame_w, flame_h = 6, 15
    svg.append(f'  <polygon class="flame-left" points="{cx-22},{cy+18} {cx-25},{cy+18+flame_h} {cx-19},{cy+18+flame_h}" fill="url(#flame-grad)"/>\n')
    svg.append(f'  <polygon class="flame-right" points="{cx+22},{cy+18} {cx+19},{cy+18+flame_h} {cx+25},{cy+18+flame_h}" fill="url(#flame-grad)"/>\n')

    # Rear Wheels
    svg.append(f'  <rect x="{cx-36}" y="{cy+6}" width="8" height="15" rx="3" fill="#0A0D17" stroke="#1E3A5F" stroke-width="0.8"/>\n')
    svg.append(f'  <rect x="{cx+28}" y="{cy+6}" width="8" height="15" rx="3" fill="#0A0D17" stroke="#1E3A5F" stroke-width="0.8"/>\n')
    svg.append(f'  <line x1="{cx-33}" y1="{cy+9}" x2="{cx-33}" y2="{cy+18}" stroke="#00FF9F" stroke-width="1.2"/>\n')
    svg.append(f'  <line x1="{cx+33}" y1="{cy+9}" x2="{cx+33}" y2="{cy+18}" stroke="#00FF9F" stroke-width="1.2"/>\n')

    # Main Chassis (Lower Body)
    svg.append(f'  <path d="M{cx-32},{cy+18} L{cx+32},{cy+18} L{cx+30},{cy+8} L{cx-30},{cy+8} Z" fill="#0E1628" stroke="#1E3A5F" stroke-width="1.2"/>\n')
    
    # Upper Cabin / Cockpit Roof
    svg.append(f'  <path d="M{cx-24},{cy+8} L{cx+24},{cy+8} L{cx+18},{cy-2} L{cx-18},{cy-2} Z" fill="#060A14" stroke="#38BDF8" stroke-width="1"/>\n')

    # Rear Windshield / Louvers
    svg.append(f'  <polygon points="{cx-20},{cy+7} {cx+20},{cy+7} {cx+15},{cy+0} {cx-15},{cy+0}" fill="#0D1B2A"/>\n')
    svg.append(f'  <line x1="{cx-17}" y1="{cy+2}" x2="{cx+17}" y2="{cy+2}" stroke="#1E3A5F" stroke-width="0.8"/>\n')
    svg.append(f'  <line x1="{cx-19}" y1="{cy+5}" x2="{cx+19}" y2="{cy+5}" stroke="#1E3A5F" stroke-width="0.8"/>\n')

    # Iconic Continuous Cyber Neon Taillight Bar
    svg.append(f'  <rect x="{cx-28}" y="{cy+9}" width="56" height="3.5" rx="1.5" fill="#FF0055" filter="url(#neon)"/>\n')
    svg.append(f'  <rect x="{cx-28}" y="{cy+9}" width="56" height="3.5" rx="1.5" fill="#FFFFFF" opacity="0.6"/>\n')

    # License Plate
    svg.append(f'  <rect x="{cx-11}" y="{cy+13}" width="22" height="5" rx="1" fill="#050811" stroke="#00FF9F" stroke-width="0.6"/>\n')
    svg.append(f'  <text x="{cx}" y="{cy+17}" text-anchor="middle" fill="#00FF9F" font-size="3.5" font-weight="900" letter-spacing="0.5">DEV-2026</text>\n')

    # Rear Aerodynamic Wing / Spoiler
    svg.append(f'  <path d="M{cx-31},{cy+3} L{cx+31},{cy+3} L{cx+29},{cy+1} L{cx-29},{cy+1} Z" fill="#091020" stroke="#00FF9F" stroke-width="0.8"/>\n')
    svg.append(f'  <line x1="{cx-25}" y1="{cy+3}" x2="{cx-25}" y2="{cy+7}" stroke="#1E3A5F" stroke-width="1"/>\n')
    svg.append(f'  <line x1="{cx+25}" y1="{cy+3}" x2="{cx+25}" y2="{cy+7}" stroke="#1E3A5F" stroke-width="1"/>\n')

    svg.append('</g>\n')

    # ── TOP HUD BANNER ──
    svg.append('<rect x="12" y="10" width="170" height="18" rx="4" fill="#0A101F" stroke="#1E3A5F" stroke-width="0.8" opacity="0.85"/>\n')
    svg.append('<circle cx="22" cy="19" r="3" fill="#FF007F"><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></circle>\n')
    svg.append('<text class="txt-hud" x="30" y="22" fill="#FF007F">CYBER CRUISE // HIGHWAY</text>\n')

    svg.append(f'<text class="txt-hud" x="{w//2}" y="22" text-anchor="middle" fill="#7A9EC5">VELOCITY: <tspan fill="#00FF9F">180 MPH</tspan> &#160;•&#160; NITRO: <tspan fill="#38BDF8">ARMED</tspan></text>\n')

    svg.append(f'<rect x="{w-182}" y="10" width="170" height="18" rx="4" fill="#0A101F" stroke="#1E3A5F" stroke-width="0.8" opacity="0.85"/>\n')
    svg.append(f'<text class="txt-hud" x="{w-18}" y="22" text-anchor="end" fill="#00FF9F">KM TRAVELED: <tspan fill="#FFFFFF">099990</tspan> ⚡</text>\n')

    # ── BOTTOM HUD BANNER ──
    svg.append(f'<line x1="20" y1="{h-22}" x2="{w-20}" y2="{h-22}" stroke="#1E3A5F" stroke-width="0.8" opacity="0.6"/>\n')
    svg.append(f'<text class="txt-hud" x="25" y="{h-9}" fill="#7A9EC5">AUDIO: <tspan fill="#FF007F">SYNTHWAVE FM 104.2</tspan></text>\n')
    svg.append(f'<text class="txt-hud" x="{w//2}" y="{h-9}" text-anchor="middle" fill="#FFFFFF" font-weight="700">★ "BUILDS WITH PASSION, CRUISES BEYOND THE LIMITS" ★</text>\n')
    svg.append(f'<text class="txt-hud" x="{w-25}" y="{h-9}" text-anchor="end" fill="#38BDF8">SYSTEM: <tspan fill="#00FF9F">ONLINE ⚡</tspan></text>\n')

    # Glowing border accent
    svg.append(f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="10" fill="none" stroke="#FF007F" stroke-width="0.8" opacity="0.4"/>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    content = build_synthwave_svg()
    OUT_SVG.write_text(content, encoding="utf-8")
    size_kb = OUT_SVG.stat().st_size / 1024
    print(f"Generated {OUT_SVG} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
