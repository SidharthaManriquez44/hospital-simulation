import random

from src import config


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
