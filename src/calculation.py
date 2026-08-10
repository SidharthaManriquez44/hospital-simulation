from collections import Counter

from src import config
import numpy as np
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

        if metrics.laboratory_tat_times:
            laboratory_waiting = np.array(metrics.laboratory_waiting_times)

            laboratory_processing = np.array(metrics.laboratory_processing_times)

            laboratory_tat = np.array(metrics.laboratory_tat_times)

            laboratory_tat_without_waiting = np.array(
                metrics.laboratory_tat_without_waiting_times
            )

            print()
            print("## Laboratory")
            print()

            print(f"Laboratory requests: {len(laboratory_tat)}")

            print(
                f"Average laboratory waiting time: "
                f"{laboratory_waiting.mean():.2f} minutes"
            )

            print(
                f"Average laboratory processing time: "
                f"{laboratory_processing.mean():.2f} minutes"
            )

            print(f"Average laboratory TAT: {laboratory_tat.mean():.2f} minutes")

            print(
                f"Average laboratory TAT without waiting: "
                f"{laboratory_tat_without_waiting.mean():.2f} minutes"
            )

            p25 = np.percentile(laboratory_tat, 25)
            p50 = np.percentile(laboratory_tat, 50)
            p75 = np.percentile(laboratory_tat, 75)

            p25_without_waiting = np.percentile(
                laboratory_tat_without_waiting,
                25,
            )

            p50_without_waiting = np.percentile(
                laboratory_tat_without_waiting,
                50,
            )

            p75_without_waiting = np.percentile(
                laboratory_tat_without_waiting,
                75,
            )

            print()
            print("| Percentile | TAT sin espera | TAT observado | Reference |")
            print("|---|---:|---:|---:|")

            print(
                f"| P25 | {p25_without_waiting:.2f} min | {p25:.2f} min | 41.10 min |"
            )

            print(
                f"| P50 | {p50_without_waiting:.2f} min | {p50:.2f} min | 51.10 min |"
            )

            print(
                f"| P75 | {p75_without_waiting:.2f} min | {p75:.2f} min | 65.00 min |"
            )

            print()
            print("### Laboratory Requests by ESI")
            print()
            print("| ESI | Patients | Requests | Observed | Expected | Difference |")
            print("|---|---:|---:|---:|---:|---:|")

            for (
                triage_level,
                expected_probability,
            ) in config.LABORATORY_PROBABILITIES.items():
                key = triage_level.value

                patients = metrics.laboratory_patients_by_triage.get(
                    key,
                    0,
                )

                requests = metrics.laboratory_requests_by_triage.get(
                    key,
                    0,
                )

                observed_probability = requests / patients if patients > 0 else 0.0

                difference = observed_probability - expected_probability

                print(
                    f"| ESI {key} "
                    f"| {patients} "
                    f"| {requests} "
                    f"| {observed_probability:.2%} "
                    f"| {expected_probability:.2%} "
                    f"| {difference:+.2%} |"
                )
            print()
            print("## Imaging Requests by ESI")
            print()

            print("| ESI | Patients | Requests | Observed | Expected | Difference |")
            print("|---|---:|---:|---:|---:|---:|")

            for (
                triage_level,
                expected_probability,
            ) in config.IMAGING_PROBABILITIES.items():
                key = triage_level.value

                patients = metrics.imaging_patients_by_triage.get(
                    key,
                    0,
                )

                requests = metrics.imaging_requests_by_triage.get(
                    key,
                    0,
                )

                observed = requests / patients if patients > 0 else 0.0

                expected = expected_probability

                difference = observed - expected

                print(
                    f"| ESI {key} "
                    f"| {patients} "
                    f"| {requests} "
                    f"| {observed:.2%} "
                    f"| {expected:.2%} "
                    f"| {difference:+.2%} |"
                )

            print()
            print("## Imaging Modalities")
            print()

            print("| Modality | Requests | Observed | Expected | Difference |")
            print("|---|---:|---:|---:|---:|")

            total_imaging_requests = sum(metrics.imaging_modalities.values())

            for (
                modality,
                expected_probability,
            ) in config.IMAGING_MODALITY_PROBABILITIES.items():
                requests = metrics.imaging_modalities.get(
                    modality,
                    0,
                )

                observed = (
                    requests / total_imaging_requests
                    if total_imaging_requests > 0
                    else 0.0
                )

                expected = expected_probability

                difference = observed - expected

                print(
                    f"| {modality} "
                    f"| {requests} "
                    f"| {observed:.2%} "
                    f"| {expected:.2%} "
                    f"| {difference:+.2%} |"
                )


if __name__ == "__main__":
    main()
