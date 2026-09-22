"""Validate the expected folder layout before model training."""

from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def inspect_dataset(data_dir: Path) -> dict[str, int]:
    """Return image counts per class or raise a clear validation error."""
    if not data_dir.is_dir():
        raise ValueError(f"Dataset directory does not exist: {data_dir}")
    class_dirs = [folder for folder in data_dir.iterdir() if folder.is_dir()]
    if len(class_dirs) < 2:
        raise ValueError("Add at least two disease-class folders before training.")
    counts = {}
    for folder in sorted(class_dirs):
        label = folder.name
        count = sum(1 for path in folder.rglob("*") if path.suffix.lower() in IMAGE_SUFFIXES)
        if count == 0:
            raise ValueError(f"No JPG or PNG images found for class: {label}")
        counts[label] = count
    return counts
