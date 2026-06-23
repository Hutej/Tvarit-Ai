from typing import List, Optional
from schemas.knowledge_base import PatientKnowledgeBase
from authorization.types import AuthorizationRequest, AuthorizationPriority, AuthorizationStatus
from schemas.patient import Patient
from schemas.administrative import InsuranceDetails, Provider

class AuthorizationBuilder:
    """
    Builder class to construct an AuthorizationRequest.
    """
    
    def __init__(self, kb: PatientKnowledgeBase):
        self.kb = kb
        self.request = AuthorizationRequest(
            knowledge_base=kb,
            requested_procedure_code="",
            requested_procedure_name=""
        )

    def set_procedure(self, code: str, name: str) -> 'AuthorizationBuilder':
        self.request.requested_procedure_code = code
        self.request.requested_procedure_name = name
        return self

    def set_priority(self, priority: AuthorizationPriority) -> 'AuthorizationBuilder':
        self.request.priority = priority
        return self

    def extract_patient(self) -> 'AuthorizationBuilder':
        if self.kb.patient:
            self.request.patient = self.kb.patient
        return self

    def extract_insurance(self) -> 'AuthorizationBuilder':
        if self.kb.administrative and self.kb.administrative.insurance_details:
            self.request.insurance = self.kb.administrative.insurance_details
        return self

    def extract_ordering_provider(self) -> 'AuthorizationBuilder':
        if self.kb.providers:
            # Select the first available provider as a fallback
            self.request.ordering_provider = self.kb.providers[0]
        return self

    def extract_supporting_documents(self) -> 'AuthorizationBuilder':
        # Automatically attach relevant documents from the knowledge base
        documents = []
        if self.kb.clinical:
            if self.kb.clinical.notes:
                documents.extend(self.kb.clinical.notes)
            if self.kb.clinical.imaging_reports:
                documents.extend(self.kb.clinical.imaging_reports)
            if self.kb.clinical.lab_results:
                documents.extend(self.kb.clinical.lab_results)
                
        self.request.supporting_documents = documents
        return self

    def build(self) -> AuthorizationRequest:
        if not self.request.requested_procedure_code or not self.request.requested_procedure_name:
            raise ValueError("Requested procedure code and name are required.")
        return self.request
