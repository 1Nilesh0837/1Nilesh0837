#!/usr/bin/env python3
"""Generate the animated GitHub profile banners for Nilesh Sahoo.

Run from the repository root:
    python scripts/banner/generate.py

Requires: numpy, scipy, Pillow  (pip install -r scripts/banner/requirements.txt)

Writes:
    assets/banner-dark.svg
    assets/banner-light.svg
"""

from __future__ import annotations

import html
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source/photo.png"
PATTERN1_SRC = ROOT / "assets/source/pattern1.jpg"
PATTERN2_SRC = ROOT / "assets/source/pattern 2.jpg"
ASSETS = ROOT / "assets"
LOGOS = Path(__file__).resolve().parent / "logos"
DATA = Path(__file__).resolve().parent / "data"

W, H = 1180, 610
LOOP_SECONDS = 14.2
INTRO_SECONDS = 3.2
TRAVELLER_COUNT = 900
SEED = 271828

PORTRAIT_W, PORTRAIT_H = 300, 340
PORTRAIT_X = 61
PORTRAIT_Y = 130

# ── Profile data (YOUR DETAILS) ─────────────────────────────────────────── #
ROWS = [
    ("Subject",        "Nilesh Sahoo"),
    ("Role",           "Full-Stack + ML Developer"),
    ("Origin",         "India"),
    ("Education",      "Self-Taught · Open Source"),
    ("Status",         "Building + Learning + Shipping"),
    ("ToolChain",      "VS Code · Git · Docker"),
    ("Core.Lang",      "Python · JavaScript · Dart"),
    ("Core.Frontend",  "React · React Native · Flutter · Tailwind"),
    ("Core.Backend",   "Node.js · Python"),
    ("Core.ML",        "TensorFlow · PyTorch · Scikit-learn"),
    ("Core.Data",      "Pandas · OpenCV · Seaborn"),
    ("Grid.Mail",      "nileshsahoo837@gmail.com"),
    ("Grid.LinkedIn",  "/in/nilesh-sahoo-b032ab289"),
    ("Grid.GitHub",    "1Nilesh0837"),
    ("Grid.LeetCode",  "1nilesh0837"),
]

# ── Themes (cyan/futuristic) ─────────────────────────────────────────────── #
THEMES = {
    "dark": {
        "bg":       "#0A101F",
        "panel":    "#0D1628",
        "panel2":   "#101B30",
        "line":     "#1E3A5F",
        "muted":    "#7A9EC5",
        "text":     "#E0F0FF",
        "portrait": "#22D3EE",
        "chrome":   "#22D3EE",
        "accent":   "#10B981",
        "shadow":   "#020810",
    },
    "light": {
        "bg":       "#F0F7FF",
        "panel":    "#FFFFFF",
        "panel2":   "#E8F4FD",
        "line":     "#B0D4F1",
        "muted":    "#4A7FA5",
        "text":     "#0A1628",
        "portrait": "#0891B2",
        "chrome":   "#0891B2",
        "accent":   "#10B981",
        "shadow":   "#8AADCC",
    },
}


# ── Logo generation ──────────────────────────────────────────────────────── #

def make_logos() -> dict[str, Image.Image]:
    """Create clean 400px black-on-transparent silhouette sources."""
    LOGOS.mkdir(parents=True, exist_ok=True)
    size = 400
    logos: dict[str, Image.Image] = {}

    # Neural network / brain icon
    brain = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(brain)
    # Simplified brain shape with connected nodes
    center = np.array([200.0, 200.0])
    # Draw interconnected nodes (neural-net inspired)
    nodes = [
        (120, 100), (280, 100), (80, 200), (200, 180),
        (320, 200), (120, 300), (280, 300), (200, 350),
    ]
    # Draw edges
    edges = [
        (0, 1), (0, 2), (0, 3), (1, 3), (1, 4),
        (2, 3), (2, 5), (3, 4), (3, 5), (3, 6),
        (4, 6), (5, 7), (6, 7), (3, 7),
    ]
    for i, j in edges:
        d.line([nodes[i], nodes[j]], fill="black", width=10)
    for x, y in nodes:
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill="black")
    logos["brain"] = brain

    # Code brackets </> icon
    code = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(code)
    stroke = 42
    d.line([(154, 95), (66, 200), (154, 305)], fill="black", width=stroke, joint="curve")
    d.line([(246, 95), (334, 200), (246, 305)], fill="black", width=stroke, joint="curve")
    d.line([(225, 72), (174, 328)], fill="black", width=stroke)
    logos["code"] = code

    # Data / chart icon
    chart = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(chart)
    # Bar chart bars
    bars = [(100, 280, 145, 340), (160, 200, 205, 340),
            (220, 240, 265, 340), (280, 140, 325, 340)]
    for x1, y1, x2, y2 in bars:
        d.rounded_rectangle((x1, y1, x2, y2), radius=6, fill="black")
    # Trend line
    d.line([(90, 300), (150, 250), (220, 270), (310, 120)],
           fill="black", width=14, joint="curve")
    # Arrow head at end
    d.polygon([(310, 120), (290, 145), (320, 140)], fill="black")
    logos["chart"] = chart

    for name, image in logos.items():
        image.save(LOGOS / f"{name}.png", optimize=True)
    return logos


