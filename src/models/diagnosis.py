from enum import Enum


class Diagnosis(str, Enum):
    """Clinical diagnoses relevant to emergency disposition."""

    SEVERE_TBI = "severe_tbi"
    HEMORRHAGIC_SHOCK = "hemorrhagic_shock"
    TENSION_PNEUMOTHORAX = "tension_pneumothorax"
    UNSTABLE_PELVIC_FRACTURE = "unstable_pelvic_fracture"
    ACUTE_MYOCARDIAL_INFARCTION = "acute_myocardial_infarction"
    MINOR_INJURY = "minor_injury"
