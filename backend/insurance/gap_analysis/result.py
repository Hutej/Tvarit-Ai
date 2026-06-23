from typing import List, Optional
from pydantic import BaseModel, Field
from insurance.gap_analysis.types import RiskLevel, EvidenceCategory, EvidenceStatus

class EvidenceItem(BaseModel):
    category: EvidenceCategory
    requirement: str
    status: EvidenceStatus
    matched_value: Optional[str] = None
    reason: Optional[str] = None

class GapAnalysisResult(BaseModel):
    procedure_code: str
    procedure_name: str
    
    matched_evidence: List[EvidenceItem] = Field(default_factory=list)
    missing_evidence: List[EvidenceItem] = Field(default_factory=list)
    partial_evidence: List[EvidenceItem] = Field(default_factory=list)
    conflicting_evidence: List[EvidenceItem] = Field(default_factory=list)
    
    overall_completeness: float = 0.0
    readiness_score: int = 0
    risk_level: RiskLevel = RiskLevel.CRITICAL
    
    recommendations: List[str] = Field(default_factory=list)
    next_best_actions: List[str] = Field(default_factory=list)
    
    summary: str = ""
