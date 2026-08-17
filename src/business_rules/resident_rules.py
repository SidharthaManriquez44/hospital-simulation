from src.models.triage_level import TriageLevel


def eligible_resident_levels(
    level: TriageLevel,
) -> tuple[str, ...]:
    """Return resident levels eligible to attend a patient."""

    if level == TriageLevel.RED:
        return ("R3",)

    if level == TriageLevel.ORANGE:
        return ("R2", "R3")

    return ("R1", "R2", "R3")
