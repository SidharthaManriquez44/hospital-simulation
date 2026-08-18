from abc import ABC, abstractmethod

from src.models.disposition import Disposition
from src.models.patient import Patient


class ClinicalDecisionEngine(ABC):
    """Contract for clinical disposition decisions."""

    @abstractmethod
    def assess_stability(
        self,
        patient: Patient,
    ) -> bool:
        """Determine whether the patient is hemodynamically stable."""
        ...

    @abstractmethod
    def assess_definitive_intervention(
        self,
        patient: Patient,
    ) -> Disposition | None:
        """Determine whether definitive intervention is required."""
        ...

    @abstractmethod
    def assess_critical_support(
        self,
        patient: Patient,
    ) -> bool:
        """Determine whether ICU-level support is required."""
        ...

    @abstractmethod
    def assess_observation_eligibility(
        self,
        patient: Patient,
    ) -> bool:
        """Determine whether the patient is eligible for observation."""
        ...

    @abstractmethod
    def assess_inpatient_need(
        self,
        patient: Patient,
    ) -> bool:
        """Determine whether inpatient care is required."""
        ...

    @abstractmethod
    def determine_disposition(
        self,
        patient: Patient,
    ) -> Disposition:
        """Determine the patient's final disposition."""
        ...
