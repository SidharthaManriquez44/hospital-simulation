from src.models.patient import Patient


def requires_critical_support(patient: Patient) -> bool:
    """Determine whether the patient requires critical support."""

    return patient.critical_support_required


def is_observation_eligible(patient: Patient) -> bool:
    """Determine whether the patient is eligible for observation."""

    return patient.observation_eligible


def requires_inpatient_care(patient: Patient) -> bool:
    """Determine whether the patient requires inpatient care."""

    return patient.inpatient_care_need


def is_discharge_eligible(patient: Patient) -> bool:
    """Determine whether the patient is eligible for discharge."""

    return patient.discharge_eligible
