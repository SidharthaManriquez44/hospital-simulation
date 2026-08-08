import random

import simpy

from src.models.patient import Patient
from src.models.patient_status import PatientStatus
from src.models.triage_level import TriageLevel
from src.resources.resources import HospitalResources
from src.simulation.metrics import SimulationMetrics
from src import config


class HospitalProcesses:
    """Processes executed by patients in the emergency department."""

    def __init__(
        self,
        env: simpy.Environment,
        resources: HospitalResources,
        metrics: SimulationMetrics,
        rng: random.Random,
    ) -> None:
        self.env = env
        self.resources = resources
        self.metrics = metrics
        self.rng = rng

    def patient_process(self, patient: Patient):
        """Execute the patient's process through the emergency department."""

        yield from self.registration(patient)
        yield from self.triage(patient)
        yield from self.consultation(patient)

        patient.status = PatientStatus.DISCHARGED
        patient.departure_time = self.env.now

        self.metrics.patients_served += 1

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.system_times.append(
                patient.departure_time - patient.arrival_time
            )

    def registration(self, patient: Patient):
        """Register the patient."""

        patient.status = PatientStatus.REGISTRATION
        patient.registration_start = self.env.now

        with self.resources.receptionists.request() as request:
            yield request

            duration = self.rng.uniform(
                config.REGISTRATION_MIN,
                config.REGISTRATION_MAX,
            )

            yield self.env.timeout(duration)

        patient.registration_end = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.registration_times.append(
                patient.registration_end - patient.registration_start
            )

    def triage(self, patient: Patient):
        """Perform the patient's triage assessment."""

        patient.status = PatientStatus.TRIAGE
        patient.triage_start = self.env.now

        with self.resources.triage_nurses.request() as request:
            yield request

            duration = self.rng.triangular(
                config.TRIAGE_MIN,
                config.TRIAGE_MODE,
                config.TRIAGE_MAX,
            )

            yield self.env.timeout(duration)

        patient.triage_end = self.env.now

        patient.triage_level = self._assign_triage_level()

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.triage_times.append(patient.triage_end - patient.triage_start)

    def consultation(self, patient: Patient):
        """Perform the initial medical consultation."""

        patient.status = PatientStatus.WAITING_DOCTOR

        doctor_request = self.resources.doctors.request()
        room_request = self.resources.consulting_rooms.request()

        yield self.env.all_of([doctor_request, room_request])

        patient.status = PatientStatus.CONSULTATION
        patient.consultation_start = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.waiting_times.append(
                patient.consultation_start - patient.arrival_time
            )

        duration = max(
            1.0,
            self.rng.gauss(
                config.CONSULTATION_MEAN,
                config.CONSULTATION_STD,
            ),
        )

        yield self.env.timeout(duration)

        patient.consultation_end = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.consultation_times.append(
                patient.consultation_end - patient.consultation_start
            )

        self.resources.doctors.release(doctor_request)
        self.resources.consulting_rooms.release(room_request)

    def _assign_triage_level(self) -> TriageLevel:
        """Assign a triage level to the patient.

        Temporary Sprint 1 assumption:
        all triage levels have equal probability.
        """

        return self.rng.choice(list(TriageLevel))
