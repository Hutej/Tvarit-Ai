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
