"""GitHub README terminal GIF.

Everything worth changing lives in the CONFIG block below.
Run:  ./.venv/bin/python main.py   ->  output.gif + a regenerated README.md
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------- CONFIG ----
# Must be set BEFORE `import gifos` — it reads its config at import time.
# setdefault means CI env vars win over these local defaults.
os.environ.setdefault("GIFOS_GENERAL_USER_NAME", "annadaavies")
os.environ.setdefault("GIFOS_GENERAL_COLOR_SCHEME", "catppuccin-mocha")
os.environ.setdefault("GIFOS_GENERAL_FPS", "15")
os.environ.setdefault("GIFOS_GENERAL_LOOP_COUNT", "0")   # 0 = loop forever
os.environ.setdefault("GIFOS_GENERAL_CURSOR", "_")
os.environ.setdefault("GIFOS_FILES_OUTPUT_GIF_NAME", "output")

GITHUB_USER = "annadaavies"
IGNORE_REPOS = []          # repos to exclude from stats
WRITE_README = True        # regenerate README.md with the gif embedded
END_HOLD = 105             # frames holding the final screen (15fps -> 7s)

# Canvas and font are coupled: rows = (HEIGHT - 2*YPAD) // cell_h, cols =
# (WIDTH - 2*XPAD) // cell_w. gifos' bundled gohufont is a BITMAP face that
# ignores font_size, so scaling the text at all means TrueType. Size 28 is near
# the ceiling — larger pushes WIDTH past GitHub's ~900px column, which scales
# the image back down. BODY_FONT = None returns to gohufont.
WIDTH, HEIGHT, XPAD, YPAD = 900, 850, 15, 15
BODY_FONT = Path(__file__).parent / "fonts" / "VT323-Regular.ttf"
BODY_FONT_SIZE = 28
LINE_SPACING = 1           # VT323 carries its own leading

# Entries with an empty value are skipped; an empty panel disappears entirely.
ABOUT = {
    "OS": "macOS Sonoma 14.3.1",     # hand-maintained: CI runs on Ubuntu
    "Host": "Stanford, CA",
    "Origin": "Shanghai & Hong Kong",
    "Kernel": "Computer Science & Policy",
    "IDE": "VSCode",
}
CONTACT = {
    "Email": "annabaumanndavies@gmail.com",
    "LinkedIn": "linkedin.com/in/annadaavies",   # <-- check this handle
}

# Press Start 2P sits on an 8px grid — keep the size a multiple of 8. Shipped
# in-repo so the splash matches on CI; system paths are a fallback, and if none
# resolve the splash quietly stays small.
LOGO_FONT_SIZE = 72
LOGO_FONT_CANDIDATES = [
    str(Path(__file__).parent / "fonts" / "PressStart2P-Regular.ttf"),
    "/System/Library/Fonts/Menlo.ttc",                        # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",    # CI
]

ICON_PATH = Path(__file__).parent / "assets" / "crt.png"   # see make_icon.py
ICON_ROWS = 10     # 256px / 28px per row — recheck if the body font changes
ICON_COL = 3       # left margin, in columns
ICON_GAP = 5       # blank columns between icon and panels

USE_GITHUB_STATS = bool(os.getenv("GITHUB_TOKEN"))
# -----------------------------------------------------------------------------

import gifos

BODY_FONT_FILE = str(
    BODY_FONT or Path(gifos.__file__).parent / "fonts" / "gohufont-uni-14.pil"
)


def visible(fields):
    """The entries of a panel that will actually render."""
    return [(k, v) for k, v in fields.items() if v != "" and v is not None]


def category(title, fields, pad):
    """One panel: highlighted title, rule, then label/value pairs padded to
    `pad`. Empty if nothing survives, so the caller can drop the separator."""
    rows = visible(fields)
    if not rows:
        return []
    return [f"\x1b[30;101m{title}\x1b[0m", f"\x1b[96m{'-' * len(title)}\x1b[0m"] + [
        f"\x1b[96m{(k + ':').ljust(pad)}\x1b[93m{v}\x1b[0m" for k, v in rows
    ]


def main():
    t = gifos.Terminal(
        WIDTH, HEIGHT, XPAD, YPAD, BODY_FONT_FILE, BODY_FONT_SIZE, LINE_SPACING
    )
    now = datetime.now()

    # ---------------------------------------------------- scene 1: BIOS ----
    t.toggle_show_cursor(False)
    t.gen_text("GIF_OS Modular BIOS v1.0", 1)
    t.gen_text(f"Copyright (C) {now.year}, \x1b[31m{GITHUB_USER}\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to skip Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 7168):
        t.delete_row(7)
        t.gen_text(f"Memory Test: {i}", 7, count=2 if i < 30000 else 1, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: \x1b[92m64KB OK\x1b[0m", 7, count=10, contin=True)

    # -------------------------------------------- scene 2: boot splash ----
    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)

    # set_font recomputes num_rows/num_cols, so centre the logo after switching.
    logo = "GIF OS"
    logo_font = next((f for f in LOGO_FONT_CANDIDATES if os.path.exists(f)), None)
    if logo_font:
        t.set_font(logo_font, LOGO_FONT_SIZE)
    mid_row = (t.num_rows + 1) // 2
    mid_col = max(1, (t.num_cols - len(logo)) // 2 + 1)
    for line in gifos.effects.text_scramble_effect_lines(logo, 3, include_special=False):
        t.delete_row(mid_row)
        t.gen_text(f"\x1b[96m{line}\x1b[0m", mid_row, mid_col)
    t.clone_frame(12)
    if logo_font:
        t.set_font(BODY_FONT_FILE, BODY_FONT_SIZE, LINE_SPACING)

    # --------------------------------------------------- scene 3: stats ----
    t.clear_frame()
    t.gen_prompt(1, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text(f"\x1b[92mfetch.sh -u {GITHUB_USER}\x1b[0m", 1, contin=True)
    t.gen_text("", 1, count=8, contin=True)

    stats = {}
    if USE_GITHUB_STATS:
        s = gifos.utils.fetch_github_stats(GITHUB_USER, IGNORE_REPOS or None)
        stats = {
            "Rank": s.user_rank.level,
            "Stars Earned": s.total_stargazers,
            "Commits": s.total_commits_all_time,
            "Pull Requests": s.total_pull_requests_made,
            "Merged PR %": s.pull_requests_merge_percentage,
            "Contributions": s.total_repo_contributions,
            "Followers": s.total_followers,
            "Top Languages": ", ".join(lang[0] for lang in s.languages_sorted[:5]),
        }

    # One label width shared by all panels, so the values form a single column.
    labels = [k for d in (ABOUT, CONTACT, stats) for k, _ in visible(d)]
    pad = max((len(k) for k in labels), default=0) + 3

    lines = category(f"{GITHUB_USER}@GitHub", ABOUT, pad)
    for title, fields in (("Contact", CONTACT), ("GitHub Stats", stats)):
        panel = category(title, fields, pad)
        if panel:
            lines += [""] + panel
    if not stats:
        lines += ["", "\x1b[90m(set GITHUB_TOKEN to show live stats)\x1b[0m"]

    t.toggle_show_cursor(False)
    text_col = 4
    if ICON_PATH.exists():
        icon_row = 3 + max(0, (len(lines) - ICON_ROWS) // 2)   # centre on the text
        t.paste_image(str(ICON_PATH), icon_row, ICON_COL)
        text_col = t.image_col + ICON_GAP
    # contin=True is load-bearing: paste_image marks the rows behind the icon
    # occupied, and without it gen_text scrolls the buffer up to reach the first
    # blank row, dragging the icon off the top. An explicit col_num still wins.
    t.gen_text("\n".join(lines), 3, text_col, count=5, contin=True)

    t.toggle_show_cursor(True)
    t.gen_prompt(t.curr_row + 1)
    t.gen_typing_text(
        "\x1b[92m# Thanks for stopping by!\x1b[0m", t.curr_row, contin=True
    )
    t.gen_text("", t.curr_row, count=END_HOLD, contin=True)

    t.gen_gif()

    if WRITE_README:
        stamp = now.strftime("%a %b %d %I:%M:%S %p %Y")
        with open("README.md", "w") as f:
            f.write(
                f"""<div align="center">
<img alt="terminal" src="./output.gif">

<sub><i>Generated with <a href="https://github.com/x0rzavi/github-readme-terminal">github-readme-terminal</a> on {stamp}</i></sub>
</div>
"""
            )
        print("INFO: README.md generated")


if __name__ == "__main__":
    main()
