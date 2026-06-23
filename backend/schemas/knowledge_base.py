from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base import EntityBase
from schemas.patient import Patient
from schemas.administrative import Provider, Organization, Insurance
from schemas.clinical import Encounter, Condition, Procedure, Medication, Allergy, Vital, LaboratoryResult, ImagingStudy, DiagnosticReport
from schemas.notes import ClinicalNote, DischargeSummary, OperativeNote, PathologyReport, ProgressNote, Referral
from schemas.document import DocumentReference
from schemas.timeline import TimelineEvent
from schemas.authorization import AuthorizationRequest

class PatientKnowledgeBase(EntityBase):
    """
    The root object representing the complete structured reality of the patient.
    """
    patient: Optional[Patient] = None
    
    # Administrative
    providers: List[Provider] = Field(default_factory=list)
    organizations: List[Organization] = Field(default_factory=list)
    insurances: List[Insurance] = Field(default_factory=list)
    
    # Clinical
    encounters: List[Encounter] = Field(default_factory=list)
    conditions: List[Condition] = Field(default_factory=list)
    procedures: List[Procedure] = Field(default_factory=list)
    medications: List[Medication] = Field(default_factory=list)
    allergies: List[Allergy] = Field(default_factory=list)
    
    # Diagnostics & Observations
    vitals: List[Vital] = Field(default_factory=list)
    laboratory_results: List[LaboratoryResult] = Field(default_factory=list)
    imaging_studies: List[ImagingStudy] = Field(default_factory=list)
    diagnostic_reports: List[DiagnosticReport] = Field(default_factory=list)
    
    # Notes
    clinical_notes: List[ClinicalNote] = Field(default_factory=list)
    progress_notes: List[ProgressNote] = Field(default_factory=list)
    operative_notes: List[OperativeNote] = Field(default_factory=list)
    pathology_reports: List[PathologyReport] = Field(default_factory=list)
    discharge_summaries: List[DischargeSummary] = Field(default_factory=list)
    referrals: List[Referral] = Field(default_factory=list)
    
    # Documents & Timeline
    documents: List[DocumentReference] = Field(default_factory=list)
    timeline: List[TimelineEvent] = Field(default_factory=list)
    
    # Authorization state
    authorization_requests: List[AuthorizationRequest] = Field(default_factory=list)
