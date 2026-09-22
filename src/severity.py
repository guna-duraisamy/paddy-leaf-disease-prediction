"""Lightweight leaf masking and visible-lesion severity estimation.

This is an image-quality aid, not a field severity measurement or a pesticide
rate calculator. A trained agronomist must verify disease severity in the field.
"""

from dataclasses import dataclass

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class SeverityAssessment:
    level: str
    visible_damage_percent: float
    note: str


def assess_severity(image: Image.Image) -> SeverityAssessment:
    """Estimate discolored area after removing bright, low-saturation background."""
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maximum, minimum = rgb.max(axis=-1), rgb.min(axis=-1)
    saturation = np.divide(maximum - minimum, maximum, out=np.zeros_like(maximum), where=maximum > 0)
    leaf = (saturation > 0.12) & (maximum < 0.96)
    leaf_count = int(leaf.sum())
    if leaf_count < 100:
        return SeverityAssessment("unknown", 0.0, "Leaf area could not be isolated. Retake the image against a plain, contrasting background.")
    brown_or_yellow = ((red > green * 1.06) & (red > blue * 1.15)) | ((red > blue * 1.25) & (green > blue * 1.15))
    damaged = brown_or_yellow & leaf
    percentage = round(float(damaged.sum()) / leaf_count * 100, 1)
    level = "low" if percentage < 10 else "moderate" if percentage < 25 else "high"
    return SeverityAssessment(level, percentage, "Visible discoloration estimate only; lighting, shadows, and background can affect it.")
