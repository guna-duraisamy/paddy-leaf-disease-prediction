"""Streamlit interface for paddy leaf prediction and recommendations."""

import json
from pathlib import Path

import numpy as np
import streamlit as st
try:
    import tensorflow as tf
except ModuleNotFoundError:
    tf = None

from src.recommendations import get_recommendation

ROOT = Path(__file__).resolve().parents[1]


@st.cache_resource
def load_model(model_file: str):
    if tf is None:
        raise RuntimeError("TensorFlow is required to load a trained model.")
    path = Path(model_file)
    return tf.keras.models.load_model(path), json.loads(path.with_suffix(".labels.json").read_text(encoding="utf-8"))


st.set_page_config(page_title="Paddy Leaf Health", page_icon="🌾")
st.title("🌾 Paddy Leaf Disease Prediction")
st.caption("Upload a clear photo of one paddy leaf. Predictions must be verified before treatment.")
upload = st.file_uploader("Upload a paddy leaf image", type=["jpg", "jpeg", "png"], help="Use a well-lit, close photograph of one leaf.")
if upload:
    preview = tf.keras.utils.load_img(upload) if tf is not None else upload
    st.image(preview, caption="Uploaded leaf", use_container_width=True)
models = sorted((ROOT / "models").glob("*.keras"))
if not models:
    st.warning("Your image was uploaded, but prediction is unavailable until a trained `.keras` model and its `.labels.json` file are added to `models/`.")
    st.info("Next: put images into `dataset/raw/<disease-name>/`, train with `python -m src.train --data-dir dataset/raw`, then restart or refresh this page.")
    if tf is None:
        st.caption("TensorFlow is not installed in this Python environment. Use a Python version supported by TensorFlow before training or running model inference.")
else:
    if tf is None:
        st.error("TensorFlow is required for model predictions. Install it in a supported Python environment.")
        st.stop()
    chosen = st.sidebar.selectbox("Model", models, format_func=lambda p: p.name)
    if upload:
        model, labels = load_model(str(chosen))
        resized = tf.keras.utils.load_img(upload, target_size=model.input_shape[1:3])
        scores = model.predict(np.expand_dims(tf.keras.utils.img_to_array(resized), axis=0), verbose=0)[0]
        index = int(np.argmax(scores)); label = labels[index]; confidence = float(scores[index])
        rec = get_recommendation(label)
        st.subheader(f"{rec.disease} — {confidence:.1%} confidence")
        st.write(rec.summary)
        if confidence < 0.65:
            st.warning("Low confidence: retake the photo in good daylight and confirm with an agronomist before applying any treatment.")
        left, right = st.columns(2)
        with left:
            st.markdown("#### Pesticide / disease management")
            for item in rec.pesticide: st.write("• " + item)
        with right:
            st.markdown("#### Fertilizer / nutrient guidance")
            for item in rec.fertilizer: st.write("• " + item)
        st.markdown("#### Prevention")
        for item in rec.prevention: st.write("• " + item)

st.divider()
st.caption("Always follow local regulations, product labels, PPE requirements, and pre-harvest intervals.")
