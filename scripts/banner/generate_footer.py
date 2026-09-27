#!/usr/bin/env python3
"""Generate Space Invaders / Galaga Retro Arcade Animated Footer SVG for GitHub Profile.

Writes:
    assets/footer-game.svg
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_SVG = ROOT / "assets/footer-game.svg"

# Arcade Palette
BG_COLOR = "#070B14"
BORDER_COLOR = "#1E3A5F"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#7A9EC5"
NEON_CYAN = "#00E5FF"
NEON_MINT = "#00FF9F"
NEON_PINK = "#FF007F"
NEON_YELLOW = "#FFD700"
NEON_ORANGE = "#FF7A00"


def build_footer_svg():
    w, h = 830, 160
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',Consolas,monospace;">\n')

    # Defs & Filters
    svg.append('<defs>\n')
    svg.append(
        '  <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">\n'
        '    <feGaussianBlur stdDeviation="2.5" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <filter id="neon-glow" x="-30%" y="-30%" width="160%" height="160%">\n'
        '    <feGaussianBlur stdDeviation="3" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <linearGradient id="footer-border" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        f'    <stop offset="0%" stop-color="{NEON_CYAN}" stop-opacity="0.9"/>\n'
        f'    <stop offset="50%" stop-color="{NEON_MINT}" stop-opacity="0.7"/>\n'
        f'    <stop offset="100%" stop-color="{NEON_PINK}" stop-opacity="0.9"/>\n'
        '  </linearGradient>\n'
    )
    svg.append('</defs>\n')

    # Outer CRT Panel
    svg.append(f'<rect width="{w}" height="{h}" rx="14" fill="{BG_COLOR}" stroke="url(#footer-border)" stroke-width="1.6"/>\n')

    # Subtle CRT Scanlines
    for y in range(8, h, 6):
        svg.append(f'<line x1="10" y1="{y}" x2="{w-10}" y2="{y}" stroke="#1E293B" stroke-width="0.5" opacity="0.35"/>\n')

    # Twinkling Background Stars
    star_coords = [
        (45, 30, 1.2, "1.2s"), (120, 75, 1.5, "2.1s"), (210, 45, 1.0, "1.7s"),
        (280, 110, 1.5, "2.5s"), (360, 25, 1.2, "1.4s"), (460, 80, 1.0, "1.9s"),
        (540, 35, 1.4, "2.2s"), (620, 95, 1.2, "1.6s"), (700, 40, 1.5, "2.4s"),
        (760, 70, 1.0, "1.8s"), (150, 130, 1.2, "2.0s"), (680, 125, 1.2, "1.5s"),
    ]
    for sx, sy, sr, sdur in star_coords:
        svg.append(
            f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#FFFFFF">\n'
            f'  <animate attributeName="opacity" values="0.1;1;0.1" dur="{sdur}" repeatCount="indefinite"/>\n'
            f'</circle>\n'
        )

    # Top HUD Bar
    svg.append(f'<text x="25" y="24" fill="{NEON_PINK}" font-size="10.5" font-weight="900" letter-spacing="1">1UP <tspan fill="#FFFFFF">099990</tspan></text>\n')
    svg.append(f'<text x="{w//2}" y="24" text-anchor="middle" fill="{NEON_MINT}" font-size="11" font-weight="900" letter-spacing="1.5" filter="url(#neon-glow)">★ MISSION COMPLETE // EOF ★</text>\n')
    svg.append(f'<text x="{w-25}" y="24" text-anchor="end" fill="{NEON_CYAN}" font-size="10.5" font-weight="900" letter-spacing="1">SHIPS <tspan fill="{NEON_YELLOW}">▲ ▲ ▲</tspan></text>\n')
    svg.append(f'<line x1="20" y1="32" x2="{w-20}" y2="32" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.6"/>\n')

    # ── Invaders Fleet (Top Row, y = 55) ──
    # 5 Invaders wiggling tentacles in neon colors
    invaders = [
        (130, 55, NEON_PINK),
        (260, 55, NEON_CYAN),
        (390, 55, NEON_MINT),
        (520, 55, NEON_YELLOW),
        (650, 55, NEON_PINK),
    ]

    for ix, iy, icol in invaders:
        # 8-bit alien sprite path with alternating flapping arms
        svg.append(f'<g transform="translate({ix}, {iy})" filter="url(#laser-glow)">\n')
        # Frame A (arms out)
        svg.append(
            f'  <path fill="{icol}" d="M-9,-6 h18 v2 h-2 v2 h4 v6 h-2 v-2 h-2 v4 h-2 v-4 h-8 v4 h-2 v-4 h-2 v2 h-2 v-6 h4 v-2 h-2 z">\n'
            f'    <animate attributeName="opacity" values="1;0;0;1" dur="0.8s" repeatCount="indefinite"/>\n'
            f'  </path>\n'
        )
        # Frame B (arms in)
        svg.append(
            f'  <path fill="{icol}" d="M-9,-6 h18 v2 h-2 v2 h2 v6 h-4 v-2 h-2 v2 h-6 v-2 h-2 v2 h-4 v-6 h2 v-2 h-2 z">\n'
            f'    <animate attributeName="opacity" values="0;1;1;0" dur="0.8s" repeatCount="indefinite"/>\n'
            f'  </path>\n'
        )
        # Invader white eyes
        svg.append(f'  <rect x="-5" y="-3" width="2.5" height="2.5" fill="#070B14"/>\n')
        svg.append(f'  <rect x="2.5" y="-3" width="2.5" height="2.5" fill="#070B14"/>\n')
        svg.append('</g>\n')

    # Explosion sparks effect at center invader (hit by laser)
    svg.append(
        f'<g transform="translate(390, 55)" filter="url(#laser-glow)">\n'
        f'  <circle cx="0" cy="0" r="1" fill="{NEON_YELLOW}">\n'
        f'    <animate attributeName="r" values="0;14;0" dur="1.6s" repeatCount="indefinite" keyTimes="0;0.5;1"/>\n'
        f'    <animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite" keyTimes="0;0.5;1"/>\n'
        f'  </circle>\n'
        f'  <text x="0" y="-12" text-anchor="middle" fill="{NEON_MINT}" font-size="9" font-weight="900" opacity="0">\n'
        f'    <animate attributeName="opacity" values="0;0;1;0" dur="1.6s" repeatCount="indefinite" keyTimes="0;0.45;0.65;1"/>\n'
        f'    <animate attributeName="y" values="-8;-8;-18;-22" dur="1.6s" repeatCount="indefinite" keyTimes="0;0.45;0.7;1"/>\n'
        f'    +500\n'
        f'  </text>\n'
        f'</g>\n'
    )

    # ── Shooting Laser Beams ──
    # Lasers traveling upward from starship (y=110 to y=55)
    laser_x = [388, 392]
    for lx in laser_x:
        svg.append(
            f'<rect x="{lx}" y="55" width="2.2" height="10" rx="1" fill="{NEON_CYAN}" filter="url(#laser-glow)">\n'
            f'  <animate attributeName="y" values="115;55" dur="0.8s" repeatCount="indefinite"/>\n'
            f'  <animate attributeName="opacity" values="1;0.9;0" dur="0.8s" repeatCount="indefinite"/>\n'
            f'</rect>\n'
        )

    # ── Player Fighter Ship (Galaga / Space Cannon at y = 118) ──
    # Ship patrols left and right across the bottom
    svg.append(
        f'<g filter="url(#laser-glow)">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" '
        f'values="260,118; 520,118; 390,118; 260,118"/>\n'
        # Ship body (Galaga retro fighter polygon)
        f'  <polygon points="0,-12 -4,-4 -10,4 -10,8 -6,6 -3,8 0,6 3,8 6,6 10,8 10,4 4,-4" fill="{NEON_CYAN}"/>\n'
        f'  <polygon points="0,-12 -2,-4 -5,4 0,2 5,4 2,-4" fill="{NEON_YELLOW}"/>\n'
        f'  <rect x="-1" y="-14" width="2" height="4" fill="#FFFFFF"/>\n'
        # Cockpit windshield
        f'  <circle cx="0" cy="-2" r="2.2" fill="#070B14"/>\n'
        f'  <circle cx="0" cy="-2" r="1.4" fill="{NEON_MINT}"/>\n'
        # Animated Thruster exhaust flames
        f'  <polygon points="-3,8 0,14 3,8" fill="{NEON_ORANGE}">\n'
        f'    <animate attributeName="points" dur="0.15s" repeatCount="indefinite" '
        f'values="-3,8 0,15 3,8; -2.5,8 0,11 2.5,8; -3,8 0,16 3,8"/>\n'
        f'  </polygon>\n'
        f'  <polygon points="-1.5,8 0,11 1.5,8" fill="{NEON_YELLOW}">\n'
        f'    <animate attributeName="points" dur="0.15s" repeatCount="indefinite" '
        f'values="-1.5,8 0,11 1.5,8; -1,8 0,8 1,8; -1.5,8 0,12 1.5,8"/>\n'
        f'  </polygon>\n'
        f'</g>\n'
    )

    # ── Bottom Arcade Banner & Inspiring Quote ──
    svg.append(f'<line x1="20" y1="138" x2="{w-20}" y2="138" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.6"/>\n')
    svg.append(f'<text x="25" y="150" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="0.5">CREDITS: <tspan fill="{NEON_YELLOW}">99</tspan></text>\n')
    svg.append(f'<text x="{w//2}" y="150" text-anchor="middle" fill="{TEXT_WHITE}" font-size="10" font-weight="700" letter-spacing="0.8">✦ "CODE IS THE MODERN SORCERY: TURNING PURE LOGIC INTO REALITY" ✦</text>\n')
    svg.append(f'<text x="{w-25}" y="150" text-anchor="end" fill="{NEON_PINK}" font-size="9.5" font-weight="800" letter-spacing="0.5">INSERT COIN TO RESTART 🪙</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    svg_content = build_footer_svg()
    OUT_SVG.write_text(svg_content, encoding="utf-8")
    size_kb = OUT_SVG.stat().st_size / 1024
    print(f"Generated {OUT_SVG} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
