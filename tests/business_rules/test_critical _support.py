from src.models.patient import Patient
from src.business_rules.critical_support import (
    requires_inpatient_care,
    requires_critical_support,
    is_observation_eligible,
    is_discharge_eligible,
)


def test_patient_requiring_critical_support_requires_icu():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.critical_support_required = True

    assert patient.critical_support_required is True


def test_critical_support_requires_icu():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.critical_support_required = True

    assert requires_critical_support(patient) is True


def test_patient_without_critical_support_does_not_require_icu():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.critical_support_required = False

    assert requires_critical_support(patient) is False


def test_stable_patient_can_be_eligible_for_observation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.observation_eligible = True

    assert is_observation_eligible(patient) is True


def test_patient_not_eligible_for_observation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.observation_eligible = False

    assert is_observation_eligible(patient) is False


def test_patient_requiring_inpatient_care_requires_hospitalization():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.inpatient_care_need = True

    assert requires_inpatient_care(patient) is True


def test_resolved_patient_is_eligible_for_discharge():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.discharge_eligible = True

    assert is_discharge_eligible(patient) is True
