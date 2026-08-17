from src.business_rules.shock_rules import (
    requires_shock_area,
)
from src.models.triage_level import TriageLevel


def test_esi_1_requires_shock_area():
    assert requires_shock_area(TriageLevel.RED) is True


def test_non_esi_1_does_not_automatically_require_shock_area():
    assert requires_shock_area(TriageLevel.ORANGE) is False
    assert requires_shock_area(TriageLevel.YELLOW) is False
    assert requires_shock_area(TriageLevel.GREEN) is False
    assert requires_shock_area(TriageLevel.BLUE) is False
