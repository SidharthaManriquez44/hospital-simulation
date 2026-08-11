import random
import pytest
from src import config

from src.business_rules.imaging_rules import (
    determine_imaging_modality,
)


def test_determine_imaging_modality_returns_valid_modality():
    rng = random.Random(42)

    result = determine_imaging_modality(rng)

    assert result in {
        "xray",
        "ct",
        "ultrasound",
        "mri",
    }


def test_determine_imaging_modality_is_reproducible():
    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    result_1 = determine_imaging_modality(rng_1)
    result_2 = determine_imaging_modality(rng_2)

    assert result_1 == result_2


def test_imaging_probabilities_sum_to_one():
    total = sum(config.IMAGING_MODALITY_PROBABILITIES.values())

    assert total == pytest.approx(1.0)
