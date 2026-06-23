from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class WorkflowRunRequest(BaseModel):
    document_id: str
    procedure_code: str
    procedure_name: str

class WorkflowResponse(BaseModel):
    authorization_id: Optional[uuid.UUID] = None
    procedure: str
    patient_name: str
    readiness_score: int
    risk_level: str
    matched_evidence_count: int
    missing_evidence_count: int
    recommendations: List[str]
    summary: str

class DashboardEvidenceItem(BaseModel):
    category: str
    requirement: str
    status: str
    matched_value: Optional[str] = None
    reason: Optional[str] = None

class DashboardResponse(BaseModel):
    authorization_id: uuid.UUID
    patient_name: str
    procedure_name: str
    readiness_score: int
    risk_level: str
    completion_percentage: float
    matched_evidence: List[DashboardEvidenceItem] = Field(default_factory=list)
    missing_evidence: List[DashboardEvidenceItem] = Field(default_factory=list)
    recommendations: List[str]
    summary: str
