from enum import Enum


class MedicationRoute(str, Enum):
    ORAL = "oral"
    IM_SC = "im_sc"
    IV_BOLUS = "iv_bolus"
    IV_INFUSION = "iv_infusion"
    NEBULIZATION = "nebulization"
    CRITICAL = "critical"
