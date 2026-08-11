import numpy as np
import csv
from pathlib import Path

from src.experiments.runner import ExperimentRunner
from src.scenarios.scenarios import SCENARIOS


def main():
    print("Hospital Emergency Department Simulation")
    print("=" * 45)
    print()

    runner = ExperimentRunner(
        scenarios=SCENARIOS,
        replications=30,
    )

    results = runner.run()
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    results_file = results_dir / "scenario_results.csv"

    with results_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    print("## Scenario Comparison")
    print()

    print(
        "| Scenario | Patients Arrived | Patients Served "
        "| Avg Waiting Time | Avg System Time | "
    )
    print("|---|---:|---:|---:|---:|---:|")

    scenario_names = []

    for scenario in SCENARIOS:
        scenario_results = [
            result for result in results if result["scenario"] == scenario.name
        ]

        scenario_names.append(scenario.name)

        print(
            f"| {scenario.name} "
            f"| {np.mean([r['patients_arrived'] for r in scenario_results]):.0f} "
            f"| {np.mean([r['patients_served'] for r in scenario_results]):.0f} "
            f"| {np.mean([r['average_waiting_time'] for r in scenario_results]):.2f} min "
            f"| {np.mean([r['average_system_time'] for r in scenario_results]):.2f} min "
        )


if __name__ == "__main__":
    main()
