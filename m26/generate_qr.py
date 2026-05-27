"""
Generate 6 QR codes for Mirror Future cards.

Center label: English slug, ASify purple (#7c5cbf), Didot serif.
Output: ~/asify-gravity-landing/m26/qr/*.png (1200x1200, print-ready, 600 DPI)
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

LABEL_OVERRIDE = {
    "emerge": "RELEASE",  # 「釋放」中央字用 RELEASE，URL slug 仍是 emerge
}
FONT_PATH = "/System/Library/Fonts/Supplemental/Didot.ttc"
FONT_INDEX = 0  # Didot Regular

QR_SIZE = 1200
PURPLE = (124, 92, 191)  # ASify #7c5cbf
MAX_LABEL_W = 460
MAX_LABEL_H = 120
MAX_FONT_SIZE = 110


def fit_font(draw, text: str, max_w: int, max_h: int, max_size: int) -> ImageFont.FreeTypeFont:
    size = max_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w and (bbox[3] - bbox[1]) <= max_h:
            return font
        size -= 2
    return font


def make_qr(url: str, slug_label: str, out_path: str) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=40,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#7c5cbf", back_color="white").convert("RGB")
    img = img.resize((QR_SIZE, QR_SIZE), Image.NEAREST)

    draw = ImageDraw.Draw(img)
    cx, cy = QR_SIZE // 2, QR_SIZE // 2

    font = fit_font(draw, slug_label, MAX_LABEL_W, MAX_LABEL_H, MAX_FONT_SIZE)
    bbox = draw.textbbox((0, 0), slug_label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    pad_x = 32
    pad_y = 18
    bg_w = tw + pad_x * 2
    bg_h = th + pad_y * 2

    draw.rounded_rectangle(
        [cx - bg_w // 2, cy - bg_h // 2, cx + bg_w // 2, cy + bg_h // 2],
        radius=10,
        fill="white",
    )

    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1]
    draw.text((tx, ty), slug_label, fill=PURPLE, font=font)

    img.save(out_path, "PNG", dpi=(600, 600))
    print(f"OK  {os.path.basename(out_path)}  label={slug_label!r}  url={url}")


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, cn in CARDS:
        url = BASE_URL.format(slug=slug)
        out = os.path.join(OUT_DIR, f"{slug}_{cn}.png")
        label = LABEL_OVERRIDE.get(slug, slug.upper())
        make_qr(url, label, out)


if __name__ == "__main__":
    main()
