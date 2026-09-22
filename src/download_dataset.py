"""Download the CC BY 4.0 UCI Rice Leaf Diseases dataset into dataset/raw."""

import shutil
import urllib.request
import zipfile
from pathlib import Path

from src.recommendations import normalize_label

UCI_URL = "https://archive.ics.uci.edu/static/public/486/rice%2Bleaf%2Bdiseases.zip"
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    destination = ROOT / "dataset" / "raw"
    archive = ROOT / "dataset" / "rice_leaf_diseases_uci.zip"
    destination.mkdir(parents=True, exist_ok=True)
    if not archive.is_file():
        print("Downloading UCI Rice Leaf Diseases dataset (CC BY 4.0)...")
        urllib.request.urlretrieve(UCI_URL, archive)
    else:
        print("Using existing UCI dataset archive.")
    with zipfile.ZipFile(archive) as zipped:
        images = [item for item in zipped.infolist() if not item.is_dir() and Path(item.filename).suffix.lower() in {".jpg", ".jpeg", ".png"}]
        for item in images:
            parts = Path(item.filename).parts
            if len(parts) < 2:
                continue
            label = normalize_label(parts[-2])
            target = destination / label / Path(item.filename).name
            target.parent.mkdir(parents=True, exist_ok=True)
            with zipped.open(item) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)
    archive.unlink(missing_ok=True)
    print(f"Downloaded {len(images)} images into {destination}")


if __name__ == "__main__":
    main()
