import random

from src import config
from src.models.triage_level import TriageLevel


def requires_observation(
    rng: random.Random,
) -> bool:
    """Determine whether the patient requires observation."""

    return rng.random() < config.OBSERVATION_GLOBAL_PROBABILITY


def deteriorates_in_observation(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """Determine whether the patient deteriorates during observation."""

    probability = config.OBSERVATION_DETERIORATION_PROBABILITIES[level]

    return rng.random() < probability


def determine_observation_disposition(
    rng: random.Random,
) -> str:
    """Determine disposition after observation without deterioration."""

    return (
        "follow_up"
        if rng.random() < config.OBSERVATION_FOLLOW_UP_PROBABILITY
        else "hospitalization"
    )
