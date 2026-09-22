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


def _reference_only(name: str, category: str) -> Recommendation:
    """Guidance for known rice diseases without a bundled image-training class."""
    if category == "viral":
        pesticide = ("There is no curative pesticide for plant viruses; confirm diagnosis and manage the insect vector using locally approved integrated pest management.",)
    elif category == "nutrient":
        pesticide = ("Do not apply a pesticide for a nutrient disorder unless a crop expert identifies a separate pest or disease.",)
    else:
        pesticide = ("Confirm the disease with a crop expert; use only a locally registered product, if one is recommended, at its label rate.",)
    return Recommendation(
        name, "Reference-only guidance: this disease is not a prediction class in the bundled UCI training dataset.", pesticide,
        ("Base nutrient changes on a soil or tissue test and the crop growth stage.", "Avoid excess nitrogen; use balanced, split nutrient applications."),
        ("Use clean seed and resistant varieties where available.", "Improve field scouting, sanitation, drainage, and crop-residue management."),
    )


CATALOG.update({
    "rice_blast": _reference_only("Rice blast", "fungal"),
    "sheath_blight": _reference_only("Sheath blight", "fungal"),
    "sheath_rot": _reference_only("Sheath rot", "fungal"),
    "false_smut": _reference_only("False smut", "fungal"),
    "leaf_scald": _reference_only("Leaf scald", "fungal"),
    "narrow_brown_leaf_spot": _reference_only("Narrow brown leaf spot", "fungal"),
    "bacterial_leaf_streak": _reference_only("Bacterial leaf streak", "bacterial"),
    "tungro": _reference_only("Rice tungro", "viral"),
    "grassy_stunt": _reference_only("Rice grassy stunt", "viral"),
    "ragged_stunt": _reference_only("Rice ragged stunt", "viral"),
    "bakanae": _reference_only("Bakanae / foot rot", "fungal"),
    "stem_rot": _reference_only("Stem rot", "fungal"),
    "bacterial_sheath_brown_rot": _reference_only("Bacterial sheath brown rot", "bacterial"),
    "bacterial_grain_rot": _reference_only("Bacterial grain rot / panicle blight", "bacterial"),
    "rice_yellow_dwarf": _reference_only("Rice yellow dwarf", "viral"),
    "rice_stripe_virus": _reference_only("Rice stripe virus", "viral"),
    "rice_yellow_mottle_virus": _reference_only("Rice yellow mottle virus", "viral"),
    "orange_leaf": _reference_only("Orange leaf phytoplasma", "viral"),
    "khaira_zinc_deficiency": _reference_only("Khaira (zinc deficiency)", "nutrient"),
    "iron_toxicity": _reference_only("Iron toxicity / bronzing", "nutrient"),
})


def normalize_label(label: str) -> str:
    return label.strip().lower().replace("-", "_").replace(" ", "_")


def get_recommendation(label: str) -> Recommendation:
    key = normalize_label(label)
    if key not in CATALOG:
        return Recommendation(label.replace("_", " ").title(), "This class has no configured crop-management guidance.", ("Do not apply a product based on this prediction alone; verify with a crop expert.",), ("Use a soil-test-based nutrient plan.",), ("Capture more field observations and consult local extension guidance.",))
    return CATALOG[key]
