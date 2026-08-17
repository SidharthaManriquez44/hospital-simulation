import random

from src.models.triage_level import TriageLevel
from src import config


def physician_orders_laboratory(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """
    Model the physician's probability of ordering laboratory
    testing after the initial medical evaluation.

    ESI is used as a clinical demand stratification variable,
    not as a deterministic decision rule.
    """

    probability = config.LABORATORY_PROBABILITIES[level]

    return rng.random() < probability


def physician_orders_imaging(
    level: TriageLevel,
    rng: random.Random,
) -> bool:
    """
    Model the physician's probability of ordering imaging
    after the initial medical evaluation.

    ESI is used as a clinical demand stratification variable,
    not as a deterministic decision rule.
    """

    probability = config.IMAGING_PROBABILITIES[level]

    return rng.random() < probability
