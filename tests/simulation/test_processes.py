import pytest
import random

import simpy

from src.business_rules.treatment_rules import determine_medication_route
from src.models.medication_category import MedicationCategory
from src.models.medication_route import MedicationRoute
from src.models.patient_status import PatientStatus
from src.models.patient import Patient
from src.resources.resources import HospitalResources
from src.scenarios.scenarios import SCENARIO_1_MORNING
from src.simulation.metrics import SimulationMetrics
from src.simulation.processes import HospitalProcesses
from src.models.triage_level import TriageLevel


def test_consultation_uses_doctor_and_consulting_room(monkeypatch):
    env = simpy.Environment()
    metrics = SimulationMetrics()

    resources = HospitalResources(
        env=env,
        scenario=SCENARIO_1_MORNING,
    )

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=random.Random(42),
        scenario=SCENARIO_1_MORNING,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.triage_end = 0.0

    def fake_diagnostic_evaluation(patient):
        """Stop the test after the initial consultation."""
        if False:
            yield

    monkeypatch.setattr(
        processes,
        "diagnostic_evaluation",
        fake_diagnostic_evaluation,
    )

    env.process(processes.consultation(patient))

    env.run()

    assert patient.consultation_start is not None
    assert patient.consultation_end is not None


def test_consultation_releases_doctor_and_room(monkeypatch):
    env = simpy.Environment()
    metrics = SimulationMetrics()

    resources = HospitalResources(
        env=env,
        scenario=SCENARIO_1_MORNING,
    )

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=random.Random(42),
        scenario=SCENARIO_1_MORNING,
    )

    patient_1 = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient_1.triage_end = 0.0

    patient_2 = Patient(
        id=2,
        arrival_time=0.0,
    )

    patient_2.triage_end = 0.0

    def fake_diagnostic_evaluation(patient):
        if False:
            yield

    monkeypatch.setattr(
        processes,
        "diagnostic_evaluation",
        fake_diagnostic_evaluation,
    )

    env.process(processes.consultation(patient_1))

    env.run()

    assert resources.doctors.count == 0
    assert resources.consulting_rooms.count == 0

    env.process(processes.consultation(patient_2))

    env.run()

    assert patient_2.consultation_start is not None


def create_processes():
    env = simpy.Environment()
    metrics = SimulationMetrics()

    resources = HospitalResources(
        env=env,
        scenario=SCENARIO_1_MORNING,
    )

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=random.Random(42),
        scenario=SCENARIO_1_MORNING,
    )

    return env, processes


def create_patient():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.triage_level = TriageLevel.YELLOW

    return patient


def test_diagnostic_evaluation_without_studies(monkeypatch):
    env, processes = create_processes()
    patient = create_patient()

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_laboratory",
        lambda level, rng: False,
    )

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_imaging",
        lambda level, rng: False,
    )

    env.process(processes.diagnostic_evaluation(patient))

    env.run()

    assert patient.requires_laboratory is False
    assert patient.imaging_required is False


def test_diagnostic_evaluation_with_laboratory(monkeypatch):
    env, processes = create_processes()
    patient = create_patient()

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_laboratory",
        lambda level, rng: True,
    )

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_imaging",
        lambda level, rng: False,
    )

    env.process(processes.diagnostic_evaluation(patient))

    env.run()

    assert patient.requires_laboratory is True
    assert patient.imaging_required is False
    assert patient.laboratory_end is not None


def test_diagnostic_evaluation_with_imaging(monkeypatch):
    env, processes = create_processes()
    patient = create_patient()

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_laboratory",
        lambda level, rng: False,
    )

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_imaging",
        lambda level, rng: True,
    )

    env.process(processes.diagnostic_evaluation(patient))

    env.run()

    assert patient.requires_laboratory is False
    assert patient.imaging_required is True
    assert patient.imaging_modality in {
        "xray",
        "ct",
        "ultrasound",
        "mri",
    }

    assert patient.imaging_end is not None


def test_diagnostic_evaluation_with_laboratory_and_imaging(
    monkeypatch,
):
    env, processes = create_processes()
    patient = create_patient()

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_laboratory",
        lambda level, rng: True,
    )

    monkeypatch.setattr(
        "src.simulation.processes.physician_orders_imaging",
        lambda level, rng: True,
    )

    env.process(processes.diagnostic_evaluation(patient))

    env.run()

    assert patient.requires_laboratory is True
    assert patient.imaging_required is True

    assert patient.laboratory_end is not None
    assert patient.imaging_end is not None


def test_diagnosis_uses_eligible_resident(monkeypatch):
    env, processes = create_processes()
    patient = create_patient()

    patient.triage_level = TriageLevel.GREEN

    env.process(processes.diagnosis(patient))

    env.run()

    assert patient.diagnosis_confirmed is True
    assert patient.status == PatientStatus.DIAGNOSIS


