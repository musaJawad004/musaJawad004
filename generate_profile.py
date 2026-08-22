#!/usr/bin/env python3
"""Generate the NEURO//MUSA V2 GitHub profile artwork.

The profile is intentionally closer to a fictional AI interface than a resume:
neural paths, synthetic signals, playful system language, and a vivid three-color
identity. Fonts are embedded so every panel renders consistently on GitHub.
"""

import base64
from html import escape
from pathlib import Path


HERE = Path(__file__).parent
FONTS = HERE / "fonts"

# --------------------------------------------------------------- BRAND / COPY
NAME = "MUSA.EXE"
EYEBROW = "HUMAN // AI SYSTEMS BUILDER"
TAGLINE = "BUILDING BRAINS FOR APPS"
DESC = "Agents that act. RAG that remembers. Mobile experiences that feel alive."
STATUS = "NEURAL LINK: ACTIVE"
COMPANY = "CURRENT NODE: GLIXEN TECHNOLOGIES"
HANDLE = "@MUHAMMADMUSADEV"

STATS = [
    ("10+", "APPS RELEASED"),
    ("10K+", "HUMANS REACHED"),
    ("5+", "MODELS TRAINED"),
    ("03", "YEARS EXPLORING"),
]

THEMES = {
    "dark": {
        "bg": "#05050A", "surface": "#0B0D14", "display": "#F7FBFF",
        "primary": "#D8E5FF", "secondary": "#8091A7", "border": "#1C2740",
        "grid": "#11182A", "cyan": "#5FFBF1", "violet": "#8B5CF6",
        "pink": "#FF4FD8", "lime": "#B6FF6A",
    },
    "light": {
        "bg": "#F8FAFF", "surface": "#FFFFFF", "display": "#111225",
        "primary": "#27304A", "secondary": "#66708A", "border": "#D8DFF2",
        "grid": "#E9ECF8", "cyan": "#007D91", "violet": "#6D3CE7",
        "pink": "#D31EB7", "lime": "#4C8F00",
    },
}

SM = "'Space Mono', monospace"
SG = "'Space Grotesk', sans-serif"
DOTO = "'Doto', 'Space Mono', monospace"


def _b64(filename):
    return base64.b64encode((FONTS / filename).read_bytes()).decode()


def font_faces():
    faces = [
        ("Doto", "100 900", "Doto-var.woff2"),
        ("Space Grotesk", "400", "SpaceGrotesk-400.woff2"),
        ("Space Grotesk", "500", "SpaceGrotesk-500.woff2"),
        ("Space Mono", "400", "SpaceMono-400.woff2"),
    ]
    return "\n".join(
        f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
        f"src:url(data:font/woff2;base64,{_b64(filename)}) format('woff2');}}"
        for family, weight, filename in faces
    )


def defs(c, prefix="n"):
    return f"""
<defs>
  <style>{font_faces()}</style>
  <linearGradient id="{prefix}-signal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['cyan']}"/>
    <stop offset="0.52" stop-color="{c['violet']}"/>
    <stop offset="1" stop-color="{c['pink']}"/>
  </linearGradient>
  <radialGradient id="{prefix}-aura">
    <stop offset="0" stop-color="{c['violet']}" stop-opacity=".2"/>
    <stop offset="1" stop-color="{c['violet']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="{prefix}-grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{c['grid']}" stroke-width="1"/>
    <circle cx="1" cy="1" r="1" fill="{c['border']}"/>
  </pattern>
  <filter id="{prefix}-glow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>"""


def frame(width, height, c):
    return (
        f'<path d="M18 42V18H42 M{width-42} 18h24v24 M18 {height-42}v24h24 '
        f'M{width-42} {height-18}h24v-24" fill="none" stroke="{c["border"]}" stroke-width="1.3"/>'
    )


