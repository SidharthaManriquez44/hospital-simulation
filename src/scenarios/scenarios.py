from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Scenario:
    """Configuration of a hospital simulation scenario."""

    name: str

    # Clinical staff
    doctors: int
    r1_residents: int
    r2_residents: int
    r3_residents: int
    nurses: int
    orderlies: int

    # Administrative staff
    receptionists: int
    triage_nurses: int

    # Clinical areas
    consulting_rooms: int
    observation_beds: int
    shock_area: int

    # Emergency equipment
    resuscitation_carts: int

    # Diagnostic services
    laboratory_technicians: int
    imaging_technicians: int

    # Pharmacy
    pharmacists: int
    pharmacy_technicians: int

    # Support services
    cleaning_staff: int
    vigilance: int

    # Operational strategy
    fast_track: bool = False


SCENARIO_1_MORNING = Scenario(
    name="Scenario 1 - Current operation",
    receptionists=2,
    triage_nurses=2,
    doctors=6,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=10,
    orderlies=3,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_2_MORNING = Scenario(
    name="Scenario 2 - Increase in medical staff",
    receptionists=2,
    triage_nurses=2,
    doctors=7,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=10,
    orderlies=3,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_3_MORNING = Scenario(
    name="Scenario 3 - Fast Track",
    receptionists=2,
    triage_nurses=2,
    doctors=6,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=10,
    orderlies=3,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIO_4_MORNING = Scenario(
    name="Scenario 4 - Increase in hospital capacity",
    receptionists=2,
    triage_nurses=2,
    doctors=6,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=10,
    orderlies=3,
    consulting_rooms=3,
    observation_beds=25,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_5_MORNING = Scenario(
    name="Scenario 5 - Combined strategy",
    receptionists=2,
    triage_nurses=2,
    doctors=7,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=10,
    orderlies=3,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIO_1_AFTERNOON = Scenario(
    name="Scenario 1 - Current operation",
    receptionists=2,
    triage_nurses=2,
    doctors=5,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=8,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_2_AFTERNOON = Scenario(
    name="Scenario 2 - Increase in medical staff",
    receptionists=2,
    triage_nurses=2,
    doctors=6,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=8,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_3_AFTERNOON = Scenario(
    name="Scenario 3 - Fast Track",
    receptionists=2,
    triage_nurses=2,
    doctors=5,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=8,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIO_4_AFTERNOON = Scenario(
    name="Scenario 4 - Increase in hospital capacity",
    receptionists=2,
    triage_nurses=2,
    doctors=5,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=8,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=25,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_5_AFTERNOON = Scenario(
    name="Scenario 5 - Combined strategy",
    receptionists=2,
    triage_nurses=2,
    doctors=6,
    r1_residents=2,
    r2_residents=2,
    r3_residents=1,
    nurses=8,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=2,
    imaging_technicians=2,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIO_1_NIGHT = Scenario(
    name="Scenario 1 - Current operation",
    receptionists=1,
    triage_nurses=1,
    doctors=4,
    r1_residents=1,
    r2_residents=1,
    r3_residents=1,
    nurses=7,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=1,
    imaging_technicians=1,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_2_NIGHT = Scenario(
    name="Scenario 2 - Increase in medical staff",
    receptionists=1,
    triage_nurses=1,
    doctors=5,
    r1_residents=1,
    r2_residents=1,
    r3_residents=1,
    nurses=7,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=1,
    imaging_technicians=1,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_3_NIGHT = Scenario(
    name="Scenario 3 - Fast Track",
    receptionists=1,
    triage_nurses=1,
    doctors=4,
    r1_residents=1,
    r2_residents=1,
    r3_residents=1,
    nurses=7,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=1,
    imaging_technicians=1,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIO_4_NIGHT = Scenario(
    name="Scenario 4 - Increase in hospital capacity",
    receptionists=1,
    triage_nurses=1,
    doctors=4,
    r1_residents=1,
    r2_residents=1,
    r3_residents=1,
    nurses=7,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=25,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=1,
    imaging_technicians=1,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=False,
)

SCENARIO_5_NIGHT = Scenario(
    name="Scenario 5 - Combined strategy",
    receptionists=1,
    triage_nurses=1,
    doctors=5,
    r1_residents=1,
    r2_residents=1,
    r3_residents=1,
    nurses=7,
    orderlies=2,
    consulting_rooms=3,
    observation_beds=15,
    shock_area=3,
    resuscitation_carts=3,
    laboratory_technicians=1,
    imaging_technicians=1,
    pharmacists=1,
    pharmacy_technicians=1,
    cleaning_staff=2,
    vigilance=2,
    fast_track=True,
)

SCENARIOS_MORNING = (
    SCENARIO_1_MORNING,
    SCENARIO_2_MORNING,
    SCENARIO_3_MORNING,
    SCENARIO_4_MORNING,
    SCENARIO_5_MORNING,
)


SCENARIOS_AFTERNOON = (
    SCENARIO_1_AFTERNOON,
    SCENARIO_2_AFTERNOON,
    SCENARIO_3_AFTERNOON,
    SCENARIO_4_AFTERNOON,
    SCENARIO_5_AFTERNOON,
)

SCENARIOS_NIGHT = (
    SCENARIO_1_NIGHT,
    SCENARIO_2_NIGHT,
    SCENARIO_3_NIGHT,
    SCENARIO_4_NIGHT,
    SCENARIO_5_NIGHT,
)
