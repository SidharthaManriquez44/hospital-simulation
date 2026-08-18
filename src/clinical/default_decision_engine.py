from src.clinical.decision_engine import ClinicalDecisionEngine
from src.models.disposition import Disposition
from src.models.patient import Patient
from src.business_rules.shock_rules import (
    requires_cardiac_catheterization,
    requires_surgery,
)


class DefaultClinicalDecisionEngine(ClinicalDecisionEngine):
    """Default implementation of clinical disposition decisions."""

    def assess_stability(
        self,
        patient: Patient,
    ) -> bool:
        return patient.hemodynamic_stability

    def assess_definitive_intervention(
        self,
        patient: Patient,
    ) -> Disposition | None:

        if patient.diagnosis is None:
            return None

        if requires_surgery(patient.diagnosis):
            return Disposition.OPERATING_ROOM

        if requires_cardiac_catheterization(patient.diagnosis):
            return Disposition.CARDIAC_CATHETERIZATION

        return None

    def assess_critical_support(
        self,
        patient: Patient,
    ) -> bool:
        return patient.critical_support_required

    def assess_observation_eligibility(
        self,
        patient: Patient,
    ) -> bool:
        return patient.observation_eligible

    def assess_inpatient_need(
        self,
        patient: Patient,
    ) -> bool:
        return patient.inpatient_care_need

    def determine_disposition(
        self,
        patient: Patient,
    ) -> Disposition:

        if not self.assess_stability(patient):
            return Disposition.CONTINUED_RESUSCITATION

        intervention = self.assess_definitive_intervention(patient)

        if intervention is not None:
            return intervention

        if self.assess_critical_support(patient):
            return Disposition.ICU

        if self.assess_observation_eligibility(patient):
            return Disposition.OBSERVATION

        if self.assess_inpatient_need(patient):
            return Disposition.HOSPITALIZATION

        if patient.discharge_eligible:
            return Disposition.DISCHARGE

        return Disposition.HOSPITALIZATION
