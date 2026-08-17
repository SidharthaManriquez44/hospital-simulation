import random

from src.models.medication_route import MedicationRoute
from src import config
from src.models.medication_category import MedicationCategory


def requires_medication(
    rng: random.Random,
) -> bool:
    """Determine whether medication is required after diagnosis."""

    return rng.random() < config.MEDICATION_PROBABILITY


def determine_medication_category(
    rng: random.Random,
) -> MedicationCategory:
    """Select a medication category using documented reference weights."""

    categories = [
        MedicationCategory.ANALGESIA,
        MedicationCategory.ANTIBIOTIC,
        MedicationCategory.ANTIEMETIC,
        MedicationCategory.BRONCHODILATOR,
        MedicationCategory.ANTIPLATELET,
        MedicationCategory.INSULIN_GLUCOSE,
        MedicationCategory.OTHER,
    ]

    weights = [
        config.MEDICATION_CATEGORY_WEIGHTS["analgesia"],
        config.MEDICATION_CATEGORY_WEIGHTS["antibiotic"],
        config.MEDICATION_CATEGORY_WEIGHTS["antiemetic"],
        config.MEDICATION_CATEGORY_WEIGHTS["bronchodilator"],
        config.MEDICATION_CATEGORY_WEIGHTS["antiplatelet"],
        config.MEDICATION_CATEGORY_WEIGHTS["insulin_glucose"],
        config.MEDICATION_RESIDUAL_WEIGHT,
    ]

    return rng.choices(
        categories,
        weights=weights,
        k=1,
    )[0]


def determine_medication_route(
    category: MedicationCategory,
    rng: random.Random,
) -> str:
    """Determine medication administration route by category."""

    route_distributions = {
        MedicationCategory.ANALGESIA: {
            "oral": 0.62,
            "iv_bolus": 0.38,
        },
        MedicationCategory.ANTIBIOTIC: {
            "iv_infusion": 1.00,
        },
        MedicationCategory.ANTIEMETIC: {
            "oral": 0.40,
            "iv_bolus": 0.60,
        },
        MedicationCategory.ANTICOAGULATION: {
            "im_sc": 0.60,
            "iv_bolus": 0.40,
        },
        MedicationCategory.ANTIPLATELET: {
            "oral": 0.95,
            "iv_bolus": 0.05,
        },
        MedicationCategory.VASOPRESSOR: {
            "iv_infusion": 1.00,
        },
        MedicationCategory.INSULIN_GLUCOSE: {
            "im_sc": 0.65,
            "iv_bolus": 0.35,
        },
        MedicationCategory.BRONCHODILATOR: {
            MedicationRoute.NEBULIZATION: 1.0,
        },
    }

    distribution = route_distributions.get(category)

    if distribution is None:
        raise ValueError(f"No route distribution defined for {category}")

    routes = list(distribution.keys())
    probabilities = list(distribution.values())

    return MedicationRoute(
        rng.choices(
            routes,
            weights=probabilities,
            k=1,
        )[0]
    )


def requires_pharmacy_preparation(
    category: MedicationCategory,
    rng: random.Random,
) -> bool:
    """Determine whether pharmacy preparation is required."""

    probability = config.PHARMACY_PREPARATION_PROBABILITIES[category]

    return rng.random() < probability
