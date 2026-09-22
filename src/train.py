"""Train a paddy leaf classifier from a directory-organized dataset."""

import argparse
import json
from datetime import datetime
from pathlib import Path

import tensorflow as tf

from src.dataset import inspect_dataset


def build_model(class_count: int, image_size: int) -> tf.keras.Model:
    base = tf.keras.applications.MobileNetV2(include_top=False, weights="imagenet", input_shape=(image_size, image_size, 3))
    base.trainable = False
    inputs = tf.keras.Input(shape=(image_size, image_size, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    outputs = tf.keras.layers.Dense(class_count, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the paddy leaf disease classifier.")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=224)
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        raise SystemExit(f"Dataset directory not found: {args.data_dir}")
    try:
        counts = inspect_dataset(args.data_dir)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print("Images per class:", counts)
    kwargs = dict(validation_split=0.2, seed=42, image_size=(args.image_size, args.image_size), batch_size=args.batch_size)
    train_ds = tf.keras.utils.image_dataset_from_directory(args.data_dir, subset="training", **kwargs)
    val_ds = tf.keras.utils.image_dataset_from_directory(args.data_dir, subset="validation", **kwargs)
    labels = train_ds.class_names
    autotune = tf.data.AUTOTUNE
    augmentation = tf.keras.Sequential([tf.keras.layers.RandomFlip("horizontal"), tf.keras.layers.RandomRotation(0.08), tf.keras.layers.RandomZoom(0.1)])
    train_ds = train_ds.map(lambda x, y: (augmentation(x, training=True), y), num_parallel_calls=autotune).prefetch(autotune)
    model = build_model(len(labels), args.image_size)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = args.output_dir / f"paddy_leaf_model_{stamp}.keras"
    model.fit(train_ds, validation_data=val_ds.prefetch(autotune), epochs=args.epochs, callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)])
    model.save(model_path)
    model_path.with_suffix(".labels.json").write_text(json.dumps(labels, indent=2), encoding="utf-8")
    print(f"Saved model: {model_path}")


if __name__ == "__main__":
    main()
