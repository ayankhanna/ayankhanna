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
    "blue": "#58a6ff", "purple": "#b392f0", "red": "#ff7b72", "track": "#21262d", "snap": "#fffc00",
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
    ("out", [("prev: ", "dim"), ("product @ Saturn", "fg"), ("  ➜  ", "dim"), ("acquired by Snap", "snap")]),
    ("blank",),
    ("cmd", "cat ~/buzzed/README"),
    ("out", [("  SaaS, but built for you.", "amber")]),
    ("out", [("  Every company gets its own software, automations baked in. We run it.", "dim")]),
    ("blank",),
    ("cmd", "git diff your-company/before your-company/after"),
    ("out", [("- ", "red"), ("bending your workflow around six SaaS tools", "red")]),
    ("out", [("+ ", "green"), ("one system built around how you actually work", "green")]),
    ("out", [("- ", "red"), ("your team copy-pasting between tabs all day", "red")]),
    ("out", [("+ ", "green"), ("an agent does it. a human signs off on the edge cases.", "green")]),
    ("out", [("- ", "red"), ('"we\'ll get to it next quarter"', "red")]),
    ("out", [("+ ", "green"), ("in production in 3 weeks", "green")]),
    ("blank",),
    ("cmd", "buzzed status --prod"),
    ("bar", "systems in prod", 1.00, "80+"),
    ("bar", "idea → production", 0.18, "3 wks"),
    ("bar", "customer rev / yr", 0.92, "$50B+"),
    ("bar", "people it touches", 0.78, "5M+"),
    ("blank",),
    ("cmd", "buzzed log --wins"),
    ("out", [("  ★ ", "amber"), ("customer-facing agent helped sell a ", "fg"), ("$4M home", "amber")]),
    ("out", [("  ★ ", "amber"), ("boosted the talent acquisition funnel at one of", "fg")]),
    ("out", [("    ", "fg"), ("the largest private companies in America", "amber")]),
    ("blank",),
    ("cmd", "ls ~/past-lives"),
    ("out", [("northwestern/", "purple"), ("    ", "fg"), ("saturn/", "blue"), (" (exit: snap)", "snap"), ("    ", "fg"), ("4am-deploys/", "red")]),
    ("blank",),
    ("cmd", "buzzed deploy --company yours"),
    ("out", [("  ✓ ", "green"), ("built around your workflow ..... ", "dim"), ("done", "green")]),
    ("out", [("  ✓ ", "green"), ("agents in production ........... ", "dim"), ("live", "green")]),
    ("out", [("  ✓ ", "green"), ("we keep it running ............. ", "dim"), ("always", "green")]),
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
            rows.append(f'<g class="{cls}t"><rect class="{cls}k" x="{x_cmd:.1f}" y="{y - FONT - 2:.1f}" width="{W:.0f}" height="{LH}" fill="{C["bg"]}"/>'
                        f'<rect class="{cls}c" x="{x_cmd:.1f}" y="{y - FONT + 1:.1f}" width="{CW:.1f}" height="{FONT + 3}" fill="{C["amber"]}"/></g></g>')
            css.append(f".{cls}t{{animation:type{n} {dur:.2f}s steps({len(cmd)}) {t + 0.15:.2f}s both}}"
                       f"@keyframes type{n}{{from{{transform:translateX(0)}}to{{transform:translateX({len(cmd) * CW:.1f}px)}}}}")
            # drop the cover once typing ends, in case steps() stops a character short
            css.append(f".{cls}k{{animation:hide .01s linear {t + 0.15 + dur + 0.02:.2f}s both}}")
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Ayan Khanna, co-founder of Buzzed. SaaS, but built for you.">
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
