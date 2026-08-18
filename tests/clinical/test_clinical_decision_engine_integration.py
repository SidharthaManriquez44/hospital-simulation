from src.clinical.default_decision_engine import (
    DefaultClinicalDecisionEngine,
)
from src.models.disposition import Disposition
from src.models.diagnosis import Diagnosis
from src.models.patient import Patient


## paciente estable con soporte crítico → UCI.
def test_clinical_decision_engine_integrates_patient_state_and_disposition():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True
    patient.discharge_eligible = False

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.ICU


## Inestable → continúa reanimación
def test_integration_unstable_patient_continues_resuscitation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = False

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.CONTINUED_RESUSCITATION


## IAM → hemodinamia


def test_integration_ami_patient_goes_to_cardiac_catheterization():
    patient = Patient(
        id=2,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.ACUTE_MYOCARDIAL_INFARCTION

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.CARDIAC_CATHETERIZATION


## Paciente estable elegible para observación
def test_integration_stable_patient_goes_to_observation():
    patient = Patient(
        id=3,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = True
    patient.inpatient_care_need = False
    patient.discharge_eligible = False

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.OBSERVATION


## Paciente estable que necesita hospitalización
def test_integration_patient_goes_to_hospitalization():
    patient = Patient(
        id=4,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = False
    patient.inpatient_care_need = True
    patient.discharge_eligible = False

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.HOSPITALIZATION


## Paciente resuelto → alta
def test_integration_resolved_patient_is_discharged():
    patient = Patient(
        id=5,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = False
    patient.inpatient_care_need = False
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    disposition = engine.determine_disposition(patient)

    assert disposition == Disposition.DISCHARGE
