from enum import Enum


class TreatmentType(str, Enum):
    MEDICATION = "medication"
    FLUID_THERAPY = "fluid_therapy"
    RESPIRATORY_THERAPY = "respiratory_therapy"
    PROCEDURE = "procedure"
