#!/usr/bin/env python3
"""Generate the retro Pac-Man animated GitHub Contribution Grid SVG.

Reads:
    scripts/banner/data/contributions.json  (or fetches fresh from API)

Writes:
    assets/github-pacman.svg
"""

import json
from pathlib import Path
import urllib.request
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "scripts/banner/data/contributions.json"
OUT_SVG = ROOT / "assets/github-pacman.svg"

# Palette: Cyberpunk Dark Arcade
BG_COLOR = "#0A101F"
BORDER_COLOR = "#1E3A5F"
TEXT_COLOR = "#E0F0FF"
MUTED_COLOR = "#7A9EC5"
ACCENT_MINT = "#00FF9F"
ACCENT_CYAN = "#38BDF8"
PACMAN_YELLOW = "#FFD700"
GHOST_CYAN = "#00E5FF"
GHOST_BLUE = "#3B82F6"

# Cell colors by GitHub contribution level (0 to 4)
LEVEL_COLORS = {
    0: "#131D31",  # Inactive day (dark pellet)
    1: "#0E4429",  # 1-2 commits
    2: "#006D32",  # 3-5 commits
    3: "#26A641",  # 6-8 commits
    4: "#00FF9F",  # 9+ commits (power pellet)
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_contributions():
    """Load or fetch the last 371 days of contributions."""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Fallback to fetching fresh
    url = "https://github-contributions-api.jogruber.de/v4/1Nilesh0837"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        contribs = sorted(data["contributions"], key=lambda x: x["date"])
        today = "2026-09-27"
        recent = [c for c in contribs if c["date"] <= today][-371:]
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(recent, f)
        return recent


def build_pacman_svg(contribs):
    w, h = 830, 222
    total_commits = sum(c.get("count", 0) for c in contribs)
    active_days = sum(1 for c in contribs if c.get("count", 0) > 0)

    # 53 weeks (cols) x 7 days (rows)
    col_w = 14.0
    row_h = 14.0
    cell_size = 10.5
    grid_x = 42.0
    grid_y = 56.0

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',Consolas,monospace;">\n')

    # Defs & Filters
    svg.append('<defs>\n')
    svg.append(
        '  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">\n'
        '    <feGaussianBlur stdDeviation="2" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <filter id="pac-glow" x="-30%" y="-30%" width="160%" height="160%">\n'
        '    <feGaussianBlur stdDeviation="3" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append('</defs>\n')

    # Outer Panel
    svg.append(f'<rect width="{w}" height="{h}" rx="10" fill="{BG_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1.5"/>\n')

    # Top Arcade Header
    svg.append(f'<text x="25" y="24" fill="#EF4444" font-weight="900" font-size="11">1UP <tspan fill="#FFFFFF">0{total_commits:04d}0</tspan></text>\n')
    svg.append(f'<text x="{w//2}" y="24" text-anchor="middle" fill="{ACCENT_MINT}" font-weight="800" font-size="11" letter-spacing="1.5">ARCADE GRID · PAC-MAN EDITION</text>\n')
    svg.append(f'<text x="{w-25}" y="24" text-anchor="end" fill="{ACCENT_CYAN}" font-weight="900" font-size="11">HIGH SCORE <tspan fill="#FFFFFF">099990</tspan></text>\n')
    svg.append(f'<line x1="20" y1="34" x2="{w-20}" y2="34" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.6"/>\n')

    # Month Labels across the top
    # Extract distinct month starts
    last_month = None
    for idx, c in enumerate(contribs):
        col = idx // 7
        row = idx % 7
        if row == 0:
            date_str = c.get("date", "")
            if date_str:
                m_num = int(date_str.split("-")[1])
                m_name = MONTH_NAMES[m_num - 1]
                if m_name != last_month and col < 51:
                    last_month = m_name
                    mx = grid_x + col * col_w
                    svg.append(f'<text x="{mx:.1f}" y="47" fill="{MUTED_COLOR}" font-size="9" font-weight="600">{m_name}</text>\n')

    # Weekday labels on left
    svg.append(f'<text x="18" y="{grid_y + 1 * row_h + 8.5:.1f}" fill="{MUTED_COLOR}" font-size="9">Mon</text>\n')
    svg.append(f'<text x="18" y="{grid_y + 3 * row_h + 8.5:.1f}" fill="{MUTED_COLOR}" font-size="9">Wed</text>\n')
    svg.append(f'<text x="18" y="{grid_y + 5 * row_h + 8.5:.1f}" fill="{MUTED_COLOR}" font-size="9">Fri</text>\n')

    # Contribution Cells
    for idx, c in enumerate(contribs):
        col = idx // 7
        row = idx % 7
        cx = grid_x + col * col_w
        cy = grid_y + row * row_h
        level = c.get("level", 0)
        count = c.get("count", 0)
        fill = LEVEL_COLORS.get(level, LEVEL_COLORS[0])
        date = c.get("date", "")

        # Power pellet pulse on level 4
        if level >= 4:
            svg.append(
                f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill}" filter="url(#neon-glow)">\n'
                f'  <title>{count} contributions on {date}</title>\n'
                f'  <animate attributeName="opacity" values="0.8;1;0.8" dur="1.5s" repeatCount="indefinite"/>\n'
                f'</rect>\n'
            )
        else:
            svg.append(
                f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill}">\n'
                f'  <title>{count} contributions on {date}</title>\n'
                f'</rect>\n'
            )

    # ── Animated Pac-Man & Ghost Movement ──
    # Total duration = 14s loop
    # Route:
    # Row 1 (y = 75.0): Left -> Right (0.0s..4.2s)
    # Turn down to Row 3 (y = 103.5) (4.2s..4.6s)
    # Row 3 (y = 103.5): Right -> Left (4.6s..8.8s)
    # Turn down to Row 5 (y = 132.0) (8.8s..9.2s)
    # Row 5 (y = 132.0): Left -> Right (9.2s..13.4s)
    # Wrap back (13.4s..14.0s)

    r1_y = grid_y + 1 * row_h + cell_size / 2.0  # 75.25
    r3_y = grid_y + 3 * row_h + cell_size / 2.0  # 103.65
    r5_y = grid_y + 5 * row_h + cell_size / 2.0  # 132.05

    x_min = grid_x + 5
    x_max = grid_x + 52 * col_w + 5  # ~775

    p_k = "0;0.300;0.328;0.628;0.657;0.957;1.0"
    p_tr = f"{x_min},{r1_y}; {x_max},{r1_y}; {x_max},{r3_y}; {x_min},{r3_y}; {x_min},{r5_y}; {x_max},{r5_y}; {x_min},{r1_y}"
    p_rot = "0;0; 90; 180; 90; 0; 0"

    # Ghost is delayed by 0.5s (~0.035 in keyTimes)
    g_k = "0;0.035;0.335;0.363;0.663;0.692;0.992;1.0"
    g_tr = f"{x_min-25},{r1_y}; {x_min},{r1_y}; {x_max},{r1_y}; {x_max},{r3_y}; {x_min},{r3_y}; {x_min},{r5_y}; {x_max},{r5_y}; {x_min-25},{r1_y}"

    # Pac-Man Element
    svg.append('<!-- Pac-Man Character -->\n')
    svg.append(
        f'<g filter="url(#pac-glow)">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" '
        f'values="{p_tr}" keyTimes="{p_k}"/>\n'
        # Pac-man yellow body with chomping mouth
        f'  <circle cx="0" cy="0" r="7.5" fill="{PACMAN_YELLOW}"/>\n'
        f'  <path fill="{BG_COLOR}">\n'
        f'    <animate attributeName="d" dur="0.22s" repeatCount="indefinite" '
        f'values="M0,0 L8,-4.5 L8,4.5 Z; M0,0 L8,-0.5 L8,0.5 Z; M0,0 L8,-4.5 L8,4.5 Z"/>\n'
        f'  </path>\n'
        f'</g>\n'
    )

    # Ghost Element (Blinky / Inky)
    # Turns scared blue on row 5 (0.657 to 0.957)
    svg.append('<!-- Ghost Character (Chasing Pac-Man) -->\n')
    ghost_colors = f"{GHOST_CYAN};{GHOST_CYAN};{GHOST_CYAN};{GHOST_CYAN};{GHOST_BLUE};{GHOST_BLUE};{GHOST_CYAN}"
    ghost_k = "0;0.300;0.328;0.628;0.657;0.957;1.0"
    svg.append(
        f'<g filter="url(#neon-glow)">\n'
        f'  <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" '
        f'values="{g_tr}" keyTimes="{g_k}"/>\n'
        # Ghost body
        f'  <path d="M-6,6 L-6,-1 A6,6 0 0,1 6,-1 L6,6 L3,4.5 L0,6 L-3,4.5 Z" fill="{GHOST_CYAN}">\n'
        f'    <animate attributeName="fill" dur="14s" repeatCount="indefinite" values="{ghost_colors}" keyTimes="{ghost_k}"/>\n'
        f'  </path>\n'
        # Ghost eyes
        f'  <circle cx="-2.5" cy="-1.5" r="1.8" fill="#FFFFFF"/>\n'
        f'  <circle cx="2.5" cy="-1.5" r="1.8" fill="#FFFFFF"/>\n'
        f'  <circle cx="-1.8" cy="-1.5" r="0.9" fill="#000080"/>\n'
        f'  <circle cx="3.2" cy="-1.5" r="0.9" fill="#000080"/>\n'
        f'</g>\n'
    )

    # Floating Score Bubble when power pellet is eaten
    svg.append(
        f'<text x="{x_max-40}" y="{r5_y-12}" fill="{PACMAN_YELLOW}" font-size="10" font-weight="900" opacity="0">\n'
        f'  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" '
        f'values="0;0;0;0;1;1;0;0" keyTimes="0;0.91;0.92;0.95;0.96;0.98;0.99;1.0"/>\n'
        f'  <animate attributeName="y" dur="14s" repeatCount="indefinite" '
        f'values="{r5_y-8};{r5_y-8};{r5_y-8};{r5_y-8};{r5_y-14};{r5_y-20};{r5_y-20};{r5_y-20}" keyTimes="0;0.91;0.92;0.95;0.96;0.98;0.99;1.0"/>\n'
        f'  +200\n'
        f'</text>\n'
    )

    # Bottom Arcade Footer
    svg.append(f'<line x1="20" y1="{h-32}" x2="{w-20}" y2="{h-32}" stroke="{BORDER_COLOR}" stroke-width="0.8" opacity="0.6"/>\n')
    svg.append(f'<text x="25" y="{h-14}" fill="{MUTED_COLOR}" font-size="10">LIVES: <tspan fill="{PACMAN_YELLOW}" font-size="12">ᗧ ᗧ ᗧ</tspan></text>\n')
    svg.append(f'<text x="{w//2}" y="{h-14}" text-anchor="middle" fill="{ACCENT_MINT}" font-size="10" font-weight="700">● {total_commits} COMMITS ACROSS 53 WEEKS · {active_days} ACTIVE DAYS</text>\n')
    svg.append(f'<text x="{w-25}" y="{h-14}" text-anchor="end" fill="{MUTED_COLOR}" font-size="10">STAGE 01 · INSERT COIN</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    print("Loading contributions...")
    contribs = load_contributions()
    print(f"Loaded {len(contribs)} contribution days.")
    svg_content = build_pacman_svg(contribs)
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(svg_content, encoding="utf-8")
    size_kb = OUT_SVG.stat().st_size / 1024
    print(f"Generated {OUT_SVG} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
