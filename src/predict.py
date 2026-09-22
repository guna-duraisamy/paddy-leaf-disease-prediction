"""Command-line inference for a trained paddy leaf disease model."""

import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf

from src.recommendations import get_recommendation


def predict(model_path: Path, image_path: Path, labels_path: Path | None = None) -> tuple[str, float]:
    labels = json.loads((labels_path or model_path.with_suffix(".labels.json")).read_text(encoding="utf-8"))
    model = tf.keras.models.load_model(model_path)
    image = tf.keras.utils.load_img(image_path, target_size=model.input_shape[1:3])
    probabilities = model.predict(np.expand_dims(tf.keras.utils.img_to_array(image), axis=0), verbose=0)[0]
    index = int(np.argmax(probabilities))
    return labels[index], float(probabilities[index])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--labels", type=Path)
    args = parser.parse_args()
    label, confidence = predict(args.model, args.image, args.labels)
    rec = get_recommendation(label)
    print(f"Prediction: {rec.disease} ({confidence:.1%})")
    print("Pesticide guidance:\n- " + "\n- ".join(rec.pesticide))
    print("Fertilizer guidance:\n- " + "\n- ".join(rec.fertilizer))


if __name__ == "__main__":
    main()