def neural_map(c):
    nodes = [
        (742, 86, 6, "cyan"), (843, 68, 4, "pink"),
        (912, 124, 7, "violet"), (792, 158, 10, "violet"),
        (885, 202, 5, "cyan"), (736, 230, 4, "pink"),
        (944, 246, 4, "pink"), (826, 274, 7, "cyan"),
    ]
    edges = [(0, 1), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4),
             (3, 5), (3, 7), (4, 6), (4, 7), (5, 7), (6, 7)]
    out = [
        '<circle cx="835" cy="174" r="170" fill="url(#hero-aura)"/>',
        f'<circle cx="835" cy="174" r="122" fill="none" stroke="{c["border"]}" stroke-dasharray="2 12">'
        '<animateTransform attributeName="transform" type="rotate" from="0 835 174" to="360 835 174" dur="28s" repeatCount="indefinite"/></circle>',
        f'<circle cx="835" cy="174" r="82" fill="none" stroke="{c["border"]}" stroke-dasharray="24 16">'
        '<animateTransform attributeName="transform" type="rotate" from="360 835 174" to="0 835 174" dur="18s" repeatCount="indefinite"/></circle>',
    ]
    for a, b in edges:
        x1, y1, _, _ = nodes[a]
        x2, y2, _, _ = nodes[b]
        out.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c["border"]}" stroke-width="1.3"/>')
    out.append(
        '<path d="M742 86L792 158L885 202L826 274" fill="none" stroke="url(#hero-signal)" '
        'stroke-width="2" stroke-dasharray="8 10" filter="url(#hero-glow)">'
        '<animate attributeName="stroke-dashoffset" values="36;0" dur="1.6s" repeatCount="indefinite"/></path>'
    )
    for index, (x, y, radius, color) in enumerate(nodes):
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{radius + 5}" fill="{c[color]}" opacity=".08">'
            f'<animate attributeName="r" values="{radius+3};{radius+10};{radius+3}" dur="{2.0+index*.18:.2f}s" repeatCount="indefinite"/></circle>'
        )
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{c[color]}" filter="url(#hero-glow)">'
            f'<animate attributeName="opacity" values="1;.35;1" dur="{1.4+index*.16:.2f}s" repeatCount="indefinite"/></circle>'
        )
    out.append(
        f'<text x="835" y="177" text-anchor="middle" font-family="{SM}" font-size="10" '
        f'letter-spacing="2" fill="{c["display"]}">THINK / BUILD / SHIP</text>'
    )
    return "\n".join(out)


