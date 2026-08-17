from src.models.triage_level import TriageLevel


def requires_attending_physician(
    level: TriageLevel,
) -> bool:
    """Determine whether attending physician involvement is required."""

    return level in (
        TriageLevel.RED,
        TriageLevel.ORANGE,
    )


def resident_can_attend(
    level: TriageLevel,
    resident_level: str,
) -> bool:
    """Determine whether a resident can attend the patient."""

    if resident_level == "R3":
        return True

    if resident_level == "R2":
        return level != TriageLevel.RED

    if resident_level == "R1":
        return level in (
            TriageLevel.GREEN,
            TriageLevel.BLUE,
        )

    return False
