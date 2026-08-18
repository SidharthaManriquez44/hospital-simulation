from src.models.disposition import Disposition
from src.models.patient import Patient
from src.clinical.default_decision_engine import DefaultClinicalDecisionEngine
from src.models.diagnosis import Diagnosis


def test_assess_stability_returns_false_for_unstable_patient():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = False

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_stability(patient) is False


def test_assess_stability_returns_true_for_stable_patient():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_stability(patient) is True


def test_severe_tbi_requires_operating_room():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.SEVERE_TBI

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) == Disposition.OPERATING_ROOM


def test_hemorrhagic_shock_requires_operating_room():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.HEMORRHAGIC_SHOCK

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) == Disposition.OPERATING_ROOM


def test_unstable_pelvic_fracture_requires_operating_room():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.UNSTABLE_PELVIC_FRACTURE

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) == Disposition.OPERATING_ROOM


def test_acute_myocardial_infarction_requires_cardiac_catheterization():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.ACUTE_MYOCARDIAL_INFARCTION

    engine = DefaultClinicalDecisionEngine()

    assert (
        engine.assess_definitive_intervention(patient)
        == Disposition.CARDIAC_CATHETERIZATION
    )


def test_stable_patient_without_definitive_intervention_returns_none():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.MINOR_INJURY

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) is None


def test_critical_support_required_returns_true():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.critical_support_required = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_critical_support(patient) is True


def test_critical_support_not_required_returns_false():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.critical_support_required = False

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_critical_support(patient) is False


def test_observation_eligible_patient_returns_true():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.observation_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_observation_eligibility(patient) is True


def test_inpatient_need_returns_true():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_inpatient_need(patient) is True


def test_inpatient_need_returns_false():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.inpatient_care_need = False

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_inpatient_need(patient) is False


def test_unstable_patient_continues_resuscitation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = False
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.CONTINUED_RESUSCITATION


def test_definitive_intervention_precedes_critical_support():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.HEMORRHAGIC_SHOCK
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.OPERATING_ROOM


def test_critical_support_precedes_observation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.ICU


def test_observation_precedes_inpatient_care():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = True
    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.OBSERVATION


def test_inpatient_care_precedes_discharge():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = False
    patient.inpatient_care_need = True
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.HOSPITALIZATION


def test_tension_pneumothorax_requires_operating_room():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.diagnosis = Diagnosis.TENSION_PNEUMOTHORAX

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) == (
        Disposition.OPERATING_ROOM
    )


def test_patient_without_diagnosis_has_no_definitive_intervention():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    engine = DefaultClinicalDecisionEngine()

    assert engine.assess_definitive_intervention(patient) is None


def test_determine_disposition_continues_resuscitation_when_unstable():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = False

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (
        Disposition.CONTINUED_RESUSCITATION
    )


def test_determine_disposition_sends_patient_to_operating_room():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.HEMORRHAGIC_SHOCK
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (Disposition.OPERATING_ROOM)


def test_determine_disposition_sends_ami_to_cardiac_catheterization():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.diagnosis = Diagnosis.ACUTE_MYOCARDIAL_INFARCTION
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (
        Disposition.CARDIAC_CATHETERIZATION
    )


def test_determine_disposition_sends_critical_patient_to_icu():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = True
    patient.observation_eligible = True
    patient.inpatient_care_need = True
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == Disposition.ICU


def test_determine_disposition_sends_observation_eligible_patient_to_observation():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = True
    patient.inpatient_care_need = True
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (Disposition.OBSERVATION)


def test_determine_disposition_sends_patient_to_hospital():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = False
    patient.inpatient_care_need = True
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (Disposition.HOSPITALIZATION)


def test_determine_disposition_discharges_resolved_patient():
    patient = Patient(
        id=1,
        arrival_time=0.0,
    )

    patient.hemodynamic_stability = True
    patient.critical_support_required = False
    patient.observation_eligible = False
    patient.inpatient_care_need = False
    patient.discharge_eligible = True

    engine = DefaultClinicalDecisionEngine()

    assert engine.determine_disposition(patient) == (Disposition.DISCHARGE)
