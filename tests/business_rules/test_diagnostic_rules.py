import random

from src.business_rules.diagnostic_rules import (
    physician_orders_imaging,
    physician_orders_laboratory,
)
from src.models.triage_level import TriageLevel


def test_physician_orders_laboratory_returns_bool():
    rng = random.Random(42)

    result = physician_orders_laboratory(
        TriageLevel.YELLOW,
        rng,
    )

    assert isinstance(result, bool)


def test_physician_orders_imaging_returns_bool():
    rng = random.Random(42)

    result = physician_orders_imaging(
        TriageLevel.YELLOW,
        rng,
    )

    assert isinstance(result, bool)
