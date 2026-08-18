from enum import Enum


class Disposition(str, Enum):
    """Possible patient dispositions from the emergency department."""

    CONTINUED_RESUSCITATION = "continued_resuscitation"
    OPERATING_ROOM = "operating_room"
    CARDIAC_CATHETERIZATION = "cardiac_catheterization"
    ICU = "icu"
    OBSERVATION = "observation"
    HOSPITALIZATION = "hospitalization"
    DISCHARGE = "discharge"
