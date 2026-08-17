from enum import Enum


class MedicationCategory(str, Enum):
    ANALGESIA = "analgesia"
    ANTIBIOTIC = "antibiotic"
    ANTIEMETIC = "antiemetic"
    BRONCHODILATOR = "nebulization"
    ANTICOAGULATION = "anticoagulation"
    ANTIPLATELET = "antiplatelet"
    VASOPRESSOR = "vasopressor"
    INSULIN_GLUCOSE = "insulin_glucose"
    OTHER = "other"
