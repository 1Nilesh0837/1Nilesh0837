#!/usr/bin/env python3
"""Auto-update Featured Projects with Animated Dark Theme SVG Cards.

Fetches user's latest pushed non-fork public repositories from GitHub API,
generates animated Cyberpunk SVG cards (assets/project-card-1.svg, assets/project-card-2.svg),
and updates README.md between `<!-- FEATURED_PROJECTS:START -->` and `<!-- FEATURED_PROJECTS:END -->`.
"""

import os
import re
import json
import textwrap
import urllib.request
from xml.sax.saxutils import escape as xml_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
ASSETS_DIR = ROOT / "assets"
USERNAME = "1Nilesh0837"

LANG_COLORS = {
    "Python": "#38BDF8",
    "HTML": "#F97316",
    "TypeScript": "#60A5FA",
    "JavaScript": "#FACC15",
    "Jupyter Notebook": "#FB923C",
    "C": "#94A3B8",
    "Java": "#F59E0B",
    "SQL": "#38BDF8",
    "PLpgSQL": "#38BDF8",
    "CSS": "#A855F7",
}


def fetch_latest_projects(limit=2):
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&direction=desc&per_page=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/vnd.github.v3+json",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            repos = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching repos from GitHub API: {e}")
        return []

    valid = []
    for r in repos:
        # Exclude forks, profile repo, and private repos
        if r.get("fork") or r.get("name") == USERNAME:
            continue
        valid.append(r)
        if len(valid) == limit:
            break

    return valid


def get_repo_icon(name, desc):
    text = (name + " " + desc).lower()

    def has_any(words):
        return any(re.search(rf"\b{re.escape(w)}", text) for w in words)

    if has_any(["mandate", "pay", "bank", "credit", "finance", "money", "autopay", "upi"]):
        return "💳"
    if has_any(["kisan", "farm", "crop", "agri"]):
        return "🌾"
    if has_any(["eco", "forensic", "waste", "carbon"]):
        return "🌿"
    if has_any(["wav", "audio", "speech", "voice", "sound"]):
        return "🎙️"
    if has_any(["care", "health", "hospital", "doctor", "emergency", "med"]):
        return "🚑"
    if has_any(["dash", "analytic", "report", "metric", "powerbi"]):
        return "📊"
    if has_any(["agent", "intelligence", "engine", "neural", "mcts"]):
        return "🧠"
    if has_any(["ai", "ml", "gpt", "model", "torch"]):
        return "🤖"
    return "⚡"


