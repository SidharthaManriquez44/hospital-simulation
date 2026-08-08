from dataclasses import dataclass
from typing import Optional
from src.models.triage_level import TriageLevel
from src.models.patient_status import PatientStatus


@dataclass(slots=True)
class Patient:
    id: int

    arrival_time: float

    triage_level: Optional[TriageLevel] = None

    status: PatientStatus = PatientStatus.ARRIVED

    registration_start: Optional[float] = None
    registration_end: Optional[float] = None

    triage_start: Optional[float] = None
    triage_end: Optional[float] = None

    consultation_start: Optional[float] = None
    consultation_end: Optional[float] = None

    departure_time: Optional[float] = None
