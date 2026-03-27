from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class HSI:
    h: np.ndarray  # [0, 1)
    s: np.ndarray  # [0, 1]
    i: np.ndarray  # [0, 1]


def rgb_to_hsi(rgb_u8: np.ndarray) -> HSI:
    if rgb_u8.dtype != np.uint8 or rgb_u8.ndim != 3 or rgb_u8.shape[2] != 3:
        raise ValueError("Expected RGB uint8 array with shape (H, W, 3).")

    rgb = rgb_u8.astype(np.float32) / 255.0
    r = rgb[..., 0]
    g = rgb[..., 1]
    b = rgb[..., 2]

    intensity = (r + g + b) / 3.0
    min_rgb = np.minimum(np.minimum(r, g), b)

    eps = 1e-8
    saturation = np.where(intensity > eps, 1.0 - (min_rgb / (intensity + eps)), 0.0)

    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
    den = np.maximum(den, eps)
    cos_theta = np.clip(num / den, -1.0, 1.0)
    theta = np.arccos(cos_theta)  # [0, pi]

    hue = np.where(b <= g, theta, (2.0 * math.pi - theta))
    hue01 = (hue / (2.0 * math.pi)) % 1.0

    return HSI(h=hue01.astype(np.float32), s=saturation.astype(np.float32), i=intensity.astype(np.float32))


def hsi_to_rgb(hsi: HSI) -> np.ndarray:
    h = (hsi.h.astype(np.float32) % 1.0) * (2.0 * math.pi)
    s = np.clip(hsi.s.astype(np.float32), 0.0, 1.0)
    i = np.clip(hsi.i.astype(np.float32), 0.0, 1.0)

    r = np.zeros_like(i, dtype=np.float32)
    g = np.zeros_like(i, dtype=np.float32)
    b = np.zeros_like(i, dtype=np.float32)

    two_pi_over_3 = 2.0 * math.pi / 3.0
    four_pi_over_3 = 4.0 * math.pi / 3.0

    eps = 1e-8

    mask0 = (h >= 0.0) & (h < two_pi_over_3)
    h0 = h[mask0]
    s0 = s[mask0]
    i0 = i[mask0]
    b0 = i0 * (1.0 - s0)
    r0 = i0 * (1.0 + (s0 * np.cos(h0)) / (np.cos((math.pi / 3.0) - h0) + eps))
    g0 = 3.0 * i0 - (r0 + b0)
    r[mask0], g[mask0], b[mask0] = r0, g0, b0

    mask1 = (h >= two_pi_over_3) & (h < four_pi_over_3)
    h1 = h[mask1] - two_pi_over_3
    s1 = s[mask1]
    i1 = i[mask1]
    r1 = i1 * (1.0 - s1)
    g1 = i1 * (1.0 + (s1 * np.cos(h1)) / (np.cos((math.pi / 3.0) - h1) + eps))
    b1 = 3.0 * i1 - (r1 + g1)
    r[mask1], g[mask1], b[mask1] = r1, g1, b1

    mask2 = h >= four_pi_over_3
    h2 = h[mask2] - four_pi_over_3
    s2 = s[mask2]
    i2 = i[mask2]
    g2 = i2 * (1.0 - s2)
    b2 = i2 * (1.0 + (s2 * np.cos(h2)) / (np.cos((math.pi / 3.0) - h2) + eps))
    r2 = 3.0 * i2 - (g2 + b2)
    r[mask2], g[mask2], b[mask2] = r2, g2, b2

    rgb = np.stack([r, g, b], axis=-1)
    rgb = np.clip(rgb, 0.0, 1.0)
    return (rgb * 255.0 + 0.5).astype(np.uint8)


def extract_rgb_channels(rgb_u8: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if rgb_u8.dtype != np.uint8 or rgb_u8.ndim != 3 or rgb_u8.shape[2] != 3:
        raise ValueError("Expected RGB uint8 array with shape (H, W, 3).")

    r = np.zeros_like(rgb_u8)
    g = np.zeros_like(rgb_u8)
    b = np.zeros_like(rgb_u8)
    r[..., 0] = rgb_u8[..., 0]
    g[..., 1] = rgb_u8[..., 1]
    b[..., 2] = rgb_u8[..., 2]
    return r, g, b


def intensity_image(rgb_u8: np.ndarray) -> np.ndarray:
    hsi = rgb_to_hsi(rgb_u8)
    i = np.clip(hsi.i, 0.0, 1.0)
    gray = (i * 255.0 + 0.5).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=-1)


def invert_intensity_in_rgb(rgb_u8: np.ndarray) -> np.ndarray:
    hsi = rgb_to_hsi(rgb_u8)
    inv = HSI(h=hsi.h, s=hsi.s, i=(1.0 - hsi.i))
    return hsi_to_rgb(inv)

