#!/usr/bin/env python3
"""Render the 21 November 2026 front page (1024x1024) over news-bg.png.

Standalone renderer: Python 3 + Pillow, no network. Reads the dotted-map
backdrop next to this script, dims it, then paints the masthead, five
numbered story cards and the footer in plain painted text.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

EDGE = 1024
MARGIN = 44
GOLD = (233, 179, 74)
PAPER = (244, 246, 248)
MIST = (206, 216, 224)
CARD_FILL = (15, 41, 62, 208)
RULE_LIGHT = (150, 168, 186)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD_PATH = FONT_DIR / "DejaVuSans-Bold.ttf"
PLAIN_PATH = FONT_DIR / "DejaVuSans.ttf"

# (number, accent colour, headline, body incl. dateline)
ITEMS = [
    (
        "01",
        (233, 179, 74),
        "MARKETS PLUNGE",
        "Nasdaq falls 5.3%, S&P enters correction; Nvidia drops 14% on SEC "
        "probe report \u2014 NEW YORK",
    ),
    (
        "02",
        (216, 92, 84),
        "MISSILES LAND IN POLAND",
        "Russia fires 400+ drones and 110 missiles at Ukraine; two missiles "
        "and a drone come down in Poland \u2014 WARSAW",
    ),
    (
        "03",
        (112, 192, 172),
        "EL CHAPO ISIDRO CAPTURED",
        "Mexico captures FBI most-wanted cartel boss Fausto Isidro Meza "
        "Flores in Sinaloa \u2014 GUASAVE",
    ),
    (
        "04",
        (234, 132, 62),
        "FBI PROBES DATABASE BREACH",
        "Hackers reported inside the FBI's national crime database; a USDA "
        "payment system also hit \u2014 WASHINGTON",
    ),
    (
        "05",
        (132, 172, 226),
        "CANCER PILL BREAKTHROUGH",
        "Daraxonrasib halts tumour growth in 90% of patients; tumours "
        "vanish in 1 in 12 \u2014 BARCELONA",
    ),
]


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def fit_text(draw: ImageDraw.ImageDraw, text: str, path: Path,
             start: int, limit: int) -> ImageFont.FreeTypeFont:
    """Largest bold size (down to 20) that keeps `text` within `limit` px."""
    size = start
    while size > 20:
        f = font(path, size)
        if draw.textlength(text, font=f) <= limit:
            return f
        size -= 1
    return font(path, 20)


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont,
         limit: int) -> list[str]:
    out: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=f) <= limit:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def backdrop() -> Image.Image:
    """news-bg.png centre-cropped to a square, then darkened for contrast."""
    raw = Image.open(ROOT / "news-bg.png").convert("RGB")
    w, h = raw.size
    side = min(w, h)
    raw = raw.crop(((w - side) // 2, (h - side) // 2,
                    (w + side) // 2, (h + side) // 2))
    raw = raw.resize((EDGE, EDGE), Image.LANCZOS)
    veil = Image.new("RGB", (EDGE, EDGE), (6, 20, 34))
    return Image.blend(raw, veil, 0.42)


def masthead(draw: ImageDraw.ImageDraw) -> None:
    title = font(BOLD_PATH, 98)
    draw.text((EDGE // 2, 24), "WORLD NEWS", font=title, fill=PAPER,
              anchor="ma")
    draw.line([(MARGIN, 148), (EDGE - MARGIN, 148)], fill=GOLD, width=4)
    sub = font(BOLD_PATH, 41)
    draw.text((EDGE // 2, 164), "SATURDAY \u2022 21 NOVEMBER 2026",
              font=sub, fill=GOLD, anchor="ma")
    draw.line([(MARGIN, 224), (EDGE - MARGIN, 224)], fill=RULE_LIGHT,
              width=3)


def story_card(draw: ImageDraw.ImageDraw, top: int, height: int,
               number: str, accent: tuple[int, int, int],
               headline: str, body: str) -> None:
    draw.rounded_rectangle(
        [MARGIN, top, EDGE - MARGIN, top + height], radius=10,
        fill=CARD_FILL)
    draw.rectangle([MARGIN, top + 12, MARGIN + 9, top + height - 12],
                   fill=accent)
    num_font = font(BOLD_PATH, 54)
    draw.text((MARGIN + 34, top + height // 2), number, font=num_font,
              fill=accent, anchor="lm")
    head_font = fit_text(draw, headline, BOLD_PATH, 40, 770)
    text_x = MARGIN + 128
    draw.text((text_x, top + 22), headline, font=head_font, fill=PAPER)
    body_font = font(PLAIN_PATH, 25)
    lines = wrap(draw, body, body_font, EDGE - MARGIN - text_x - 18)
    y = top + 68
    for line in lines[:2]:
        draw.text((text_x, y), line, font=body_font, fill=MIST)
        y += 31


def main() -> None:
    canvas = backdrop()
    draw = ImageDraw.Draw(canvas, "RGBA")

    masthead(draw)

    card_h, gap, first = 126, 14, 244
    for i, (number, accent, headline, body) in enumerate(ITEMS):
        story_card(draw, first + i * (card_h + gap), card_h,
                   number, accent, headline, body)

    foot = font(PLAIN_PATH, 26)
    draw.text((EDGE // 2, 946), "THE DAY IN FIVE STORIES \u2022 21 NOVEMBER 2026",
              font=foot, fill=MIST, anchor="ma")

    out = ROOT / "entry.png"
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
