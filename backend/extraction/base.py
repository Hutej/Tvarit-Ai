from abc import ABC, abstractmethod
from typing import Tuple
from schemas.knowledge_base import PatientKnowledgeBase
from documents.parser.types import ParserResult
from documents.constants import DocumentType
from extraction.types import ExtractionResult, ExtractionRequest
from core.ai.client import AIClient
from extraction.exceptions import ExtractionValidationException

class MedicalExtractor(ABC):
    """
    Abstract base class for all medical document extractors.
    """
    
    def __init__(self):
        self.ai_client = AIClient()

    @abstractmethod
    def supports(self, document_type: DocumentType) -> bool:
        """Check if this extractor handles the specific document type."""
        pass

    @abstractmethod
    def build_prompt(self, parser_result: ParserResult) -> Tuple[str, str]:
        """
        Convert the parser result into (system_prompt, user_prompt).
        """
        pass

    @abstractmethod
    def validate(self, output: PatientKnowledgeBase) -> bool:
        """
        Validate the extracted schema before returning.
        """
        pass

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        """
        Execute the extraction process via AI Client.
        """
        system_prompt, user_prompt = self.build_prompt(request.parser_result)
        
        # Call AI Provider
        kb_result, stats = self.ai_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_schema=PatientKnowledgeBase
        )

        if not self.validate(kb_result):
            raise ExtractionValidationException()

        return ExtractionResult(
            knowledge_base=kb_result,
            statistics=stats,
            warnings=[]
        )
