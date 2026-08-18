from src.models.triage_level import TriageLevel
from src.business_rules.shock_rules import shock_is_stabilized
from src.business_rules.shock_rules import requires_surgery
from src.models.patient import Patient
from src.business_rules.shock_rules import (
    requires_cardiac_catheterization,
)
from src.business_rules.shock_rules import (
    requires_shock_area,
)


def test_esi_1_requires_shock_area():
    assert requires_shock_area(TriageLevel.RED) is True


def test_non_esi_1_does_not_automatically_require_shock_area():
    assert requires_shock_area(TriageLevel.ORANGE) is False
    assert requires_shock_area(TriageLevel.YELLOW) is False
    assert requires_shock_area(TriageLevel.GREEN) is False
    assert requires_shock_area(TriageLevel.BLUE) is False


def test_unstabilized_patient_requires_continued_resuscitation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.shock_stabilized = False

    assert shock_is_stabilized(patient) is False


def test_stabilized_patient_can_continue_to_disposition():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.shock_stabilized = True

    assert shock_is_stabilized(patient) is True


def test_severe_tbi_requires_surgery():
    assert requires_surgery("severe_tbi") is True


def test_hemorrhagic_shock_requires_surgery():
    assert requires_surgery("hemorrhagic_shock") is True


def test_tension_pneumothorax_requires_surgery():
    assert requires_surgery("tension_pneumothorax") is True


def test_unstable_pelvic_fracture_requires_surgery():
    assert requires_surgery("unstable_pelvic_fracture") is True


def test_acute_myocardial_infarction_does_not_require_surgery():
    assert requires_surgery("acute_myocardial_infarction") is False


def test_acute_myocardial_infarction_requires_cardiac_catheterization():
    assert requires_cardiac_catheterization("acute_myocardial_infarction") is True


def test_trauma_diagnoses_do_not_require_cardiac_catheterization():
    diagnoses = {
        "severe_tbi",
        "hemorrhagic_shock",
        "tension_pneumothorax",
        "unstable_pelvic_fracture",
    }

    for diagnosis in diagnoses:
        assert requires_cardiac_catheterization(diagnosis) is False


def test_unstabilized_patient_does_not_proceed_to_disposition():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.shock_stabilized = False

    assert shock_is_stabilized(patient) is False
