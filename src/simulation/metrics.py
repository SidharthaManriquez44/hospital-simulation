from dataclasses import dataclass, field


@dataclass(slots=True)
class SimulationMetrics:
    # -------------------------
    # Times
    # -------------------------

    waiting_times: list[float] = field(default_factory=list)

    registration_times: list[float] = field(default_factory=list)

    triage_times: list[float] = field(default_factory=list)

    consultation_times: list[float] = field(default_factory=list)

    system_times: list[float] = field(default_factory=list)

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
    # Utilización de recursos
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
