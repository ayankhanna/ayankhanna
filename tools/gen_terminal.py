#!/usr/bin/env python3
"""Generate assets/buzzed-terminal.svg — an animated terminal for the GitHub profile README.

GitHub serves README images through a proxy that strips scripts, so everything here is
pure CSS animation inside the SVG. Edit SCRIPT below and re-run:

    python3 tools/gen_terminal.py
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "buzzed-terminal.svg"

# ---- look ----------------------------------------------------------------
W = 860
FONT = 14
CW = 8.45          # approx monospace char width at 14px (Menlo / SF Mono)
LH = 22            # line height
PAD_X = 24
TOP = 44           # below the title bar
C = {
    "bg": "#0b0e14", "bar": "#161b22", "border": "#30363d",
    "fg": "#c9d1d9", "dim": "#6e7681", "amber": "#fbbf24", "green": "#3fb950",
    "blue": "#58a6ff", "purple": "#b392f0", "red": "#ff7b72", "track": "#21262d",
}

# ---- timing (seconds) ----------------------------------------------------
START = 0.6
TYPE = 0.045       # per character
AFTER_CMD = 0.25   # pause between typing and output
OUT_GAP = 0.09     # between output lines
AFTER_BLOCK = 0.55 # pause before next prompt

PROMPT = [("ayan", "amber"), ("@", "dim"), ("buzzed", "amber"), (" ~ ", "blue"), ("% ", "dim")]
PROMPT_LEN = sum(len(t) for t, _ in PROMPT)

# ---- what the terminal says ----------------------------------------------
# ("cmd", text) | ("out", [(text, color), ...]) | ("bar", label, pct, value) | ("blank",)
SCRIPT = [
    ("cmd", "whoami"),
    ("out", [("Ayan Khanna", "fg"), (" — co-founder @ ", "dim"), ("Buzzed", "amber"), ("  (NYC)", "dim")]),
    ("blank",),
    ("cmd", "cat ~/buzzed/thesis.md"),
    ("out", [("  Agencies sell hours. SaaS sells seats.", "dim")]),
    ("out", [("  We ship AI systems you own.", "green")]),
    ("blank",),
    ("cmd", "buzzed --help"),
    ("out", [("  what   ", "dim"), ("forward-deployed AI engineers for the real economy", "fg")]),
    ("out", [("  how    ", "dim"), ("embed with your team, find the work done by hand,", "fg")]),
    ("out", [("         ", "dim"), ("replace it with software that runs in production", "fg")]),
    ("out", [("  you    ", "dim"), ("own the code. no seats. no lock-in. no retainer.", "fg")]),
    ("blank",),
    ("cmd", "buzzed status --prod"),
    ("bar", "systems in prod", 1.00, "80+"),
    ("bar", "idea → production", 0.18, "3 wks"),
    ("bar", "customer rev / yr", 0.92, "$50B+"),
    ("bar", "people it touches", 0.78, "5M+"),
    ("blank",),
    ("cmd", "ls ~/past-lives"),
    ("out", [("northwestern/", "purple"), ("    ", "fg"), ("saturn/", "blue"), ("    ", "fg"), ("4am-deploys/", "red")]),
    ("blank",),
    ("cmd", "buzzed deploy --company yours"),
    ("out", [("  ✓ ", "green"), ("shadowing your ops team ...... ", "dim"), ("done", "green")]),
    ("out", [("  ✓ ", "green"), ("agents in production ......... ", "dim"), ("live", "green")]),
    ("out", [("  ✓ ", "green"), ("handing over the keys ........ ", "dim"), ("yours", "green")]),
    ("out", [("  ➜ ", "amber"), ("next up: your company  ", "fg"), ("buzzedtech.com", "amber")]),
    ("blank",),
    ("final",),
]


def tspans(spans):
    return "".join(f'<tspan fill="{C[c]}">{escape(t)}</tspan>' for t, c in spans)


def build():
    rows, css = [], []
    t = START
    y = TOP + LH
    n = 0

    def fade(cls, at):
        css.append(f".{cls}{{animation:show .01s linear {at:.2f}s both}}")

    for item in SCRIPT:
        kind = item[0]
        if kind == "blank":
            y += LH * 0.55
            continue

        n += 1
        cls = f"l{n}"

        if kind in ("cmd", "final"):
            cmd = item[1] if kind == "cmd" else ""
            fade(cls, t)
            x_cmd = PAD_X + PROMPT_LEN * CW
            rows.append(f'<g class="{cls}"><text x="{PAD_X}" y="{y:.1f}">{tspans(PROMPT)}'
                        f'<tspan fill="{C["fg"]}">{escape(cmd)}</tspan></text>')
            if kind == "final":
                rows.append(f'<rect class="blink" x="{x_cmd:.1f}" y="{y - FONT + 1:.1f}" width="{CW:.1f}" height="{FONT + 3}" fill="{C["amber"]}"/></g>')
                css.append(f".blink{{animation:show .01s linear {t:.2f}s both, blink 1s step-end {t:.2f}s infinite}}")
                break
            # a cover that slides right one character at a time, dragging the cursor with it
            dur = max(len(cmd), 1) * TYPE
            rows.append(f'<g class="{cls}t"><rect x="{x_cmd:.1f}" y="{y - FONT - 2:.1f}" width="{W:.0f}" height="{LH}" fill="{C["bg"]}"/>'
                        f'<rect class="{cls}c" x="{x_cmd:.1f}" y="{y - FONT + 1:.1f}" width="{CW:.1f}" height="{FONT + 3}" fill="{C["amber"]}"/></g></g>')
            css.append(f".{cls}t{{animation:type{n} {dur:.2f}s steps({len(cmd)}) {t + 0.15:.2f}s both}}"
                       f"@keyframes type{n}{{from{{transform:translateX(0)}}to{{transform:translateX({len(cmd) * CW:.1f}px)}}}}")
            css.append(f".{cls}c{{animation:hide .01s linear {t + 0.15 + dur + AFTER_CMD:.2f}s both}}")
            t += 0.15 + dur + AFTER_CMD

        elif kind == "out":
            fade(cls, t)
            rows.append(f'<text class="{cls}" x="{PAD_X}" y="{y:.1f}">{tspans(item[1])}</text>')
            t += OUT_GAP

        elif kind == "bar":
            _, label, pct, value = item
            fade(cls, t)
            bx, bw = PAD_X + 22 * CW, 300
            rows.append(
                f'<g class="{cls}"><text x="{PAD_X}" y="{y:.1f}"><tspan fill="{C["amber"]}">  ▸ </tspan>'
                f'<tspan fill="{C["dim"]}">{escape(label)}</tspan></text>'
                f'<rect x="{bx:.1f}" y="{y - 11:.1f}" width="{bw}" height="10" rx="2" fill="{C["track"]}"/>'
                f'<rect class="{cls}b" x="{bx:.1f}" y="{y - 11:.1f}" width="{bw * pct:.1f}" height="10" rx="2" fill="{C["amber"]}"/>'
                f'<text x="{bx + bw + 14:.1f}" y="{y:.1f}" fill="{C["fg"]}" font-weight="700">{escape(value)}</text></g>')
            css.append(f".{cls}b{{transform-box:fill-box;transform-origin:left center;"
                       f"animation:grow .9s cubic-bezier(.2,.8,.2,1) {t:.2f}s both}}")
            t += OUT_GAP * 1.6

        y += LH
        if kind != "cmd":
            nxt = SCRIPT[SCRIPT.index(item) + 1]
            if nxt[0] == "blank":
                t += AFTER_BLOCK

    H = int(y + LH)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Ayan Khanna, co-founder of Buzzed, forward-deployed AI engineers">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FONT}px;white-space:pre}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes hide{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes glow{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.glow{{animation:glow 2.4s ease-in-out infinite}}
{"".join(css)}
</style>
<defs><clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="{C["bg"]}"/>
<rect width="{W}" height="32" fill="{C["bar"]}"/>
<circle cx="20" cy="16" r="6" fill="#ff5f57"/><circle cx="40" cy="16" r="6" fill="#febc2e"/><circle cx="60" cy="16" r="6" fill="#28c840"/>
<text x="{W / 2}" y="21" text-anchor="middle" fill="{C["dim"]}" style="font-size:12px">ayan@buzzed: ~ — zsh</text>
<circle class="glow" cx="{W - 22}" cy="16" r="4" fill="{C["amber"]}"/>
{chr(10).join(rows)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["border"]}"/>
</svg>
'''


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT}")
