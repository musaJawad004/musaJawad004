#!/usr/bin/env python3
"""
Generates the animated "Neural Net Hero" GitHub profile header (dark.svg + light.svg).

A neural-network graph on the left feeds glowing signal pulses into the name on
the right. Everything you'd normally tweak lives in CONFIG below. No external
calls: live GitHub stats are shown by the stats cards in README.md instead.
"""

from datetime import datetime, timezone, timedelta
from html import escape
from pathlib import Path

# ---------------------------------------------------------------- CONFIG
USERNAME = "musaJawad004"
NAME     = "Muhammad Musa"
ROLE     = "AI Engineer & Mobile App Developer"
TAG      = "AI agents  ·  RAG  ·  custom LLMs  ·  shipped to 10k+ users"
HANDLE   = "@muhammadmusadev"
OPEN_TO  = "open to AI Engineer / Mobile Developer roles"
CHIPS    = ["LLMs", "AI Agents", "RAG", "Fine-Tuning", "Flutter", "React Native"]

W, H = 1000, 340

THEMES = {
    "dark": {
        "bg": "#0d1117", "panel": "#0d1117", "border": "#233043",
        "name": "#e9edf3", "role": "#58a6ff", "muted": "#8b949e",
        "c1": "#58a6ff", "c2": "#bc8cff", "c3": "#3fb950", "c4": "#39c5cf",
        "edge": "#2b3a54", "chipbg": "#161b22", "chiptx": "#c9d1d9", "chipbd": "#30363d",
        "grid": "#161d29",
    },
    "light": {
        "bg": "#ffffff", "panel": "#ffffff", "border": "#d0d7de",
        "name": "#1f2328", "role": "#0969da", "muted": "#59636e",
        "c1": "#0969da", "c2": "#8250df", "c3": "#1a7f37", "c4": "#1b7c83",
        "edge": "#c9d3e0", "chipbg": "#f6f8fa", "chiptx": "#1f2328", "chipbd": "#d0d7de",
        "grid": "#eef1f5",
    },
}

# node layers: (x, [y positions])
LAYERS = [
    (70,  [95, 170, 245]),
    (162, [70, 132, 198, 258]),
    (255, [102, 170, 238]),
    (340, [170]),
]

def _nearest2(y, ys):
    return sorted(range(len(ys)), key=lambda k: abs(ys[k] - y))[:2]

def build_graph():
    nodes = []   # (x, y, colorkey)
    layer_ids = []
    ck = ["c1", "c2", "c3", "c4"]
    idx = 0
    for li, (x, ys) in enumerate(LAYERS):
        ids = []
        for yi, y in enumerate(ys):
            nodes.append((x, y, ck[(li + yi) % 4]))
            ids.append(idx); idx += 1
        layer_ids.append(ids)
    edges = []
    for li in range(len(LAYERS) - 1):
        x0, ys0 = LAYERS[li]
        x1, ys1 = LAYERS[li + 1]
        for a_i, ya in zip(layer_ids[li], ys0):
            for k in _nearest2(ya, ys1):
                edges.append((a_i, layer_ids[li + 1][k]))
    return nodes, edges

