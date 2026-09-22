"""Curated, conservative crop-management guidance for supported classes."""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Recommendation:
    disease: str
    summary: str
    pesticide: Tuple[str, ...]
    fertilizer: Tuple[str, ...]
    prevention: Tuple[str, ...]


CATALOG: Dict[str, Recommendation] = {
    "bacterial_leaf_blight": Recommendation(
        "Bacterial leaf blight", "Bacterial disease often associated with warm, wet conditions and excess nitrogen.",
        ("Prioritize sanitation, drainage, and resistant varieties; antibiotics should not be used routinely.", "Where locally registered and recommended by an extension officer, a copper-based bactericide may be considered according to its label."),
        ("Avoid additional nitrogen while symptoms are active.", "Use a balanced, soil-test-based nutrient plan; maintain adequate potassium to support plant vigor."),
        ("Remove volunteer rice and infected residue.", "Avoid leaf injury and improve field drainage."),
    ),
    "brown_spot": Recommendation(
        "Brown spot", "Fungal leaf disease that is commonly more severe in nutrient-stressed crops.",
        ("Use disease-free seed and remove heavily infected residue.", "If disease pressure is confirmed, use only a locally registered rice fungicide at the label rate after extension guidance."),
        ("Correct potassium and silicon deficiencies where soil tests indicate need.", "Apply nitrogen in split, recommended doses; do not over-apply."),
        ("Use balanced fertilization.", "Maintain suitable plant spacing and water management."),
    ),
    "leaf_smut": Recommendation(
        "Leaf smut", "Fungal disease producing small dark lesions, favored by dense crop canopies and high humidity.",
        ("Monitor disease progression and use clean seed.", "When necessary, select a fungicide registered locally for rice leaf diseases and follow the label exactly."),
        ("Avoid excessive nitrogen that creates a dense canopy.", "Maintain balanced N-P-K according to a soil test or local recommendation."),
        ("Improve airflow with recommended spacing.", "Remove crop residue after harvest."),
    ),
    "healthy": Recommendation(
        "Healthy leaf", "No supported disease pattern was detected with high confidence.",
        ("No pesticide is recommended. Continue regular scouting.",),
        ("Follow your soil-test or local crop-stage nutrient schedule.", "Use split nitrogen applications and avoid unnecessary inputs."),
        ("Scout weekly for early symptoms.", "Keep field records of fertilizer, irrigation, and disease observations."),
    ),
}


def normalize_label(label: str) -> str:
    return label.strip().lower().replace("-", "_").replace(" ", "_")


def get_recommendation(label: str) -> Recommendation:
    key = normalize_label(label)
    if key not in CATALOG:
        return Recommendation(label.replace("_", " ").title(), "This class has no configured crop-management guidance.", ("Do not apply a product based on this prediction alone; verify with a crop expert.",), ("Use a soil-test-based nutrient plan.",), ("Capture more field observations and consult local extension guidance.",))
    return CATALOG[key]
