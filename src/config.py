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
