#!/usr/bin/env python3
"""Generate Cyber Holographic Bento Grid Social Cards for GitHub Profile README.

Outputs into:
    assets/socials/comms-header.svg
    assets/socials/card-linkedin.svg
    assets/socials/card-leetcode.svg
    assets/socials/card-kaggle.svg
    assets/socials/card-hackerearth.svg
    assets/socials/card-gmail.svg
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "assets/socials"
ICONS_FILE = ROOT / "scripts/banner/data/social_icons.json"

BG_COLOR = "#0A101F"
BORDER_BASE = "#1E3A5F"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#7A9EC5"
TEXT_CYAN = "#38BDF8"
ACCENT_MINT = "#00FF9F"


def get_icons():
    with open(ICONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_comms_header():
    w, h = 810, 68
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',Consolas,monospace;">\n')
    svg.append('<defs>\n')
    svg.append(
        '  <filter id="green-glow" x="-40%" y="-40%" width="180%" height="180%">\n'
        '    <feGaussianBlur stdDeviation="3" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <filter id="cyan-glow" x="-40%" y="-40%" width="180%" height="180%">\n'
        '    <feGaussianBlur stdDeviation="2.5" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append(
        '  <linearGradient id="header-border" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        f'    <stop offset="0%" stop-color="{ACCENT_MINT}" stop-opacity="0.8"/>\n'
        f'    <stop offset="50%" stop-color="{TEXT_CYAN}" stop-opacity="0.4"/>\n'
        f'    <stop offset="100%" stop-color="{BORDER_BASE}" stop-opacity="0.8"/>\n'
        '  </linearGradient>\n'
    )
    svg.append('</defs>\n')

    # Background card
    svg.append(f'<rect width="{w}" height="{h}" rx="10" fill="#0A101F" stroke="url(#header-border)" stroke-width="1.2"/>\n')

    # Radar Scope on Left
    rcx, rcy, rad = 38, 34, 18
    svg.append(f'<circle cx="{rcx}" cy="{rcy}" r="{rad}" fill="#0D1627" stroke="{BORDER_BASE}" stroke-width="1"/>\n')
    svg.append(f'<circle cx="{rcx}" cy="{rcy}" r="{rad*0.6:.1f}" fill="none" stroke="{BORDER_BASE}" stroke-width="0.8" stroke-dasharray="2,2"/>\n')
    svg.append(f'<circle cx="{rcx}" cy="{rcy}" r="{rad*0.3:.1f}" fill="none" stroke="{BORDER_BASE}" stroke-width="0.8"/>\n')
    svg.append(f'<line x1="{rcx-rad}" y1="{rcy}" x2="{rcx+rad}" y2="{rcy}" stroke="{BORDER_BASE}" stroke-width="0.7"/>\n')
    svg.append(f'<line x1="{rcx}" y1="{rcy-rad}" x2="{rcx}" y2="{rcy+rad}" stroke="{BORDER_BASE}" stroke-width="0.7"/>\n')

    # Rotating radar sweep
    svg.append(
        f'<g>\n'
        f'  <line x1="{rcx}" y1="{rcy}" x2="{rcx}" y2="{rcy-rad}" stroke="{ACCENT_MINT}" stroke-width="1.8" stroke-linecap="round" filter="url(#green-glow)"/>\n'
        f'  <animateTransform attributeName="transform" type="rotate" from="0 {rcx} {rcy}" to="360 {rcx} {rcy}" dur="3.5s" repeatCount="indefinite"/>\n'
        f'</g>\n'
    )
    # Pulsing detected blip
    svg.append(
        f'<circle cx="{rcx+8}" cy="{rcy-6}" r="2" fill="{ACCENT_MINT}">\n'
        f'  <animate attributeName="opacity" values="0.1;1;0.1" dur="3.5s" repeatCount="indefinite"/>\n'
        f'</circle>\n'
    )

    # Title & Telemetry Header
    svg.append(f'<text x="68" y="27" fill="{TEXT_MUTED}" font-size="9" letter-spacing="1">/// QUANTUM COMMS LINK // PORT 8080 // CH-01..05</text>\n')
    svg.append(f'<text x="68" y="47" fill="{TEXT_WHITE}" font-size="14" font-weight="900" letter-spacing="1.2">TRANSMIT &amp; CONNECT <tspan fill="{ACCENT_MINT}" font-size="10">● ONLINE</tspan></text>\n')

    # Center Telemetry Waveform Bars
    eq_x = 380
    bar_heights = [12, 22, 16, 26, 14, 20, 10, 18]
    for i, bh in enumerate(bar_heights):
        bx = eq_x + i * 8
        by = 34 - bh / 2
        durs = [1.2, 0.9, 1.4, 0.8, 1.1, 1.3, 0.7, 1.0]
        dur = durs[i % len(durs)]
        svg.append(
            f'<rect x="{bx}" y="{by:.1f}" width="4" height="{bh}" rx="2" fill="{TEXT_CYAN}" opacity="0.85">\n'
            f'  <animate attributeName="height" values="{bh};{max(6, bh*0.4):.1f};{bh}" dur="{dur}s" repeatCount="indefinite"/>\n'
            f'  <animate attributeName="y" values="{by:.1f};{34 - max(6, bh*0.4)/2:.1f};{by:.1f}" dur="{dur}s" repeatCount="indefinite"/>\n'
            f'</rect>\n'
        )

    # Status Beacon on Right
    sb_x = 560
    svg.append(
        f'<circle cx="{sb_x}" cy="34" r="5" fill="{ACCENT_MINT}" filter="url(#green-glow)">\n'
        f'  <animate attributeName="opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite"/>\n'
        f'</circle>\n'
    )
    svg.append(
        f'<circle cx="{sb_x}" cy="34" r="9" fill="none" stroke="{ACCENT_MINT}" stroke-width="1" opacity="0.6">\n'
        f'  <animate attributeName="r" values="5;12;5" dur="1.8s" repeatCount="indefinite"/>\n'
        f'  <animate attributeName="opacity" values="0.8;0;0.8" dur="1.8s" repeatCount="indefinite"/>\n'
        f'</circle>\n'
    )
    svg.append(f'<text x="{sb_x + 18}" y="31" fill="{TEXT_MUTED}" font-size="9" letter-spacing="0.8">SIGNAL PROTOCOL</text>\n')
    svg.append(f'<text x="{sb_x + 18}" y="45" fill="{ACCENT_MINT}" font-size="11" font-weight="800" letter-spacing="0.5">OPEN TO COLLABORATION</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def build_card(icon_name, icon_path, title, subtitle, handle, channel, color_hex, is_wide=False):
    w = 810 if is_wide else 395
    h = 92
    grad_id = f"grad-{icon_name}"
    glow_id = f"glow-{icon_name}"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\',Consolas,monospace;">\n')
    svg.append('<defs>\n')
    svg.append(
        f'  <filter id="{glow_id}" x="-30%" y="-30%" width="160%" height="160%">\n'
        f'    <feGaussianBlur stdDeviation="2.5" result="blur"/>\n'
        f'    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        f'  </filter>\n'
    )
    svg.append(
        f'  <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        f'    <stop offset="0%" stop-color="{color_hex}" stop-opacity="0.35"/>\n'
        f'    <stop offset="40%" stop-color="#0E172A" stop-opacity="0.95"/>\n'
        f'    <stop offset="100%" stop-color="#0A101F" stop-opacity="1"/>\n'
        f'  </linearGradient>\n'
    )
    svg.append(
        f'  <linearGradient id="border-{icon_name}" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        f'    <stop offset="0%" stop-color="{color_hex}" stop-opacity="0.9"/>\n'
        f'    <stop offset="35%" stop-color="{color_hex}" stop-opacity="0.4"/>\n'
        f'    <stop offset="100%" stop-color="{BORDER_BASE}" stop-opacity="0.4"/>\n'
        f'  </linearGradient>\n'
    )
    svg.append('</defs>\n')

    # Card background with gradient & border
    svg.append(f'<rect width="{w}" height="{h}" rx="12" fill="url(#{grad_id})" stroke="url(#border-{icon_name})" stroke-width="1.2"/>\n')

    # Corner brackets / tech accents
    svg.append(f'<path d="M12,6 L6,6 L6,12" stroke="{color_hex}" stroke-width="1" fill="none" opacity="0.6"/>\n')
    svg.append(f'<path d="M{w-12},6 L{w-6},6 L{w-6},12" stroke="{color_hex}" stroke-width="1" fill="none" opacity="0.4"/>\n')
    svg.append(f'<path d="M12,{h-6} L6,{h-6} L6,{h-12}" stroke="{color_hex}" stroke-width="1" fill="none" opacity="0.4"/>\n')
    svg.append(f'<path d="M{w-12},{h-6} L{w-6},{h-6} L{w-6},{h-12}" stroke="{color_hex}" stroke-width="1" fill="none" opacity="0.4"/>\n')

    # Icon Pod on Left
    pod_size = 54
    pod_x = 16
    pod_y = (h - pod_size) / 2
    svg.append(f'<rect x="{pod_x}" y="{pod_y:.1f}" width="{pod_size}" height="{pod_size}" rx="10" '
               f'fill="#0D1627" stroke="{color_hex}" stroke-width="1" stroke-opacity="0.6"/>\n')

    # Center 24x24 icon inside 54x54 pod (scale 1.25, offset to center)
    # 24 * 1.25 = 30px width. (54 - 30) / 2 = 12px padding
    icon_scale = 1.25
    icon_ox = pod_x + (pod_size - 24 * icon_scale) / 2
    icon_oy = pod_y + (pod_size - 24 * icon_scale) / 2
    svg.append(
        f'<g transform="translate({icon_ox:.1f}, {icon_oy:.1f}) scale({icon_scale})" filter="url(#{glow_id})">\n'
        f'  <path d="{icon_path}" fill="{color_hex}"/>\n'
        f'</g>\n'
    )

    # Text details
    text_x = pod_x + pod_size + 14
    svg.append(f'<text x="{text_x}" y="28" fill="{TEXT_MUTED}" font-size="8.5" font-weight="600" letter-spacing="1">{channel}</text>\n')
    svg.append(f'<text x="{text_x}" y="47" fill="{TEXT_WHITE}" font-size="13.5" font-weight="900" letter-spacing="0.5">{title}</text>\n')
    svg.append(f'<text x="{text_x}" y="66" fill="{TEXT_MUTED}" font-size="9.5">{subtitle}</text>\n')

    # Action / Handle Pill on Right
    if not is_wide:
        pill_w = 118
        pill_h = 30
        pill_x = w - pill_w - 14
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="15" '
                   f'fill="#0D1627" stroke="{color_hex}" stroke-width="1" stroke-opacity="0.7"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 19:.1f}" text-anchor="middle" '
                   f'fill="{color_hex}" font-size="10" font-weight="700">{handle} <tspan font-size="11">↗</tspan></text>\n')
    else:
        # Wide layout for Gmail
        pill_w = 270
        pill_h = 34
        pill_x = w - pill_w - 18
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="17" '
                   f'fill="#0D1627" stroke="{color_hex}" stroke-width="1.2" stroke-opacity="0.8"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 22:.1f}" text-anchor="middle" '
                   f'fill="{color_hex}" font-size="11" font-weight="800">{handle} <tspan font-size="12">✉ ↗</tspan></text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    icons = get_icons()

    # 1. Comms Header
    header_svg = build_comms_header()
    (OUT_DIR / "comms-header.svg").write_text(header_svg, encoding="utf-8")
    print("Generated comms-header.svg")

    cards = [
        {
            "filename": "card-linkedin.svg",
            "icon_name": "linkedin",
            "title": "LINKEDIN",
            "subtitle": "Professional Network · Let's Connect",
            "handle": "@nilesh-sahoo",
            "channel": "CH-01 // NETWORKING",
            "color": "#38BDF8",  # Cyber Cyan
            "is_wide": False,
        },
        {
            "filename": "card-leetcode.svg",
            "icon_name": "leetcode",
            "title": "LEETCODE",
            "subtitle": "DSA & Problem Solving · 197+ Solved",
            "handle": "@1nilesh0837",
            "channel": "CH-02 // ALGORITHMS",
            "color": "#FFA116",  # LeetCode Neon Amber
            "is_wide": False,
        },
        {
            "filename": "card-kaggle.svg",
            "icon_name": "kaggle",
            "title": "KAGGLE",
            "subtitle": "Machine Learning & Data Science",
            "handle": "@nileshsahoo07",
            "channel": "CH-03 // DATA SCIENCE",
            "color": "#00E5FF",  # Kaggle Electric Azure
            "is_wide": False,
        },
        {
            "filename": "card-hackerearth.svg",
            "icon_name": "hackerearth",
            "title": "HACKEREARTH",
            "subtitle": "Competitive Coding & Contests",
            "handle": "@nileshsahoo837",
            "channel": "CH-04 // CONTESTS",
            "color": "#A855F7",  # Cyberpunk Purple
            "is_wide": False,
        },
        {
            "filename": "card-gmail.svg",
            "icon_name": "gmail",
            "title": "DIRECT EMAIL INQUIRY",
            "subtitle": "Freelance · Collaborations · Tech Discussions",
            "handle": "nileshsahoo837@gmail.com",
            "channel": "CH-05 // ENCRYPTED INBOX",
            "color": "#EF4444",  # Coral Flame
            "is_wide": True,
        },
    ]

    for c in cards:
        svg_content = build_card(
            icon_name=c["icon_name"],
            icon_path=icons[c["icon_name"]],
            title=c["title"],
            subtitle=c["subtitle"],
            handle=c["handle"],
            channel=c["channel"],
            color_hex=c["color"],
            is_wide=c["is_wide"]
        )
        (OUT_DIR / c["filename"]).write_text(svg_content, encoding="utf-8")
        print(f"Generated {c['filename']}")


if __name__ == "__main__":
    main()
