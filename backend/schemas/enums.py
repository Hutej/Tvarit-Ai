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
