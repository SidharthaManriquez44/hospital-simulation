import simpy

from src.resources.resources import HospitalResources
from src.scenarios.scenarios import SCENARIO_1_MORNING


def test_resources_use_scenario_capacity():
    env = simpy.Environment()

    resources = HospitalResources(
        env=env,
        scenario=SCENARIO_1_MORNING,
    )

    assert resources.receptionists.capacity == 2
    assert resources.triage_nurses.capacity == 2
    assert resources.doctors.capacity == 6
    assert resources.nurses.capacity == 10
    assert resources.orderlies.capacity == 3

    assert resources.consulting_rooms.capacity == 3
    assert resources.observation_beds.capacity == 15
    assert resources.shock_area.capacity == 3

    assert resources.resuscitation_carts.capacity == 3

    assert resources.laboratory_technicians.capacity == 2
    assert resources.imaging_technicians.capacity == 2

    assert resources.pharmacists.capacity == 1
    assert resources.pharmacy_technicians.capacity == 1
