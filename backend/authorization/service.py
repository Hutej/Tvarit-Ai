from schemas.knowledge_base import PatientKnowledgeBase
from authorization.types import AuthorizationRequest, AuthorizationPriority
from authorization.builder import AuthorizationBuilder

class AuthorizationService:
    """
    Service for managing Authorization Requests.
    """

    def build_authorization_request(
        self, 
        kb: PatientKnowledgeBase, 
        procedure_code: str, 
        procedure_name: str,
        priority: AuthorizationPriority = AuthorizationPriority.STANDARD
    ) -> AuthorizationRequest:
        """
        Build an Authorization Request from a PatientKnowledgeBase and procedure details.
        """
        builder = AuthorizationBuilder(kb)
        
        request = (
            builder
            .set_procedure(procedure_code, procedure_name)
            .set_priority(priority)
            .extract_patient()
            .extract_insurance()
            .extract_ordering_provider()
            .extract_supporting_documents()
            .build()
        )
        
        return request
