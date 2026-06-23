# Universal Canonical Medical Schema

This artifact contains the complete Pydantic v2 implementation of the Universal Canonical Medical Schema. It serves as the single source of truth for the entire Tvarit AI platform.

## 1. Files Created/Modified

**Files Modified (Overwritten from stubs):**
- `schemas/__init__.py`
- `schemas/patient.py`
- `schemas/document.py`
- `schemas/timeline.py`
- `schemas/insurance.py`
- `schemas/authorization.py`

**Files Created:**
- `schemas/enums.py`
- `schemas/base.py`
- `schemas/administrative.py`
- `schemas/clinical.py`
- `schemas/notes.py`
- `schemas/knowledge_base.py`

---

## 2. Complete Schema Implementation

### `schemas/enums.py`
```python
from enum import Enum

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"

class DocumentType(str, Enum):
    PRESCRIPTION = "PRESCRIPTION"
    LAB_REPORT = "LAB_REPORT"
    RADIOLOGY_REPORT = "RADIOLOGY_REPORT"
    CLINICAL_NOTE = "CLINICAL_NOTE"
    DISCHARGE_SUMMARY = "DISCHARGE_SUMMARY"
    OPERATIVE_NOTE = "OPERATIVE_NOTE"
    PATHOLOGY_REPORT = "PATHOLOGY_REPORT"
    INSURANCE_FORM = "INSURANCE_FORM"
    REFERRAL = "REFERRAL"
    OTHER = "OTHER"

class ConditionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    CHRONIC = "CHRONIC"
    UNKNOWN = "UNKNOWN"

class MedicationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISCONTINUED = "DISCONTINUED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ProcedureStatus(str, Enum):
    PROPOSED = "PROPOSED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Severity(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    UNKNOWN = "UNKNOWN"

class Priority(str, Enum):
    ROUTINE = "ROUTINE"
    URGENT = "URGENT"
    STAT = "STAT"

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class EvidenceStatus(str, Enum):
    MET = "MET"
    NOT_MET = "NOT_MET"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"

class RecommendationType(str, Enum):
    MISSING_DOCUMENT = "MISSING_DOCUMENT"
    CLINICAL_CLARIFICATION = "CLINICAL_CLARIFICATION"
    SIGNATURE_REQUIRED = "SIGNATURE_REQUIRED"
    OTHER = "OTHER"

class DecisionStatus(str, Enum):
    READY = "READY"
    NOT_READY = "NOT_READY"
    PENDING_REVIEW = "PENDING_REVIEW"
```

### `schemas/base.py`
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
import uuid
from schemas.enums import ConfidenceLevel

class Confidence(BaseModel):
    level: ConfidenceLevel = Field(default=ConfidenceLevel.HIGH)
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    reasoning: Optional[str] = None

class Provenance(BaseModel):
    source_document_id: str
    document_name: str
    page: Optional[int] = None
    bounding_box: Optional[List[float]] = None
    paragraph: Optional[str] = None
    extraction_model: str
    confidence: Confidence
    created_time: datetime = Field(default_factory=datetime.utcnow)
    updated_time: datetime = Field(default_factory=datetime.utcnow)

class Metadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1)
    tags: List[str] = Field(default_factory=list)
    custom_attributes: Dict[str, Any] = Field(default_factory=dict)

class Audit(BaseModel):
    created_by: str = Field(default="system")
    updated_by: str = Field(default="system")
    audit_log: List[str] = Field(default_factory=list)

class EntityBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provenance: List[Provenance] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)
    audit: Audit = Field(default_factory=Audit)
```

### `schemas/administrative.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base import EntityBase

class Provider(EntityBase):
    npi: Optional[str] = None
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

class Organization(EntityBase):
    name: str
    npi: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

class Coverage(EntityBase):
    group_number: Optional[str] = None
    plan_name: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None

class Insurance(EntityBase):
    payer_name: str
    payer_id: Optional[str] = None
    policy_number: str
    coverage: Optional[Coverage] = None
    subscriber_name: Optional[str] = None
    subscriber_dob: Optional[str] = None
```

### `schemas/patient.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from schemas.base import EntityBase
from schemas.enums import Gender

class Patient(EntityBase):
    first_name: str
    last_name: str
    dob: date
    gender: Gender
    mrn: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    family_history: List[str] = Field(default_factory=list)
    social_history: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
```

### `schemas/clinical.py`
```python
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
```

### `schemas/notes.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.base import EntityBase

class ClinicalNote(EntityBase):
    title: str
    text: str
    date: datetime
    author_id: Optional[str] = None

class ProgressNote(ClinicalNote):
    pass

class OperativeNote(ClinicalNote):
    pre_op_diagnosis: Optional[str] = None
    post_op_diagnosis: Optional[str] = None
    procedure_details: Optional[str] = None

class PathologyReport(ClinicalNote):
    specimen: Optional[str] = None
    macroscopic_description: Optional[str] = None
    microscopic_description: Optional[str] = None

class DischargeSummary(ClinicalNote):
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
    discharge_disposition: Optional[str] = None

class Referral(EntityBase):
    referring_provider_id: str
    target_provider_id: Optional[str] = None
    target_specialty: Optional[str] = None
    reason: str
    date: datetime
```

### `schemas/document.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base import EntityBase
from schemas.enums import DocumentType

class DocumentReference(EntityBase):
    filename: str
    document_type: DocumentType
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    hash: Optional[str] = None
```

### `schemas/timeline.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.base import EntityBase

class TimelineEvent(EntityBase):
    date: datetime
    event_type: str
    description: str
    related_entity_ids: List[str] = Field(default_factory=list)
```

### `schemas/authorization.py`
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from schemas.base import EntityBase
from schemas.enums import EvidenceStatus, RecommendationType, DecisionStatus, Priority

class RequestedProcedure(EntityBase):
    name: str
    cpt_code: str
    priority: Priority = Field(default=Priority.ROUTINE)

class SupportingEvidence(EntityBase):
    rule_id: str
    rule_description: str
    status: EvidenceStatus
    matched_entity_id: Optional[str] = None
    explanation: Optional[str] = None

class MissingEvidence(EntityBase):
    rule_id: str
    rule_description: str
    explanation: str

class Conflict(EntityBase):
    description: str
    conflicting_entity_ids: List[str] = Field(default_factory=list)
    resolution_notes: Optional[str] = None
    resolved: bool = False

class Recommendation(EntityBase):
    type: RecommendationType
    description: str
    action_required_by: Optional[str] = None

class ReadinessScore(EntityBase):
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    medical_necessity_score: float = Field(default=0.0, ge=0.0, le=100.0)
    clinical_evidence_score: float = Field(default=0.0, ge=0.0, le=100.0)
    documentation_quality_score: float = Field(default=0.0, ge=0.0, le=100.0)

class DecisionSummary(EntityBase):
    status: DecisionStatus
    primary_reason: Optional[str] = None
    score: Optional[ReadinessScore] = None

class AuthorizationRequest(EntityBase):
    patient_id: str
    provider_id: str
    insurance_id: str
    requested_procedures: List[RequestedProcedure] = Field(default_factory=list)
    supporting_evidence: List[SupportingEvidence] = Field(default_factory=list)
    missing_evidence: List[MissingEvidence] = Field(default_factory=list)
    conflicts: List[Conflict] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    decision: Optional[DecisionSummary] = None
```

### `schemas/knowledge_base.py`
```python
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
```

### `schemas/__init__.py`
```python
from .enums import *
from .base import *
from .administrative import *
from .patient import *
from .clinical import *
from .notes import *
from .document import *
from .timeline import *
from .authorization import *
from .knowledge_base import *
```
