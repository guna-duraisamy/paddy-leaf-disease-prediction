# Paddy Leaf Disease Prediction

A deep-learning starter project that identifies paddy leaf diseases from a photograph and returns practical pesticide and fertilizer/nutrient guidance. It uses TensorFlow transfer learning for classification and Streamlit for a simple web interface.

> **Important:** Recommendations are educational defaults, not a pesticide prescription. Confirm the disease with a local agricultural extension officer, follow the product label, use the locally registered formulation, and observe all safety and pre-harvest requirements.

## Project layout

```
paddy-leaf-disease-prediction/
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
├── src/
├── models/
├── images/
└── dataset/
```

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run src/app.py
```

The app starts in demo mode if no trained model is present. To use real predictions, train a model and then choose it in the sidebar.

## Dataset format

Create one folder per class under `dataset/raw`. Folder names must match the labels below (case-insensitive is supported):

```
dataset/raw/
├── bacterial_leaf_blight/
├── brown_spot/
├── leaf_smut/
└── healthy/
```

Use clear, single-leaf JPG/PNG images. Keep the image source and license in `dataset/README.md`; do not commit private or very large datasets.

## Train

```bash
python -m src.train --data-dir dataset/raw --epochs 12 --batch-size 16
```

This saves a timestamped Keras model and label map under `models/`. MobileNetV2 ImageNet weights are used by default; the first run may download those weights.

## Predict from the command line

```bash
python -m src.predict --model models/paddy_leaf_model_YYYYMMDD_HHMMSS.keras --image path/to/leaf.jpg
```

## Recommendation labels

The built-in knowledge base covers bacterial leaf blight, brown spot, leaf smut, and healthy leaves. It provides integrated management suggestions and nutrient advice. Update `src/recommendations.py` with region-specific guidance after consulting a crop expert.

## Validation

```bash
python -m unittest discover -s tests -v
```

## License

Add a license appropriate for your data and deployment before publishing the application.
