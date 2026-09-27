#!/usr/bin/env python3
"""Generate Dark-Theme Neon Bento Social Cards for GitHub Profile README.

Outputs into:
    assets/socials/connect-header.svg
    assets/socials/connect-linkedin.svg
    assets/socials/connect-leetcode.svg
    assets/socials/connect-kaggle.svg
    assets/socials/connect-hackerearth.svg
    assets/socials/connect-gmail.svg
"""

import json
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "assets/socials"
ICONS_FILE = ROOT / "scripts/banner/data/social_icons.json"

BG_COLOR = "#0A101F"
BORDER_BASE = "#1E3A5F"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#94A3B8"


def get_icons():
    with open(ICONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_dark_header():
    w, h = 810, 72
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">\n')
    svg.append('<defs>\n')
    svg.append(
        '  <linearGradient id="rainbow-border" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        '    <stop offset="0%" stop-color="#38BDF8"/>\n'
        '    <stop offset="25%" stop-color="#FB923C"/>\n'
        '    <stop offset="50%" stop-color="#00FF9F"/>\n'
        '    <stop offset="75%" stop-color="#A855F7"/>\n'
        '    <stop offset="100%" stop-color="#F43F5E"/>\n'
        '  </linearGradient>\n'
    )
    svg.append(
        '  <filter id="soft-glow" x="-10%" y="-10%" width="120%" height="120%">\n'
        '    <feGaussianBlur stdDeviation="2" result="blur"/>\n'
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        '  </filter>\n'
    )
    svg.append('</defs>\n')

    # Dark background card with neon rainbow border
    svg.append(f'<rect width="{w}" height="{h}" rx="18" fill="{BG_COLOR}" stroke="url(#rainbow-border)" stroke-width="1.8"/>\n')

    # Waving hand icon with playful bounce
    svg.append(
        '<!-- Animated Waving Hand -->\n'
        '<g transform="translate(24, 18)">\n'
        f'  <rect width="36" height="36" rx="10" fill="#131D31" stroke="{BORDER_BASE}" stroke-width="1.2"/>\n'
        '  <text x="18" y="25" font-size="20" text-anchor="middle">\n'
        '    <animateTransform attributeName="transform" type="rotate" values="0 18 25; 18 18 25; -12 18 25; 18 18 25; 0 18 25" dur="1.8s" repeatCount="indefinite"/>\n'
        '    👋\n'
        '  </text>\n'
        '</g>\n'
    )

    # Title & Subtitle in dark theme
    svg.append(f'<text x="74" y="32" fill="{TEXT_WHITE}" font-size="14.5" font-weight="800" letter-spacing="0.2">LET\'S CONNECT &amp; SAY HELLO! <tspan fill="#F43F5E" font-size="14">✨</tspan></text>\n')
    svg.append(f'<text x="74" y="52" fill="{TEXT_MUTED}" font-size="10.5" font-weight="500">Drop by to chat about projects, open-source collabs, tech ideas or just say hi 💬</text>\n')

    # Cute status pill on right (Dark emerald)
    pill_w = 175
    pill_h = 32
    pill_x = w - pill_w - 20
    pill_y = (h - pill_h) / 2
    svg.append(f'<rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" rx="16" fill="#0A2A1E" stroke="#10B981" stroke-width="1.2"/>\n')
    # Pulsing green dot
    svg.append(
        f'<circle cx="{pill_x + 16}" cy="{pill_y + 16}" r="4.5" fill="#00FF9F" filter="url(#soft-glow)">\n'
        f'  <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>\n'
        f'</circle>\n'
    )
    svg.append(f'<text x="{pill_x + 28}" y="{pill_y + 20}" fill="#00FF9F" font-size="10" font-weight="800" letter-spacing="0.5">OPEN TO COLLAB 🚀</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def build_dark_card(icon_name, icon_path, title, subtitle, handle, channel, brand_color, emoji, is_wide=False):
    w = 810 if is_wide else 395
    h = 94
    grad_id = f"dark-bg-{icon_name}"
    glow_id = f"glow-{icon_name}"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:{BG_COLOR}; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">\n')
    svg.append('<defs>\n')
    svg.append(
        f'  <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        f'    <stop offset="0%" stop-color="{brand_color}" stop-opacity="0.25"/>\n'
        f'    <stop offset="45%" stop-color="#0E172A" stop-opacity="0.95"/>\n'
        f'    <stop offset="100%" stop-color="{BG_COLOR}" stop-opacity="1"/>\n'
        f'  </linearGradient>\n'
    )
    svg.append(
        f'  <filter id="{glow_id}" x="-30%" y="-30%" width="160%" height="160%">\n'
        f'    <feGaussianBlur stdDeviation="2.5" result="blur"/>\n'
        f'    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>\n'
        f'  </filter>\n'
    )
    svg.append('</defs>\n')

    # Card background: Deep Dark glassmorphic with neon colored border
    svg.append(f'<rect width="{w}" height="{h}" rx="18" fill="url(#{grad_id})" stroke="{brand_color}" stroke-width="1.4"/>\n')

    # Icon Pod on Left (Dark container with neon border)
    pod_size = 54
    pod_x = 16
    pod_y = (h - pod_size) / 2
    svg.append(f'<rect x="{pod_x}" y="{pod_y:.1f}" width="{pod_size}" height="{pod_size}" rx="14" '
               f'fill="#0D1627" stroke="{brand_color}" stroke-width="1.2" stroke-opacity="0.8"/>\n')

    # Center official icon inside pod with glowing neon color
    icon_scale = 1.25
    icon_ox = pod_x + (pod_size - 24 * icon_scale) / 2
    icon_oy = pod_y + (pod_size - 24 * icon_scale) / 2
    svg.append(
        f'<g transform="translate({icon_ox:.1f}, {icon_oy:.1f}) scale({icon_scale})" filter="url(#{glow_id})">\n'
        f'  <path d="{icon_path}" fill="{brand_color}"/>\n'
        f'</g>\n'
    )

    # Text details (Clean escaped text)
    text_x = pod_x + pod_size + 14
    esc_channel = html.escape(channel)
    esc_title = html.escape(title)
    esc_sub = html.escape(subtitle)
    esc_handle = html.escape(handle)

    svg.append(f'<text x="{text_x}" y="28" fill="{brand_color}" font-size="9" font-weight="700" letter-spacing="0.6">{esc_channel} {emoji}</text>\n')
    svg.append(f'<text x="{text_x}" y="48" fill="{TEXT_WHITE}" font-size="14.5" font-weight="800" letter-spacing="0.3">{esc_title}</text>\n')
    svg.append(f'<text x="{text_x}" y="67" fill="{TEXT_MUTED}" font-size="10" font-weight="500">{esc_sub}</text>\n')

    # Action / Handle Pill on Right (Dark container with glowing border)
    if not is_wide:
        pill_w = 122
        pill_h = 32
        pill_x = w - pill_w - 14
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="16" '
                   f'fill="#0D1627" stroke="{brand_color}" stroke-width="1.2" stroke-opacity="0.85"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 20:.1f}" text-anchor="middle" '
                   f'fill="{brand_color}" font-size="10.5" font-weight="800">{esc_handle} <tspan font-size="11">↗</tspan></text>\n')
    else:
        # Wide layout for Gmail
        pill_w = 265
        pill_h = 36
        pill_x = w - pill_w - 18
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="18" '
                   f'fill="#0D1627" stroke="{brand_color}" stroke-width="1.4" stroke-opacity="0.85"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 23:.1f}" text-anchor="middle" '
                   f'fill="{brand_color}" font-size="11.5" font-weight="800">{esc_handle} <tspan font-size="12">✉ ↗</tspan></text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    icons = get_icons()

    # 1. Dark Header Card
    header_svg = build_dark_header()
    (OUT_DIR / "connect-header.svg").write_text(header_svg, encoding="utf-8")
    print("Generated connect-header.svg (Dark Theme)")

    # 5 Bright Distinct Neon Colors on Dark Theme
    cards = [
        {
            "filename": "connect-linkedin.svg",
            "icon_name": "linkedin",
            "title": "LINKEDIN",
            "subtitle": "Professional Network & Career Besties",
            "handle": "@nilesh-sahoo",
            "channel": "COMMUNITY & CONNECT",
            "brand_color": "#38BDF8",   # Neon Sky Blue
            "emoji": "🤝",
            "is_wide": False,
        },
        {
            "filename": "connect-leetcode.svg",
            "icon_name": "leetcode",
            "title": "LEETCODE",
            "subtitle": "Daily Brain Puzzles · 197+ Solved",
            "handle": "@1nilesh0837",
            "channel": "DSA & CODING",
            "brand_color": "#FFA116",   # LeetCode Neon Amber
            "emoji": "🧩",
            "is_wide": False,
        },
        {
            "filename": "connect-kaggle.svg",
            "icon_name": "kaggle",
            "title": "KAGGLE",
            "subtitle": "Data Science & Machine Learning Hub",
            "handle": "@nileshsahoo07",
            "channel": "AI & DATA SCIENCE",
            "brand_color": "#00E5FF",   # Electric Cyan
            "emoji": "🤖",
            "is_wide": False,
        },
        {
            "filename": "connect-hackerearth.svg",
            "icon_name": "hackerearth",
            "title": "HACKEREARTH",
            "subtitle": "Coding Contests & Problem Solving",
            "handle": "@nileshsahoo837",
            "channel": "ALGORITHM CONTESTS",
            "brand_color": "#A855F7",   # Cyberpunk Purple
            "emoji": "⚡",
            "is_wide": False,
        },
        {
            "filename": "connect-gmail.svg",
            "icon_name": "gmail",
            "title": "DIRECT EMAIL INQUIRY",
            "subtitle": "Freelance, fun collabs, research or casual talks",
            "handle": "nileshsahoo837@gmail.com",
            "channel": "SAY HELLO ANYTIME",
            "brand_color": "#F43F5E",   # Neon Strawberry Rose
            "emoji": "💌",
            "is_wide": True,
        },
    ]

    for c in cards:
        svg_content = build_dark_card(
            icon_name=c["icon_name"],
            icon_path=icons[c["icon_name"]],
            title=c["title"],
            subtitle=c["subtitle"],
            handle=c["handle"],
            channel=c["channel"],
            brand_color=c["brand_color"],
            emoji=c["emoji"],
            is_wide=c["is_wide"]
        )
        (OUT_DIR / c["filename"]).write_text(svg_content, encoding="utf-8")
        print(f"Generated {c['filename']}")


if __name__ == "__main__":
    main()
