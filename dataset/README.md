# Dataset

Place training images in `raw/<class-name>/` using this exact layout:

```
dataset/raw/
├── bacterial_leaf_blight/
├── brown_spot/
├── leaf_smut/
└── healthy/
```

Each folder needs JPG, JPEG, or PNG images. Aim for at least 200 clear field images per class, including varying lighting, cultivars, and crop stages. Keep classes reasonably balanced.

No dataset images are committed to this repository: their source, license, quality, and regional suitability must be reviewed first. Record the dataset URL, license, collection date, and any cleaning steps here before training.
