from collections import Counter

from src import config
from src.scenarios.scenarios import SCENARIO_1
from src.simulation.hospital import HospitalSimulation


def main() -> None:
    simulation = HospitalSimulation(
        scenario=SCENARIO_1,
        seed=42,
    )

    metrics = simulation.run()

    print("# Hospital Emergency Department Simulation")
    print()
    print(f"Scenario: {SCENARIO_1.name}")
    print(f"Patients arrived: {metrics.patients_arrived}")
    print(f"Patients served: {metrics.patients_served}")

    if metrics.waiting_times:
        average_waiting_time = sum(metrics.waiting_times) / len(metrics.waiting_times)

        print(f"Average waiting time: {average_waiting_time:.2f} minutes")

    if metrics.system_times:
        average_system_time = sum(metrics.system_times) / len(metrics.system_times)

        print(f"Average system time: {average_system_time:.2f} minutes")

    if metrics.triage_levels:
        triage_counts = Counter(metrics.triage_levels)
        total_triage_patients = len(metrics.triage_levels)

        print()
        print("## ESI Distribution")
        print()
        print("| ESI | Expected | Observed | Difference (pp) |")
        print("|---|---:|---:|---:|")

        for level, expected_probability in config.ESI_PROBABILITIES.items():
            observed_count = triage_counts.get(level, 0)
            observed_probability = observed_count / total_triage_patients

            difference = observed_probability - expected_probability

            print(
                f"| ESI {level.value} "
                f"| {expected_probability:.2%} "
                f"| {observed_probability:.2%} "
                f"| {difference * 100:+.2f} pp |"
            )


if __name__ == "__main__":
    main()
