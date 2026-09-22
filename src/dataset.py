"""Validate the expected folder layout before model training."""

from pathlib import Path

SUPPORTED_CLASSES = {"bacterial_leaf_blight", "brown_spot", "leaf_smut", "healthy"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def inspect_dataset(data_dir: Path) -> dict[str, int]:
    """Return image counts per class or raise a clear validation error."""
    if not data_dir.is_dir():
        raise ValueError(f"Dataset directory does not exist: {data_dir}")
    found = {folder.name.lower() for folder in data_dir.iterdir() if folder.is_dir()}
    missing = SUPPORTED_CLASSES - found
    if missing:
        raise ValueError("Missing class folders: " + ", ".join(sorted(missing)))
    counts = {}
    for label in sorted(SUPPORTED_CLASSES):
        count = sum(1 for path in (data_dir / label).rglob("*") if path.suffix.lower() in IMAGE_SUFFIXES)
        if count == 0:
            raise ValueError(f"No JPG or PNG images found for class: {label}")
        counts[label] = count
    return counts
