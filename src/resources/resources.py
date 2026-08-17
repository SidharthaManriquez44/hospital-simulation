import simpy

from src.scenarios.scenarios import Scenario


class HospitalResources:
    """Resources available in the hospital emergency department."""

    def __init__(
        self,
        env: simpy.Environment,
        scenario: Scenario,
    ) -> None:
        self.env = env
        self.scenario = scenario

        # -------------------------
        # Administrative staff
        # -------------------------

        self.receptionists = simpy.Resource(
            env,
            capacity=scenario.receptionists,
        )

        # -------------------------
        # Triage
        # -------------------------

        self.triage_nurses = simpy.Resource(
            env,
            capacity=scenario.triage_nurses,
        )

        # -------------------------
        # Clinical staff
        # -------------------------

        self.doctors = simpy.Resource(
            env,
            capacity=scenario.doctors,
        )

        self.nurses = simpy.Resource(
            env,
            capacity=scenario.nurses,
        )

        self.orderlies = simpy.Resource(
            env,
            capacity=scenario.orderlies,
        )

        self.r1_residents = simpy.Resource(
            env,
            capacity=scenario.r1_residents,
        )

        self.r2_residents = simpy.Resource(
            env,
            capacity=scenario.r2_residents,
        )

        self.r3_residents = simpy.Resource(
            env,
            capacity=scenario.r3_residents,
        )

        # -------------------------
        # Clinical areas
        # -------------------------

        self.consulting_rooms = simpy.Resource(
            env,
            capacity=scenario.consulting_rooms,
        )

        self.observation_beds = simpy.Resource(
            env,
            capacity=scenario.observation_beds,
        )

        self.shock_area = simpy.Resource(
            env,
            capacity=scenario.shock_area,
        )

        # -------------------------
        # Diagnostic services
        # -------------------------

        self.laboratory_technicians = simpy.Resource(
            env,
            capacity=scenario.laboratory_technicians,
        )

        self.imaging_technicians = simpy.Resource(
            env,
            capacity=scenario.imaging_technicians,
        )

        # -------------------------
        # Pharmacy
        # -------------------------

        self.pharmacists = simpy.Resource(
            env,
            capacity=scenario.pharmacists,
        )

        self.pharmacy_technicians = simpy.Resource(
            env,
            capacity=scenario.pharmacy_technicians,
        )

        # -------------------------
        # Emergency equipment
        # -------------------------

        self.resuscitation_carts = simpy.Resource(
            env,
            capacity=scenario.resuscitation_carts,
        )

        # -------------------------
        # Support services
        # -------------------------

        self.cleaning_staff = simpy.Resource(
            env,
            capacity=scenario.cleaning_staff,
        )

        self.vigilance = simpy.Resource(
            env,
            capacity=scenario.vigilance,
        )
