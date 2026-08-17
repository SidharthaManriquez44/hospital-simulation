import random

from src.business_rules.resuscitation_rules import resuscitation_achieves_rosc
from src.business_rules.observation_rules import requires_observation
from src.models.triage_level import TriageLevel

from src.business_rules.observation_rules import (
    deteriorates_in_observation,
)
from src.business_rules.observation_rules import (
    determine_observation_disposition,
)


def test_requires_observation_returns_boolean():
    rng = random.Random(42)

    result = requires_observation(rng)

    assert isinstance(result, bool)


def test_deteriorates_in_observation_returns_boolean():
    rng = random.Random(42)

    result = deteriorates_in_observation(
        TriageLevel.YELLOW,
        rng,
    )

    assert isinstance(result, bool)


def test_esi_3_deterioration_probability():
    rng = random.Random(42)

    trials = 10_000

    deteriorations = sum(
        deteriorates_in_observation(
            TriageLevel.YELLOW,
            rng,
        )
        for _ in range(trials)
    )

    observed_probability = deteriorations / trials

    assert 0.09 <= observed_probability <= 0.13


def test_esi_1_has_higher_deterioration_probability_than_esi_5():
    rng_1 = random.Random(42)
    rng_5 = random.Random(42)

    trials = 10_000

    esi_1_deteriorations = sum(
        deteriorates_in_observation(
            TriageLevel.RED,
            rng_1,
        )
        for _ in range(trials)
    )

    esi_5_deteriorations = sum(
        deteriorates_in_observation(
            TriageLevel.BLUE,
            rng_5,
        )
        for _ in range(trials)
    )

    assert esi_1_deteriorations > esi_5_deteriorations


def test_observation_disposition_returns_valid_value():
    rng = random.Random(42)

    result = determine_observation_disposition(rng)

    assert result in {
        "follow_up",
        "hospitalization",
    }


def test_observation_disposition_probability():
    rng = random.Random(42)

    trials = 10_000

    follow_ups = sum(
        determine_observation_disposition(rng) == "follow_up" for _ in range(trials)
    )

    observed_probability = follow_ups / trials

    assert 0.61 <= observed_probability <= 0.67


def test_resuscitation_achieves_rosc_returns_boolean():
    rng = random.Random(42)

    result = resuscitation_achieves_rosc(rng)

    assert isinstance(result, bool)


def test_resuscitation_rosc_probability():
    rng = random.Random(42)

    trials = 10_000

    rosc_events = sum(resuscitation_achieves_rosc(rng) for _ in range(trials))

    observed_probability = rosc_events / trials

    assert 0.27 <= observed_probability <= 0.33
