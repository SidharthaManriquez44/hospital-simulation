from src.scenarios.scenarios import (
    SCENARIO_1_MORNING,
    SCENARIO_2_MORNING,
    SCENARIO_4_MORNING,
)
from src.simulation.hospital import HospitalSimulation


def test_simulation_uses_scenario_resources():
    simulation = HospitalSimulation(
        scenario=SCENARIO_1_MORNING,
        seed=42,
    )

    resources = simulation.resources

    assert resources.doctors.capacity == 6
    assert resources.nurses.capacity == 10
    assert resources.orderlies.capacity == 3

    assert resources.consulting_rooms.capacity == 3
    assert resources.observation_beds.capacity == 15
    assert resources.shock_area.capacity == 3

    assert resources.resuscitation_carts.capacity == 3


def test_medical_staff_scenario_changes_doctors():
    simulation = HospitalSimulation(
        scenario=SCENARIO_2_MORNING,
        seed=42,
    )

    assert simulation.resources.doctors.capacity == 7


def test_hospital_capacity_scenario_changes_observation_beds():
    simulation = HospitalSimulation(
        scenario=SCENARIO_4_MORNING,
        seed=42,
    )

    assert simulation.resources.observation_beds.capacity == 25
