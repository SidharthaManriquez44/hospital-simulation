from dataclasses import dataclass
from typing import Optional
from src.models.triage_level import TriageLevel
from src.models.patient_status import PatientStatus


@dataclass(slots=True)
class Patient:
    # -------------------------
    # Identification
    # -------------------------
    id: int

    # -------------------------
    # General times
    # -------------------------
    arrival_time: float
    departure_time: float | None = None

    # -------------------------
    # Register
    # -------------------------
    registration_start: Optional[float] = None
    registration_end: Optional[float] = None

    # -------------------------
    # Triage
    # -------------------------
    triage_level: Optional[TriageLevel] = None
    triage_start: Optional[float] = None
    triage_end: Optional[float] = None

    # -------------------------
    # Consult
    # -------------------------
    consultation_start: Optional[float] = None
    consultation_end: Optional[float] = None

    # -------------------------
    # Diagnosis
    # -------------------------
    diagnosis_confirmed: bool = False

    # -------------------------
    # Laboratory
    # -------------------------
    requires_laboratory: bool = False
    laboratory_start: Optional[float] = None
    laboratory_end: Optional[float] = None

    # -------------------------
    # Imaging
    # -------------------------
    imaging_required: bool = False
    imaging_modality: Optional[str] = None
    imaging_start: Optional[float] = None
    imaging_end: Optional[float] = None

    # -------------------------
    # Waiting
    # -------------------------
    waiting_time: float = 0.0
    waiting_room_start: Optional[float] = None
    waiting_room_end: Optional[float] = None

    # -------------------------
    # Status
    # -------------------------
    status: PatientStatus = PatientStatus.ARRIVED
