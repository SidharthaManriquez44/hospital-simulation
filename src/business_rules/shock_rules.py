import random

from src.models.patient import Patient
from src.models.triage_level import TriageLevel
from src import config


def requires_shock_area(level: TriageLevel) -> bool:
    """Determine whether the patient requires the shock area."""

    return level == TriageLevel.RED


def requires_observation_after_shock(
    rng: random.Random,
) -> bool:
    """Determine whether a stabilized shock patient requires observation."""

    return rng.random() < config.SHOCK_TO_OBSERVATION_PROBABILITY


def shock_is_stabilized(patient: Patient) -> bool:
    """Determine whether the patient is stabilized after resuscitation."""

    return patient.shock_stabilized


def requires_surgery(diagnosis: str) -> bool:
    """Determine whether the patient requires surgical intervention."""

    return diagnosis in {
        "severe_tbi",
        "hemorrhagic_shock",
        "tension_pneumothorax",
        "unstable_pelvic_fracture",
    }


def requires_cardiac_catheterization(
    diagnosis: str,
) -> bool:
    """Determine whether the patient requires cardiac intervention."""

    return diagnosis == "acute_myocardial_infarction"
