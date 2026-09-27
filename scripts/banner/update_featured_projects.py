#!/usr/bin/env python3
"""Auto-update Featured Projects in README.md with the latest 2 repositories.

Fetches user's latest pushed non-fork public repositories from GitHub API and
updates the section between `<!-- FEATURED_PROJECTS:START -->` and
`<!-- FEATURED_PROJECTS:END -->` in README.md.
"""

import os
import re
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README_PATH = ROOT / "README.md"
USERNAME = "1Nilesh0837"

LANG_COLORS = {
    "Python": ("3776AB", "white", "python"),
    "HTML": ("E34F26", "white", "html5"),
    "TypeScript": ("3178C6", "white", "typescript"),
    "JavaScript": ("F7DF1E", "black", "javascript"),
    "Jupyter Notebook": ("DA5B0B", "white", "jupyter"),
    "C": ("A8B9CC", "black", "c"),
    "Java": ("ED8B00", "white", "openjdk"),
    "SQL": ("4479A1", "white", "mysql"),
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
        # Exclude forks, profile README repo, and private repos
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


def format_project_card(repo):
    name = repo.get("name", "Project")
    html_url = repo.get("html_url", f"https://github.com/{USERNAME}/{name}")
    raw_desc = (repo.get("description") or "Innovative project built with cutting-edge engineering.").strip()
    
    clean_desc = raw_desc.replace("|", "｜").replace("\n", " ")
    if len(clean_desc) > 130:
        cut = clean_desc[:127]
        # cut at last space
        last_space = cut.rfind(" ")
        clean_desc = (cut[:last_space] if last_space > 80 else cut) + "..."

    lang = repo.get("language") or "Code"
    stars = repo.get("stargazers_count", 0)
    topics = repo.get("topics", [])
    icon = get_repo_icon(name, raw_desc)

    lang_info = LANG_COLORS.get(lang, ("0A101F", "white", "github"))
    lang_badge = f'<img src="https://img.shields.io/badge/{lang}-{lang_info[0]}?style=flat-square&logo={lang_info[2]}&logoColor={lang_info[1]}" alt="{lang}" />'
    
    tags_str = ""
    if topics:
        selected_topics = [t for t in topics if t.lower() != lang.lower()][:3]
        if selected_topics:
            tags_str = " " + " ".join([f"`{t}`" for t in selected_topics])

    card = {
        "title": f"{icon} **[{name}]({html_url})**",
        "desc": clean_desc,
        "badges": f"{lang_badge} &nbsp; ⭐ `{stars}`{tags_str}",
        "action": f"[View Repo →]({html_url})",
    }
    return card


def build_markdown_section(repos):
    if not repos:
        print("No repos found, keeping existing section.")
        return None

    cards = [format_project_card(r) for r in repos]
    
    # If 1 repo
    if len(cards) == 1:
        c1 = cards[0]
        md = [
            f"| {c1['title']} |",
            "|:---:|",
            f"| {c1['desc']} |",
            f"| {c1['badges']} |",
            f"| {c1['action']} |",
        ]
        return "\n".join(md)

    # 2 repos side-by-side
    c1, c2 = cards[0], cards[1]
    md = [
        f"| {c1['title']} | {c2['title']} |",
        "|:---:|:---:|",
        f"| {c1['desc']} | {c2['desc']} |",
        f"| {c1['badges']} | {c2['badges']} |",
        f"| {c1['action']} | {c2['action']} |",
    ]
    return "\n".join(md)


def update_readme():
    if not README_PATH.exists():
        print(f"README file not found at {README_PATH}")
        return

    content = README_PATH.read_text(encoding="utf-8")
    
    start_tag = "<!-- FEATURED_PROJECTS:START -->"
    end_tag = "<!-- FEATURED_PROJECTS:END -->"

    repos = fetch_latest_projects(limit=2)
    if not repos:
        print("Could not retrieve latest projects.")
        return

    print(f"Latest 2 projects: {[r['name'] for r in repos]}")
    new_table = build_markdown_section(repos)
    if not new_table:
        return

    replacement = f"{start_tag}\n<div align=\"center\">\n\n{new_table}\n\n</div>\n{end_tag}"

    if start_tag in content and end_tag in content:
        pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
        updated_content = pattern.sub(replacement, content)
    else:
        # Replace the existing hardcoded Featured Projects section
        target_section_regex = re.compile(
            r"## 🚀 Featured Projects\s*\n\s*<div align=\"center\">.*?</div>",
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
    print(f"Successfully updated {README_PATH} with latest projects!")


if __name__ == "__main__":
    update_readme()
