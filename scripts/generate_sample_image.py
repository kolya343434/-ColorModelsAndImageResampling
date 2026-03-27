from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def generate(width: int = 900, height: int = 520) -> Image.Image:
    yy, xx = np.mgrid[0:height, 0:width]
    x = xx.astype(np.float32) / max(1, width - 1)
    y = yy.astype(np.float32) / max(1, height - 1)

    sky_r = 30 + 200 * (1 - y) * (0.9 + 0.1 * np.sin(2 * math.pi * x))
    sky_g = 20 + 80 * (1 - y) + 40 * (x * (1 - y))
    sky_b = 60 + 160 * (1 - y) + 20 * np.cos(2 * math.pi * x) * (1 - y)

    mountains = (y > (0.35 + 0.15 * np.sin(3 * math.pi * x + 0.8))) & (y < 0.85)
    mshade = (0.4 + 0.6 * (1 - y)) * (0.7 + 0.3 * np.cos(6 * math.pi * x))

    r = sky_r
    g = sky_g
    b = sky_b

    r = np.where(mountains, 35 + 90 * mshade, r)
    g = np.where(mountains, 30 + 70 * mshade, g)
    b = np.where(mountains, 45 + 110 * mshade, b)

    river = (y > (0.55 + 0.08 * np.sin(2 * math.pi * x + 0.2))) & (y < (0.62 + 0.08 * np.sin(2 * math.pi * x + 0.2)))
    r = np.where(river, 30 + 20 * (1 - y), r)
    g = np.where(river, 70 + 90 * (1 - y), g)
    b = np.where(river, 130 + 110 * (1 - y), b)

    img = np.stack([r, g, b], axis=-1)
    img = np.clip(img, 0, 255).astype(np.uint8)
    pil = Image.fromarray(img)

    draw = ImageDraw.Draw(pil, "RGBA")
    sun_center = (int(width * 0.78), int(height * 0.22))
    for rad, alpha in [(90, 70), (60, 120), (35, 180)]:
        bbox = [sun_center[0] - rad, sun_center[1] - rad, sun_center[0] + rad, sun_center[1] + rad]
        draw.ellipse(bbox, fill=(255, 230, 160, alpha))

    for i in range(9):
        x0 = int(width * (0.05 + 0.1 * i))
        y0 = int(height * (0.1 + 0.02 * (i % 3)))
        x1 = x0 + int(width * 0.18)
        y1 = y0 + int(height * 0.05)
        draw.ellipse([x0, y0, x1, y1], fill=(255, 120, 90, 45))

    return pil


def main() -> None:
    out_path = Path("images/source.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = generate()
    img.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