def build_card_svg(repo, card_index):
    w, h = 400, 195
    name = repo.get("name", "Project")
    raw_desc = (repo.get("description") or "High-impact software engineering project.").strip()
    lang = repo.get("language") or "Code"
    stars = repo.get("stargazers_count", 0)
    icon = get_repo_icon(name, raw_desc)
    
    # Accent color based on card index
    accent = "#00FF9F" if card_index == 1 else "#38BDF8"
    accent_glow = "rgba(0, 255, 159, 0.4)" if card_index == 1 else "rgba(56, 189, 248, 0.4)"
    lang_color = LANG_COLORS.get(lang, "#38BDF8")

    # Clean description and wrap into lines
    clean_desc = raw_desc.replace("\n", " ").strip()
    wrapped_lines = textwrap.wrap(clean_desc, width=46)
    if len(wrapped_lines) > 3:
        wrapped_lines = wrapped_lines[:3]
        wrapped_lines[-1] = wrapped_lines[-1][:43] + "..."

    # Fallback to at least 1 line
    if not wrapped_lines:
        wrapped_lines = ["Innovative engineering project built with precision."]

    # Calculate language badge width
    lang_w = max(55, len(lang) * 8 + 30)

    # Safe XML strings
    safe_name = xml_escape(name)
    safe_lines = [xml_escape(l) for l in wrapped_lines]
    safe_lang = xml_escape(lang)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n')
    svg.append('<defs>\n')
    svg.append(f'  <pattern id="grid-{card_index}" width="18" height="18" patternUnits="userSpaceOnUse">\n')
    svg.append('    <circle cx="2" cy="2" r="0.8" fill="#1E3A5F" opacity="0.45"/>\n')
    svg.append('  </pattern>\n')
    svg.append(f'  <linearGradient id="top-grad-{card_index}" x1="0%" y1="0%" x2="100%" y2="0%">\n')
    svg.append(f'    <stop offset="0%" stop-color="{accent}" stop-opacity="0.95"/>\n')
    svg.append(f'    <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.85"/>\n')
    svg.append(f'    <stop offset="100%" stop-color="#A855F7" stop-opacity="0.6"/>\n')
    svg.append('  </linearGradient>\n')
    svg.append(f'  <linearGradient id="laser-grad-{card_index}" x1="0%" y1="0%" x2="100%" y2="0%">\n')
    svg.append('    <stop offset="0%" stop-color="#00FF9F" stop-opacity="0"/>\n')
    svg.append(f'    <stop offset="50%" stop-color="{accent}" stop-opacity="0.5"/>\n')
    svg.append('    <stop offset="100%" stop-color="#00FF9F" stop-opacity="0"/>\n')
    svg.append('  </linearGradient>\n')
    svg.append('  <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">\n')
    svg.append('    <feGaussianBlur stdDeviation="3" result="blur"/>\n')
    svg.append('    <feComposite in="SourceGraphic" in2="blur" operator="over"/>\n')
    svg.append('  </filter>\n')
    svg.append('  <style>\n')
    svg.append('    @keyframes pulse-dot {\n')
    svg.append('      0%, 100% { opacity: 1; transform: scale(1); }\n')
    svg.append('      50% { opacity: 0.25; transform: scale(0.85); }\n')
    svg.append('    }\n')
    svg.append('    @keyframes scan-beam {\n')
    svg.append('      0% { transform: translateY(0px); opacity: 0; }\n')
    svg.append('      15% { opacity: 0.7; }\n')
    svg.append('      85% { opacity: 0.7; }\n')
    svg.append('      100% { transform: translateY(195px); opacity: 0; }\n')
    svg.append('    }\n')
    svg.append('    .pulse-dot { animation: pulse-dot 1.8s infinite ease-in-out; transform-origin: 26px 24px; }\n')
    svg.append('    .scan-line { animation: scan-beam 4s infinite linear; }\n')
    svg.append('    .txt-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 800; }\n')
    svg.append('    .txt-body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11.5px; font-weight: 450; fill: #94A3B8; }\n')
    svg.append('    .txt-meta { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 9px; font-weight: 800; letter-spacing: 0.8px; }\n')
    svg.append('  </style>\n')
    svg.append('</defs>\n')

    # Card background & borders
    svg.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#0A101F" stroke="#1E3A5F" stroke-width="1.2"/>\n')
    # Background subtle grid pattern
    svg.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#grid-{card_index})" opacity="0.6"/>\n')
    # Glowing top header line
    svg.append(f'<rect x="12" y="1" width="{w-24}" height="2.5" rx="1" fill="url(#top-grad-{card_index})"/>\n')
    
    # Animated subtle radar scanline
    svg.append(f'<line class="scan-line" x1="4" y1="0" x2="{w-4}" y2="0" stroke="url(#laser-grad-{card_index})" stroke-width="2"/>\n')

    # Header Telemetry
    # Pulsing live release pill
    svg.append(f'<rect x="16" y="14" width="134" height="20" rx="10" fill="{accent}1A" stroke="{accent}" stroke-width="0.8"/>\n')
    svg.append(f'<circle class="pulse-dot" cx="26" cy="24" r="3.5" fill="{accent}"/>\n')
    svg.append(f'<text class="txt-meta" x="35" y="27.5" fill="{accent}">LATEST RELEASE</text>\n')

    # Stargazers / Telemetry right badge
    svg.append(f'<text class="txt-meta" x="{w-18}" y="27.5" text-anchor="end" fill="#FFD700">★ {stars} STARS &#160;<tspan fill="#38BDF8">⚡ VERIFIED</tspan></text>\n')

    # Title with Domain Icon
    svg.append(f'<text class="txt-title" x="16" y="56" fill="#FFFFFF">\n')
    svg.append(f'  <tspan fill="{accent}">{icon} </tspan>{safe_name}\n')
    svg.append(f'</text>\n')

    # Body Description lines
    svg.append(f'<text class="txt-body" x="16" y="78">\n')
    for idx, line in enumerate(safe_lines):
        dy = 0 if idx == 0 else 18
        svg.append(f'  <tspan x="16" dy="{dy}">{line}</tspan>\n')
    svg.append(f'</text>\n')

    # Divider before footer
    svg.append(f'<line x1="16" y1="{h-44}" x2="{w-16}" y2="{h-44}" stroke="#1E3A5F" stroke-width="0.8" opacity="0.6"/>\n')

    # Language badge pill (bottom-left)
    svg.append(f'<rect x="16" y="{h-34}" width="{lang_w}" height="22" rx="4" fill="#131D31" stroke="{lang_color}" stroke-width="0.8"/>\n')
    svg.append(f'<circle cx="26" cy="{h-23}" r="3" fill="{lang_color}"/>\n')
    svg.append(f'<text class="txt-meta" x="34" y="{h-20}" fill="{lang_color}">{safe_lang}</text>\n')

    # View Repo Button (bottom-right)
    btn_w = 110
    btn_x = w - 16 - btn_w
    svg.append(f'<rect x="{btn_x}" y="{h-36}" width="{btn_w}" height="25" rx="5" fill="{accent}1A" stroke="{accent}" stroke-width="1"/>\n')
    svg.append(f'<text class="txt-meta" x="{btn_x + (btn_w // 2)}" y="{h-20}" text-anchor="middle" fill="{accent}">VIEW REPO →</text>\n')

    svg.append('</svg>\n')
    return ''.join(svg)