# ── Floyd-Steinberg dithering ────────────────────────────────────────────── #

def floyd_steinberg(gray: np.ndarray) -> np.ndarray:
    """Serpentine 1-bit Floyd-Steinberg diffusion; True means a lit pixel."""
    work = gray.astype(np.float32) / 255.0
    out = np.zeros_like(work, dtype=bool)
    height, width = work.shape
    for y in range(height):
        left_to_right = y % 2 == 0
        xs = range(width) if left_to_right else range(width - 1, -1, -1)
        direction = 1 if left_to_right else -1
        for x in xs:
            old = work[y, x]
            new = 1.0 if old >= 0.5 else 0.0
            out[y, x] = bool(new)
            err = old - new
            nx = x + direction
            if 0 <= nx < width:
                work[y, nx] += err * 7 / 16
            if y + 1 < height:
                if 0 <= x - direction < width:
                    work[y + 1, x - direction] += err * 3 / 16
                work[y + 1, x] += err * 5 / 16
                if 0 <= nx < width:
                    work[y + 1, nx] += err * 1 / 16
    return out


# ── Portrait point extraction ────────────────────────────────────────────── #

def portrait_points(theme: str, rng: np.random.Generator) -> np.ndarray:
    """Return sampled x/y banner coordinates from a 300x340 dither grid."""
    if not SOURCE.exists():
        print(f"  [!] Portrait source not found at {SOURCE}")
        print(f"      Place your photo at: assets/source/photo.png")
        # Return random scatter as placeholder
        pts = rng.uniform([74, 154], [374, 494], size=(5000, 2)).astype(np.float32)
        return pts

    source = Image.open(SOURCE).convert("RGBA")
    w, h = source.size

    # Check if image has meaningful alpha (cutout) or is a regular photo
    has_alpha = False
    if source.mode == "RGBA":
        alpha_channel = source.split()[3]
        if alpha_channel.getextrema()[0] < 250:
            has_alpha = True

    # If already 300x340, use directly
    if w == 300 and h == 340:
        crop = source
    else:
        # Intelligent crop to 300:340 aspect ratio
        target_ratio = 300 / 340  # ~0.882
        src_ratio = w / h

        # If it's a very tall portrait (e.g. phone photo), focus on top 65%
        if src_ratio < 0.75:
            crop_w = int(w * 0.75)
            crop_h = int(crop_w / target_ratio)
            left = (w - crop_w) // 2
            top = max(0, int(h * 0.05))
            crop = source.crop((left, top, left + crop_w, min(h, top + crop_h)))
        elif src_ratio > target_ratio:
            # Wider image (or square) - crop sides slightly to fit 300:340
            crop_w = int(h * target_ratio)
            left = (w - crop_w) // 2
            crop = source.crop((left, 0, left + crop_w, h))
        else:
            # Slightly taller - crop top/bottom slightly
            crop_h = int(w / target_ratio)
            top = (h - crop_h) // 2
            crop = source.crop((0, top, w, top + crop_h))

        crop = crop.resize((300, 340), Image.Resampling.LANCZOS)
    rgb = crop.convert("RGB")

    if has_alpha:
        alpha = np.asarray(crop.getchannel("A"), dtype=np.float32) / 255.0
    else:
        alpha = np.ones((340, 300), dtype=np.float32)

    gray = ImageOps.grayscale(rgb)

    if theme == "dark":
        # Dark theme: dots represent lit pixels of subject & background
        if has_alpha:
            lum = np.asarray(gray, dtype=np.float32)
            prep = Image.fromarray(np.uint8(np.clip(lum * alpha, 0, 255)), "L")
        else:
            prep = gray
        prep = ImageOps.autocontrast(prep, cutoff=1)
        prep = ImageEnhance.Contrast(prep).enhance(1.4)
        prep = ImageEnhance.Brightness(prep).enhance(1.05)
        prep = prep.filter(ImageFilter.UnsharpMask(radius=2, percent=220, threshold=1))
        bits = floyd_steinberg(np.asarray(prep))
        active = bits
        if has_alpha:
            active &= (alpha > 0.15)
    else:
        # Light theme: dots represent dark ink pixels (features, arches, shadows)
        if has_alpha:
            white_bg = Image.new("RGBA", crop.size, "white")
            white_bg.alpha_composite(crop)
            prep = ImageOps.grayscale(white_bg.convert("RGB"))
        else:
            prep = gray
        prep = ImageOps.autocontrast(prep, cutoff=1)
        prep = ImageEnhance.Contrast(prep).enhance(1.4)
        prep = ImageEnhance.Brightness(prep).enhance(1.05)
        prep = prep.filter(ImageFilter.UnsharpMask(radius=2, percent=220, threshold=1))
        bits = floyd_steinberg(np.asarray(prep))
        active = ~bits
        if has_alpha:
            active &= (alpha > 0.15)

    ys, xs = np.where(active)
    if len(xs) == 0:
        return np.zeros((0, 2), dtype=np.float32), active
    points = np.column_stack((PORTRAIT_X + xs, PORTRAIT_Y + ys)).astype(np.float32)
    print(f"  portrait-{theme}: {len(points)} points extracted")
    return points, active


