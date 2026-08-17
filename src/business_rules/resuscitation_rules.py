import random
from src import config


def resuscitation_achieves_rosc(
    rng: random.Random,
) -> bool:
    """Determine whether resuscitation achieves ROSC."""

    return rng.random() < config.RESUSCITATION_ROSC_PROBABILITY