def update_readme_and_assets():
    if not README_PATH.exists():
        print(f"README file not found at {README_PATH}")
        return

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    repos = fetch_latest_projects(limit=2)
    if not repos:
        print("Could not retrieve latest projects.")
        return

    print(f"Latest 2 projects: {[r['name'] for r in repos]}")

    # Generate SVGs for both cards
    repo1 = repos[0]
    repo2 = repos[1] if len(repos) > 1 else repos[0]

    svg1 = build_card_svg(repo1, card_index=1)
    svg2 = build_card_svg(repo2, card_index=2)

    card1_path = ASSETS_DIR / "project-card-1.svg"
    card2_path = ASSETS_DIR / "project-card-2.svg"

    card1_path.write_text(svg1, encoding="utf-8")
    card2_path.write_text(svg2, encoding="utf-8")
    print(f"Saved {card1_path} and {card2_path}")

    # Build README section
    url1 = repo1.get("html_url", f"https://github.com/{USERNAME}/{repo1.get('name')}")
    url2 = repo2.get("html_url", f"https://github.com/{USERNAME}/{repo2.get('name')}")
    name1 = xml_escape(repo1.get("name", "Project 1"))
    name2 = xml_escape(repo2.get("name", "Project 2"))

    start_tag = "<!-- FEATURED_PROJECTS:START -->"
    end_tag = "<!-- FEATURED_PROJECTS:END -->"

    replacement = f"""{start_tag}
<div align="center">

<p>
  <img src="https://img.shields.io/badge/AUTO--SYNCED-ACTIVE-00FF9F?style=for-the-badge&logo=githubactions&logoColor=0A101F" alt="Auto-Synced" />
  &nbsp;
  <em><b>📡 Live Repository Feed · Automatically updates whenever a new project is uploaded</b></em>
</p>

<a href="{url1}">
  <img width="48.5%" src="assets/project-card-1.svg" alt="{name1}" />
</a>
&nbsp;
<a href="{url2}">
  <img width="48.5%" src="assets/project-card-2.svg" alt="{name2}" />
</a>

</div>
{end_tag}"""

    content = README_PATH.read_text(encoding="utf-8")
    if start_tag in content and end_tag in content:
        pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
        updated_content = pattern.sub(replacement, content)
    else:
        target_section_regex = re.compile(
            r"## 🚀 Featured Projects[^\n]*\n\s*<div align=\"center\">.*?</div>",
            re.DOTALL
        )
        if target_section_regex.search(content):
            updated_content = target_section_regex.sub(
                f"## 🚀 Featured Projects · Auto-Synced\n\n{replacement}",
                content
            )
        else:
            print("Could not find Featured Projects section to replace.")
            return

    README_PATH.write_text(updated_content, encoding="utf-8")
    print(f"Successfully updated {README_PATH} with dark-theme animated project cards!")


if __name__ == "__main__":
    update_readme_and_assets()
