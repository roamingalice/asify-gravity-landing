"""
Generate 6 QR codes for Mirror Future cards.

Each QR has a centered Chinese character (typesetting in Songti).
Output: ~/asify-gravity-landing/m26/qr/*.png (1200x1200, print-ready)
"""

import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

CARDS = [
    ("embrace", "包覆"),
    ("lightness", "輕盈"),
    ("rise", "延展"),
    ("root", "扎根"),
    ("emerge", "釋放"),
    ("still", "沉澱"),
]

BASE_URL = "https://oracle.as-for-me.com/m26/{slug}/"
OUT_DIR = os.path.expanduser("~/asify-gravity-landing/m26/qr")
SONGTI_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"

QR_SIZE = 1200  # final pixel dimension
CENTER_BOX = 280  # white box behind char
CHAR_SIZE = 220  # character font size in pixels


def make_qr(url: str, char: str, out_path: str) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=40,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((QR_SIZE, QR_SIZE), Image.NEAREST)

    # white circular/rounded square in center
    draw = ImageDraw.Draw(img)
    cx, cy = QR_SIZE // 2, QR_SIZE // 2
    box_half = CENTER_BOX // 2
    draw.rounded_rectangle(
        [cx - box_half, cy - box_half, cx + box_half, cy + box_half],
        radius=16,
        fill="white",
    )

    # render character
    font = ImageFont.truetype(SONGTI_PATH, CHAR_SIZE)
    bbox = draw.textbbox((0, 0), char, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1]
    draw.text((tx, ty), char, fill="black", font=font)

    img.save(out_path, "PNG", dpi=(600, 600))
    print(f"OK  {out_path}  ({char}, {url})")


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, char in CARDS:
        url = BASE_URL.format(slug=slug)
        out = os.path.join(OUT_DIR, f"{slug}_{char}.png")
        make_qr(url, char, out)


if __name__ == "__main__":
    main()
