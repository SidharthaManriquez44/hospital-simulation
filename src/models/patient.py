from dataclasses import dataclass
from typing import Optional
from src.models.triage_level import TriageLevel
from src.models.patient_status import PatientStatus


@dataclass(slots=True)
class Patient:
    id: int

    arrival_time: float
    waiting_time: float = 0.0

    triage_level: Optional[TriageLevel] = None
    requires_laboratory: bool = False

    status: PatientStatus = PatientStatus.ARRIVED

    registration_start: Optional[float] = None
    registration_end: Optional[float] = None

    triage_start: Optional[float] = None
    triage_end: Optional[float] = None

    waiting_room_start: Optional[float] = None
    waiting_room_end: Optional[float] = None

    consultation_start: Optional[float] = None
    consultation_end: Optional[float] = None

    departure_time: Optional[float] = None
