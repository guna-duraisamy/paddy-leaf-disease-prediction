"""Streamlit interface for paddy leaf prediction and recommendations."""

import json
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image, UnidentifiedImageError

try:
    import tensorflow as tf
except ModuleNotFoundError:
    tf = None

from src.history import record_prediction
from src.recommendations import get_recommendation
from src.severity import assess_severity

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data" / "predictions.sqlite3"


@st.cache_resource
def load_model(model_file: str):
    if tf is None:
        raise RuntimeError("TensorFlow is required to load a trained model.")
    path = Path(model_file)
    labels = json.loads(path.with_suffix(".labels.json").read_text(encoding="utf-8"))
    return tf.keras.models.load_model(path), labels


def bullets(items: tuple[str, ...]) -> None:
    for item in items:
        st.write("- " + item)


st.set_page_config(page_title="Paddy Leaf Health", page_icon="P")
st.title("Paddy Leaf Disease Prediction")
st.caption("Upload one clear paddy-leaf photo. A qualified local crop advisor must verify every diagnosis before treatment.")
upload = st.file_uploader("Upload a paddy leaf image", type=["jpg", "jpeg", "png"], help="Use a well-lit, close image of one leaf.")
image = None
if upload:
    try:
        image = Image.open(upload).convert("RGB")
        st.image(image, caption="Uploaded leaf", use_container_width=True)
    except UnidentifiedImageError:
        st.error("The uploaded file is not a valid JPG or PNG image.")

models = sorted((ROOT / "models").glob("*.keras"))
if not models:
    st.warning("Prediction is unavailable until a trained model and labels file are present in models/.")
elif tf is None:
    st.error("TensorFlow is required for model predictions. Run the app with the project's Python 3.13 environment.")
elif image is not None:
    chosen = st.sidebar.selectbox("Model", models, format_func=lambda path: path.name)
    model, labels = load_model(str(chosen))
    height, width = model.input_shape[1:3]
    pixels = np.asarray(image.resize((width, height)), dtype=np.float32)
    scores = model.predict(np.expand_dims(pixels, axis=0), verbose=0)[0]
    index = int(np.argmax(scores)
    )
    label, confidence = labels[index], float(scores[index])
    recommendation = get_recommendation(label)
    severity = assess_severity(image)

    st.subheader(f"{recommendation.disease} - {confidence:.1%} confidence")
    st.write(recommendation.summary)
    st.metric("Visible discoloration estimate", f"{severity.visible_damage_percent:.1f}%", severity.level.title())
    st.caption(severity.note)
    if confidence < 0.65:
        st.warning("Low confidence: retake the photo in good daylight and verify the disease with an agronomist before taking action.")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Pesticide / disease management")
        bullets(recommendation.pesticide)
    with right:
        st.markdown("#### Fertilizer / nutrient guidance")
        bullets(recommendation.fertilizer)
    st.markdown("#### Prevention")
    bullets(recommendation.prevention)

    history_key = f"{upload.name}:{upload.size}:{chosen.name}"
    if st.session_state.get("history_key") != history_key:
        record_prediction(DATABASE, recommendation.disease, confidence, severity.level, severity.visible_damage_percent)
        st.session_state.history_key = history_key
        st.caption("Prediction logged locally without storing the uploaded image.")

st.divider()
st.caption("Follow local regulations, product labels, PPE requirements, and pre-harvest intervals. The app does not provide pesticide rates.")