def dither_pattern(path: Path, theme: str, invert_dark: bool = False,
                   invert_light: bool = True) -> np.ndarray:
    """Load, center-crop to 300:340, and dither a pattern image."""
    if not path.exists():
        print(f"  [!] Pattern file not found: {path}")
        return np.zeros((PORTRAIT_H, PORTRAIT_W), dtype=bool)

    img = Image.open(path).convert("RGB")
    w, h = img.size
    target_ratio = PORTRAIT_W / PORTRAIT_H
    src_ratio = w / h

    if src_ratio > target_ratio:
        crop_w = int(h * target_ratio)
        left = (w - crop_w) // 2
        crop = img.crop((left, 0, left + crop_w, h))
    else:
        crop_h = int(w / target_ratio)
        top = (h - crop_h) // 2
        crop = img.crop((0, top, w, top + crop_h))

    crop = crop.resize((PORTRAIT_W, PORTRAIT_H), Image.Resampling.LANCZOS)
    gray = ImageOps.grayscale(crop)
    prep = ImageOps.autocontrast(gray, cutoff=1)
    prep = ImageEnhance.Contrast(prep).enhance(1.4)
    prep = prep.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=1))
    bits = floyd_steinberg(np.asarray(prep))

    if theme == "dark":
        return ~bits if invert_dark else bits
    else:
        return ~bits if invert_light else bits


def get_runs_from_active(active: np.ndarray, px: int, py: int) -> str:
    """Encode a 2D boolean array into a compact SVG path d attribute using RLE."""
    h, w = active.shape
    runs = []
    for y in range(h):
        in_run = False
        run_start = 0
        for x in range(w):
            if active[y, x]:
                if not in_run:
                    in_run = True
                    run_start = x
            else:
                if in_run:
                    in_run = False
                    runs.append((run_start, y, x - run_start))
        if in_run:
            runs.append((run_start, y, w - run_start))

    cmds = []
    for rx, ry, rlen in runs:
        if rlen == 1:
            cmds.append(f"M{px+rx},{py+ry}h1v1h-1z")
        else:
            cmds.append(f"M{px+rx},{py+ry}h{rlen}v1h-{rlen}z")
    return "".join(cmds)


# ── Logo point extraction ────────────────────────────────────────────────── #

