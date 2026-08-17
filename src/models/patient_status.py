from enum import Enum


class PatientStatus(str, Enum):
    ARRIVED = "arrived"

    REGISTRATION = "registration"

    TRIAGE = "triage"

    WAITING_DOCTOR = "waiting_doctor"

    CONSULTATION = "consultation"

    DIAGNOSTIC_EVALUATION = "diagnostic_evaluation"

    WAITING_DIAGNOSTIC_RESULTS = "waiting_diagnostic_results"

    WAITING_REASSESSMENT = "waiting_reassessment"

    REASSESSMENT = "reassessment"

    LABORATORY = "laboratory"

    IMAGING = "imaging"

    DIAGNOSIS = "diagnosis"

    TREATMENT = "treatment"

    PHARMACY = "pharmacy"

    OBSERVATION = "observation"

    DETERIORATING = "deteriorating"

    SHOCK = "shock"

    HOSPITALIZED = "hospitalized"

    OUTPATIENT_REFERRAL = "outpatient_referral"

    DECEASED = "deceased"
