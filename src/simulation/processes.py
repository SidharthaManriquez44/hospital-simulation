import random
import simpy

from src.scenarios.scenarios import Scenario
from src.models.patient import Patient
from src.models.patient_status import PatientStatus
from src.resources.resources import HospitalResources
from src.simulation.metrics import SimulationMetrics
from src.business_rules.triage_rules import (
    determine_triage_level,
)

from src.business_rules.diagnostic_rules import (
    physician_orders_laboratory,
    physician_orders_imaging,
)

from src.business_rules.imaging_rules import (
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
            self.metrics.triage_levels.append(patient.triage_level)

    def consultation(self, patient: Patient):
        """Perform the initial medical evaluation."""

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

        yield self.env.timeout(duration)

        patient.consultation_end = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.consultation_times.append(
                patient.consultation_end - patient.consultation_start
            )
            self.metrics.waiting_times.append(patient.waiting_time)

        self.resources.doctors.release(doctor_request)
        self.resources.consulting_rooms.release(room_request)

        yield from self.diagnostic_evaluation(patient)

    def diagnostic_evaluation(self, patient: Patient):
        """Determine whether additional diagnostic information is required."""

        patient.requires_laboratory = physician_orders_laboratory(
            patient.triage_level,
            self.rng,
        )

        patient.imaging_required = physician_orders_imaging(
            patient.triage_level,
            self.rng,
        )

        diagnostic_processes = []

        if patient.requires_laboratory:
            diagnostic_processes.append(self.env.process(self.laboratory(patient)))

        if patient.imaging_required:
            patient.imaging_modality = determine_imaging_modality(self.rng)

            diagnostic_processes.append(self.env.process(self.imaging(patient)))

        if diagnostic_processes:
            yield self.env.all_of(diagnostic_processes)

        self.diagnosis(patient)

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

    def imaging(self, patient: Patient):
        """Process the imaging study requested by the physician."""

        patient.status = PatientStatus.IMAGING
        patient.imaging_start = self.env.now

        try:
            minimum, mode, maximum = config.IMAGING_DURATION_PARAMETERS[
                patient.imaging_modality
            ]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported imaging modality: {patient.imaging_modality}"
            ) from exc

        duration = self.rng.triangular(
            minimum,
            maximum,
            mode,
        )

        yield self.env.timeout(duration)

        patient.imaging_end = self.env.now

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.imaging_times.append(
                patient.imaging_end - patient.imaging_start
            )

        if patient.arrival_time >= config.WARMUP_TIME:
            self.metrics.imaging_requests_by_modality[patient.imaging_modality] = (
                self.metrics.imaging_requests_by_modality.get(
                    patient.imaging_modality,
                    0,
                )
                + 1
            )

    def diagnosis(self, patient: Patient):
        """Establish the medical diagnosis after clinical evaluation."""

        patient.diagnosis_confirmed = True

        # yield from self.treatment(patient)

    def treatment(self, patient: Patient):
        """Provide the treatment determined by the physician."""

        patient.status = PatientStatus.TREATMENT

        duration = max(
            1.0,
            self.rng.gauss(
                config.TREATMENT_MEAN,
                config.TREATMENT_STD,
            ),
        )

        yield self.env.timeout(duration)

        yield from self.disposition(patient)

    def pharmacy(self, patient: Patient): ...

    def disposition(self, patient: Patient):
        """Determine the patient's final clinical disposition."""

        ...

    def observation(self, patient: Patient): ...

    def hospitalization(self, patient: Patient): ...
