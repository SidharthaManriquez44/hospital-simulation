import simpy


class HospitalResources:
    """Resources available in the hospital emergency department."""

    def __init__(
        self,
        env: simpy.Environment,
        receptionists: int,
        triage_nurses: int,
        nurses: int,
        doctors: int,
        consulting_rooms: int,
        # laboratory_technicians: int = 0,
        # pharmacy_staff: int = 0,
        shock_area: int = 0,
        # imaging_technicians: int = 0,
        # observation_beds: int = 0,
    ) -> None:
        self.receptionists = simpy.Resource(
            env,
            capacity=receptionists,
        )

        self.triage_nurses = simpy.Resource(
            env,
            capacity=triage_nurses,
        )

        self.nurses = simpy.Resource(
            env,
            capacity=nurses,
        )

        self.doctors = simpy.PriorityResource(
            env,
            capacity=doctors,
        )

        self.consulting_rooms = simpy.Resource(
            env,
            capacity=consulting_rooms,
        )

        """
        self.laboratory_technicians = simpy.Resource(
            env,
            capacity=laboratory_technicians,
        )

         self.shock_area = simpy.Resource(
            env,
            capacity=shock_area,
        )

        self.pharmacy_staff = simpy.Resource(
            env,
            capacity=pharmacy_staff,
        )

        self.imaging_technicians = simpy.Resource(
            env,
            capacity=imaging_technicians,
        )

        self.observation_beds = simpy.Resource(
            env,
            capacity=observation_beds,
        ) """