def render(colors):
    nodes, edges = build_graph()
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="ui-sans-serif, -apple-system, '
             f"'Segoe UI', Roboto, Helvetica, Arial, sans-serif\">")
    # defs: glow + gradient
    p.append(f'''<defs>
      <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="2.4" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{colors['c1']}"/>
        <stop offset="0.5" stop-color="{colors['c2']}"/>
        <stop offset="1" stop-color="{colors['c3']}"/>
      </linearGradient>
    </defs>''')
    # card
    p.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16" '
             f'fill="{colors["bg"]}" stroke="{colors["border"]}" stroke-width="1.6"/>')
    # faint dotted grid on the left half
    p.append(f'<rect x="2" y="2" width="380" height="{H-4}" rx="16" fill="url(#gridpat)" opacity="0"/>')

    # ---- edges ----
    p.append('<g stroke-linecap="round">')
    for i, (a, b) in enumerate(edges):
        x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]
        dur = 3.2 + (i % 5) * 0.4
        beg = (i % 7) * 0.3
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colors["edge"]}" stroke-width="1.4">'
                 f'<animate attributeName="opacity" values="0.35;0.85;0.35" dur="{dur}s" '
                 f'begin="{beg}s" repeatCount="indefinite"/></line>')
    p.append('</g>')

    # edges converging from last hidden layer to output node -> then to name (accent)
    ox, oy, _ = nodes[-1]
    p.append(f'<line x1="{ox}" y1="{oy}" x2="392" y2="150" stroke="{colors["role"]}" '
             f'stroke-width="1.8" opacity="0.55" stroke-dasharray="4 5">'
             f'<animate attributeName="stroke-dashoffset" values="18;0" dur="1.1s" repeatCount="indefinite"/></line>')

    # ---- travelling signal pulses on a subset of edges ----
    sig = edges[::max(1, len(edges)//7)][:7] + [(len(nodes)-1, None)]
    for i, (a, b) in enumerate(sig):
        if b is None:
            x1, y1, _ = nodes[a]; x2, y2 = 392, 150
            col = colors["role"]
        else:
            x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]
            col = colors["c1"] if i % 2 else colors["c2"]
        dur = 2.1 + (i % 4) * 0.5
        beg = i * 0.42
        p.append(f'<circle r="3.1" fill="{col}" filter="url(#glow)" opacity="0">'
                 f'<animate attributeName="cx" values="{x1};{x2}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{y1};{y2}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.05;0.2;0.85;1" '
                 f'dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></circle>')

    # ---- nodes (halo pulse + core) ----
    for i, (x, y, ckey) in enumerate(nodes):
        col = colors[ckey]
        d = 3 + (i % 6) * 0.5
        p.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{col}" opacity="0.16">'
                 f'<animate attributeName="r" values="8;13;8" dur="{d}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.05;0.22;0.05" dur="{d}s" repeatCount="indefinite"/></circle>')
        p.append(f'<circle cx="{x}" cy="{y}" r="4.4" fill="{col}" filter="url(#glow)"/>')
    # output node bigger
    p.append(f'<circle cx="{ox}" cy="{oy}" r="7" fill="{colors["role"]}" filter="url(#glow)">'
             f'<animate attributeName="r" values="6.5;8.5;6.5" dur="2.2s" repeatCount="indefinite"/></circle>')

    # ---- text block ----
    tx = 396
    p.append(f'<text x="{tx}" y="120" fill="{colors["muted"]}" font-size="14" '
             f'letter-spacing="3" font-weight="600">{escape(HANDLE.upper())}</text>')
    p.append(f'<text x="{tx-2}" y="168" fill="{colors["name"]}" font-size="46" '
             f'font-weight="800" letter-spacing="-0.5">{escape(NAME)}</text>')
    p.append(f'<text x="{tx}" y="200" fill="{colors["role"]}" font-size="20.5" '
             f'font-weight="700">{escape(ROLE)}</text>')
    p.append(f'<text x="{tx}" y="226" fill="{colors["muted"]}" font-size="13.5">{escape(TAG)}</text>')

    # ---- chips ----
    cx = tx; cy = 250
    for i, label in enumerate(CHIPS):
        wch = int(len(label) * 8.0) + 26
        p.append(f'<g>'
                 f'<rect x="{cx}" y="{cy}" width="{wch}" height="27" rx="8" '
                 f'fill="{colors["chipbg"]}" stroke="{colors["chipbd"]}" stroke-width="1.3"/>'
                 f'<circle cx="{cx+13}" cy="{cy+13.5}" r="3" fill="{colors[["c1","c2","c3","c4"][i%4]]}"/>'
                 f'<text x="{cx+23}" y="{cy+18}" fill="{colors["chiptx"]}" font-size="13" '
                 f'font-weight="600">{escape(label)}</text></g>')
        cx += wch + 9
        if cx > W - 130:  # wrap
            cx = tx; cy += 34

    # ---- footer ----
    p.append(f'<line x1="{tx}" y1="303" x2="{W-40}" y2="303" stroke="{colors["border"]}" stroke-width="1"/>')
    p.append(f'<text x="{tx}" y="322" fill="{colors["c3"]}" font-size="13">'
             f'<tspan font-weight="700">●</tspan>'
             f'<tspan dx="7" fill="{colors["muted"]}">{escape(OPEN_TO)}</tspan></text>')
    p.append(f'<text x="{W-40}" y="322" fill="{colors["muted"]}" font-size="12" '
             f'text-anchor="end">{escape(HANDLE)}</text>')

    p.append("</svg>")
    return "\n".join(p)


def main():
    out = Path(__file__).parent
    for name, colors in THEMES.items():
        (out / f"{name}.svg").write_text(render(colors), encoding="utf-8")
        print(f"wrote {name}.svg")


if __name__ == "__main__":
    main()