def render(c):
    width, height = 1000, 390
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        defs(c, "hero"),
        f'<rect width="{width}" height="{height}" fill="{c["bg"]}"/>',
        '<rect width="1000" height="390" fill="url(#hero-grid)" opacity=".8"/>',
        frame(width, height, c), neural_map(c),
        f'<text x="54" y="49" font-family="{SM}" font-size="11" letter-spacing="2.4" fill="{c["secondary"]}">{escape(EYEBROW)}</text>',
        f'<circle cx="784" cy="44" r="4" fill="{c["lime"]}" filter="url(#hero-glow)"><animate attributeName="opacity" values="1;.25;1" dur="1.3s" repeatCount="indefinite"/></circle>',
        f'<text x="798" y="49" font-family="{SM}" font-size="11" letter-spacing="1.5" fill="{c["secondary"]}">{escape(STATUS)}</text>',
        f'<text x="50" y="135" font-family="{DOTO}" font-size="76" font-weight="700" letter-spacing="1" fill="url(#hero-signal)">{escape(NAME)}</text>',
        f'<text x="54" y="176" font-family="{SM}" font-size="15" letter-spacing="3" fill="{c["display"]}">{escape(TAGLINE)}</text>',
        f'<text x="54" y="207" font-family="{SG}" font-size="16" fill="{c["primary"]}">{escape(DESC)}</text>',
        f'<text x="54" y="238" font-family="{SM}" font-size="10" letter-spacing="1.5" fill="{c["secondary"]}">NOT A BOT. PROBABLY.</text>',
        '<line x1="54" y1="276" x2="946" y2="276" stroke="url(#hero-signal)" stroke-width="1.5"/>',
    ]
    cell_width = 892 / len(STATS)
    for index, (value, label) in enumerate(STATS):
        x = 54 + index * cell_width
        if index:
            parts.append(f'<line x1="{x:.1f}" y1="300" x2="{x:.1f}" y2="352" stroke="{c["border"]}"/>')
        tx = x + (18 if index else 0)
        color = ["cyan", "violet", "pink", "lime"][index]
        parts.extend([
            f'<text x="{tx:.1f}" y="327" font-family="{SM}" font-size="27" fill="{c[color]}">{escape(value)}</text>',
            f'<text x="{tx:.1f}" y="348" font-family="{SM}" font-size="10" letter-spacing="1.5" fill="{c["secondary"]}">{escape(label)}</text>',
        ])
    parts.extend([
        f'<text x="54" y="375" font-family="{SM}" font-size="9" letter-spacing="1.3" fill="{c["secondary"]}">{escape(COMPANY)}</text>',
        f'<text x="946" y="375" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.3" fill="{c["secondary"]}">{escape(HANDLE)}</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def render_status(c):
    bars = []
    for i, bar_height in enumerate([8, 16, 28, 20, 38, 24, 32, 14, 26, 10]):
        bars.append(
            f'<rect x="{795+i*13}" y="{34-bar_height/2:.1f}" width="6" height="{bar_height}" rx="3" fill="url(#status-signal)" opacity="{.35 + i*.055:.2f}">'
            f'<animate attributeName="height" values="{bar_height};{max(6, 44-bar_height)};{bar_height}" dur="{1.1+i*.09:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="68" viewBox="0 0 1000 68">', defs(c, "status"),
        f'<rect x="1" y="1" width="998" height="66" rx="9" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        f'<circle cx="28" cy="34" r="5" fill="{c["lime"]}" filter="url(#status-glow)"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>',
        f'<text x="44" y="39" font-family="{SM}" font-size="12" letter-spacing="1.5" fill="{c["display"]}">SYSTEM ONLINE</text>',
        f'<line x1="188" y1="17" x2="188" y2="51" stroke="{c["border"]}"/>',
        f'<text x="213" y="30" font-family="{SM}" font-size="9" letter-spacing="1.5" fill="{c["secondary"]}">LOADED CHANNELS</text>',
        f'<text x="213" y="47" font-family="{SM}" font-size="11" fill="{c["cyan"]}">AGENTS</text>',
        f'<text x="295" y="47" font-family="{SM}" font-size="11" fill="{c["violet"]}">RAG MEMORY</text>',
        f'<text x="414" y="47" font-family="{SM}" font-size="11" fill="{c["pink"]}">MOBILE AI</text>',
        f'<text x="555" y="39" font-family="{SM}" font-size="10" letter-spacing="1.4" fill="{c["secondary"]}">MODE:</text>',
        f'<text x="604" y="39" font-family="{SM}" font-size="11" letter-spacing="1.4" fill="{c["display"]}">BUILD / BREAK / LEARN</text>',
        *bars,
        f'<text x="948" y="39" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1" fill="{c["secondary"]}">SIGNAL 98%</text>',
        '</svg>',
    ])


def render_divider(c):
    path = "M18 17 H170 L194 7 L218 27 L246 11 L270 22 L292 17 H982"
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="34" viewBox="0 0 1000 34">', defs(c, "divider"),
        f'<path d="{path}" fill="none" stroke="{c["border"]}" stroke-width="1.3"/>',
        f'<path d="{path}" fill="none" stroke="url(#divider-signal)" stroke-width="2" stroke-dasharray="90 900" filter="url(#divider-glow)"><animate attributeName="stroke-dashoffset" values="0;-1000" dur="3.2s" repeatCount="indefinite"/></path>',
        f'<circle cx="18" cy="17" r="3" fill="{c["cyan"]}"/><circle cx="982" cy="17" r="3" fill="{c["pink"]}"/>', '</svg>',
    ])


