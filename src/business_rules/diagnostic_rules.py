import random

from src.models.triage_level import TriageLevel
from src import config


def physician_orders_laboratory(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """Model the probability of a laboratory order after medical evaluation."""

    probability = config.LABORATORY_PROBABILITIES[level]

    return rng.random() < probability


def physician_orders_imaging(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """Model the probability of an imaging order after medical evaluation."""

    probability = config.IMAGING_PROBABILITIES[level]

    return rng.random() < probability
