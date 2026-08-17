import random

from src.models.medication_route import MedicationRoute
from src.business_rules.treatment_rules import (
    requires_medication,
    requires_pharmacy_preparation,
    MedicationCategory,
    determine_medication_route,
)


def test_requires_medication_is_reproducible():
    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    result_1 = requires_medication(rng_1)
    result_2 = requires_medication(rng_2)

    assert result_1 == result_2


def test_requires_medication_returns_boolean():
    rng = random.Random(42)

    result = requires_medication(rng)

    assert isinstance(result, bool)


def test_requires_pharmacy_preparation_returns_boolean():
    rng = random.Random(42)

    result = requires_pharmacy_preparation(
        MedicationCategory.ANALGESIA,
        rng,
    )

    assert isinstance(result, bool)


def test_requires_pharmacy_preparation_is_reproducible():
    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    result_1 = requires_pharmacy_preparation(
        MedicationCategory.VASOPRESSOR,
        rng_1,
    )

    result_2 = requires_pharmacy_preparation(
        MedicationCategory.VASOPRESSOR,
        rng_2,
    )

    assert result_1 == result_2


def test_high_probability_category_can_require_preparation():
    rng = random.Random(1)

    result = requires_pharmacy_preparation(
        MedicationCategory.VASOPRESSOR,
        rng,
    )

    assert result is True


def test_pharmacy_preparation_probability_for_analgesia():
    rng = random.Random(42)

    trials = 10_000

    preparations = sum(
        requires_pharmacy_preparation(
            MedicationCategory.ANALGESIA,
            rng,
        )
        for _ in range(trials)
    )

    observed_probability = preparations / trials

    assert 0.08 <= observed_probability <= 0.12


def test_bronchodilator_requires_pharmacy_preparation_probability():
    rng = random.Random(42)

    trials = 10_000

    preparations = sum(
        requires_pharmacy_preparation(
            MedicationCategory.BRONCHODILATOR,
            rng,
        )
        for _ in range(trials)
    )

    observed_probability = preparations / trials

    assert 0.01 <= observed_probability <= 0.03


def test_bronchodilator_route_is_nebulization():
    rng = random.Random(42)

    for _ in range(100):
        route = determine_medication_route(
            MedicationCategory.BRONCHODILATOR,
            rng,
        )

        assert route == MedicationRoute.NEBULIZATION
