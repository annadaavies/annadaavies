"""Render the pixel icon used on the stats screen.

Run:  ./.venv/bin/python make_icon.py   ->  assets/crt.png
"""

from pathlib import Path

from PIL import Image, ImageColor

SCALE = 16          # 16px art * 16 = 256px
OUT = Path(__file__).parent / "assets" / "crt.png"

# "." must match the terminal background: gifos frames are RGB and paste_image
# pastes without a mask, so real transparency would land as a black rectangle.
PALETTE = {
    ".": "#1e1e2e",   # background
    "#": "#cba6f7",   # case
    "g": "#a6e3a1",   # phosphor text
}

# One character per pixel. Edit here, re-run, then run main.py.
ART = """
................
.##############.
.#............#.
.#.gg.gggg....#.
.#............#.
.#.gggggg.gg..#.
.#............#.
.#.ggg.gggggg.#.
.#............#.
.#.gg.gg......#.
.#............#.
.#.g..........#.
.##############.
....########....
...##########...
................
"""


def render():
    rows = [line.strip() for line in ART.strip().splitlines()]
    if len({len(r) for r in rows}) != 1:
        raise ValueError("ragged art: every row must be the same width")
    w, h = len(rows[0]), len(rows)

    img = Image.new("RGB", (w, h))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            img.putpixel((x, y), ImageColor.getrgb(PALETTE[ch]))

    # NEAREST, never the default BICUBIC, or the pixels blur into mush.
    img = img.resize((w * SCALE, h * SCALE), Image.Resampling.NEAREST)
    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT)
    print(f"INFO: wrote {OUT} ({img.width}x{img.height}px)")


if __name__ == "__main__":
    render()
