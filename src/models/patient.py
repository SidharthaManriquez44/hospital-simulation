from dataclasses import dataclass
from typing import Optional

from src.models.medication_route import MedicationRoute
from src.models.patient_status import PatientStatus
from src.models.triage_level import TriageLevel


@dataclass(slots=True)
class Patient:
    """Represent a patient throughout the emergency department process."""

    # -------------------------
    # Identification
    # -------------------------

    id: int
    arrival_time: float

    # -------------------------
    # General
    # -------------------------

    departure_time: Optional[float] = None

    status: PatientStatus = PatientStatus.ARRIVED

    waiting_time: float = 0.0

    # -------------------------
    # Triage
    # -------------------------

    triage_level: Optional[TriageLevel] = None

    triage_start: Optional[float] = None
    triage_end: Optional[float] = None

    # Initial physical route
    initial_area: Optional[str] = None

    # -------------------------
    # Initial medical evaluation
    # -------------------------

    initial_evaluation_start: Optional[float] = None
    initial_evaluation_end: Optional[float] = None

    # -------------------------
    # Diagnostic evaluation
    # -------------------------

    diagnostic_evaluation_start: Optional[float] = None
    diagnostic_evaluation_end: Optional[float] = None

    # -------------------------
    # Laboratory
    # -------------------------

    requires_laboratory: bool = False
    laboratory_start: Optional[float] = None
    laboratory_end: Optional[float] = None
    laboratory_result_available: bool = False

    # -------------------------
    # Imaging
    # -------------------------

    imaging_required: bool = False
    imaging_modality: Optional[str] = None
    imaging_start: Optional[float] = None
    imaging_end: Optional[float] = None
    imaging_result_available: bool = False

    # -------------------------
    # Reassessment
    # -------------------------

    reassessment_start: Optional[float] = None
    reassessment_end: Optional[float] = None

    # -------------------------
    # Diagnosis
    # -------------------------

    diagnosis_confirmed: bool = False

    # -------------------------
    # Treatment
    # -------------------------

    treatment_required: bool = False
    treatment_start: Optional[float] = None
    treatment_end: Optional[float] = None

    # -------------------------
    # Pharmacy
    # -------------------------
    pharmacy_validation_start: Optional[float] = None
    pharmacy_validation_end: Optional[float] = None

    pharmacy_preparation_start: Optional[float] = None
    pharmacy_preparation_end: Optional[float] = None

    pharmacy_distribution_start: Optional[float] = None
    pharmacy_distribution_end: Optional[float] = None

    pharmacy_preparation_required: bool = False

    # -------------------------
    # Medication administration
    # -------------------------
    medication_route: Optional[MedicationRoute] = None
    medication_administration_start: Optional[float] = None
    medication_administration_end: Optional[float] = None
    medication_category: Optional[str] = None

    # -------------------------
    # Disposition
    # -------------------------

    disposition: Optional[str] = None

    # -------------------------
    # Observation
    # -------------------------

    observation_start: Optional[float] = None
    observation_end: Optional[float] = None

    # -------------------------
    # Hospitalization
    # -------------------------

    hospitalized: bool = False

    # -------------------------
    # External referral
    # -------------------------

    outpatient_referral: bool = False

    # -------------------------
    # Terminal outcome
    # -------------------------

    deceased: bool = False

    # -------------------------
    # Waiting areas
    # -------------------------

    waiting_room_start: Optional[float] = None
    waiting_room_end: Optional[float] = None

    # -------------------------
    # Clinical status
    # -------------------------

    clinical_status: Optional[str] = None

    # -------------------------
    # Current care area
    # -------------------------

    current_area: Optional[str] = None

    # -------------------------
    # Emergency / Shock
    # -------------------------

    arrival_mode: str = "walk_in"

    shock_required: bool = False

    shock_start: Optional[float] = None
    shock_end: Optional[float] = None

    shock_stabilized: bool = False

    # -------------------------
    # Consultation
    # -------------------------
    consultation_start: Optional[float] = None
    consultation_end: Optional[float] = None
