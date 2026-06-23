from typing import TypedDict, Optional, List, Any
from pydantic import BaseModel, Field
from documents.parser.types import ParserResult
from schemas.knowledge_base import PatientKnowledgeBase
from authorization.types import AuthorizationRequest
from insurance.templates.models import ProcedureTemplate
from insurance.gap_analysis.result import GapAnalysisResult
from insurance.rules.result import RuleEvaluationResult
from insurance.gap_analysis.types import RiskLevel

class WorkflowResult(BaseModel):
    authorization_request: Optional[AuthorizationRequest] = None
    gap_analysis_result: Optional[GapAnalysisResult] = None
    rule_evaluation_result: Optional[RuleEvaluationResult] = None
    
    overall_readiness_score: int = 0
    overall_risk: RiskLevel = RiskLevel.CRITICAL
    recommendations: List[str] = Field(default_factory=list)
    summary: str = ""
    errors: List[str] = Field(default_factory=list)

class OrchestrationState(TypedDict):
    # Inputs
    document_id: str
    procedure_code: str
    procedure_name: str
    
    # Processing Objects
    document: Optional[Any]
    parser_result: Optional[ParserResult]
    knowledge_base: Optional[PatientKnowledgeBase]
    authorization_request: Optional[AuthorizationRequest]
    procedure_template: Optional[ProcedureTemplate]
    
    # Results
    gap_analysis_result: Optional[GapAnalysisResult]
    rule_evaluation_result: Optional[RuleEvaluationResult]
    
    # Workflow control
    status: str
    errors: List[str]
    
    # Final Output
    workflow_result: Optional[WorkflowResult]