def render_stack(c):
    modules = [
        ("01", "INTELLIGENCE", "LLMs  ·  AGENTS  ·  RAG  ·  FINE-TUNING", "cyan"),
        ("02", "MODEL LAB", "OLLAMA  ·  RUNPOD  ·  OPENAI  ·  HUGGING FACE", "violet"),
        ("03", "MOBILE SHELL", "FLUTTER  ·  REACT NATIVE  ·  EXPO  ·  DART", "pink"),
        ("04", "BACKBONE", "NODE.JS  ·  EXPRESS  ·  REST  ·  DOCKER", "lime"),
        ("05", "MEMORY", "POSTGRES  ·  PGVECTOR  ·  MONGODB  ·  FIREBASE", "cyan"),
        ("06", "LANGUAGE", "TYPESCRIPT  ·  PYTHON  ·  JAVASCRIPT", "violet"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="322" viewBox="0 0 1000 322">', defs(c, "stack"),
        f'<rect x="1" y="1" width="998" height="320" rx="12" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        '<rect x="1" y="1" width="998" height="320" rx="12" fill="url(#stack-grid)" opacity=".45"/>',
        f'<text x="32" y="38" font-family="{DOTO}" font-size="22" font-weight="650" letter-spacing="2" fill="{c["display"]}">NEURAL TOOLBELT</text>',
        f'<text x="968" y="36" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">06 MODULES LOADED</text>',
        '<line x1="32" y1="55" x2="968" y2="55" stroke="url(#stack-signal)" stroke-width="1"/>',
    ]
    for i, (number, label, tech, color) in enumerate(modules):
        x = 32 + (i % 2) * 476
        y = 76 + (i // 2) * 76
        parts.extend([
            f'<rect x="{x}" y="{y}" width="450" height="58" rx="8" fill="{c["bg"]}" stroke="{c["border"]}"/>',
            f'<circle cx="{x+22}" cy="{y+29}" r="7" fill="{c[color]}" opacity=".18"><animate attributeName="r" values="7;12;7" dur="{1.7+i*.2:.2f}s" repeatCount="indefinite"/></circle>',
            f'<circle cx="{x+22}" cy="{y+29}" r="3" fill="{c[color]}"/>',
            f'<text x="{x+42}" y="{y+22}" font-family="{SM}" font-size="9" letter-spacing="1.5" fill="{c[color]}">{number} / {label}</text>',
            f'<text x="{x+42}" y="{y+42}" font-family="{SM}" font-size="10.5" fill="{c["primary"]}">{escape(tech)}</text>',
        ])
    parts.extend([
        f'<text x="32" y="302" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">STACK CHANGES. CURIOSITY DOESN\'T.</text>',
        f'<text x="968" y="302" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">READY FOR NEXT EXPERIMENT →</text>', '</svg>',
    ])
    return "\n".join(parts)


def render_achievements(c):
    cards = [
        ("10+", "APPS RELEASED", "FROM IDEA → STORE", "cyan"),
        ("10K+", "HUMANS REACHED", "REAL USERS / REAL CHAOS", "violet"),
        ("5+", "MODELS TRAINED", "CUSTOM WEIGHTS / REAL TASKS", "pink"),
        ("03", "YEARS EXPLORING", "STILL ASKING WHY", "lime"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="250" viewBox="0 0 1000 250">', defs(c, "impact"),
        f'<rect x="1" y="1" width="998" height="248" rx="12" fill="{c["surface"]}" stroke="{c["border"]}"/>',
        f'<text x="32" y="38" font-family="{DOTO}" font-size="22" font-weight="650" letter-spacing="2" fill="{c["display"]}">SIGNAL OUTPUT</text>',
        f'<text x="968" y="36" text-anchor="end" font-family="{SM}" font-size="9" letter-spacing="1.4" fill="{c["secondary"]}">REAL PRODUCTS &gt; PRETTY DEMOS</text>',
        '<line x1="32" y1="55" x2="968" y2="55" stroke="url(#impact-signal)"/>',
    ]
    for i, (value, label, sub, color) in enumerate(cards):
        x = 32 + i * 236
        parts.extend([
            f'<rect x="{x}" y="77" width="220" height="120" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>',
            f'<path d="M{x+16} 93h24" stroke="{c[color]}" stroke-width="3"/>',
            f'<text x="{x+16}" y="139" font-family="{DOTO}" font-size="34" font-weight="700" fill="{c[color]}">{value}</text>',
            f'<text x="{x+16}" y="165" font-family="{SM}" font-size="10" letter-spacing="1.2" fill="{c["display"]}">{label}</text>',
            f'<text x="{x+16}" y="184" font-family="{SM}" font-size="8" letter-spacing="1" fill="{c["secondary"]}">{escape(sub)}</text>',
        ])
    parts.extend([
        f'<path d="M32 224H188l16-10 18 18 20-12 18 4h708" fill="none" stroke="{c["border"]}"/>',
        '<path d="M32 224H188l16-10 18 18 20-12 18 4h708" fill="none" stroke="url(#impact-signal)" stroke-width="2" stroke-dasharray="70 900"><animate attributeName="stroke-dashoffset" values="0;-970" dur="3s" repeatCount="indefinite"/></path>',
        '</svg>',
    ])
    return "\n".join(parts)


def main():
    for theme, colors in THEMES.items():
        (HERE / f"{theme}.svg").write_text(render(colors), encoding="utf-8")
        (HERE / f"status-{theme}.svg").write_text(render_status(colors), encoding="utf-8")
        (HERE / f"divider-{theme}.svg").write_text(render_divider(colors), encoding="utf-8")
        (HERE / f"stack-{theme}.svg").write_text(render_stack(colors), encoding="utf-8")
        (HERE / f"achievements-{theme}.svg").write_text(render_achievements(colors), encoding="utf-8")
        print(f"wrote {theme} NEURO//MUSA set")


if __name__ == "__main__":
    main()
