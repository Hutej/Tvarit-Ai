from langgraph.graph import StateGraph, START, END
from agents.graph.state import OrchestrationState, WorkflowResult
from agents.graph.edges import continue_or_fail
from documents.repositories.document_repository import DocumentRepository
from documents.parser.factory import ParserFactory
from documents.constants import DocumentType
from extraction.factory import ExtractorFactory
from extraction.types import ExtractionRequest
from authorization.service import AuthorizationService
from insurance.templates.registry import TemplateRegistry
from insurance.gap_analysis.analyzer import GapAnalyzer
from insurance.rules.engine import RuleEngine

def parse_document(state: OrchestrationState):
    try:
        repo = DocumentRepository()
        document = repo.get_active_by_id(state["document_id"])
        if not document:
            return {"errors": state.get("errors", []) + [f"Document {state['document_id']} not found"]}
        
        parser = ParserFactory.get_parser_for_document(document)
        parser_result = parser.parse(document)
        
        return {"document": document, "parser_result": parser_result, "status": "PARSED"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def extract_knowledge(state: OrchestrationState):
    try:
        parser_result = state["parser_result"]
        document = state["document"]
        doc_type_str = parser_result.metadata.document_type_hint or document.document_type
        try:
            doc_type = DocumentType(doc_type_str)
        except ValueError:
            doc_type = DocumentType.UNKNOWN
            
        extractor = ExtractorFactory.get_extractor_for_type(doc_type)
        request = ExtractionRequest(
            parser_result=parser_result,
            document_type_hint=doc_type.value
        )
        extraction_result = extractor.extract(request)
        return {"knowledge_base": extraction_result.knowledge_base, "status": "EXTRACTED"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def build_auth_request(state: OrchestrationState):
    try:
        auth_service = AuthorizationService()
        auth_req = auth_service.build_authorization_request(
            kb=state["knowledge_base"],
            procedure_code=state["procedure_code"],
            procedure_name=state["procedure_name"]
        )
        return {"authorization_request": auth_req, "status": "AUTH_BUILT"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def load_template(state: OrchestrationState):
    try:
        template = TemplateRegistry.get(state["procedure_code"])
        if not template:
            return {"errors": state.get("errors", []) + [f"Procedure Template not found for code {state['procedure_code']}"]}
        return {"procedure_template": template, "status": "TEMPLATE_LOADED"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def run_gap_analysis(state: OrchestrationState):
    try:
        analyzer = GapAnalyzer()
        gap_result = analyzer.analyze(state["knowledge_base"], state["procedure_template"])
        return {"gap_analysis_result": gap_result, "status": "GAP_ANALYSIS_COMPLETE"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def run_rule_engine(state: OrchestrationState):
    try:
        engine = RuleEngine()
        rule_result = engine.evaluate(state["knowledge_base"])
        return {"rule_evaluation_result": rule_result, "status": "RULES_EVALUATED"}
    except Exception as e:
        return {"errors": state.get("errors", []) + [str(e)]}

def generate_result(state: OrchestrationState):
    if state.get("errors"):
        result = WorkflowResult(
            summary="Workflow failed with errors.",
            errors=state["errors"]
        )
        return {"workflow_result": result, "status": "FAILED"}
        
    gap = state.get("gap_analysis_result")
    rules = state.get("rule_evaluation_result")
    
    score = 0
    if gap and rules:
        score = min(gap.readiness_score, rules.readiness_score)
    elif gap:
        score = gap.readiness_score
    elif rules:
        score = rules.readiness_score
        
    recommendations = []
    if gap:
        recommendations.extend(gap.recommendations)
    if rules:
        recommendations.extend(rules.global_recommendations)
        
    recommendations = list(dict.fromkeys(recommendations))
    
    result = WorkflowResult(
        authorization_request=state.get("authorization_request"),
        gap_analysis_result=gap,
        rule_evaluation_result=rules,
        overall_readiness_score=score,
        overall_risk=gap.risk_level if gap else None,
        recommendations=recommendations,
        summary="Workflow completed successfully."
    )
    
    return {"workflow_result": result, "status": "COMPLETED"}

class WorkflowOrchestrator:
    @classmethod
    def build_graph(cls):
        workflow = StateGraph(OrchestrationState)
        
        # Nodes
        workflow.add_node("parse_document", parse_document)
        workflow.add_node("extract_knowledge", extract_knowledge)
        workflow.add_node("build_auth_request", build_auth_request)
        workflow.add_node("load_template", load_template)
        workflow.add_node("run_gap_analysis", run_gap_analysis)
        workflow.add_node("run_rule_engine", run_rule_engine)
        workflow.add_node("generate_result", generate_result)
        
        # Edges
        workflow.add_edge(START, "parse_document")
        
        workflow.add_conditional_edges("parse_document", continue_or_fail, {"continue": "extract_knowledge", "fail": "generate_result"})
        workflow.add_conditional_edges("extract_knowledge", continue_or_fail, {"continue": "build_auth_request", "fail": "generate_result"})
        workflow.add_conditional_edges("build_auth_request", continue_or_fail, {"continue": "load_template", "fail": "generate_result"})
        workflow.add_conditional_edges("load_template", continue_or_fail, {"continue": "run_gap_analysis", "fail": "generate_result"})
        workflow.add_conditional_edges("run_gap_analysis", continue_or_fail, {"continue": "run_rule_engine", "fail": "generate_result"})
        workflow.add_conditional_edges("run_rule_engine", continue_or_fail, {"continue": "generate_result", "fail": "generate_result"})
        
        workflow.add_edge("generate_result", END)
        
        return workflow.compile()