def test_diagnosis_uses_available_eligible_resident():
    env, processes = create_processes()
    patient = create_patient()

    patient.triage_level = TriageLevel.GREEN

    r1_request = processes.resources.r1_residents.request()

    env.process(processes.diagnosis(patient))

    env.run()

    assert patient.diagnosis_confirmed is True

    processes.resources.r1_residents.release(r1_request)


def test_diagnosis_esi_2_uses_r2_or_r3():
    env, processes = create_processes()

    patient = create_patient()
    patient.triage_level = TriageLevel.ORANGE

    env.process(processes.diagnosis(patient))

    env.run()

    assert patient.diagnosis_confirmed is True


def test_diagnosis_esi_1_uses_r3():
    env, processes = create_processes()

    patient = create_patient()
    patient.triage_level = TriageLevel.RED

    env.process(processes.diagnosis(patient))

    env.run()

    assert patient.diagnosis_confirmed is True


def test_administer_medication_uses_nurse():
    env, processes = create_processes()
    patient = create_patient()

    process = env.process(
        processes.administer_medication(
            patient,
            "oral",
        )
    )

    env.run()

    assert process.triggered
    assert patient.medication_route == "oral"
    assert patient.medication_administration_start is not None
    assert patient.medication_administration_end is not None


def test_administer_medication_duration_is_valid():
    env, processes = create_processes()
    patient = create_patient()

    env.process(
        processes.administer_medication(
            patient,
            "iv_bolus",
        )
    )

    env.run()

    duration = (
        patient.medication_administration_end - patient.medication_administration_start
    )

    assert 3 <= duration <= 10


def test_administer_medication_rejects_invalid_route():
    env, processes = create_processes()
    patient = create_patient()

    env.process(
        processes.administer_medication(
            patient,
            "invalid_route",
        )
    )

    with pytest.raises(ValueError):
        env.run()


def test_pharmacy_validation_uses_pharmacist():
    env, processes = create_processes()
    patient = create_patient()

    env.process(processes.pharmacy_validation(patient))

    env.run()

    assert patient.pharmacy_validation_start is not None
    assert patient.pharmacy_validation_end is not None

    duration = patient.pharmacy_validation_end - patient.pharmacy_validation_start

    assert 1 <= duration <= 7


def test_pharmacy_preparation_uses_pharmacy_technician():
    env, processes = create_processes()
    patient = create_patient()

    env.process(processes.pharmacy_preparation(patient))

    env.run()

    assert patient.pharmacy_preparation_start is not None
    assert patient.pharmacy_preparation_end is not None

    duration = patient.pharmacy_preparation_end - patient.pharmacy_preparation_start

    assert 3 <= duration <= 12


def test_pharmacy_distribution_has_valid_duration():
    env, processes = create_processes()
    patient = create_patient()

    env.process(processes.pharmacy_distribution(patient))

    env.run()

    duration = patient.pharmacy_distribution_end - patient.pharmacy_distribution_start

    assert 1 <= duration <= 6


def test_analgesia_route_distribution():
    rng = random.Random(42)

    routes = [
        determine_medication_route(
            MedicationCategory.ANALGESIA,
            rng,
        )
        for _ in range(10_000)
    ]

    oral_probability = routes.count(MedicationRoute.ORAL) / len(routes)

    assert 0.60 <= oral_probability <= 0.64


def test_antibiotic_route_is_iv_infusion():
    rng = random.Random(42)

    for _ in range(100):
        route = determine_medication_route(
            MedicationCategory.ANTIBIOTIC,
            rng,
        )

        assert route == MedicationRoute.IV_INFUSION


def test_anticoagulation_route_distribution():
    rng = random.Random(42)

    routes = [
        determine_medication_route(
            MedicationCategory.ANTICOAGULATION,
            rng,
        )
        for _ in range(10_000)
    ]

    sc_probability = routes.count(MedicationRoute.IM_SC) / len(routes)

    assert 0.58 <= sc_probability <= 0.62


