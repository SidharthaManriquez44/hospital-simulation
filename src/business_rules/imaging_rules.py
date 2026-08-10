import random

from src import config
from src.models.triage_level import TriageLevel


def requires_imaging(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """Determine whether imaging is required based on ESI."""

    probability = config.IMAGING_PROBABILITIES[level]

    return rng.random() < probability


def determine_imaging_modality(
    rng: random.Random,
) -> str:
    """Select an imaging modality based on configured probabilities."""

    modalities = list(config.IMAGING_MODALITY_PROBABILITIES.keys())

    probabilities = list(config.IMAGING_MODALITY_PROBABILITIES.values())

    return rng.choices(
        modalities,
        weights=probabilities,
        k=1,
    )[0]
