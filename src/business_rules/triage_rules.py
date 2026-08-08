from enum import IntEnum


class TriageLevel(IntEnum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5


def get_priority(level: TriageLevel) -> int:
    return level.value


def determine_next_area(triage_level):
    if triage_level == TriageLevel.RED:
        return "shock_area"

    if triage_level == TriageLevel.ORANGE:
        return "consultation"

    if triage_level == TriageLevel.YELLOW:
        return "consultation"

    return "waiting_room"