def test_treatment_to_medication_administration_flow(monkeypatch):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    monkeypatch.setattr(
        "src.simulation.processes.requires_medication",
        lambda rng: True,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_medication_category",
        lambda rng: MedicationCategory.ANTIBIOTIC,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_medication_route",
        lambda category, rng: MedicationRoute.IV_INFUSION,
    )

    monkeypatch.setattr(
        "src.simulation.processes.requires_pharmacy_preparation",
        lambda category, rng: True,
    )

    env.process(processes.treatment(patient))

    env.run()

    assert patient.medication_category == (MedicationCategory.ANTIBIOTIC)

    assert patient.medication_route == (MedicationRoute.IV_INFUSION)

    assert patient.pharmacy_preparation_required is True

    assert patient.pharmacy_validation_start is not None
    assert patient.pharmacy_validation_end is not None

    assert patient.pharmacy_preparation_start is not None
    assert patient.pharmacy_preparation_end is not None

    assert patient.pharmacy_distribution_start is not None
    assert patient.pharmacy_distribution_end is not None

    assert patient.medication_administration_start is not None
    assert patient.medication_administration_end is not None
    assert patient.pharmacy_validation_end <= patient.pharmacy_preparation_start

    assert patient.pharmacy_preparation_end <= patient.pharmacy_distribution_start

    assert patient.pharmacy_distribution_end <= patient.medication_administration_start


def test_treatment_to_medication_administration_flow_is_none(monkeypatch):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    monkeypatch.setattr(
        "src.simulation.processes.requires_medication",
        lambda rng: True,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_medication_category",
        lambda rng: MedicationCategory.ANTIBIOTIC,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_medication_route",
        lambda category, rng: MedicationRoute.IV_INFUSION,
    )

    monkeypatch.setattr(
        "src.simulation.processes.requires_pharmacy_preparation",
        lambda category, rng: False,
    )

    env.process(processes.treatment(patient))

    env.run()
    assert patient.pharmacy_preparation_start is None
    assert patient.pharmacy_preparation_end is None

    assert patient.pharmacy_validation_start is not None
    assert patient.pharmacy_validation_end is not None

    assert patient.pharmacy_distribution_start is not None
    assert patient.pharmacy_distribution_end is not None

    assert patient.medication_administration_start is not None
    assert patient.medication_administration_end is not None

    assert patient.pharmacy_validation_end <= patient.pharmacy_distribution_start
    assert patient.pharmacy_distribution_end <= patient.medication_administration_start


def test_observation_records_observation_times(monkeypatch):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )

    monkeypatch.setattr(
        "src.simulation.processes.deteriorates_in_observation",
        lambda level, rng: False,
    )

    env.process(processes.observation(patient))
    env.run()

    assert patient.observation_start is not None
    assert patient.observation_end is not None

    observation_duration = patient.observation_end - patient.observation_start

    assert 480 <= observation_duration <= 1440


def test_observation_deterioration_occurs_in_observation_area(
    monkeypatch,
):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )

    monkeypatch.setattr(
        "src.simulation.processes.deteriorates_in_observation",
        lambda level, rng: True,
    )

    env.process(processes.observation_deterioration(patient))

    env.run()

    assert patient.current_area == "observation"

    assert patient.clinical_status == "deteriorating"

    assert patient.deceased is False


def test_observation_deterioration_results_in_death_without_rosc(
    monkeypatch,
):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )
    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )
    monkeypatch.setattr(
        "src.simulation.processes.resuscitation_achieves_rosc",
        lambda rng: False,
    )
    env.process(processes.observation(patient))
    env.run()

    assert patient.deceased is True
    assert patient.status == PatientStatus.DECEASED
    assert patient.clinical_status == "deceased"
    assert patient.departure_time is not None


def test_observation_deterioration_transfers_patient_after_rosc(
    monkeypatch,
):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )
    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )
    monkeypatch.setattr(
        "src.simulation.processes.resuscitation_achieves_rosc",
        lambda rng: True,
    )
    env.process(processes.observation(patient))
    env.run()

    assert patient.deceased is False
    assert patient.shock_stabilized is True
    assert patient.clinical_status == "stabilized"
    assert patient.hospitalized is True
    assert patient.disposition == "hospitalization"
    assert patient.departure_time is not None


def test_observation_ends_with_follow_up(
    monkeypatch,
):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )

    monkeypatch.setattr(
        "src.simulation.processes.deteriorates_in_observation",
        lambda level, rng: False,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_observation_disposition",
        lambda rng: "follow_up",
    )

    env.process(processes.observation(patient))
    env.run()

    assert patient.disposition == "follow_up"

    assert patient.outpatient_referral is True
    assert patient.hospitalized is False
    assert patient.departure_time is not None


def test_observation_ends_hospitalization(
    monkeypatch,
):
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
    )

    patient = Patient(
        id=1,
        arrival_time=0.0,
        triage_level=TriageLevel.YELLOW,
    )

    monkeypatch.setattr(
        "src.simulation.processes.deteriorates_in_observation",
        lambda level, rng: False,
    )

    monkeypatch.setattr(
        "src.simulation.processes.determine_observation_disposition",
        lambda rng: "hospitalization",
    )

    env.process(processes.observation(patient))
    env.run()

    assert patient.disposition == "hospitalization"

    assert patient.hospitalized is True
    assert patient.outpatient_referral is False
    assert patient.departure_time is not None