def logo_points(name: str, theme: str, rng: np.random.Generator,
                target: int = 900) -> np.ndarray:
    """Dither a logo silhouette into banner-space coordinates."""
    path = LOGOS / f"{name}.png"
    if not path.exists():
        return rng.uniform([900, 200], [1100, 400], size=(target, 2)).astype(np.float32)

    img = Image.open(path).convert("L")
    img = img.resize((120, 120), Image.Resampling.LANCZOS)
    arr = np.asarray(img)
    if theme == "dark":
        ys, xs = np.where(arr < 128)
    else:
        ys, xs = np.where(arr < 128)

    if len(xs) == 0:
        return rng.uniform([900, 200], [1100, 400], size=(target, 2)).astype(np.float32)

    # Place logo in the right-side area of the banner
    cx, cy = 1020, 300
    points = np.column_stack((cx - 60 + xs, cy - 60 + ys)).astype(np.float32)

    if len(points) > target:
        points = points[rng.choice(len(points), target, replace=False)]
    elif len(points) < target:
        extra = rng.choice(len(points), target - len(points), replace=True)
        points = np.vstack([points, points[extra]])
    return points


# ── Point matching (Hungarian algorithm) ─────────────────────────────────── #

def match_points(src: np.ndarray, dst: np.ndarray,
                 rng: np.random.Generator) -> np.ndarray:
    """Optimal matching between src and dst point sets using Hungarian algorithm.
    Returns indices into dst that minimize total travel distance from src."""
    n = len(src)
    m = len(dst)

    if n == 0 or m == 0:
        return np.arange(min(n, m))

    # Subsample for tractability if too large
    if n > 800:
        idx = rng.choice(n, 800, replace=False)
        src_sub = src[idx]
    else:
        src_sub = src
        idx = np.arange(n)

    if m > 800:
        dst_idx = rng.choice(m, min(800, m), replace=False)
        dst_sub = dst[dst_idx]
    else:
        dst_sub = dst
        dst_idx = np.arange(m)

    cost = cdist(src_sub[:min(len(src_sub), len(dst_sub))],
                 dst_sub[:min(len(src_sub), len(dst_sub))])
    row_ind, col_ind = linear_sum_assignment(cost)
    return dst_idx[col_ind]


# ── Pre-compute and cache point data ─────────────────────────────────────── #

def precompute_data():
    """Generate and save all point arrays for both themes."""
    DATA.mkdir(parents=True, exist_ok=True)
    logos = make_logos()

    for theme in ("dark", "light"):
        rng = np.random.default_rng(SEED)

        # Portrait points
        pp, active_grid = portrait_points(theme, rng)
        np.save(DATA / f"portrait-{theme}.npy", pp)
        print(f"  portrait-{theme}: {len(pp)} points")

        # Logo points
        for logo_name in logos:
            lp = logo_points(logo_name, theme, rng, target=TRAVELLER_COUNT)
            np.save(DATA / f"{logo_name}-{theme}.npy", lp)
            print(f"  {logo_name}-{theme}: {len(lp)} points")


