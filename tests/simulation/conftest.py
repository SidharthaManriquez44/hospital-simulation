from dataclasses import dataclass
import random

import simpy
import pytest

from src.models.patient import Patient
from src.models.triage_level import TriageLevel
from src.clinical.decision_engine import ClinicalDecisionEngine
from src.clinical.default_decision_engine import (
    DefaultClinicalDecisionEngine,
)
from src.resources.resources import HospitalResources
from src.scenarios.scenarios import SCENARIO_1_MORNING, Scenario
from src.simulation.metrics import SimulationMetrics
from src.simulation.processes import HospitalProcesses


@dataclass
class HospitalTestContext:
    env: simpy.Environment
    scenario: Scenario
    resources: HospitalResources
    metrics: SimulationMetrics
    rng: random.Random
    clinical_decision_engine: ClinicalDecisionEngine
    processes: HospitalProcesses


@pytest.fixture
def hospital_processes():
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    clinical_decision_engine = DefaultClinicalDecisionEngine()

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
        clinical_decision_engine=clinical_decision_engine,
    )

    return processes


@pytest.fixture
def hospital_context() -> HospitalTestContext:
    env = simpy.Environment()

    scenario = SCENARIO_1_MORNING

    resources = HospitalResources(
        env=env,
        scenario=scenario,
    )

    metrics = SimulationMetrics()

    rng = random.Random(42)

    clinical_decision_engine = DefaultClinicalDecisionEngine()

    processes = HospitalProcesses(
        env=env,
        resources=resources,
        metrics=metrics,
        rng=rng,
        scenario=scenario,
        clinical_decision_engine=clinical_decision_engine,
    )

    return HospitalTestContext(
        env=env,
        scenario=scenario,
        resources=resources,
        metrics=metrics,
        rng=rng,
        clinical_decision_engine=clinical_decision_engine,
        processes=processes,
    )


@pytest.fixture
def create_patient():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.triage_level = TriageLevel.YELLOW

    return patient
