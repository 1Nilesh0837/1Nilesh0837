#!/usr/bin/env python3
"""Generate Chrome Dino Endless Runner Animated Footer SVG for GitHub Profile.

Writes:
    assets/footer-dino.svg
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_SVG = ROOT / "assets/footer-dino.svg"

# Palette: Dark Cyberpunk Chrome Dino
BG_COLOR = "#0A101F"
BORDER_COLOR = "#1E3A5F"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#7A9EC5"
NEON_MINT = "#00FF9F"
NEON_CYAN = "#38BDF8"
NEON_YELLOW = "#FFD700"
DINO_COLOR = "#00FF9F"      # Vibrant glowing neon mint
CACTUS_CYAN = "#38BDF8"     # Electric Cyan cactus
CACTUS_PINK = "#FF007F"     # Neon Pink cactus


def build_dino_svg():
    w, h = 830, 150
    ground_y = 104
    dino_x = 120

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',Consolas,monospace;">\n')

    # Defs & Filters
    svg.append('<defs>\n')
    svg.append(
        '  <filter id="dino-glow" x="-30%" y="-30%" width="160%" height="160%">\n'
        '    <feGaussianBlur stdDeviation="2.5" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">\n'
        '    <feGaussianBlur stdDeviation="2" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <linearGradient id="dino-border" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        f'    <stop offset="0%" stop-color="{NEON_MINT}" stop-opacity="0.9"/>\n'
        f'    <stop offset="50%" stop-color="{NEON_CYAN}" stop-opacity="0.6"/>\n'
        f'    <stop offset="100%" stop-color="{BORDER_COLOR}" stop-opacity="0.9"/>\n'
        '  </linearGradient>\n'
    )
    svg.append('</defs>\n')

    # Outer Panel
    svg.append(f'<rect width="{w}" height="{h}" rx="14" fill="{BG_COLOR}" stroke="url(#dino-border)" stroke-width="1.6"/>\n')

    # Top HUD Bar
    svg.append(f'<text x="25" y="24" fill="{NEON_MINT}" font-size="10.5" font-weight="900" letter-spacing="1">CHROME DINO // NO INTERNET 🦖</text>\n')
    # Score counter (with blinking effect)
    svg.append(
        f'<text x="{w-25}" y="24" text-anchor="end" font-size="11" font-weight="900" letter-spacing="1.5">\n'
        f'  <tspan fill="{TEXT_MUTED}">HI</tspan> <tspan fill="{TEXT_WHITE}">099990</tspan>  <tspan fill="{NEON_YELLOW}">001970</tspan>\n'
        f'</text>\n'
    )
    svg.append(f'<line x1="20" y1="32" x2="{w-20}" y2="32" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.5"/>\n')

    # Crescent Moon in top sky
    svg.append(f'<g transform="translate(680, 48)">\n')
    svg.append(f'  <path d="M12,0 A12,12 0 1,0 24,12 A10,10 0 1,1 12,0 Z" fill="{NEON_YELLOW}" opacity="0.85"/>\n')
    svg.append(f'</g>\n')

    # Drifting Pixel Clouds (varying speeds)
    clouds = [
        (120, 48, "16s"),
        (420, 42, "22s"),
        (720, 52, "18s"),
    ]
    for cx, cy, cdur in clouds:
        svg.append(
            f'<g opacity="0.3">\n'
            f'  <animateTransform attributeName="transform" type="translate" dur="{cdur}" repeatCount="indefinite" '
            f'values="{w},{cy}; -100,{cy}"/>\n'
            f'  <path fill="{TEXT_MUTED}" d="M0,8 h36 v-4 h-6 v-4 h-16 v4 h-6 v4 h-8 z"/>\n'
            f'</g>\n'
        )

    # Flying Pterodactyl in the sky
    svg.append(
        f'<g opacity="0.85" filter="url(#neon-glow)">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="11s" repeatCount="indefinite" '
        f'values="{w+60},46; -60,46"/>\n'
        # Frame A (wings up)
        f'  <path fill="{NEON_CYAN}" d="M0,0 h12 v2 h4 v2 h-6 v2 h-10 v-2 h-4 v-2 h4 z M4,-4 h4 v4 h-4 z">\n'
        f'    <animate attributeName="opacity" values="1;0;1" dur="0.36s" repeatCount="indefinite"/>\n'
        f'  </path>\n'
        # Frame B (wings down)
        f'  <path fill="{NEON_CYAN}" d="M0,0 h12 v2 h4 v2 h-6 v2 h-10 v-2 h-4 v-2 h4 z M4,4 h4 v4 h-4 z">\n'
        f'    <animate attributeName="opacity" values="0;1;0" dur="0.36s" repeatCount="indefinite"/>\n'
        f'  </path>\n'
        f'</g>\n'
    )

    # Ground line
    svg.append(f'<line x1="20" y1="{ground_y}" x2="{w-20}" y2="{ground_y}" stroke="{BORDER_COLOR}" stroke-width="1.2"/>\n')

    # Scrolling ground texture / pebbles
    svg.append(
        f'<g stroke="{TEXT_MUTED}" stroke-width="1.2" stroke-linecap="round" opacity="0.4">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="1.2s" repeatCount="indefinite" '
        f'values="0,0; -120,0"/>\n'
        + ''.join([f'<line x1="{x}" y1="{ground_y+4}" x2="{x+6}" y2="{ground_y+4}"/>' for x in range(30, w+160, 48)])
        + ''.join([f'<line x1="{x+18}" y1="{ground_y+8}" x2="{x+22}" y2="{ground_y+8}"/>' for x in range(30, w+160, 64)])
        + f'</g>\n'
    )

    # ── Incoming Obstacles (Cacti) ──
    # Cactus 1 (Electric Cyan, arrives at x=120 at t=2.967s, normalized key=0.824):
    svg.append(
        f'<g>\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="3.6s" repeatCount="indefinite" '
        f'values="{w+40},{ground_y}; -40,{ground_y}"/>\n'
        f'  <g filter="url(#dino-glow)">\n'
        f'    <rect x="-4" y="-28" width="8" height="28" fill="{CACTUS_CYAN}" rx="1.5"/>\n'
        f'    <rect x="-11" y="-21" width="7" height="4" fill="{CACTUS_CYAN}"/>\n'
        f'    <rect x="-11" y="-26" width="4" height="6" fill="{CACTUS_CYAN}" rx="1"/>\n'
        f'    <rect x="4" y="-17" width="7" height="4" fill="{CACTUS_CYAN}"/>\n'
        f'    <rect x="7" y="-24" width="4" height="8" fill="{CACTUS_CYAN}" rx="1"/>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # Cactus 2 (Delayed by 1.8s, Neon Pink double cactus, arrives at x=120 at t=1.167s, normalized key=0.324):
    svg.append(
        f'<g>\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="3.6s" repeatCount="indefinite" '
        f'begin="-1.8s" values="{w+40},{ground_y}; -40,{ground_y}"/>\n'
        f'  <g filter="url(#dino-glow)">\n'
        f'    <rect x="-9" y="-23" width="7" height="23" fill="{CACTUS_PINK}" rx="1.5"/>\n'
        f'    <rect x="2" y="-28" width="7" height="28" fill="{CACTUS_PINK}" rx="1.5"/>\n'
        f'    <rect x="-14" y="-16" width="5" height="4" fill="{CACTUS_PINK}"/>\n'
        f'    <rect x="-14" y="-21" width="4" height="6" fill="{CACTUS_PINK}"/>\n'
        f'    <rect x="9" y="-20" width="5" height="4" fill="{CACTUS_PINK}"/>\n'
        f'    <rect x="10" y="-25" width="4" height="6" fill="{CACTUS_PINK}"/>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # ── Chrome T-Rex Dinosaur (Position x = 120) ──
    # Perfectly synchronized jump physics:
    # Cactus 2 passes underneath at key=0.324 (Dino at peak y=58, 46px above cactus!)
    # Cactus 1 passes underneath at key=0.824 (Dino at peak y=58, 46px above cactus!)
    jump_keys = "0;0.244;0.284;0.324;0.364;0.404;0.744;0.784;0.824;0.864;0.904;1.0"
    jump_vals = (
        f"{dino_x},{ground_y}; "      # 0.000: Running on ground
        f"{dino_x},{ground_y}; "      # 0.244: Starts Jump 1
        f"{dino_x},{ground_y-26}; "   # 0.284: Ascending
        f"{dino_x},{ground_y-46}; "   # 0.324: PEAK! Cactus 2 passes directly underneath!
        f"{dino_x},{ground_y-26}; "   # 0.364: Descending
        f"{dino_x},{ground_y}; "      # 0.404: Lands on ground
        f"{dino_x},{ground_y}; "      # 0.744: Starts Jump 2
        f"{dino_x},{ground_y-26}; "   # 0.784: Ascending
        f"{dino_x},{ground_y-46}; "   # 0.824: PEAK! Cactus 1 passes directly underneath!
        f"{dino_x},{ground_y-26}; "   # 0.864: Descending
        f"{dino_x},{ground_y}; "      # 0.904: Lands on ground
        f"{dino_x},{ground_y}"        # 1.000: Running on ground
    )

    svg.append(
        f'<!-- Animated T-Rex Dinosaur (Jumping over Cacti with Zero Overlap) -->\n'
        f'<g filter="url(#dino-glow)">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="3.6s" repeatCount="indefinite" '
        f'values="{jump_vals}" keyTimes="{jump_keys}"/>\n'
        # Scale up dino slightly (1.25x) so it's super prominent
        f'  <g transform="scale(1.25)">\n'
        # Dino Body & Head (Pixel art)
        f'    <g fill="{DINO_COLOR}">\n'
        # Head & Snout
        f'      <rect x="6" y="-36" width="18" height="13" rx="1.5"/>\n'
        f'      <rect x="18" y="-36" width="8" height="7" rx="1"/>\n'
        # Eye (cutout with dark background)
        f'      <rect x="11" y="-34" width="2.5" height="2.5" fill="{BG_COLOR}"/>\n'
        # Snout / Mouth line
        f'      <rect x="17" y="-26" width="9" height="2.5" fill="{BG_COLOR}"/>\n'
        # Neck & Torso
        f'      <rect x="5" y="-27" width="11" height="17"/>\n'
        f'      <rect x="-8" y="-23" width="20" height="13"/>\n'
        # Tail
        f'      <rect x="-14" y="-23" width="7" height="7"/>\n'
        f'      <rect x="-18" y="-21" width="5" height="5"/>\n'
        # Short Arm
        f'      <rect x="13" y="-18" width="6" height="3" rx="1"/>\n'
        f'      <rect x="17" y="-16" width="2.5" height="4"/>\n'
        f'    </g>\n'
        # Running Legs (Alternating 2-frame walk cycle)
        f'    <g fill="{DINO_COLOR}">\n'
        # Leg Frame 1: Left down, right up
        f'      <g>\n'
        f'        <animate attributeName="opacity" values="1;0;1" dur="0.16s" repeatCount="indefinite"/>\n'
        f'        <rect x="-1" y="-10" width="3.5" height="10"/>\n'
        f'        <rect x="-1" y="-2" width="7" height="2.5"/>\n'
        f'        <rect x="7" y="-10" width="3.5" height="6"/>\n'
        f'      </g>\n'
        # Leg Frame 2: Left up, right down
        f'      <g>\n'
        f'        <animate attributeName="opacity" values="0;1;0" dur="0.16s" repeatCount="indefinite"/>\n'
        f'        <rect x="-1" y="-10" width="3.5" height="6"/>\n'
        f'        <rect x="7" y="-10" width="3.5" height="10"/>\n'
        f'        <rect x="7" y="-2" width="7" height="2.5"/>\n'
        f'      </g>\n'
        f'    </g>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # ── Bottom Arcade Banner & Inspiring Quote ──
    svg.append(f'<line x1="20" y1="{h-24}" x2="{w-20}" y2="{h-24}" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.6"/>\n')
    svg.append(f'<text x="25" y="{h-10}" fill="{TEXT_MUTED}" font-size="9.5" letter-spacing="0.5">STATUS: <tspan fill="{NEON_MINT}">ONLINE</tspan></text>\n')
    svg.append(f'<text x="{w//2}" y="{h-10}" text-anchor="middle" fill="{TEXT_WHITE}" font-size="9.5" font-weight="700" letter-spacing="0.6">✦ "BUGS ARE JUST OBSTACLES WAITING TO BE LEAPED OVER — KEEP RUNNING" ✦</text>\n')
    svg.append(f'<text x="{w-25}" y="{h-10}" text-anchor="end" fill="{NEON_CYAN}" font-size="9.5" font-weight="800" letter-spacing="0.5">PRESS SPACE TO JUMP 🦖</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    svg_content = build_dino_svg()
    OUT_SVG.write_text(svg_content, encoding="utf-8")
    size_kb = OUT_SVG.stat().st_size / 1024
    print(f"Generated {OUT_SVG} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
