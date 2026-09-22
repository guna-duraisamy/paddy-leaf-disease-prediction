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

## Bundled training dataset

This repository includes the **UCI Rice Leaf Diseases** dataset (downloaded 2026-09-22): 120 JPG images, with 40 images each for bacterial leaf blight, brown spot, and leaf smut. The original images have a white background, so results should not be treated as a guarantee of performance on real field photographs.

- Source: https://archive.ics.uci.edu/dataset/486/rice%C2%B1leaf%C2%B1diseases
- License: CC BY 4.0
- Citation: Shah, J., Prajapati, H., & Dabhi, V. (2017). *Rice Leaf Diseases* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R013

Any additional dataset must have an explicit, compatible license. Record its URL, license, collection date, and cleaning steps here before use.
