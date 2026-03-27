from __future__ import annotations

import numpy as np


def resample_nearest(rgb_u8: np.ndarray, scale: float) -> np.ndarray:
    if scale <= 0:
        raise ValueError("scale must be > 0")
    if rgb_u8.dtype != np.uint8 or rgb_u8.ndim != 3 or rgb_u8.shape[2] != 3:
        raise ValueError("Expected RGB uint8 array with shape (H, W, 3).")

    in_h, in_w, _ = rgb_u8.shape
    out_h = max(1, int(round(in_h * scale)))
    out_w = max(1, int(round(in_w * scale)))

    out = np.empty((out_h, out_w, 3), dtype=np.uint8)

    for y_out in range(out_h):
        y_in = int(y_out / scale)
        if y_in >= in_h:
            y_in = in_h - 1
        row = rgb_u8[y_in]
        for x_out in range(out_w):
            x_in = int(x_out / scale)
            if x_in >= in_w:
                x_in = in_w - 1
            out[y_out, x_out] = row[x_in]

    return out


def decimate(rgb_u8: np.ndarray, n: int) -> np.ndarray:
    if n <= 0:
        raise ValueError("n must be >= 1")
    if rgb_u8.dtype != np.uint8 or rgb_u8.ndim != 3 or rgb_u8.shape[2] != 3:
        raise ValueError("Expected RGB uint8 array with shape (H, W, 3).")
    return rgb_u8[::n, ::n].copy()


def resample_two_pass(rgb_u8: np.ndarray, m: int, n: int) -> np.ndarray:
    if m <= 0 or n <= 0:
        raise ValueError("m and n must be >= 1")
    stretched = resample_nearest(rgb_u8, float(m))
    return decimate(stretched, n)

