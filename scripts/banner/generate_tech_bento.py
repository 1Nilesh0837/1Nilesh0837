#!/usr/bin/env python3
"""Generate Dark Cyber Bento Grid SVG for 'Tech I Work With' section.

Builds:
    assets/tech-bento.svg (830x350)
Featuring 4 dark glassmorphism pods with glowing neon accents and high-contrast
dark-themed skill badges.
"""

from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[2]
OUT_SVG = ROOT / "assets/tech-bento.svg"

BG_COLOR = "#0A101F"
BORDER_BASE = "#1E3A5F"

PODS = [
    {
        "title": "AI / MACHINE LEARNING & VISION",
        "tag": "AI MATRIX",
        "accent": "#38BDF8",
        "skills_row1": [
            ("Python", "#38BDF8"),
            ("PyTorch", "#EE4C2C"),
            ("TensorFlow", "#FF6F00"),
            ("OpenCV", "#5C3EE8"),
        ],
        "skills_row2": [
            ("Scikit-Learn", "#F7931E"),
            ("R Lang", "#276DC3"),
            ("MATLAB", "#E16727"),
        ],
    },
    {
        "title": "DATA & ADVANCED ANALYTICS",
        "tag": "BIG DATA",
        "accent": "#FACC15",
        "skills_row1": [
            ("Pandas", "#38BDF8"),
            ("NumPy", "#4DABCF"),
            ("MySQL", "#4479A1"),
            ("Hadoop", "#66CCFF"),
        ],
        "skills_row2": [
            ("Power BI", "#F2C811"),
            ("Excel", "#217346"),
            ("PL/pgSQL", "#336791"),
        ],
    },
    {
        "title": "FRONTEND & MOBILE DEV",
        "tag": "CLIENT LAYER",
        "accent": "#A855F7",
        "skills_row1": [
            ("React", "#61DAFB"),
            ("Flutter", "#54C5F8"),
            ("Dart", "#0175C2"),
            ("Node.js", "#339933"),
        ],
        "skills_row2": [
            ("Tailwind CSS", "#06B6D4"),
            ("HTML5", "#E34F26"),
            ("CSS3", "#1572B6"),
            ("TypeScript", "#3178C6"),
        ],
    },
    {
        "title": "SYSTEMS, DEVOPS & TOOLS",
        "tag": "CORE INFRA",
        "accent": "#00FF9F",
        "skills_row1": [
            ("Docker", "#2496ED"),
            ("Linux", "#FCC624"),
            ("Git", "#F05032"),
            ("GitHub", "#FFFFFF"),
        ],
        "skills_row2": [
            ("VS Code", "#007ACC"),
            ("MongoDB", "#47A248"),
            ("C Lang", "#A8B9CC"),
            ("Java", "#ED8B00"),
        ],
    },
]


def render_badge(x, y, name, color):
    # Calculate pill width based on text length
    text_w = len(name) * 7.5
    pill_w = max(68, int(text_w + 32))
    svg = []
    svg.append(f'<g transform="translate({x},{y})">\n')
    # Pill background with subtle border
    svg.append(f'  <rect width="{pill_w}" height="28" rx="6" fill="#0D1627" stroke="#1E3A5F" stroke-width="1"/>\n')
    # Inner subtle highlight
    svg.append(f'  <rect x="4" y="1" width="{pill_w-8}" height="1" rx="0.5" fill="#FFFFFF" opacity="0.08"/>\n')
    # Glowing brand dot
    svg.append(f'  <circle cx="12" cy="14" r="3.5" fill="{color}"/>\n')
    # Skill text
    safe_name = xml_escape(name)
    svg.append(f'  <text x="22" y="17.5" fill="#E2E8F0" font-size="10.5" font-weight="700">{safe_name}</text>\n')
    svg.append('</g>\n')
    return ''.join(svg), pill_w


def render_pod(px, py, pw, ph, pod, pod_idx):
    accent = pod["accent"]
    svg = []

    # Glassmorphism Pod background
    svg.append(f'<g transform="translate({px},{py})">\n')
    # Outer dark rect
    svg.append(f'  <rect width="{pw}" height="{ph}" rx="12" fill="#080E1A" stroke="#1E3A5F" stroke-width="1.2"/>\n')
    # Glass gradient overlay
    svg.append(f'  <rect width="{pw}" height="{ph}" rx="12" fill="url(#pod-glass-grad)" opacity="0.7"/>\n')
    # Glowing top accent line
    svg.append(f'  <rect x="12" y="1" width="{pw-24}" height="2.5" rx="1" fill="url(#accent-grad-{pod_idx})"/>\n')
    
    # Subtle inner corner radar dot
    svg.append(f'  <circle cx="{pw-12}" cy="{ph-12}" r="1.5" fill="{accent}" opacity="0.4"/>\n')

    # Header: Status beacon dot
    svg.append(f'  <circle cx="18" cy="22" r="3.5" fill="{accent}" class="pulse-beacon"/>\n')
    
    # Header: Title
    safe_title = xml_escape(pod["title"])
    svg.append(f'  <text x="28" y="25.5" fill="#FFFFFF" font-size="11" font-weight="800" letter-spacing="0.6">{safe_title}</text>\n')

    # Header: Tag badge (right side)
    tag_w = len(pod["tag"]) * 7 + 16
    tag_x = pw - 14 - tag_w
    svg.append(f'  <rect x="{tag_x}" y="13" width="{tag_w}" height="18" rx="4" fill="{accent}1A" stroke="{accent}" stroke-width="0.8"/>\n')
    svg.append(f'  <text x="{tag_x + tag_w//2}" y="25" text-anchor="middle" fill="{accent}" font-size="8.5" font-weight="800" letter-spacing="0.5">{pod["tag"]}</text>\n')

    # Header Divider
    svg.append(f'  <line x1="12" y1="36" x2="{pw-12}" y2="36" stroke="#1E3A5F" stroke-width="0.8" opacity="0.6"/>\n')

    # Skills Row 1 (y = 46)
    cur_x = 14
    for sname, scolor in pod["skills_row1"]:
        badge_svg, bw = render_badge(cur_x, 46, sname, scolor)
        svg.append("  " + badge_svg)
        cur_x += bw + 8

    # Skills Row 2 (y = 82)
    cur_x = 14
    for sname, scolor in pod["skills_row2"]:
        badge_svg, bw = render_badge(cur_x, 82, sname, scolor)
        svg.append("  " + badge_svg)
        cur_x += bw + 8

    svg.append('</g>\n')
    return ''.join(svg)


