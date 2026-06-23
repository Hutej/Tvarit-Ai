from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.base import EntityBase
from schemas.enums import ConditionStatus, MedicationStatus, ProcedureStatus, Severity

class Encounter(EntityBase):
    provider_id: str
    organization_id: Optional[str] = None
    date: datetime
    encounter_type: str
    chief_complaint: Optional[str] = None

class Condition(EntityBase):
    name: str
    icd10_code: Optional[str] = None
    snomed_code: Optional[str] = None
    status: ConditionStatus
    severity: Optional[Severity] = None
    onset_date: Optional[datetime] = None
    resolution_date: Optional[datetime] = None

class Diagnosis(Condition):
    diagnosed_by: Optional[str] = None

class Symptom(Condition):
    pass

class Procedure(EntityBase):
    name: str
    cpt_code: Optional[str] = None
    status: ProcedureStatus
    date: Optional[datetime] = None
    provider_id: Optional[str] = None
    outcome: Optional[str] = None

class Medication(EntityBase):
    name: str
    rxnorm_code: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    status: MedicationStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reason_for_discontinuation: Optional[str] = None

class Allergy(EntityBase):
    substance: str
    reaction: Optional[str] = None
    severity: Optional[Severity] = None

class Observation(EntityBase):
    name: str
    loinc_code: Optional[str] = None
    value: str
    unit: Optional[str] = None
    date: datetime

class Vital(Observation):
    pass

class LaboratoryResult(Observation):
    reference_range: Optional[str] = None
    is_abnormal: Optional[bool] = None

class ImagingStudy(EntityBase):
    modality: str
    body_site: str
    date: datetime
    findings: str
    impression: Optional[str] = None

class DiagnosticReport(EntityBase):
    name: str
    date: datetime
    conclusion: str
    results: List[Observation] = Field(default_factory=list)
