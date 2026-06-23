from ninja_extra import api_controller, route
from core.responses import ErrorResponse
from workflow.schemas import WorkflowRunRequest, WorkflowResponse, DashboardResponse
from workflow.services import WorkflowIntegrationService, WorkflowException
import uuid

@api_controller('/workflow', tags=['Workflow'])
class WorkflowController:
    
    def __init__(self):
        self.service = WorkflowIntegrationService()

    @route.post('/run', response={200: WorkflowResponse, 400: ErrorResponse, 500: ErrorResponse})
    def run_workflow(self, request: WorkflowRunRequest):
        """
        Run the complete Prior Authorization workflow.
        """
        try:
            result = self.service.run_workflow(
                document_id=request.document_id,
                procedure_code=request.procedure_code,
                procedure_name=request.procedure_name
            )
            return 200, result
        except WorkflowException as e:
            return 500, {"error": e.code, "details": e.message}
        except Exception as e:
            return 500, {"error": "INTERNAL_SERVER_ERROR", "details": str(e)}

    @route.get('/dashboard/{authorization_id}', response={200: DashboardResponse, 404: ErrorResponse, 500: ErrorResponse})
    def get_dashboard(self, authorization_id: uuid.UUID):
        """
        Retrieve frontend-friendly dashboard data for an authorization request.
        """
        try:
            result = self.service.get_dashboard(authorization_id)
            return 200, result
        except WorkflowException as e:
            return 404, {"error": "NOT_FOUND", "details": e.message}
        except Exception as e:
            return 500, {"error": "INTERNAL_SERVER_ERROR", "details": str(e)}
