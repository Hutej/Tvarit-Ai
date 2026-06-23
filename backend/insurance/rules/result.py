from typing import List, Optional, Any
from pydantic import BaseModel, Field
from insurance.rules.types import RuleStatus, RulePriority, RuleCategory

class RuleResult(BaseModel):
    rule_id: str
    name: str
    category: RuleCategory
    priority: RulePriority
    status: RuleStatus
    confidence: float = 1.0
    reason: str
    evidence: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    recommendation: Optional[str] = None

class RuleEvaluationResult(BaseModel):
    passed_rules: List[RuleResult] = Field(default_factory=list)
    failed_rules: List[RuleResult] = Field(default_factory=list)
    warnings: List[RuleResult] = Field(default_factory=list)
    not_applicable: List[RuleResult] = Field(default_factory=list)
    
    readiness_score: int = 100
    completion_percentage: float = 0.0
    
    global_recommendations: List[str] = Field(default_factory=list)
    all_missing_fields: List[str] = Field(default_factory=list)
