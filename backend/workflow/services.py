import uuid
from typing import Dict
from agents.graph.executor import WorkflowExecutor
from workflow.schemas import WorkflowResponse, DashboardResponse, DashboardEvidenceItem
from core.exceptions import TvaritException

class WorkflowException(TvaritException):
    def __init__(self, message: str = "Workflow failed"):
        super().__init__(message, code="WORKFLOW_ERROR", status_code=500)

class WorkflowIntegrationService:
    """
    Service integrating the LangGraph executor and managing persistence of results.
    """
    
    # In a real app, this would be a database. For this sprint, we'll store results in memory.
    _dashboard_data_store: Dict[uuid.UUID, DashboardResponse] = {}
    
    def __init__(self):
        self.executor = WorkflowExecutor()

    def run_workflow(self, document_id: str, procedure_code: str, procedure_name: str) -> WorkflowResponse:
        result = self.executor.execute(
            document_id=document_id,
            procedure_code=procedure_code,
            procedure_name=procedure_name
        )
        
        if result.errors:
            raise WorkflowException(f"Workflow execution failed: {', '.join(result.errors)}")
            
        auth_req = result.authorization_request
        gap = result.gap_analysis_result
        rules = result.rule_evaluation_result
        
        if not auth_req:
            raise WorkflowException("Workflow completed but no Authorization Request was generated.")
            
        patient_name = "Unknown Patient"
        if auth_req.patient:
            patient_name = f"{auth_req.patient.first_name} {auth_req.patient.last_name}".strip()
            
        matched_count = len(gap.matched_evidence) if gap else 0
        missing_count = len(gap.missing_evidence) if gap else 0
        
        response = WorkflowResponse(
            authorization_id=auth_req.id,
            procedure=auth_req.requested_procedure_name,
            patient_name=patient_name,
            readiness_score=result.overall_readiness_score,
            risk_level=result.overall_risk.value if result.overall_risk else "UNKNOWN",
            matched_evidence_count=matched_count,
            missing_evidence_count=missing_count,
            recommendations=result.recommendations,
            summary=result.summary
        )
        
        # Save to dashboard mock store
        dashboard_res = DashboardResponse(
            authorization_id=auth_req.id,
            patient_name=patient_name,
            procedure_name=auth_req.requested_procedure_name,
            readiness_score=result.overall_readiness_score,
            risk_level=result.overall_risk.value if result.overall_risk else "UNKNOWN",
            completion_percentage=gap.overall_completeness if gap else 0.0,
            matched_evidence=[
                DashboardEvidenceItem(
                    category=item.category.value,
                    requirement=item.requirement,
                    status=item.status.value,
                    matched_value=item.matched_value,
                    reason=item.reason
                ) for item in (gap.matched_evidence if gap else [])
            ],
            missing_evidence=[
                DashboardEvidenceItem(
                    category=item.category.value,
                    requirement=item.requirement,
                    status=item.status.value,
                    matched_value=item.matched_value,
                    reason=item.reason
                ) for item in (gap.missing_evidence if gap else [])
            ],
            recommendations=result.recommendations,
            summary=result.summary
        )
        self.__class__._dashboard_data_store[auth_req.id] = dashboard_res
        
        return response

    def get_dashboard(self, authorization_id: uuid.UUID) -> DashboardResponse:
        data = self.__class__._dashboard_data_store.get(authorization_id)
        if not data:
            raise WorkflowException(f"Authorization {authorization_id} not found.")
        return data