# ── SVG rendering ────────────────────────────────────────────────────────── #

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def render_banner(theme: str) -> str:
    """Render the full animated SVG banner for a given theme."""
    c = THEMES[theme]
    rng = np.random.default_rng(SEED)

    # Portrait points & active grid
    pp, active_grid = portrait_points(theme, rng)

    # Load or compute logo points
    logo_names = ["brain", "code", "chart"]
    logo_data = {}
    for name in logo_names:
        lf = DATA / f"{name}-{theme}.npy"
        if lf.exists():
            logo_data[name] = np.load(lf)
        else:
            logo_data[name] = logo_points(name, theme, rng)

    # Generate random traveller starting positions
    travellers = rng.uniform([0, 0], [W, H], size=(TRAVELLER_COUNT, 2)).astype(np.float32)

    # ── Build SVG ──
    svg_parts = []

    # Header
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" style="font-family:ui-monospace,\'SF Mono\',\'Cascadia Mono\','
        f'Consolas,monospace; background:{c["bg"]}">\n'
    )

    # Definitions
    svg_parts.append('<defs>\n')
    # Glow filter
    svg_parts.append(
        f'<filter id="glow"><feGaussianBlur stdDeviation="1.5" result="blur"/>'
        f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
    )
    # Portrait boundary clip
    svg_parts.append(
        f'<clipPath id="portrait-clip">'
        f'<rect x="{PORTRAIT_X}" y="{PORTRAIT_Y}" width="{PORTRAIT_W}" height="{PORTRAIT_H}"/>'
        f'</clipPath>\n'
    )
    # Laser trail gradient
    svg_parts.append(
        f'<linearGradient id="laser-glow-{theme}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{c["portrait"]}" stop-opacity="0"/>'
        f'<stop offset="70%" stop-color="{c["portrait"]}" stop-opacity="0.3"/>'
        f'<stop offset="100%" stop-color="{c["accent"]}" stop-opacity="0.95"/>'
        f'</linearGradient>\n'
    )
    # Glitch slice gradient
    svg_parts.append(
        f'<linearGradient id="glitch-slice-{theme}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{c["accent"]}" stop-opacity="0"/>'
        f'<stop offset="30%" stop-color="{c["accent"]}" stop-opacity="0.6"/>'
        f'<stop offset="70%" stop-color="{c["portrait"]}" stop-opacity="0.6"/>'
        f'<stop offset="100%" stop-color="{c["accent"]}" stop-opacity="0"/>'
        f'</linearGradient>\n'
    )
    svg_parts.append('</defs>\n')

    # ── Window chrome (macOS-style dots) ──
    svg_parts.append(f'<rect x="0" y="0" width="{W}" height="36" fill="{c["panel"]}" rx="8" ry="8"/>\n')
    svg_parts.append(f'<rect x="0" y="20" width="{W}" height="16" fill="{c["panel"]}"/>\n')
    svg_parts.append(f'<circle cx="20" cy="18" r="6" fill="#FF5F57"/>\n')
    svg_parts.append(f'<circle cx="40" cy="18" r="6" fill="#FEBC2E"/>\n')
    svg_parts.append(f'<circle cx="60" cy="18" r="6" fill="#28C840"/>\n')
    svg_parts.append(
        f'<text x="{W//2}" y="22" text-anchor="middle" fill="{c["muted"]}" '
        f'font-size="12" font-weight="500">profile.sh --live</text>\n'
    )

    # ── Left panel: VISUAL.MAP ──
    lp_x, lp_y, lp_w, lp_h = 16, 50, 390, 544
    svg_parts.append(
        f'<rect x="{lp_x}" y="{lp_y}" width="{lp_w}" height="{lp_h}" '
        f'rx="6" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>\n'
    )
    # Panel header
    svg_parts.append(
        f'<text x="{lp_x+14}" y="{lp_y+24}" fill="{c["chrome"]}" font-size="11" '
        f'font-weight="700" letter-spacing="0.08em">VISUAL.MAP</text>\n'
    )
    # Dynamic Stream indicator for active frame
    svg_parts.append(
        f'<g font-size="10" font-weight="600" text-anchor="end">\n'
        f'  <text x="{lp_x+lp_w-14}" y="{lp_y+24}" fill="{c["muted"]}">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="1;1;0;0;0;1" keyTimes="0;0.29;0.33;0.96;0.99;1.0"/>\n'
        f'    01/03 · NILESH.RAW\n'
        f'  </text>\n'
        f'  <text x="{lp_x+lp_w-14}" y="{lp_y+24}" fill="{c["muted"]}">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="0;0;1;1;0;0" keyTimes="0;0.29;0.33;0.62;0.66;1.0"/>\n'
        f'    02/03 · SPIDER.PIX\n'
        f'  </text>\n'
        f'  <text x="{lp_x+lp_w-14}" y="{lp_y+24}" fill="{c["muted"]}">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="0;0;1;1;0;0" keyTimes="0;0.62;0.66;0.96;0.99;1.0"/>\n'
        f'    03/03 · BUTTERFLY.XRAY\n'
        f'  </text>\n'
        f'</g>\n'
    )

    # Corner brackets precisely framing the 300x340 image with neon switch pulse
    pad = 10
    bx = PORTRAIT_X - pad
    by = PORTRAIT_Y - pad
    bw = PORTRAIT_W + 2 * pad
    bh = PORTRAIT_H + 2 * pad
    bracket_len = 22
    b_k = "0;0.020;0.025;0.300;0.320;0.353;0.360;0.633;0.655;0.687;0.694;0.967;0.985;1.0"
    b_stroke = (f'{c["accent"]};{c["accent"]};{c["line"]};{c["line"]};'
                f'{c["accent"]};{c["accent"]};{c["line"]};{c["line"]};'
                f'{c["accent"]};{c["accent"]};{c["line"]};{c["line"]};'
                f'{c["accent"]};{c["accent"]}')
    b_sw = "2.2;2.2;1.5;1.5;2.2;2.2;1.5;1.5;2.2;2.2;1.5;1.5;2.2;2.2"
    svg_parts.append(
        f'<g fill="none" stroke="{c["line"]}" stroke-width="1.5">\n'
        f'  <animate attributeName="stroke" dur="6s" repeatCount="indefinite" '
        f'values="{b_stroke}" keyTimes="{b_k}"/>\n'
        f'  <animate attributeName="stroke-width" dur="6s" repeatCount="indefinite" '
        f'values="{b_sw}" keyTimes="{b_k}"/>\n'
        f'  <polyline points="{bx},{by+bracket_len} {bx},{by} {bx+bracket_len},{by}"/>\n'
        f'  <polyline points="{bx+bw-bracket_len},{by} {bx+bw},{by} {bx+bw},{by+bracket_len}"/>\n'
        f'  <polyline points="{bx},{by+bh-bracket_len} {bx},{by+bh} {bx+bracket_len},{by+bh}"/>\n'
        f'  <polyline points="{bx+bw-bracket_len},{by+bh} {bx+bw},{by+bh} {bx+bw},{by+bh-bracket_len}"/>\n'
        f'</g>\n'
    )

    # ── Three Cycling Frames: Photo -> Pattern 1 -> Pattern 2 (every 2.0s, 6s loop) ──
    total_portrait = len(pp)
    d_photo = get_runs_from_active(active_grid, PORTRAIT_X, PORTRAIT_Y) if active_grid is not None else ""

    # Pattern 1 (Spider-Man pixel art)
    active_p1 = dither_pattern(PATTERN1_SRC, theme, invert_dark=True, invert_light=True)
    d_p1 = get_runs_from_active(active_p1, PORTRAIT_X, PORTRAIT_Y)

    # Pattern 2 (Butterflies in lungs)
    active_p2 = dither_pattern(PATTERN2_SRC, theme, invert_dark=False, invert_light=True)
    d_p2 = get_runs_from_active(active_p2, PORTRAIT_X, PORTRAIT_Y)

    # Frame 1: Nilesh Sahoo Portrait (Active 0.0s..2.0s in 6.0s cycle)
    # T1 exit: 0.304..0.353. T3 entrance: 0.970..0.020
    f1_k = "0;0.010;0.020;0.300;0.308;0.317;0.326;0.336;0.345;0.353;0.967;0.975;0.983;0.991;1.0"
    f1_op = "0.9;0.4;1.0;1.0;0.4;0.9;0.2;0.75;0.15;0;0;0.2;0.7;0.35;0.9"
    f1_dx = "-2,0;3,0;0,0;0,0;-7,0;8,0;-5,0;6,0;-3,0;0,0;0,0;5,0;-6,0;4,0;-2,0"
    svg_parts.append(
        f'<g clip-path="url(#portrait-clip)">\n'
        f'  <g opacity="1">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="{f1_op}" keyTimes="{f1_k}"/>\n'
        f'    <animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" '
        f'values="{f1_dx}" keyTimes="{f1_k}"/>\n'
        f'    <path fill="{c["portrait"]}" d="{d_photo}"/>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # Frame 2: Spider-Man Pattern (Active 2.0s..4.0s in 6.0s cycle)
    # T1 entrance: 0.304..0.353. T2 exit: 0.637..0.687
    f2_k = "0;0.300;0.308;0.317;0.326;0.336;0.345;0.353;0.633;0.642;0.651;0.660;0.670;0.679;0.687;1.0"
    f2_op = "0;0;0.2;0.75;0.25;0.85;0.4;1.0;1.0;0.4;0.9;0.2;0.75;0.15;0;0"
    f2_dx = "0,0;0,0;6,0;-7,0;5,0;-4,0;3,0;0,0;0,0;-7,0;8,0;-5,0;6,0;-3,0;0,0;0,0"
    svg_parts.append(
        f'<g clip-path="url(#portrait-clip)">\n'
        f'  <g opacity="0">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="{f2_op}" keyTimes="{f2_k}"/>\n'
        f'    <animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" '
        f'values="{f2_dx}" keyTimes="{f2_k}"/>\n'
        f'    <path fill="{c["portrait"]}" d="{d_p1}"/>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # Frame 3: Butterflies in Lungs Pattern (Active 4.0s..6.0s in 6.0s cycle)
    # T2 entrance: 0.637..0.687. T3 exit: 0.970..0.020
    f3_k = "0;0.010;0.020;0.633;0.642;0.651;0.660;0.670;0.679;0.687;0.967;0.975;0.983;0.991;1.0"
    f3_op = "0.2;0.05;0;0;0.2;0.75;0.25;0.85;0.4;1.0;1.0;0.4;0.9;0.2;0.75"
    f3_dx = "4,0;-2,0;0,0;0,0;6,0;-7,0;5,0;-4,0;3,0;0,0;0,0;-7,0;8,0;-5,0;6,0"
    svg_parts.append(
        f'<g clip-path="url(#portrait-clip)">\n'
        f'  <g opacity="0">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="{f3_op}" keyTimes="{f3_k}"/>\n'
        f'    <animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" '
        f'values="{f3_dx}" keyTimes="{f3_k}"/>\n'
        f'    <path fill="{c["portrait"]}" d="{d_p2}"/>\n'
        f'  </g>\n'
        f'</g>\n'
    )

    # ── Cyber Laser Scanline Beam & Glitch Slices Overlay ──
    beam_k = "0;0.020;0.024;0.300;0.304;0.353;0.357;0.633;0.637;0.687;0.691;0.967;0.970;1.0"
    beam_op = "1;1;0;0;1;1;0;0;1;1;0;0;1;1"
    beam_tr = "0,336;0,480;0,120;0,120;0,120;0,480;0,120;0,120;0,120;0,480;0,120;0,120;0,120;0,336"
    svg_parts.append(
        f'<g clip-path="url(#portrait-clip)">\n'
        # Cyber laser sweep beam
        f'  <g opacity="1">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="{beam_op}" keyTimes="{beam_k}"/>\n'
        f'    <animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" '
        f'values="{beam_tr}" keyTimes="{beam_k}"/>\n'
        f'    <rect x="{PORTRAIT_X}" y="-36" width="{PORTRAIT_W}" height="36" fill="url(#laser-glow-{theme})"/>\n'
        f'    <line x1="{PORTRAIT_X}" y1="0" x2="{PORTRAIT_X+PORTRAIT_W}" y2="0" '
        f'stroke="{c["accent"]}" stroke-width="2.5" filter="url(#glow)"/>\n'
        f'    <line x1="{PORTRAIT_X}" y1="0" x2="{PORTRAIT_X+PORTRAIT_W}" y2="0" '
        f'stroke="#FFFFFF" stroke-width="1.2" opacity="0.9"/>\n'
        f'  </g>\n'
        # Glitch distortion scan band 1
        f'  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y+65}" width="{PORTRAIT_W}" height="8" '
        f'fill="url(#glitch-slice-{theme})" opacity="0">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="0;0;0.7;0;0;0.7;0;0;0.7;0;0" '
        f'keyTimes="0;0.31;0.32;0.34;0.64;0.65;0.67;0.975;0.985;0.995;1.0"/>\n'
        f'  </rect>\n'
        # Glitch distortion scan band 2
        f'  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y+175}" width="{PORTRAIT_W}" height="14" '
        f'fill="{c["portrait"]}" opacity="0">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="0;0;0.4;0;0;0.4;0;0;0.4;0;0" '
        f'keyTimes="0;0.32;0.33;0.35;0.65;0.66;0.68;0.98;0.99;0.998;1.0"/>\n'
        f'  </rect>\n'
        # Glitch distortion scan band 3
        f'  <rect x="{PORTRAIT_X}" y="{PORTRAIT_Y+265}" width="{PORTRAIT_W}" height="6" '
        f'fill="{c["accent"]}" opacity="0">\n'
        f'    <animate attributeName="opacity" dur="6s" repeatCount="indefinite" '
        f'values="0;0;0.6;0;0;0.6;0;0;0.6;0;0" '
        f'keyTimes="0;0.33;0.34;0.36;0.66;0.67;0.69;0.985;0.995;0.999;1.0"/>\n'
        f'  </rect>\n'
        f'</g>\n'
    )

    # Footer of portrait panel
    svg_parts.append(
        f'<text x="{lp_x+14}" y="{lp_y+lp_h-14}" fill="{c["muted"]}" '
        f'font-size="9" letter-spacing="0.05em">PTS {total_portrait} · FS/SERPENTINE · 3 CYCLES @ 2.0S</text>\n'
    )

    # ── Right panel: SYSTEM.INFO ──
    rp_x, rp_y, rp_w, rp_h = 420, 50, W - 420 - 16, 544
    svg_parts.append(
        f'<rect x="{rp_x}" y="{rp_y}" width="{rp_w}" height="{rp_h}" '
        f'rx="6" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>\n'
    )
    # Panel header with badges
    svg_parts.append(
        f'<text x="{rp_x+14}" y="{rp_y+24}" fill="{c["chrome"]}" font-size="11" '
        f'font-weight="700" letter-spacing="0.08em">SYSTEM.INFO</text>\n'
    )
    # LIVE badge
    badge_x = rp_x + rp_w - 200
    svg_parts.append(
        f'<circle cx="{badge_x}" cy="{rp_y+20}" r="4" fill="#EF4444">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>'
        f'</circle>\n'
    )
    svg_parts.append(
        f'<text x="{badge_x+10}" y="{rp_y+24}" fill="#EF4444" font-size="10" '
        f'font-weight="700">LIVE</text>\n'
    )
    # Username badge
    ubx = rp_x + rp_w - 130
    svg_parts.append(
        f'<rect x="{ubx}" y="{rp_y+8}" width="120" height="24" rx="12" '
        f'fill="{c["chrome"]}" opacity="0.15"/>\n'
    )
    svg_parts.append(
        f'<text x="{ubx+60}" y="{rp_y+24}" text-anchor="middle" '
        f'fill="{c["chrome"]}" font-size="10" font-weight="700">@1Nilesh0837</text>\n'
    )

    # ── System info rows ──
    row_y_start = rp_y + 60
    row_spacing = 30
    for i, (key, value) in enumerate(ROWS):
        y = row_y_start + i * row_spacing
        # Key
        svg_parts.append(
            f'<text x="{rp_x+20}" y="{y}" fill="{c["muted"]}" font-size="13" '
            f'font-weight="500">{html.escape(key)}</text>\n'
        )
        # Value (right-aligned)
        svg_parts.append(
            f'<text x="{rp_x+rp_w-20}" y="{y}" text-anchor="end" fill="{c["text"]}" '
            f'font-size="13" font-weight="600">{html.escape(value)}</text>\n'
        )
        # Separator line
        if i < len(ROWS) - 1:
            svg_parts.append(
                f'<line x1="{rp_x+20}" y1="{y+10}" x2="{rp_x+rp_w-20}" y2="{y+10}" '
                f'stroke="{c["line"]}" stroke-width="0.5" opacity="0.4"/>\n'
            )

    # ── Status bar at bottom of right panel ──
    status_y = rp_y + rp_h - 24
    svg_parts.append(
        f'<circle cx="{rp_x+24}" cy="{status_y}" r="4" fill="{c["accent"]}"/>\n'
    )
    svg_parts.append(
        f'<text x="{rp_x+34}" y="{status_y+4}" fill="{c["accent"]}" '
        f'font-size="10" font-weight="700" letter-spacing="0.05em">ALL SYSTEMS NOMINAL</text>\n'
    )
    svg_parts.append(
        f'<text x="{rp_x+rp_w-20}" y="{status_y+4}" text-anchor="end" '
        f'fill="{c["muted"]}" font-size="10">UTC+5:30 · INDIA NODE</text>\n'
    )

    # ── Floating particles (animated travellers) ──
    for i in range(min(TRAVELLER_COUNT, 60)):  # Limit for SVG size
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        dur = rng.uniform(8, 20)
        dx = rng.uniform(-100, 100)
        dy = rng.uniform(-60, 60)
        opacity = rng.uniform(0.05, 0.2)
        r = rng.uniform(0.5, 1.5)
        svg_parts.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c["chrome"]}" opacity="{opacity:.2f}">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0,0;{dx:.0f},{dy:.0f};0,0" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'</circle>\n'
        )

    # Close SVG
    svg_parts.append('</svg>\n')

    return ''.join(svg_parts)


# ── Main ─────────────────────────────────────────────────────────────────── #

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate profile banners")
    parser.add_argument("--precompute", action="store_true",
                        help="Pre-compute point data and save to .npy files")
    parser.add_argument("--out", type=Path, default=ASSETS,
                        help="Output directory (default: assets/)")
    args = parser.parse_args()

    ASSETS.mkdir(parents=True, exist_ok=True)

    if args.precompute:
        print("Pre-computing point data...")
        precompute_data()
        print("Done! Point data saved to scripts/banner/data/")
        return

    for theme in ("dark", "light"):
        print(f"Rendering {theme} banner...")
        svg = render_banner(theme)
        out_path = args.out / f"banner-{theme}.svg"
        out_path.write_text(svg, encoding="utf-8")
        size_kb = out_path.stat().st_size / 1024
        print(f"  -> {out_path} ({size_kb:.0f} KB)")

    print("[OK] All banners generated!")


if __name__ == "__main__":
    main()
