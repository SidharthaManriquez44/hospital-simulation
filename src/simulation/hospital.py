import random

import simpy

from src import config
from src.clinical.default_decision_engine import (
    DefaultClinicalDecisionEngine,
)
from src.models.patient import Patient
from src.resources.resources import HospitalResources
from src.scenarios.scenarios import Scenario
from src.simulation.metrics import SimulationMetrics
from src.simulation.processes import HospitalProcesses


class HospitalSimulation:
    """Discrete-event simulation of the hospital emergency department."""

    def __init__(
        self,
        scenario: Scenario,
        seed: int = 42,
    ) -> None:
        self.scenario = scenario
        self.seed = seed

        self.env = simpy.Environment()
        self.rng = random.Random(seed)

        self.metrics = SimulationMetrics()

        self.resources = HospitalResources(
            env=self.env,
            scenario=scenario,
        )

        self.clinical_decision_engine = DefaultClinicalDecisionEngine()

        self.processes = HospitalProcesses(
            env=self.env,
            resources=self.resources,
            metrics=self.metrics,
            rng=self.rng,
            scenario=scenario,
            clinical_decision_engine=self.clinical_decision_engine,
        )

        self.patient_id = 0

    def run(self) -> SimulationMetrics:
        """Run the simulation and return the collected metrics."""

        self.env.process(self.patient_generator())

        self.env.run(until=config.SIMULATION_TIME)

        return self.metrics

    def patient_generator(self):
        """Generate patients according to the configured arrival process."""

        while True:
            interarrival_time = self.rng.expovariate(1 / config.MEAN_INTERARRIVAL_TIME)

            yield self.env.timeout(interarrival_time)

            self.patient_id += 1

            patient = Patient(
                id=self.patient_id,
                arrival_time=self.env.now,
            )

            self.metrics.patients_arrived += 1

            self.env.process(self.processes.patient_process(patient))
