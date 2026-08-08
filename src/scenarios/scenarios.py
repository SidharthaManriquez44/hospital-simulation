from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Scenario:
    """Configuration of a hospital simulation scenario."""

    name: str
    doctors: int
    nurses: int
    receptionists: int
    triage_nurses: int
    consulting_rooms: int
    observation_beds: int
    laboratory_technicians: int
    imaging_technicians: int
    fast_track: bool = False
    additional_beds: int = 0


SCENARIO_1 = Scenario(
    name="Escenario 1 - Operación actual",
    receptionists=2,
    triage_nurses=2,
    doctors=3,
    nurses=15,
    consulting_rooms=3,
    observation_beds=15,
    laboratory_technicians=2,
    imaging_technicians=2,
    fast_track=False,
)

SCENARIO_2 = Scenario(
    name="Escenario 2 - Incremento de personal médico",
    receptionists=2,
    triage_nurses=2,
    doctors=4,
    nurses=15,
    consulting_rooms=3,
    observation_beds=15,
    laboratory_technicians=2,
    imaging_technicians=2,
    fast_track=False,
)

SCENARIO_3 = Scenario(
    name="Escenario 3 - Fast Track",
    receptionists=2,
    triage_nurses=2,
    doctors=3,
    nurses=15,
    consulting_rooms=3,
    observation_beds=15,
    laboratory_technicians=2,
    imaging_technicians=2,
    fast_track=True,
)

SCENARIO_4 = Scenario(
    name="Escenario 4 - Incremento de capacidad hospitalaria",
    receptionists=2,
    triage_nurses=2,
    doctors=3,
    nurses=15,
    consulting_rooms=3,
    observation_beds=25,
    laboratory_technicians=2,
    imaging_technicians=2,
    fast_track=False,
)

SCENARIO_5 = Scenario(
    name="Escenario 5 - Estrategia combinada",
    receptionists=2,
    triage_nurses=2,
    doctors=4,
    nurses=15,
    consulting_rooms=3,
    observation_beds=15,
    laboratory_technicians=2,
    imaging_technicians=2,
    fast_track=True,
)

SCENARIOS = (
    SCENARIO_1,
    SCENARIO_2,
    SCENARIO_3,
    SCENARIO_4,
    SCENARIO_5,
)
