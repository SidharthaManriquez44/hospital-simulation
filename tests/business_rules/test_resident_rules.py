from src.business_rules.resident_rules import (
    eligible_resident_levels,
)
from src.models.triage_level import TriageLevel


def test_esi_1_requires_r3():
    assert eligible_resident_levels(TriageLevel.RED) == ("R3",)


def test_esi_2_allows_r2_and_r3():
    assert eligible_resident_levels(TriageLevel.ORANGE) == ("R2", "R3")


def test_esi_3_allows_all_resident_levels():
    assert eligible_resident_levels(TriageLevel.YELLOW) == ("R1", "R2", "R3")


def test_esi_4_allows_all_resident_levels():
    assert eligible_resident_levels(TriageLevel.GREEN) == ("R1", "R2", "R3")


def test_esi_5_allows_all_resident_levels():
    assert eligible_resident_levels(TriageLevel.BLUE) == ("R1", "R2", "R3")