def build_tech_bento_svg():
    w, h = 830, 318
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n')
    svg.append('<defs>\n')
    # Glass gradient
    svg.append('  <linearGradient id="pod-glass-grad" x1="0%" y1="0%" x2="100%" y2="100%">\n')
    svg.append('    <stop offset="0%" stop-color="#1E3A5F" stop-opacity="0.15"/>\n')
    svg.append('    <stop offset="100%" stop-color="#0A101F" stop-opacity="0.6"/>\n')
    svg.append('  </linearGradient>\n')

    # Scanner beam gradient
    svg.append('  <linearGradient id="scanner-grad" x1="0%" y1="0%" x2="100%" y2="0%">\n')
    svg.append('    <stop offset="0%" stop-color="#00FF9F" stop-opacity="0"/>\n')
    svg.append('    <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.5"/>\n')
    svg.append('    <stop offset="100%" stop-color="#00FF9F" stop-opacity="0"/>\n')
    svg.append('  </linearGradient>\n')

    # Accent gradients for 4 pods
    accents = ["#38BDF8", "#FACC15", "#A855F7", "#00FF9F"]
    for idx, acc in enumerate(accents):
        svg.append(f'  <linearGradient id="accent-grad-{idx}" x1="0%" y1="0%" x2="100%" y2="0%">\n')
        svg.append(f'    <stop offset="0%" stop-color="{acc}" stop-opacity="0.95"/>\n')
        svg.append(f'    <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.4"/>\n')
        svg.append('  </linearGradient>\n')

    # Styles
    svg.append('  <style>\n')
    svg.append('    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }\n')
    svg.append('    @keyframes pulse-beacon {\n')
    svg.append('      0%, 100% { opacity: 1; transform: scale(1); }\n')
    svg.append('      50% { opacity: 0.3; transform: scale(0.85); }\n')
    svg.append('    }\n')
    svg.append('    @keyframes sweep-beam {\n')
    svg.append('      0% { transform: translateY(0px); opacity: 0; }\n')
    svg.append('      15% { opacity: 0.6; }\n')
    svg.append('      85% { opacity: 0.6; }\n')
    svg.append(f'      100% {{ transform: translateY({h}px); opacity: 0; }}\n')
    svg.append('    }\n')
    svg.append('    .pulse-beacon { animation: pulse-beacon 2s infinite ease-in-out; }\n')
    svg.append('    .sweep-line { animation: sweep-beam 5s infinite linear; }\n')
    svg.append('  </style>\n')
    svg.append('</defs>\n')

    # Main Outer Terminal Frame
    svg.append(f'<rect width="{w}" height="{h}" rx="14" fill="{BG_COLOR}" stroke="{BORDER_BASE}" stroke-width="1.5"/>\n')
    # Top subtle border glow
    svg.append(f'<rect x="20" y="0" width="{w-40}" height="2" fill="url(#accent-grad-0)"/>\n')
    
    # Animated sweeping laser beam
    svg.append(f'<line class="sweep-line" x1="4" y1="0" x2="{w-4}" y2="0" stroke="url(#scanner-grad)" stroke-width="2"/>\n')

    # Top HUD Bar
    svg.append('<text x="20" y="24" fill="#00FF9F" font-size="9.5" font-weight="800" letter-spacing="1">/// TECH ARSENAL // CYBER BENTO MATRIX</text>\n')
    svg.append('<text x="440" y="24" text-anchor="middle" fill="#7A9EC5" font-size="9" font-weight="700" letter-spacing="0.5">STATUS: <tspan fill="#38BDF8">OPTIMAL</tspan> &#160;•&#160; ARCHITECTURE: <tspan fill="#00FF9F">FULL-STACK &amp; AI</tspan></text>\n')
    svg.append(f'<text x="{w-20}" y="24" text-anchor="end" fill="#00FF9F" font-size="9" font-weight="800" letter-spacing="0.5">● 27 SKILLS VERIFIED</text>\n')
    svg.append(f'<line x1="20" y1="34" x2="{w-20}" y2="34" stroke="{BORDER_BASE}" stroke-width="0.8" opacity="0.6"/>\n')

    # Bento Pods Grid (2x2)
    pod_w = 390
    pod_h = 124
    coords = [
        (18, 44),     # Top-Left: AI/ML
        (422, 44),    # Top-Right: Data & Analytics
        (18, 178),    # Bottom-Left: Frontend & Mobile
        (422, 178),   # Bottom-Right: DevOps & Systems
    ]

    for idx, pod in enumerate(PODS):
        cx, cy = coords[idx]
        svg.append(render_pod(cx, cy, pod_w, pod_h, pod, idx))

    svg.append('</svg>\n')
    return ''.join(svg)


def main():
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    svg_content = build_tech_bento_svg()
    OUT_SVG.write_text(svg_content, encoding="utf-8")
    size_kb = OUT_SVG.stat().st_size / 1024
    print(f"Generated {OUT_SVG} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
