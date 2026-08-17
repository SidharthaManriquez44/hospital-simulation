from src.models.triage_level import TriageLevel
from src.models.medication_category import MedicationCategory


"""
Global configuration for the hospital simulation.
"""

# -----------------------------------------------------------------------------
# Simulation
# -----------------------------------------------------------------------------

SIMULATION_DAYS = 31
WARMUP_DAYS = 1

MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR

SIMULATION_TIME = SIMULATION_DAYS * MINUTES_PER_DAY
WARMUP_TIME = WARMUP_DAYS * MINUTES_PER_DAY

REPLICATIONS = 30


# -----------------------------------------------------------------------------
# Hospital resources (Scenario 1 - Base)
# -----------------------------------------------------------------------------

RECEPTIONISTS = 2
TRIAGE_NURSES = 2
DOCTORS = 3

CONSULTING_ROOMS = 3
OBSERVATION_BEDS = 15


# -----------------------------------------------------------------------------
# Patient arrivals
# -----------------------------------------------------------------------------

MEAN_INTERARRIVAL_TIME = 8.0  # minutes


# -----------------------------------------------------------------------------
# Process durations (minutes)
# -----------------------------------------------------------------------------

REGISTRATION_MIN = 3
REGISTRATION_MAX = 7

TRIAGE_MIN = 5
TRIAGE_MODE = 8
TRIAGE_MAX = 12

CONSULTATION_MEAN = 20
CONSULTATION_STD = 5

# -----------------------------------------------------------------------------
# ESI distribution
# -----------------------------------------------------------------------------

ESI_PROBABILITIES = {
    TriageLevel.RED: 0.03,
    TriageLevel.ORANGE: 0.05,
    TriageLevel.YELLOW: 0.42,
    TriageLevel.GREEN: 0.42,
    TriageLevel.BLUE: 0.08,
}

# -----------------------------------------------------------------------------
# Laboratory request probability by ESI
# -----------------------------------------------------------------------------

LABORATORY_PROBABILITIES = {
    TriageLevel.RED: 0.95,
    TriageLevel.ORANGE: 0.76,
    TriageLevel.YELLOW: 0.55,
    TriageLevel.GREEN: 0.15,
    TriageLevel.BLUE: 0.02,
}

# -----------------------------------------------------------------------------
# Laboratory
# -----------------------------------------------------------------------------

LABORATORY_SAMPLE_MIN = 3
LABORATORY_SAMPLE_MODE = 5
LABORATORY_SAMPLE_MAX = 10

LABORATORY_TRANSPORT_MIN = 15
LABORATORY_TRANSPORT_MODE = 22
LABORATORY_TRANSPORT_MAX = 35

LABORATORY_PROCESSING_MIN = 20
LABORATORY_PROCESSING_MODE = 30
LABORATORY_PROCESSING_MAX = 45

# -----------------------------------------------------------------------------
# Imaging
# -----------------------------------------------------------------------------
IMAGING_PROBABILITIES = {
    TriageLevel.RED: 0.80,
    TriageLevel.ORANGE: 0.75,
    TriageLevel.YELLOW: 0.60,
    TriageLevel.GREEN: 0.25,
    TriageLevel.BLUE: 0.00,
}

IMAGING_MODALITY_PROBABILITIES = {
    "xray": 0.583,
    "ct": 0.305,
    "ultrasound": 0.066,
    "mri": 0.046,
}

# -----------------------------------------------------------------------------
# Imaging duration parameters
# -----------------------------------------------------------------------------

XRAY_MIN = 25
XRAY_MODE = 41
XRAY_MAX = 83

CT_MIN = 42
CT_MODE = 67
CT_MAX = 142

ULTRASOUND_MIN = 30
ULTRASOUND_MODE = 48
ULTRASOUND_MAX = 84

MRI_MIN = 108
MRI_MODE = 156
MRI_MAX = 222

IMAGING_DURATION_PARAMETERS = {
    "xray": (
        XRAY_MIN,
        XRAY_MODE,
        XRAY_MAX,
    ),
    "ct": (
        CT_MIN,
        CT_MODE,
        CT_MAX,
    ),
    "ultrasound": (
        ULTRASOUND_MIN,
        ULTRASOUND_MODE,
        ULTRASOUND_MAX,
    ),
    "mri": (
        MRI_MIN,
        MRI_MODE,
        MRI_MAX,
    ),
}

