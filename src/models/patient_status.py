from enum import Enum


class PatientStatus(str, Enum):
    ARRIVED = "arrived"
    REGISTRATION = "registration"
    TRIAGE = "triage"
    WAITING_DOCTOR = "waiting_doctor"
    CONSULTATION = "consultation"
    DIAGNOSTIC_EVALUATION = "diagnostic_evaluation"
    LABORATORY = "laboratory"
    IMAGING = "imaging"
    DIAGNOSIS = "diagnosis"
    TREATMENT = "treatment"
    PHARMACY = "pharmacy"
    OBSERVATION = "observation"
    HOSPITALIZED = "hospitalized"
    DISCHARGED = "discharged"
    DECEASED = "deceased"
    LEFT_WITHOUT_BEING_SEEN = "left_without_being_seen"
