import numpy as np

from src import config
from src.scenarios.scenarios import Scenario
from src.simulation.hospital import HospitalSimulation


class ExperimentRunner:
    """Run multiple replications for a set of scenarios."""

    def __init__(
        self,
        scenarios: tuple[Scenario, ...],
        replications: int = config.REPLICATIONS,
    ) -> None:
        self.scenarios = scenarios
        self.replications = replications

    def run(self) -> list[dict]:
        """Run all scenarios and return results for every replication."""

        results = []

        for scenario in self.scenarios:
            for replication in range(1, self.replications + 1):
                simulation = HospitalSimulation(
                    scenario=scenario,
                    seed=replication,
                )

                metrics = simulation.run()

                results.append(
                    self._extract_metrics(
                        scenario=scenario,
                        replication=replication,
                        metrics=metrics,
                    )
                )

        return results

    @staticmethod
    def _extract_metrics(
        scenario: Scenario,
        replication: int,
        metrics,
    ) -> dict:
        """Extract KPI values from one replication."""

        return {
            "scenario": scenario.name,
            "replication": replication,
            "patients_arrived": metrics.patients_arrived,
            "patients_served": metrics.patients_served,
            "average_waiting_time": (
                float(np.mean(metrics.waiting_times)) if metrics.waiting_times else 0.0
            ),
            "average_system_time": (
                float(np.mean(metrics.system_times)) if metrics.system_times else 0.0
            ),
            "laboratory_requests": sum(metrics.laboratory_requests_by_triage.values()),
        }
