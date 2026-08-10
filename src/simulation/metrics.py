from dataclasses import dataclass, field
from src.models.triage_level import TriageLevel


@dataclass(slots=True)
class SimulationMetrics:
    # -------------------------
    # Times
    # -------------------------

    arrival_to_consultation_times: list[float] = field(default_factory=list)

    registration_times: list[float] = field(default_factory=list)

    triage_times: list[float] = field(default_factory=list)

    triage_levels: list[TriageLevel] = field(default_factory=list)

    consultation_times: list[float] = field(default_factory=list)

    system_times: list[float] = field(default_factory=list)

    waiting_times: list[float] = field(default_factory=list)

    # -------------------------
    # Laboratory
    # -------------------------

    laboratory_waiting_times: list[float] = field(default_factory=list)

    laboratory_processing_times: list[float] = field(default_factory=list)

    laboratory_tat_times: list[float] = field(default_factory=list)

    laboratory_tat_without_waiting_times: list[float] = field(default_factory=list)

    laboratory_patients_by_triage: dict[str, int] = field(default_factory=dict)

    laboratory_requests_by_triage: dict[str, int] = field(default_factory=dict)
    # -------------------------
    # Imaging
    # -------------------------

    imaging_patients_by_triage: dict[str, int] = field(default_factory=dict)

    imaging_requests_by_triage: dict[str, int] = field(default_factory=dict)

    imaging_modalities: dict[str, int] = field(default_factory=dict)

    # -------------------------
    # Queues
    # -------------------------

    registration_queue_lengths: list[int] = field(default_factory=list)

    triage_queue_lengths: list[int] = field(default_factory=list)

    consultation_queue_lengths: list[int] = field(default_factory=list)

    # -------------------------
    # Patients
    # -------------------------

    patients_arrived: int = 0

    patients_served: int = 0

    hospitalizations: int = 0

    deaths: int = 0

    # -------------------------
    # Resource utilization
    # -------------------------

    doctor_busy_time: float = 0.0

    nurse_busy_time: float = 0.0

    consulting_room_busy_time: float = 0.0

    stretcher_busy_time: float = 0.0

    shock_area_busy_time: float = 0.0

    laboratory_busy_time: float = 0.0

    xray_busy_time: float = 0.0

    ct_busy_time: float = 0.0

    mri_busy_time: float = 0.0

    ultrasound_busy_time: float = 0.0
