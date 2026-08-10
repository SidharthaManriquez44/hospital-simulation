import random

import simpy

from models.triage_level import TriageLevel
from scenarios.scenarios import Scenario
from src.models.patient import Patient
from src.models.patient_status import PatientStatus
from src.resources.resources import HospitalResources
from src.simulation.metrics import SimulationMetrics
from src.business_rules.triage_rules import (
    determine_triage_level,
    requires_laboratory,
)
from src.business_rules.imaging_rules import (
    requires_imaging,
    determine_imaging_modality,
)
from src import config


class HospitalProcesses:
    """Processes executed by patients in the emergency department."""

    def __init__(
        self,
        env: simpy.Environment,
        resources: HospitalResources,
        metrics: SimulationMetrics,
        rng: random.Random,
        scenario: Scenario,
    ) -> None:
        self.env = env
        self.resources = resources
        self.metrics = metrics
        self.rng = rng
        self.scenario = scenario

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

            patient.waiting_time += self.env.now - patient.registration_start

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

            patient.waiting_time += self.env.now - patient.triage_start

            duration = self.rng.triangular(
                config.TRIAGE_MIN,
                config.TRIAGE_MODE,
                config.TRIAGE_MAX,
            )

            yield self.env.timeout(duration)

        patient.triage_end = self.env.now

        patient.triage_level = determine_triage_level(self.rng)

        if patient.arrival_time >= config.WARMUP_TIME:
            triage_key = patient.triage_level.value

            self.metrics.laboratory_patients_by_triage[triage_key] = (
                self.metrics.laboratory_patients_by_triage.get(
                    triage_key,
                    0,
                )
                + 1
            )

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.triage_levels.append(patient.triage_level)

    def consultation(self, patient: Patient):
        """Perform the initial medical consultation."""

        patient.status = PatientStatus.WAITING_DOCTOR

        doctor_request = self.resources.doctors.request()
        room_request = self.resources.consulting_rooms.request()

        yield self.env.all_of([doctor_request, room_request])

        patient.waiting_time += self.env.now - patient.triage_end

        patient.status = PatientStatus.CONSULTATION
        patient.consultation_start = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.arrival_to_consultation_times.append(
                patient.consultation_start - patient.arrival_time
            )

        duration = max(
            1.0,
            self.rng.gauss(
                config.CONSULTATION_MEAN,
                config.CONSULTATION_STD,
            ),
        )

        if self.scenario.fast_track and patient.triage_level in (
            TriageLevel.GREEN,
            TriageLevel.BLUE,
        ):
            duration *= config.FAST_TRACK_CONSULTATION_FACTOR

        yield self.env.timeout(duration)

        patient.consultation_end = self.env.now

        # -----------------------------------------------------------------
        # Laboratory decision
        # -----------------------------------------------------------------

        patient.requires_laboratory = requires_laboratory(
            patient.triage_level,
            self.rng,
        )

        if patient.requires_laboratory and patient.arrival_time >= config.WARMUP_TIME:
            triage_key = patient.triage_level.value

            self.metrics.laboratory_requests_by_triage[triage_key] = (
                self.metrics.laboratory_requests_by_triage.get(
                    triage_key,
                    0,
                )
                + 1
            )

        # -----------------------------------------------------------------
        # Imaging decision
        # -----------------------------------------------------------------

        patient.imaging_required = requires_imaging(
            patient.triage_level,
            self.rng,
        )

        if patient.imaging_required:
            patient.imaging_modality = determine_imaging_modality(
                self.rng,
            )

        if patient.arrival_time >= config.WARMUP_TIME:
            triage_key = patient.triage_level.value

            self.metrics.imaging_patients_by_triage[triage_key] = (
                self.metrics.imaging_patients_by_triage.get(
                    triage_key,
                    0,
                )
                + 1
            )

            if patient.imaging_required:
                self.metrics.imaging_requests_by_triage[triage_key] = (
                    self.metrics.imaging_requests_by_triage.get(
                        triage_key,
                        0,
                    )
                    + 1
                )

                self.metrics.imaging_modalities[patient.imaging_modality] = (
                    self.metrics.imaging_modalities.get(
                        patient.imaging_modality,
                        0,
                    )
                    + 1
                )

        # -----------------------------------------------------------------
        # Consultation metrics
        # -----------------------------------------------------------------

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.consultation_times.append(
                patient.consultation_end - patient.consultation_start
            )

            self.metrics.waiting_times.append(patient.waiting_time)

        # Release medical resources immediately after consultation.
        self.resources.doctors.release(doctor_request)
        self.resources.consulting_rooms.release(room_request)

        # -----------------------------------------------------------------
        # Laboratory process
        # -----------------------------------------------------------------

        if patient.requires_laboratory:
            yield from self.laboratory(patient)

    def laboratory(self, patient: Patient):
        """Process laboratory testing for the patient."""

        patient.status = PatientStatus.LABORATORY
        patient.laboratory_start = self.env.now

        # Sample collection does not occupy the laboratory technician.
        sample_duration = self.rng.triangular(
            config.LABORATORY_SAMPLE_MIN,
            config.LABORATORY_SAMPLE_MODE,
            config.LABORATORY_SAMPLE_MAX,
        )

        yield self.env.timeout(sample_duration)

        # Specimen transport does not occupy the laboratory technician.
        transport_duration = self.rng.triangular(
            config.LABORATORY_TRANSPORT_MIN,
            config.LABORATORY_TRANSPORT_MODE,
            config.LABORATORY_TRANSPORT_MAX,
        )

        yield self.env.timeout(transport_duration)

        # Request the laboratory technician only for sample processing.
        processing_request_time = self.env.now

        with self.resources.laboratory_technicians.request() as request:
            yield request

            processing_start = self.env.now

            laboratory_waiting_time = processing_start - processing_request_time

            processing_duration = self.rng.triangular(
                config.LABORATORY_PROCESSING_MIN,
                config.LABORATORY_PROCESSING_MODE,
                config.LABORATORY_PROCESSING_MAX,
            )

            yield self.env.timeout(processing_duration)

        patient.laboratory_end = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.laboratory_waiting_times.append(laboratory_waiting_time)

            self.metrics.laboratory_processing_times.append(processing_duration)

            self.metrics.laboratory_tat_times.append(
                patient.laboratory_end - patient.laboratory_start
            )

            self.metrics.laboratory_tat_without_waiting_times.append(
                sample_duration + transport_duration + processing_duration
            )

    def determine_imaging(self, patient: Patient) -> None:
        """Determine whether the patient requires imaging."""
        pass
