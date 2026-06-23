from agents.graph.builder import WorkflowOrchestrator
from agents.graph.state import OrchestrationState, WorkflowResult

class WorkflowExecutor:
    """
    Executes the LangGraph orchestration workflow.
    """
    def __init__(self):
        self.app = WorkflowOrchestrator.build_graph()
        
    def execute(self, document_id: str, procedure_code: str, procedure_name: str) -> WorkflowResult:
        """
        Run the workflow from start to finish.
        """
        initial_state = OrchestrationState(
            document_id=document_id,
            procedure_code=procedure_code,
            procedure_name=procedure_name,
            document=None,
            parser_result=None,
            knowledge_base=None,
            authorization_request=None,
            procedure_template=None,
            gap_analysis_result=None,
            rule_evaluation_result=None,
            status="INITIALIZED",
            errors=[],
            workflow_result=None
        )
        
        final_state = self.app.invoke(initial_state)
        
        if final_state.get("workflow_result"):
            return final_state["workflow_result"]
            
        return WorkflowResult(
            summary="Workflow failed to generate a result.",
            errors=final_state.get("errors", [])
        )
