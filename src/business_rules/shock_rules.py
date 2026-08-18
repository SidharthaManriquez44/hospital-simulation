import random

from src.models.patient import Patient
from src.models.diagnosis import Diagnosis
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


def requires_surgery(diagnosis: Diagnosis) -> bool:
    """Determine whether the diagnosis requires surgical intervention."""

    return diagnosis in {
        Diagnosis.SEVERE_TBI,
        Diagnosis.HEMORRHAGIC_SHOCK,
        Diagnosis.TENSION_PNEUMOTHORAX,
        Diagnosis.UNSTABLE_PELVIC_FRACTURE,
    }


def requires_cardiac_catheterization(
    diagnosis: Diagnosis,
) -> bool:
    """Determine whether the diagnosis requires cardiac intervention."""

    return diagnosis == Diagnosis.ACUTE_MYOCARDIAL_INFARCTION
