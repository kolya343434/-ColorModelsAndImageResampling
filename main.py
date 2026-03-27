from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from src.color_models import extract_rgb_channels, intensity_image, invert_intensity_in_rgb
from src.resampling import decimate, resample_nearest, resample_two_pass


def load_rgb(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    return np.array(img, dtype=np.uint8)


def save_rgb(path: Path, rgb_u8: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb_u8).save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Color models (RGB/HSI) and image resampling without built-in resize.")
    parser.add_argument("--input", type=Path, default=Path("images/source.png"), help="Path to input PNG/BMP image.")
    parser.add_argument("--out", type=Path, default=Path("results"), help="Output directory.")
    parser.add_argument("--m", type=int, default=3, help="Stretch factor M (integer).")
    parser.add_argument("--n", type=int, default=2, help="Decimation factor N (integer).")
    args = parser.parse_args()

    rgb = load_rgb(args.input)

    save_rgb(args.out / "01_source.png", rgb)

    r_img, g_img, b_img = extract_rgb_channels(rgb)
    save_rgb(args.out / "02_channel_r.png", r_img)
    save_rgb(args.out / "03_channel_g.png", g_img)
    save_rgb(args.out / "04_channel_b.png", b_img)

    save_rgb(args.out / "05_intensity.png", intensity_image(rgb))
    save_rgb(args.out / "06_inverted_intensity.png", invert_intensity_in_rgb(rgb))

    stretched = resample_nearest(rgb, float(args.m))
    save_rgb(args.out / f"07_stretch_M{args.m}.png", stretched)

    dec = decimate(rgb, args.n)
    save_rgb(args.out / f"08_decimate_N{args.n}.png", dec)

    k = args.m / args.n
    two_pass = resample_two_pass(rgb, args.m, args.n)
    save_rgb(args.out / f"09_resample_2pass_K{k:g}_M{args.m}_N{args.n}.png", two_pass)

    one_pass = resample_nearest(rgb, float(k))
    save_rgb(args.out / f"10_resample_1pass_K{k:g}.png", one_pass)

    print("Done. Outputs in:", args.out)


if __name__ == "__main__":
    main()