# -----------------------------------------------------------------------------
# Fast Track
# -----------------------------------------------------------------------------

FAST_TRACK_CONSULTATION_FACTOR = 0.50

# -----------------------------------------------------------------------------
# Treatment
# -----------------------------------------------------------------------------

MEDICATION_PROBABILITY = 0.774

# -----------------------------------------------------------------------------
# Medication administration duration parameters
# -----------------------------------------------------------------------------

MEDICATION_ORAL_MIN = 2
MEDICATION_ORAL_MODE = 5
MEDICATION_ORAL_MAX = 8

MEDICATION_IM_SC_MIN = 2
MEDICATION_IM_SC_MODE = 5
MEDICATION_IM_SC_MAX = 8

MEDICATION_IV_BOLUS_MIN = 3
MEDICATION_IV_BOLUS_MODE = 6
MEDICATION_IV_BOLUS_MAX = 10

MEDICATION_IV_INFUSION_MIN = 5
MEDICATION_IV_INFUSION_MODE = 12
MEDICATION_IV_INFUSION_MAX = 20

MEDICATION_CRITICAL_MIN = 1
MEDICATION_CRITICAL_MODE = 3
MEDICATION_CRITICAL_MAX = 5

# -----------------------------------------------------------------------------
# Pharmacy
# -----------------------------------------------------------------------------

PHARMACY_VALIDATION_MIN = 1
PHARMACY_VALIDATION_MODE = 4
PHARMACY_VALIDATION_MAX = 7

PHARMACY_PREPARATION_MIN = 3
PHARMACY_PREPARATION_MODE = 7
PHARMACY_PREPARATION_MAX = 12

PHARMACY_DISTRIBUTION_MIN = 1
PHARMACY_DISTRIBUTION_MODE = 3
PHARMACY_DISTRIBUTION_MAX = 6

# -----------------------------------------------------------------------------
# Medication category weights
# -----------------------------------------------------------------------------

MEDICATION_CATEGORY_WEIGHTS = {
    "analgesia": 22.80,
    "antibiotic": 5.40,
    "antiemetic": 9.60,
    "bronchodilator": 3.20,
    "antiplatelet": 1.70,
    "insulin_glucose": 1.30,
}

# -----------------------------------------------------------------------------
# Pharmacy probabilities
# -----------------------------------------------------------------------------

PHARMACY_PREPARATION_PROBABILITIES = {
    MedicationCategory.ANALGESIA: 0.10,
    MedicationCategory.ANTIBIOTIC: 0.30,
    MedicationCategory.ANTIEMETIC: 0.05,
    MedicationCategory.BRONCHODILATOR: 0.02,
    MedicationCategory.ANTICOAGULATION: 0.30,
    MedicationCategory.ANTIPLATELET: 0.05,
    MedicationCategory.VASOPRESSOR: 0.80,
    MedicationCategory.INSULIN_GLUCOSE: 0.25,
    MedicationCategory.OTHER: 0.15,
}

# -----------------------------------------------------------------------------
# Observation
# -----------------------------------------------------------------------------

OBSERVATION_GLOBAL_PROBABILITY = 0.025

OBSERVATION_MIN = 480
OBSERVATION_MODE = 1080
OBSERVATION_MAX = 1440

OBSERVATION_FOLLOW_UP_PROBABILITY = 0.64
OBSERVATION_HOSPITALIZATION_PROBABILITY = 0.36

OBSERVATION_DETERIORATION_PROBABILITIES = {
    TriageLevel.RED: 0.25,
    TriageLevel.ORANGE: 0.18,
    TriageLevel.YELLOW: 0.11,
    TriageLevel.GREEN: 0.05,
    TriageLevel.BLUE: 0.015,
}

OBSERVATION_GLOBAL_DETERIORATION_REFERENCE = 0.10

RESUSCITATION_ROSC_PROBABILITY = 0.30

# -----------------------------------------------------------------------------
# Shock
# -----------------------------------------------------------------------------

SHOCK_MIN = 20
SHOCK_MODE = 50
SHOCK_MAX = 120

SHOCK_TO_OBSERVATION_PROBABILITY = 0.20
