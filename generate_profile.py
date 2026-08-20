#!/usr/bin/env python3
"""
Generates the Nothing-style GitHub profile header (dark.svg + light.svg).

Design system: Nothing / Teenage Engineering / Swiss. Monochrome, three-layer
hierarchy (Doto hero / Space Grotesk body / Space Mono labels), one red signal.
Fonts are embedded as base64 woff2 so they render on GitHub. No API calls.
"""

import base64
from pathlib import Path
from html import escape

HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# ---------------------------------------------------------------- CONFIG
NAME     = "MUHAMMAD MUSA"
KICKER   = "AI ENGINEER  ·  MOBILE APP DEVELOPER"
DESC     = "AI agents, RAG systems and custom LLMs. Shipped inside real mobile apps."
STATUS   = "OPEN TO WORK"
COMPANY  = "GLIXEN TECHNOLOGIES"
HANDLE   = "@MUHAMMADMUSADEV"
STATS = [
    ("3",    "YEARS EXP"),
    ("10+",  "APPS SHIPPED"),
    ("10K+", "ACTIVE USERS"),
    ("5",    "CUSTOM LLMS"),
]

W, H = 1000, 330
PAD_L, PAD_R = 56, 56
RIGHT = W - PAD_R

THEMES = {
    "dark": {
        "bg": "#000000", "display": "#FFFFFF", "primary": "#E8E8E8",
        "secondary": "#999999", "disabled": "#666666", "borderv": "#333333",
        "accent": "#D71921", "dot": "#2A2A2A",
    },
    "light": {
        "bg": "#F5F5F5", "display": "#000000", "primary": "#1A1A1A",
        "secondary": "#666666", "disabled": "#999999", "borderv": "#CCCCCC",
        "accent": "#D71921", "dot": "#DADADA",
    },
}

def _b64(fname):
    return base64.b64encode((FONTS / fname).read_bytes()).decode()

def font_faces():
    faces = [
        ("Doto",          "100 900", "Doto-var.woff2"),
        ("Space Grotesk", "400",     "SpaceGrotesk-400.woff2"),
        ("Space Grotesk", "500",     "SpaceGrotesk-500.woff2"),
        ("Space Mono",    "400",     "SpaceMono-400.woff2"),
    ]
    out = []
    for fam, wght, f in faces:
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;"
                   f"font-weight:{wght};src:url(data:font/woff2;base64,{_b64(f)}) format('woff2');}}")
    return "\n".join(out)

def corner(x, y, dx, dy, c):
    return (f'<path d="M{x+dx*16} {y} H{x} V{y+dy*16}" stroke="{c}" '
            f'stroke-width="1.4" fill="none"/>')

def render(c):
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    p.append(f'<defs><style>{font_faces()}</style>'
             f'<pattern id="dg" width="16" height="16" patternUnits="userSpaceOnUse">'
             f'<circle cx="1" cy="1" r="1" fill="{c["dot"]}"/></pattern></defs>')
    # canvas + subtle dot grid
    p.append(f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#dg)" opacity="0.55"/>')
    # corner registration ticks
    p.append(corner(20, 20, 1, 1, c["borderv"]))
    p.append(corner(W-20, 20, -1, 1, c["borderv"]))
    p.append(corner(20, H-20, 1, -1, c["borderv"]))
    p.append(corner(W-20, H-20, -1, -1, c["borderv"]))

    SM = "'Space Mono', monospace"
    SG = "'Space Grotesk', sans-serif"
    DOTO = "'Doto', 'Space Mono', monospace"

    # --- tertiary top labels ---
    p.append(f'<text x="{PAD_L}" y="54" font-family="{SM}" font-size="12" '
             f'letter-spacing="3" fill="{c["secondary"]}">{escape(KICKER)}</text>')
    # status, top-right, with red signal dot
    st_w = len(STATUS) * 7.4 + 16
    sx = RIGHT - st_w
    p.append(f'<circle cx="{sx+4:.0f}" cy="50" r="4" fill="{c["accent"]}">'
             f'<animate attributeName="opacity" values="1;1;0.18;1" '
             f'keyTimes="0;0.55;0.66;1" dur="1.7s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{sx+16:.0f}" y="54" font-family="{SM}" font-size="12" '
             f'letter-spacing="2" fill="{c["secondary"]}">{escape(STATUS)}</text>')

    # --- PRIMARY: Doto dot-matrix hero name ---
    p.append(f'<text x="{PAD_L-2}" y="138" font-family="{DOTO}" font-size="66" '
             f'font-weight="600" letter-spacing="1" fill="{c["display"]}">{escape(NAME)}</text>')

    # --- secondary description ---
    p.append(f'<text x="{PAD_L}" y="176" font-family="{SG}" font-size="16.5" '
             f'font-weight="400" fill="{c["primary"]}">{escape(DESC)}</text>')

    # --- instrument stat row ---
    top, bot = 232, 288
    vy, ly = 268, 285
    cellw = (W - PAD_L - PAD_R) / len(STATS)
    for i, (val, lab) in enumerate(STATS):
        cx = PAD_L + i * cellw
        if i > 0:
            p.append(f'<line x1="{cx:.0f}" y1="{top}" x2="{cx:.0f}" y2="{bot}" '
                     f'stroke="{c["borderv"]}" stroke-width="1"/>')
        px = cx + (18 if i > 0 else 0)
        p.append(f'<text x="{px:.0f}" y="{vy}" font-family="{SM}" font-size="30" '
                 f'fill="{c["display"]}">{escape(val)}</text>')
        p.append(f'<text x="{px:.0f}" y="{ly}" font-family="{SM}" font-size="11" '
                 f'letter-spacing="1.5" fill="{c["secondary"]}">{escape(lab)}</text>')

    # --- bottom meta line ---
    p.append(f'<text x="{PAD_L}" y="{H-22}" font-family="{SM}" font-size="11" '
             f'letter-spacing="1.5" fill="{c["disabled"]}">{escape(COMPANY)}</text>')
    p.append(f'<text x="{RIGHT}" y="{H-22}" font-family="{SM}" font-size="11" '
             f'letter-spacing="1.5" text-anchor="end" fill="{c["disabled"]}">{escape(HANDLE)}</text>')

    p.append("</svg>")
    return "\n".join(p)

def main():
    for name, c in THEMES.items():
        (HERE / f"{name}.svg").write_text(render(c), encoding="utf-8")
        print(f"wrote {name}.svg")

if __name__ == "__main__":
    main()
