"""Streamlit interface for paddy leaf prediction and recommendations."""

import json
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf

from src.recommendations import get_recommendation

ROOT = Path(__file__).resolve().parents[1]


@st.cache_resource
def load_model(model_file: str):
    path = Path(model_file)
    return tf.keras.models.load_model(path), json.loads(path.with_suffix(".labels.json").read_text(encoding="utf-8"))


st.set_page_config(page_title="Paddy Leaf Health", page_icon="🌾")
st.title("🌾 Paddy Leaf Disease Prediction")
st.caption("Upload a clear photo of one paddy leaf. Predictions must be verified before treatment.")
models = sorted((ROOT / "models").glob("*.keras"))
if not models:
    st.info("Demo mode: train a model first to enable image classification.")
else:
    chosen = st.sidebar.selectbox("Model", models, format_func=lambda p: p.name)
    upload = st.file_uploader("Leaf image", type=["jpg", "jpeg", "png"])
    if upload:
        image = tf.keras.utils.load_img(upload)
        st.image(image, caption="Uploaded leaf", use_container_width=True)
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
