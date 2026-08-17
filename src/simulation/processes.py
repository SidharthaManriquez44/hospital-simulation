import random
import simpy

from src.business_rules.resuscitation_rules import resuscitation_achieves_rosc
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
from src.business_rules.resident_rules import (
    eligible_resident_levels,
)
from src.business_rules.treatment_rules import (
    requires_medication,
    requires_pharmacy_preparation,
    determine_medication_route,
    determine_medication_category,
)
from src.business_rules.observation_rules import (
    deteriorates_in_observation,
    determine_observation_disposition,
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

        # The physician and consultation room are released
        # after the initial medical evaluation.
        self.resources.doctors.release(doctor_request)

        self.resources.consulting_rooms.release(room_request)

        # The physician's diagnostic decision occurs
        # after the initial medical evaluation.
        yield from self.diagnostic_evaluation(patient)

    def _request_resident(self, patient: Patient):
        """Request the first available resident eligible for the patient."""

        eligible_levels = eligible_resident_levels(patient.triage_level)

        resources = {
            "R1": self.resources.r1_residents,
            "R2": self.resources.r2_residents,
            "R3": self.resources.r3_residents,
        }

        requests = {level: resources[level].request() for level in eligible_levels}

        result = yield self.env.any_of(list(requests.values()))

        selected_level = next(
            level for level, request in requests.items() if request in result
        )

        selected_request = requests[selected_level]

        # Cancel requests that were not granted.
        for level, request in requests.items():
            if level != selected_level:
                request.cancel()

        return resources[selected_level], selected_request

    def diagnostic_evaluation(self, patient: Patient):
        """Determine and execute diagnostic studies."""

        patient.status = PatientStatus.DIAGNOSTIC_EVALUATION

        diagnostic_processes = []

        patient.requires_laboratory = physician_orders_laboratory(
            patient.triage_level,
            self.rng,
        )

        patient.imaging_required = physician_orders_imaging(
            patient.triage_level,
            self.rng,
        )

        if patient.requires_laboratory:
            diagnostic_processes.append(self.env.process(self.laboratory(patient)))

        if patient.imaging_required:
            patient.imaging_modality = determine_imaging_modality(self.rng)

            diagnostic_processes.append(self.env.process(self.imaging(patient)))

        if diagnostic_processes:
            yield self.env.all_of(diagnostic_processes)

        yield from self.diagnosis(patient)

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
        """Establish the diagnosis after diagnostic results are available."""

        patient.status = PatientStatus.WAITING_DOCTOR

        resource, request = yield from self._request_resident(patient)

        patient.status = PatientStatus.DIAGNOSIS
        # The diagnosis is established after the clinical evaluation
        # and any required laboratory or imaging results are available.
        patient.diagnosis_confirmed = True

        resource.release(request)

    def treatment(self, patient: Patient):
        """Initiate treatment after diagnosis."""

        patient.status = PatientStatus.TREATMENT

        if not requires_medication(self.rng):
            return

        patient.medication_category = determine_medication_category(self.rng)

        patient.medication_route = determine_medication_route(
            patient.medication_category,
            self.rng,
        )

        patient.pharmacy_preparation_required = requires_pharmacy_preparation(
            patient.medication_category,
            self.rng,
        )

        yield from self.pharmacy(patient)

    def requires_medication(
        rng: random.Random,
    ) -> bool:
        """Determine whether medication is required after diagnosis."""

        return rng.random() < config.MEDICATION_PROBABILITY

    def administer_medication(
        self,
        patient: Patient,
        route: str,
    ):
        """Administer prescribed medication through nursing care."""

        patient.status = PatientStatus.TREATMENT
        patient.medication_route = route
        patient.medication_administration_start = self.env.now

        with self.resources.nurses.request() as request:
            yield request

            if route == "oral":
                duration = self.rng.triangular(
                    config.MEDICATION_ORAL_MIN,
                    config.MEDICATION_ORAL_MODE,
                    config.MEDICATION_ORAL_MAX,
                )

            elif route == "im_sc":
                duration = self.rng.triangular(
                    config.MEDICATION_IM_SC_MIN,
                    config.MEDICATION_IM_SC_MODE,
                    config.MEDICATION_IM_SC_MAX,
                )

            elif route == "iv_bolus":
                duration = self.rng.triangular(
                    config.MEDICATION_IV_BOLUS_MIN,
                    config.MEDICATION_IV_BOLUS_MODE,
                    config.MEDICATION_IV_BOLUS_MAX,
                )

            elif route == "iv_infusion":
                duration = self.rng.triangular(
                    config.MEDICATION_IV_INFUSION_MIN,
                    config.MEDICATION_IV_INFUSION_MODE,
                    config.MEDICATION_IV_INFUSION_MAX,
                )

            elif route == "critical":
                duration = self.rng.triangular(
                    config.MEDICATION_CRITICAL_MIN,
                    config.MEDICATION_CRITICAL_MODE,
                    config.MEDICATION_CRITICAL_MAX,
                )

            else:
                raise ValueError(f"Unsupported medication route: {route}")

            yield self.env.timeout(duration)

        patient.medication_administration_end = self.env.now

    def pharmacy_validation(self, patient: Patient):
        """Validate the medical prescription."""

        patient.status = PatientStatus.PHARMACY
        patient.pharmacy_validation_start = self.env.now

        with self.resources.pharmacists.request() as request:
            yield request

            duration = self.rng.triangular(
                config.PHARMACY_VALIDATION_MIN,
                config.PHARMACY_VALIDATION_MODE,
                config.PHARMACY_VALIDATION_MAX,
            )

            yield self.env.timeout(duration)

        patient.pharmacy_validation_end = self.env.now

    def pharmacy_preparation(self, patient: Patient):
        """Prepare medication when preparation is required."""

        patient.pharmacy_preparation_start = self.env.now

        with self.resources.pharmacy_technicians.request() as request:
            yield request

            duration = self.rng.triangular(
                config.PHARMACY_PREPARATION_MIN,
                config.PHARMACY_PREPARATION_MODE,
                config.PHARMACY_PREPARATION_MAX,
            )

            yield self.env.timeout(duration)

        patient.pharmacy_preparation_end = self.env.now

    def pharmacy_distribution(self, patient: Patient):
        """Distribute the dispensed medication to nursing."""

        patient.pharmacy_distribution_start = self.env.now

        duration = self.rng.triangular(
            config.PHARMACY_DISTRIBUTION_MIN,
            config.PHARMACY_DISTRIBUTION_MODE,
            config.PHARMACY_DISTRIBUTION_MAX,
        )

        yield self.env.timeout(duration)

        patient.pharmacy_distribution_end = self.env.now

    def pharmacy(self, patient: Patient):
        """Process the medication through emergency pharmacy."""

        patient.status = PatientStatus.PHARMACY

        yield from self.pharmacy_validation(patient)

        if patient.pharmacy_preparation_required:
            yield from self.pharmacy_preparation(patient)

        yield from self.pharmacy_distribution(patient)

        yield from self.administer_medication(
            patient,
            patient.medication_route,
        )

    def observation(self, patient: Patient):
        """Monitor a patient during emergency observation."""

        patient.status = PatientStatus.OBSERVATION
        patient.current_area = "observation"

        with self.resources.observation_beds.request() as request:
            yield request

            patient.observation_start = self.env.now

            observation_duration = self.rng.triangular(
                config.OBSERVATION_MIN,
                config.OBSERVATION_MAX,
                config.OBSERVATION_MODE,
            )

            deteriorates = deteriorates_in_observation(
                patient.triage_level,
                self.rng,
            )

            if deteriorates:
                deterioration_time = self.rng.uniform(
                    0,
                    observation_duration,
                )

                yield self.env.timeout(deterioration_time)

                yield from self.observation_deterioration(patient)

                patient.observation_end = self.env.now

                yield from self.resuscitation(patient)

                return

            yield self.env.timeout(observation_duration)

            patient.observation_end = self.env.now

            patient.disposition = determine_observation_disposition(
                self.rng,
            )

            if patient.disposition == "follow_up":
                patient.outpatient_referral = True
            else:
                patient.hospitalized = True

            patient.current_area = None
            patient.departure_time = self.env.now

    def observation_deterioration(self, patient: Patient):
        """Handle clinical deterioration during observation."""

        patient.clinical_status = "deteriorating"
        patient.current_area = "observation"

        yield self.env.timeout(1)

    def resuscitation(self, patient: Patient):
        """Perform immediate resuscitation after clinical deterioration."""

        if not resuscitation_achieves_rosc(self.rng):
            patient.deceased = True
            patient.status = PatientStatus.DECEASED
            patient.clinical_status = "deceased"
            patient.departure_time = self.env.now
            return

        patient.shock_stabilized = True
        patient.clinical_status = "stabilized"

        # The patient leaves the emergency department model.
        patient.hospitalized = True
        patient.disposition = "hospitalization"
        patient.departure_time = self.env.now

        yield self.env.timeout(1)

    def disposition(self, patient: Patient):
        """Determine the patient's final clinical disposition."""

        ...

    def requires_hospitalization(
        rng: random.Random,
    ) -> bool:
        """Determine whether the patient requires hospital admission."""

        ...
