import random

from src import config
from src.models.triage_level import TriageLevel


def get_priority(level: TriageLevel) -> int:
    """Return the numerical priority associated with a triage level."""

    priorities = {
        TriageLevel.RED: 1,
        TriageLevel.ORANGE: 2,
        TriageLevel.YELLOW: 3,
        TriageLevel.GREEN: 4,
        TriageLevel.BLUE: 5,
    }

    return priorities[level]


def determine_next_area(triage_level: TriageLevel) -> str:
    """Determine the next clinical area based on the triage level."""

    if triage_level == TriageLevel.RED:
        return "shock_area"

    if triage_level in (
        TriageLevel.ORANGE,
        TriageLevel.YELLOW,
    ):
        return "consultation"

    return "waiting_room"


def determine_triage_level(
    rng: random.Random,
) -> TriageLevel:
    levels = list(config.ESI_PROBABILITIES.keys())
    probabilities = list(config.ESI_PROBABILITIES.values())

    return rng.choices(
        levels,
        weights=probabilities,
        k=1,
    )[0]
