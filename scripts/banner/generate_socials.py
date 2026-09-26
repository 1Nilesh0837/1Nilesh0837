#!/usr/bin/env python3
"""Generate Cute, Light-Theme, Bright Colorful Social Cards for GitHub Profile README.

Outputs into:
    assets/socials/cute-header.svg
    assets/socials/cute-linkedin.svg
    assets/socials/cute-leetcode.svg
    assets/socials/cute-kaggle.svg
    assets/socials/cute-hackerearth.svg
    assets/socials/cute-gmail.svg
"""

import json
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "assets/socials"
ICONS_FILE = ROOT / "scripts/banner/data/social_icons.json"


def get_icons():
    with open(ICONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cute_header():
    w, h = 810, 72
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:transparent; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">\n')
    svg.append('<defs>\n')
    svg.append(
        '  <linearGradient id="rainbow-border" x1="0%" y1="0%" x2="100%" y2="0%">\n'
        '    <stop offset="0%" stop-color="#38BDF8"/>\n'
        '    <stop offset="25%" stop-color="#FB923C"/>\n'
        '    <stop offset="50%" stop-color="#22D3EE"/>\n'
        '    <stop offset="75%" stop-color="#A855F7"/>\n'
        '    <stop offset="100%" stop-color="#F43F5E"/>\n'
        '  </linearGradient>\n'
    )
    svg.append(
        '  <linearGradient id="header-bg" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        '    <stop offset="0%" stop-color="#FFFFFF"/>\n'
        '    <stop offset="100%" stop-color="#F8FAFC"/>\n'
        '  </linearGradient>\n'
    )
    svg.append(
        '  <filter id="soft-shadow" x="-5%" y="-5%" width="110%" height="115%">\n'
        '    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>\n'
        '  </filter>\n'
    )
    svg.append('</defs>\n')

    # Background card with cute rainbow border
    svg.append(f'<rect width="{w}" height="{h}" rx="18" fill="url(#header-bg)" stroke="url(#rainbow-border)" stroke-width="2" filter="url(#soft-shadow)"/>\n')

    # Waving hand icon with playful bounce
    svg.append(
        '<!-- Animated Waving Hand -->\n'
        '<g transform="translate(24, 18)">\n'
        '  <rect width="36" height="36" rx="10" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1.2"/>\n'
        '  <text x="18" y="25" font-size="20" text-anchor="middle">\n'
        '    <animateTransform attributeName="transform" type="rotate" values="0 18 25; 18 18 25; -12 18 25; 18 18 25; 0 18 25" dur="1.8s" repeatCount="indefinite"/>\n'
        '    👋\n'
        '  </text>\n'
        '</g>\n'
    )

    # Title & Subtitle
    svg.append('<text x="74" y="32" fill="#0F172A" font-size="14.5" font-weight="800" letter-spacing="0.2">LET\'S CONNECT &amp; SAY HELLO! <tspan fill="#F43F5E" font-size="14">✨</tspan></text>\n')
    svg.append('<text x="74" y="52" fill="#64748B" font-size="10.5" font-weight="500">Drop by to chat about projects, open-source collabs, tech ideas or just say hi 💬</text>\n')

    # Cute status pill on right
    pill_w = 175
    pill_h = 32
    pill_x = w - pill_w - 20
    pill_y = (h - pill_h) / 2
    svg.append(f'<rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" rx="16" fill="#ECFDF5" stroke="#10B981" stroke-width="1.2"/>\n')
    # Pulsing green dot
    svg.append(
        f'<circle cx="{pill_x + 16}" cy="{pill_y + 16}" r="4.5" fill="#10B981">\n'
        f'  <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>\n'
        f'</circle>\n'
    )
    svg.append(f'<text x="{pill_x + 28}" y="{pill_y + 20}" fill="#047857" font-size="10" font-weight="800" letter-spacing="0.5">OPEN TO COLLAB 🚀</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def build_cute_card(icon_name, icon_path, title, subtitle, handle, channel, brand_color, bg_tint, pill_bg, emoji, is_wide=False):
    w = 810 if is_wide else 395
    h = 94
    grad_id = f"cute-bg-{icon_name}"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" '
               f'style="background:transparent; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">\n')
    svg.append('<defs>\n')
    svg.append(
        f'  <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        f'    <stop offset="0%" stop-color="#FFFFFF"/>\n'
        f'    <stop offset="65%" stop-color="#FFFFFF"/>\n'
        f'    <stop offset="100%" stop-color="{bg_tint}"/>\n'
        f'  </linearGradient>\n'
    )
    svg.append(
        '  <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="115%">\n'
        '    <feDropShadow dx="0" dy="2" stdDeviation="3.5" flood-opacity="0.06"/>\n'
        '  </filter>\n'
    )
    svg.append('</defs>\n')

    # Card background: Clean crisp white with pastel undertone and colored border
    svg.append(f'<rect width="{w}" height="{h}" rx="18" fill="url(#{grad_id})" stroke="{brand_color}" stroke-width="1.6" filter="url(#card-shadow)"/>\n')

    # Icon Pod on Left
    pod_size = 54
    pod_x = 16
    pod_y = (h - pod_size) / 2
    svg.append(f'<rect x="{pod_x}" y="{pod_y:.1f}" width="{pod_size}" height="{pod_size}" rx="14" '
               f'fill="{pill_bg}" stroke="{brand_color}" stroke-width="1.2"/>\n')

    # Center official icon inside pod
    icon_scale = 1.25
    icon_ox = pod_x + (pod_size - 24 * icon_scale) / 2
    icon_oy = pod_y + (pod_size - 24 * icon_scale) / 2
    svg.append(
        f'<g transform="translate({icon_ox:.1f}, {icon_oy:.1f}) scale({icon_scale})">\n'
        f'  <path d="{icon_path}" fill="{brand_color}"/>\n'
        f'</g>\n'
    )

    # Text details (All escaped properly for XML validity)
    text_x = pod_x + pod_size + 14
    esc_channel = html.escape(channel)
    esc_title = html.escape(title)
    esc_sub = html.escape(subtitle)
    esc_handle = html.escape(handle)

    svg.append(f'<text x="{text_x}" y="28" fill="{brand_color}" font-size="9" font-weight="700" letter-spacing="0.6">{esc_channel} {emoji}</text>\n')
    svg.append(f'<text x="{text_x}" y="48" fill="#0F172A" font-size="14.5" font-weight="800" letter-spacing="0.3">{esc_title}</text>\n')
    svg.append(f'<text x="{text_x}" y="67" fill="#64748B" font-size="10" font-weight="500">{esc_sub}</text>\n')

    # Cute Action / Handle Pill on Right
    if not is_wide:
        pill_w = 122
        pill_h = 32
        pill_x = w - pill_w - 14
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="16" '
                   f'fill="{pill_bg}" stroke="{brand_color}" stroke-width="1.2"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 20:.1f}" text-anchor="middle" '
                   f'fill="{brand_color}" font-size="10.5" font-weight="800">{esc_handle} <tspan font-size="11">↗</tspan></text>\n')
    else:
        # Wide layout for Gmail
        pill_w = 265
        pill_h = 36
        pill_x = w - pill_w - 18
        pill_y = (h - pill_h) / 2
        svg.append(f'<rect x="{pill_x}" y="{pill_y:.1f}" width="{pill_w}" height="{pill_h}" rx="18" '
                   f'fill="{pill_bg}" stroke="{brand_color}" stroke-width="1.4"/>\n')
        svg.append(f'<text x="{pill_x + pill_w/2:.1f}" y="{pill_y + 23:.1f}" text-anchor="middle" '
                   f'fill="{brand_color}" font-size="11.5" font-weight="800">{esc_handle} <tspan font-size="12">✉ ↗</tspan></text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    icons = get_icons()

    # 1. Header Card (cute-header.svg)
    header_svg = build_cute_header()
    (OUT_DIR / "cute-header.svg").write_text(header_svg, encoding="utf-8")
    print("Generated cute-header.svg")

    # 5 Bright Different Cute Colors
    cards = [
        {
            "filename": "cute-linkedin.svg",
            "icon_name": "linkedin",
            "title": "LINKEDIN",
            "subtitle": "Professional Network & Career Besties",
            "handle": "@nilesh-sahoo",
            "channel": "COMMUNITY & CONNECT",
            "brand_color": "#0284C7",   # Bright Electric Sky Blue
            "bg_tint": "#F0F9FF",
            "pill_bg": "#E0F2FE",
            "emoji": "🤝",
            "is_wide": False,
        },
        {
            "filename": "cute-leetcode.svg",
            "icon_name": "leetcode",
            "title": "LEETCODE",
            "subtitle": "Daily Brain Puzzles · 197+ Solved",
            "handle": "@1nilesh0837",
            "channel": "DSA & CODING",
            "brand_color": "#EA580C",   # Bright Warm Sunny Orange
            "bg_tint": "#FFF7ED",
            "pill_bg": "#FFEDD5",
            "emoji": "🧩",
            "is_wide": False,
        },
        {
            "filename": "cute-kaggle.svg",
            "icon_name": "kaggle",
            "title": "KAGGLE",
            "subtitle": "Data Science & Machine Learning Hub",
            "handle": "@nileshsahoo07",
            "channel": "AI & DATA SCIENCE",
            "brand_color": "#0891B2",   # Bright Vibrant Aquamarine / Teal
            "bg_tint": "#ECFEFF",
            "pill_bg": "#CFFAFE",
            "emoji": "🤖",
            "is_wide": False,
        },
        {
            "filename": "cute-hackerearth.svg",
            "icon_name": "hackerearth",
            "title": "HACKEREARTH",
            "subtitle": "Coding Contests & Problem Solving",
            "handle": "@nileshsahoo837",
            "channel": "ALGORITHM CONTESTS",
            "brand_color": "#7C3AED",   # Bright Royal Violet
            "bg_tint": "#FAF5FF",
            "pill_bg": "#F3E8FF",
            "emoji": "⚡",
            "is_wide": False,
        },
        {
            "filename": "cute-gmail.svg",
            "icon_name": "gmail",
            "title": "DIRECT EMAIL INQUIRY",
            "subtitle": "Freelance, fun collabs, research or casual talks",
            "handle": "nileshsahoo837@gmail.com",
            "channel": "SAY HELLO ANYTIME",
            "brand_color": "#E11D48",   # Bright Cute Strawberry Rose
            "bg_tint": "#FFF1F2",
            "pill_bg": "#FFE4E6",
            "emoji": "💌",
            "is_wide": True,
        },
    ]

    for c in cards:
        svg_content = build_cute_card(
            icon_name=c["icon_name"],
            icon_path=icons[c["icon_name"]],
            title=c["title"],
            subtitle=c["subtitle"],
            handle=c["handle"],
            channel=c["channel"],
            brand_color=c["brand_color"],
            bg_tint=c["bg_tint"],
            pill_bg=c["pill_bg"],
            emoji=c["emoji"],
            is_wide=c["is_wide"]
        )
        (OUT_DIR / c["filename"]).write_text(svg_content, encoding="utf-8")
        print(f"Generated {c['filename']}")


if __name__ == "__main__":
    main()
